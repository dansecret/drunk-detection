# 🚶‍♂️ Real-time Gait Anomaly & Drunk Detection Engine

Aplikasi deteksi anomali cara berjalan (gait anomaly) dan indikasi mabuk secara real-time menggunakan model AI YOLO11-Large.

Proyek ini telah sepenuhnya menggunakan kontainerisasi Docker dengan dukungan akselerasi hardware NVIDIA GPU (CUDA) serta sistem display forwarding pintar untuk Linux modern (X11 & Wayland).

------------------------------------------------------------
🚀 FITUR UTAMA
------------------------------------------------------------

✅ YOLO11-Large Tracking
   Akurasi pelacakan objek manusia yang kokoh dengan identitas ID digital terikat.

✅ Smart AND Logic
   Meminimalkan false alarm akibat gerakan tangan, lambaian, atau aktivitas ringan saat subjek diam.

✅ Auto-Closeup Filter
   Secara otomatis mematikan analisis bentuk kotak jika subjek terlalu dekat dengan kamera untuk menghindari distorsi lensa.

✅ Identity Status Locking
   Mengunci status jika subjek telah terbukti positif mabuk/anomali untuk menghemat beban CPU/GPU.

------------------------------------------------------------
🛠️ PRASYARAT SISTEM
------------------------------------------------------------

Pastikan sistem Anda telah terpasang:

1. Docker
2. Docker Compose v2
3. NVIDIA Driver
4. NVIDIA Container Toolkit

Catatan:
NVIDIA Container Toolkit wajib terpasang agar Docker dapat mengakses CUDA GPU host.

------------------------------------------------------------
📦 QUICK START
------------------------------------------------------------

1. Clone Repository
------------------------------------------------------------

Buka terminal lalu jalankan:

git clone https://github.com/dansecret/drunk-detection.git
cd drunk-detection


2. Izinkan Akses Grafis Docker (Linux)
------------------------------------------------------------

Karena aplikasi akan menampilkan jendela video GUI langsung dari dalam Docker ke layar host, jalankan:

xhost +local:docker

Pastikan muncul pesan:

non-network local connections being added to access control list


3. Jalankan Docker Compose
------------------------------------------------------------

docker compose up --build

Catatan:
Pada proses pertama kali berjalan, Docker akan mengunduh bobot model AI:
yolo11l.pt

Proses ini membutuhkan waktu beberapa menit tergantung koneksi internet.

------------------------------------------------------------
🕹️ CARA MENGUJI SISTEM
------------------------------------------------------------

🟢 STATUS NORMAL (HIJAU)
------------------------------------------------------------

- Berdirilah tegak atau duduk diam di depan kamera.
- Anda dapat menggerakkan tangan atau melompat ringan.
- Sistem akan tetap mendeteksi kondisi NORMAL.


🔴 STATUS DRUNK / ANOMALY (MERAH - LOCKED)
------------------------------------------------------------

1. Mundur sekitar 2–3 meter dari kamera.
2. Pastikan seluruh badan terlihat penuh.
3. Berjalan maju dengan pola:
   - zigzag
   - sempoyongan
   - ritme langkah tidak konstan
4. Lakukan minimal 3 perubahan arah.

Jika sistem mendeteksi anomali:
- status akan berubah menjadi LOCKED
- kotak deteksi tetap merah
- status tidak akan kembali normal meskipun subjek berdiri tegak


------------------------------------------------------------
❌ MENUTUP APLIKASI
------------------------------------------------------------

1. Klik jendela video aplikasi.
2. Tekan tombol:

q

3. Webcam dan container akan berhenti dengan aman.

------------------------------------------------------------
⚡ TEKNOLOGI YANG DIGUNAKAN
------------------------------------------------------------

- Python
- OpenCV
- Ultralytics YOLO11
- CUDA
- Docker
- Docker Compose
- NVIDIA Container Toolkit

------------------------------------------------------------
📄 LICENSE
------------------------------------------------------------

Gunakan proyek ini untuk kebutuhan penelitian, pembelajaran, dan pengembangan AI Computer Vision.

------------------------------------------------------------
👨‍💻 AUTHOR
------------------------------------------------------------

Developed by:
Hamdandih

GitHub:
https://github.com/dansecret