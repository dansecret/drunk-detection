import cv2
import numpy as np
from collections import deque
from ultralytics import YOLO

model = YOLO("yolo11l.pt")
model.to('cuda')

MAX_BUFFER = 30
gait_history = {}   
ratio_history = {}  

drunk_locked_ids = set()

SWAY_THRESHOLD = 3            
VELOCITY_VAR_THRESHOLD = 15   
ASPECT_RATIO_THRESHOLD = 0.65 
RATIO_VAR_THRESHOLD = 0.06    
FRAME_AREA_THRESHOLD = 0.30   

def analyze_gait_anomaly(coordinate_list):
    if len(coordinate_list) < 15:
        return False, 0, 0
        
    x_coords = [pt[0] for pt in coordinate_list]
    direction_changes = 0
    previous_direction = 0 
    
    for i in range(1, len(x_coords)):
        delta_x = x_coords[i] - x_coords[i-1]
        if abs(delta_x) > 3: 
            current_direction = 1 if delta_x > 0 else -1
            if previous_direction != 0 and current_direction != previous_direction:
                direction_changes += 1
            previous_direction = current_direction

    frame_distances = []
    for i in range(1, len(coordinate_list)):
        dist = np.sqrt((coordinate_list[i][0] - coordinate_list[i-1][0])**2 + 
                       (coordinate_list[i][1] - coordinate_list[i-1][1])**2)
        frame_distances.append(dist)
        
    velocity_variance = np.std(frame_distances) if frame_distances else 0
    is_gait_unstable = (direction_changes >= SWAY_THRESHOLD) and (velocity_variance >= VELOCITY_VAR_THRESHOLD)
        
    return is_gait_unstable, direction_changes, velocity_variance


# cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture("drunk.mp4")

print("Inference Engine (YOLO11-Large) - Active Lock Status Version Started...")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
        
    img_height, img_width, _ = frame.shape
    total_frame_area = img_width * img_height

    results = model.track(frame, persist=True, classes=[0], verbose=False)

    if results[0].boxes is not None and results[0].boxes.id is not None:
        boxes = results[0].boxes.xyxy.cpu().numpy()  
        track_ids = results[0].boxes.id.cpu().numpy().astype(int)

        for box, track_id in zip(boxes, track_ids):
            x_min, y_min, x_max, y_max = box
            
            # --- 1. HITUNG DIMENSI & LUAS BOX ---
            box_width = x_max - x_min
            box_height = y_max - y_min
            aspect_ratio = box_width / box_height if box_height > 0 else 0
            area_percentage = (box_width * box_height) / total_frame_area
            
            # --- 2. JIKA ID SUDAH PERNAH DI-LOCK MABUK, BYPASS PERHITUNGAN ---
            if track_id in drunk_locked_ids:
                box_color = (0, 0, 255)
                status_text = f"ID {track_id}: DRUNK / LOCKED"
                
                cv2.rectangle(frame, (int(x_min), int(y_min)), (int(x_max), int(y_max)), box_color, 2)
                cv2.putText(frame, status_text, (int(x_min), int(y_min) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, box_color, 2)
                cv2.putText(frame, "STATUS LOCKED - BLACKLISTED", (int(x_min), int(y_max) + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)
                continue # Langsung skip ke orang berikutnya, hemat CPU!
            
            # --- 3. RECORD DATA REKAM JEJAK (UNTUK ID YANG BELUM BLACKLIST) ---
            x_center = int((x_min + x_max) / 2)
            y_bottom = int(y_max)
            if track_id not in gait_history:
                gait_history[track_id] = deque(maxlen=MAX_BUFFER)
            gait_history[track_id].append((x_center, y_bottom))
            
            if track_id not in ratio_history:
                ratio_history[track_id] = deque(maxlen=MAX_BUFFER)
            ratio_history[track_id].append(aspect_ratio)
            
            is_gait_anomaly, sway_count, velocity_var = analyze_gait_anomaly(gait_history[track_id])
            
            if len(ratio_history[track_id]) >= 15:
                ratio_variance = np.std(list(ratio_history[track_id]))
            else:
                ratio_variance = 0
            
            is_dynamic_tilt = ratio_variance > RATIO_VAR_THRESHOLD
            if area_percentage > FRAME_AREA_THRESHOLD:
                is_static_tilt = False  
                distance_status = "CLOSEUP"
            else:
                is_static_tilt = aspect_ratio > ASPECT_RATIO_THRESHOLD
                distance_status = "OK"
            
            # --- (LOCKING) ---
            if (is_gait_anomaly and is_dynamic_tilt) or is_static_tilt:
                # KETOK PALU! Masukkan ID ini ke dalam daftar blacklist lock
                drunk_locked_ids.add(track_id)
                box_color = (0, 0, 255)
                status_text = f"ID {track_id}: DRUNK / LOCKED"
            else:
                box_color = (0, 255, 0)
                status_text = f"ID {track_id}: NORMAL"
                
            # Render visualisasi normal/baru terdeteksi
            cv2.rectangle(frame, (int(x_min), int(y_min)), (int(x_max), int(y_max)), box_color, 2)
            cv2.putText(frame, status_text, (int(x_min), int(y_min) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, box_color, 2)
            
            cv2.putText(frame, f"Sway: {sway_count}/3 | Var: {velocity_var:.1f}/15 | R-Var: {ratio_variance:.3f} | {distance_status}", 
                        (int(x_min), int(y_max) + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)

    cv2.imshow("YOLO11 - Ultimate Bulletproof Detection", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()