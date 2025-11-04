# Quick Start Guide - Gesture Detection

## 🚀 Instalasi & Setup

### 1. Pastikan Python 3.11.7 Terinstall
```bash
python --version
# Output: Python 3.11.7
```

### 2. Install Dependencies (Sudah Selesai)
```bash
pip install opencv-python mediapipe numpy Pillow
```

## ▶️ Cara Menjalankan

### Windows (PowerShell):
```powershell
cd e:\make_meme_with_Python1
python main.py
```

### Expected Output:
```
============================================================
GESTURE DETECTION - POSE MATCHING
============================================================
Aplikasi untuk mendeteksi pose dan mencocokkan dengan gambar referensi

INFO: Created TensorFlow Lite XNNPACK delegate for CPU.

Memuat 6 gambar referensi...
  Processing: monkey1.jpg...
    ✓ Pose 'monkey1' berhasil dimuat
  ...

✓ Total 3 pose referensi berhasil dimuat
Pose: monkey1, monkey2, monkey3

Webcam terbuka. Mulai deteksi pose + hand tracking...
Tekan 'q' untuk keluar, 's' untuk save screenshot

Window Layout:
  - Camera Feed: Webcam + Skeleton (Pose + Hand Tracking)
  - Detected Gesture: Gambar Referensi yang Match
```

## 🎮 Controls

| Key | Action |
|-----|--------|
| `Q` | Quit/Keluar dari aplikasi |
| `S` | Save screenshot kedua window |

## 📺 Dual Window Display

### Window 1: Camera Feed
- **Apa yang ditampilkan**: Webcam real-time dengan skeleton overlay
- **Info yang muncul**:
  - FPS counter
  - Nama gesture terdeteksi (atau "No Gesture")
  - Progress bar stability (merah → biru → hijau)

### Window 2: Detected Gesture
- **Apa yang ditampilkan**: Reference image yang match
- **Status**:
  - Jika match: Menampilkan gambar referensi + label "DETECTED: [GESTURE]"
  - Jika tidak match: Placeholder "No Gesture Detected" + "Strike a Pose!"

## 🎯 Tips Penggunaan

### 1. Posisi yang Baik
- Jarak dari webcam: 1-2 meter
- Pencahayaan: Cukup terang, tidak backlit
- Background: Polos lebih baik

### 2. Gesture Detection
- **Mulai gesture**: Tahan pose selama ~1 detik
- **Watch progress bar**: 
  - 🔴 Merah: Belum stabil, adjust pose
  - 🔵 Biru: Hampir terdeteksi, tahan pose
  - 🟢 Hijau: Terdeteksi! Gesture locked
- **Smooth transition**: Gesture harus konsisten untuk terdeteksi

### 3. Best Practices
- Lakukan gerakan dengan jelas dan distingtif
- Tahan pose sampai progress bar penuh (hijau)
- Jika tidak terdeteksi, coba sesuaikan pose Anda dengan referensi

## 🔧 Troubleshooting

### Webcam Tidak Terdeteksi
```python
# Edit config.py, ubah CAMERA_INDEX
CAMERA_INDEX = 0  # Coba 0, 1, atau 2
```

### Gesture Tidak Terdeteksi
1. **Similarity terlalu tinggi**: Edit `config.py`
   ```python
   SIMILARITY_THRESHOLD = 0.75  # Turunkan dari 0.85
   ```

2. **Pose kurang mirip**: Perhatikan reference image, sesuaikan pose Anda

3. **Pencahayaan buruk**: Perbaiki lighting di ruangan

### Window Terlalu Besar/Kecil
Windows dapat di-resize karena menggunakan `cv2.WINDOW_NORMAL`

### FPS Rendah
- Close aplikasi lain yang berat
- Reduce camera resolution di `config.py`:
  ```python
  CAMERA_WIDTH = 320   # Default: 640
  CAMERA_HEIGHT = 240  # Default: 480
  ```

## 📂 File Outputs

### Screenshots Tersimpan Di:
```
outputs/
├── camera_20240101_120000.jpg    # Camera feed window
└── gesture_20240101_120000.jpg   # Gesture display window
```

## 🎨 Tambah Reference Gestures Sendiri

### 1. Siapkan Gambar
- Format: JPG, PNG, atau format image lainnya
- Nama file: Sesuai nama gesture (contoh: `peace_sign.jpg`)
- Usahakan gambar jelas dengan pose yang distingtif

### 2. Copy ke Folder Reference Images
```
reference_images/
├── monkey1.jpg
├── monkey2.jpg
├── monkey3.jpg
└── peace_sign.jpg    ← Gambar baru Anda
```

### 3. Restart Aplikasi
Aplikasi akan otomatis load semua gambar di folder tersebut.

## 📊 Understanding the Stability Bar

### Progress Bar Colors:
- **🔴 Red (0-50%)**: Gesture tidak stabil atau tidak match
- **🔵 Blue (50-99%)**: Gesture mulai terdeteksi, keep holding!
- **🟢 Green (100%)**: Gesture locked, fully detected!

### Smoothing Parameters (di main.py):
```python
HISTORY_SIZE = 8         # Tracking last 8 frames
MIN_HOLD_FRAMES = 10     # Must be stable for 10 frames
```

**Artinya**: Gesture harus konsisten di mayoritas (60%) dari 8 frame terakhir, dan tahan stabil selama 10 frame untuk di-confirm.

## 🔍 Advanced: Mengubah Sensitivity

### 1. Gesture Terlalu Susah Terdeteksi
Edit `config.py`:
```python
SIMILARITY_THRESHOLD = 0.70  # Lower = easier to match
```

Edit `main.py` (di smooth_gesture function):
```python
threshold = self.HISTORY_SIZE * 0.5  # Lower dari 0.6 (60%)
MIN_HOLD_FRAMES = 5  # Lower dari 10
```

### 2. Gesture Terlalu Banyak False Positives
Edit `config.py`:
```python
SIMILARITY_THRESHOLD = 0.90  # Higher = stricter matching
```

Edit `main.py`:
```python
threshold = self.HISTORY_SIZE * 0.7  # Higher dari 0.6
MIN_HOLD_FRAMES = 15  # Higher dari 10
```

## ❓ FAQ

### Q: Kenapa ada dua window?
A: Dual window pattern dari repository referensi memberikan pengalaman lebih baik - satu window untuk live camera, satu untuk detected gesture.

### Q: Kenapa gesture butuh waktu untuk terdeteksi?
A: Gesture smoothing algorithm mencegah false detection dan flickering. Ini normal dan intentional untuk akurasi.

### Q: Bisa deteksi lebih dari satu gesture sekaligus?
A: Saat ini sistem mendeteksi satu gesture terbaik yang match. Untuk multi-gesture, perlu enhancement.

### Q: Bisa ganti ke hand tracking saja?
A: Ya, bisa. Edit `gesture_detector.py` dan disable pose tracking, hanya enable hands tracking.

---

**Happy Gesture Detecting!** 🎉
