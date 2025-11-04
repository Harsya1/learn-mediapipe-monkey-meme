# 🎭 Gesture Detection - Pose Matching

Project mini Python untuk belajar **gesture detection** menggunakan **OpenCV** dan **MediaPipe**. Aplikasi ini mendeteksi pose tubuh Anda melalui webcam dan mencocokkannya dengan gambar referensi yang Anda berikan.

## 🌟 Fitur

- ✅ **Deteksi pose tubuh** real-time menggunakan MediaPipe (33 landmarks)
- ✅ **Hand tracking** untuk deteksi jari-jari tangan (21 landmarks per tangan)
- ✅ **Pencocokan pose** dengan gambar referensi
- ✅ **Side-by-side view**: Webcam vs Gambar Referensi
- ✅ **Visualisasi skeleton** pose dan tangan
- ✅ **Similarity score** untuk setiap pose
- ✅ **Screenshot feature**
- ✅ **FPS counter**

## 📋 Requirements

- Python 3.8 atau lebih tinggi
- Webcam
- Dependencies (lihat `requirements.txt`)

## 🚀 Instalasi

### 1. Clone atau Download Project

```bash
cd e:\make_meme_with_Python1
```

### 2. Buat Virtual Environment (Opsional tapi Direkomendasikan)

```powershell
# Buat virtual environment
python -m venv .venv

# Aktifkan virtual environment
.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

## 📸 Persiapan Gambar Referensi

1. Siapkan gambar pose yang ingin Anda deteksi
2. Letakkan gambar-gambar tersebut di folder `reference_images/`
3. Beri nama file sesuai dengan nama pose (contoh: `tpose.jpg`, `wave.png`, `peace.jpg`)

**Tips untuk gambar referensi yang baik:**
- Pastikan pose tubuh terlihat jelas
- Background yang kontras dengan tubuh
- Resolusi yang cukup (minimal 640x480)
- Format: JPG, JPEG, PNG, atau BMP

**Contoh struktur:**
```
reference_images/
├── tpose.jpg          # Pose T dengan tangan terbentang
├── wave.png           # Pose melambai
├── peace.jpg          # Pose peace sign
└── superhero.png      # Pose superhero
```

## 🎮 Cara Menggunakan

### Menjalankan Aplikasi

**1. Test Detection (tanpa gambar referensi):**
```powershell
python test_detection.py
```
Ini akan menampilkan webcam dengan skeleton detection untuk test apakah pose + hand tracking bekerja.

**2. Aplikasi Utama (dengan matching):**
```powershell
python main.py
```

### Kontrol Aplikasi

- **Q**: Keluar dari aplikasi
- **S**: Save screenshot side-by-side ke folder `output/`

### Cara Kerja

1. Aplikasi membaca semua gambar di folder `reference_images/`
2. MediaPipe mendeteksi **pose + hands** di setiap gambar referensi
3. Webcam terbuka dan mulai mendeteksi pose + tangan Anda
4. **Side-by-side view**:
   - **Kiri**: Webcam Anda dengan skeleton overlay
   - **Kanan**: Gambar referensi yang match
5. Pose Anda dibandingkan dengan semua pose referensi
6. Jika similarity ≥ 85%, gambar referensi ditampilkan di kanan

## ⚙️ Konfigurasi

Edit file `config.py` untuk mengubah pengaturan:

```python
# Threshold untuk menganggap pose cocok (0-1)
SIMILARITY_THRESHOLD = 0.85

# Resolusi camera
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480

# Confidence untuk deteksi
MIN_DETECTION_CONFIDENCE = 0.5
MIN_TRACKING_CONFIDENCE = 0.5
```

## 📁 Struktur Project

```
make_meme_with_Python1/
├── main.py                    # File utama aplikasi
├── gesture_detector.py        # Modul deteksi pose
├── pose_matcher.py            # Modul pencocokan pose
├── config.py                  # File konfigurasi
├── requirements.txt           # Dependencies
├── README.md                  # Dokumentasi (file ini)
├── reference_images/          # Folder untuk gambar referensi
│   ├── tpose.jpg
│   └── wave.png
├── output/                    # Folder untuk screenshot
└── utils/                     # Folder untuk utility (future use)
```

## 🧠 Cara Kerja Algoritma

### 1. Deteksi Pose (MediaPipe)
- MediaPipe mendeteksi 33 landmark points di tubuh
- Setiap landmark memiliki koordinat (x, y, visibility)

### 2. Normalisasi
- Koordinat dinormalisasi dengan centering dan scaling
- Menghilangkan efek posisi dan ukuran tubuh

### 3. Similarity Calculation
- Menggunakan **Cosine Similarity**
- Membandingkan vektor pose saat ini dengan pose referensi
- Score: 0 (tidak mirip) - 1 (identik)

### 4. Matching
- Pose dianggap cocok jika similarity ≥ threshold (default: 0.85)
- Menampilkan nama pose dan score

## 🎯 Tips Penggunaan

1. **Pencahayaan**: Pastikan ruangan cukup terang
2. **Background**: Background yang bersih membantu deteksi
3. **Jarak**: Berdiri sekitar 1-2 meter dari webcam
4. **Framing**: Pastikan seluruh tubuh terlihat di frame
5. **Pose yang Jelas**: Buat pose yang distinctive dan mudah dibedakan

## 🐛 Troubleshooting

### Webcam tidak terbuka
- Pastikan webcam terhubung dan tidak digunakan aplikasi lain
- Coba ubah `CAMERA_INDEX` di `config.py` (0, 1, 2, ...)

### Pose tidak terdeteksi
- Pastikan pencahayaan cukup
- Pastikan seluruh tubuh terlihat
- Coba ubah `MIN_DETECTION_CONFIDENCE` di `config.py`

### Similarity terlalu rendah
- Turunkan `SIMILARITY_THRESHOLD` di `config.py`
- Pastikan pose referensi yang baik
- Coba pose yang lebih ekstrim/jelas

### Import error
```powershell
# Pastikan dependencies terinstall
pip install -r requirements.txt
```

## 🔧 Pengembangan Lebih Lanjut

Ide untuk pengembangan:
- [ ] Tambah gesture tangan (hand landmarks)
- [ ] Record video hasil matching
- [ ] Database pose dengan SQLite
- [ ] GUI dengan Tkinter/PyQt
- [ ] Real-time pose correction feedback
- [ ] Multi-person detection
- [ ] Export pose data ke JSON

## 📚 Referensi

- [MediaPipe Pose](https://google.github.io/mediapipe/solutions/pose.html)
- [OpenCV Documentation](https://docs.opencv.org/)
- [NumPy Documentation](https://numpy.org/doc/)

## 📝 License

Free to use for learning purposes.

## 👨‍💻 Author

Created for learning gesture detection with Python, OpenCV, and MediaPipe.

---

**Happy Coding! 🚀**
