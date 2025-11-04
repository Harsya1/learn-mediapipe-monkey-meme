# Gesture Detection - Dual Window Display Implementation

## 📋 Overview
Berhasil mengimplementasikan **Dual Window Display** dengan **Gesture Smoothing** berdasarkan referensi repository [learning-imagerecognition](https://github.com/aaronhubhachen/learning-imagerecognition.git).

## ✅ Features yang Diimplementasikan

### 1. **Dual Window Display**
- **Camera Feed Window**: Menampilkan webcam real-time dengan skeleton overlay (pose + hand tracking)
- **Detected Gesture Window**: Menampilkan gambar referensi yang match dengan gesture Anda

### 2. **Gesture Smoothing Algorithm**
Mencegah flickering dan false detection dengan:
- **History Buffer**: Menyimpan 8 frame terakhir (`HISTORY_SIZE = 8`)
- **Stability Threshold**: Gesture harus konsisten di 60% dari history
- **Hold Frames**: Gesture harus stabil minimal 10 frames (`MIN_HOLD_FRAMES = 10`)

### 3. **Visual Feedback**
- **FPS Counter**: Monitoring real-time performance
- **Gesture Label**: Menampilkan nama gesture yang terdeteksi
- **Stability Progress Bar**: 
  - 🔴 Merah: Tidak stabil (0-50%)
  - 🔵 Biru: Mendekati stabil (50-100%)
  - 🟢 Hijau: Stabil (100%)

### 4. **Keyboard Controls**
- `Q`: Quit aplikasi
- `S`: Save screenshot (kedua window)

## 🎯 Algoritma Smoothing

```python
def smooth_gesture(self, gesture_name):
    # 1. Tambahkan ke history
    self.gesture_history.append(gesture_name)
    
    # 2. Hitung occurrence
    gesture_count = self.gesture_history.count(gesture_name)
    threshold = self.HISTORY_SIZE * 0.6  # 60%
    
    # 3. Check stability
    if gesture_count > threshold:
        self.gesture_hold_frames += 1
        if self.gesture_hold_frames >= self.MIN_HOLD_FRAMES:
            self.last_stable_gesture = gesture_name
    
    # 4. Decay jika tidak match
    else:
        self.gesture_hold_frames = max(0, self.gesture_hold_frames - 1)
    
    return self.last_stable_gesture
```

## 🔧 Technical Stack

### Dependencies
- **Python**: 3.11.7
- **OpenCV**: 4.12.0 (Video capture & display)
- **MediaPipe**: 0.10.8 (Pose + Hand tracking)
- **NumPy**: 1.24.3 (Similarity calculations)
- **Pillow**: 10.1.0 (Image loading)

### Detection Components
- **Pose Landmarks**: 33 points (MediaPipe Pose)
- **Hand Landmarks**: 21 points per hand, max 2 hands (MediaPipe Hands)
- **Similarity Algorithm**: Cosine similarity
- **Matching Threshold**: 0.85 (85% similarity)

## 📁 File Structure

```
make_meme_with_Python1/
├── main.py                    # Main application (UPDATED - Dual Window)
├── gesture_detector.py        # MediaPipe pose + hand detection
├── pose_matcher.py           # Similarity calculation & matching
├── config.py                 # Configuration constants
├── test_detection.py         # Test script
├── reference_images/         # Reference gesture images
│   ├── monkey1.jpg
│   ├── monkey2.jpg
│   └── monkey3.jpg
└── outputs/                  # Saved screenshots
    ├── camera_*.jpg
    └── gesture_*.jpg
```

## 🚀 How to Use

### 1. Start Application
```bash
python main.py
```

### 2. Two Windows Will Open
- **Camera Feed**: Shows your live webcam
- **Detected Gesture**: Shows matched reference image

### 3. Perform Gestures
- Strike poses/gestures similar to reference images
- Watch the stability bar fill up (red → blue → green)
- When green (stable), gesture is confirmed

### 4. Save Screenshots
- Press `S` to save both windows
- Files saved in `outputs/` folder

### 5. Exit
- Press `Q` to quit

## 🎨 Visual Layout

### Camera Feed Window
```
┌─────────────────────────────────────┐
│ ┌─────────────────────────────────┐ │
│ │ FPS: 30.0                       │ │
│ │ Gesture: monkey1                │ │
│ │ ████████░░ Stability: 80%       │ │
│ └─────────────────────────────────┘ │
│                                     │
│     [Webcam Feed + Skeleton]        │
│                                     │
└─────────────────────────────────────┘
```

### Detected Gesture Window
```
┌─────────────────────────────────────┐
│ DETECTED: MONKEY1                   │
├─────────────────────────────────────┤
│                                     │
│     [Reference Image]               │
│                                     │
└─────────────────────────────────────┘
```

## 🔍 Key Improvements from Repository Reference

1. **Gesture Smoothing**: Eliminates flickering matches
2. **Visual Progress Bar**: User feedback untuk stability
3. **Dual Window**: Cleaner separation of concerns
4. **History Buffer**: Better accuracy dengan temporal consistency
5. **Hold Frames**: Prevents rapid switching between gestures

## 📊 Performance Metrics

- **FPS**: ~30 FPS (depends on hardware)
- **Detection Latency**: ~33ms per frame
- **Smoothing Delay**: 10 frames (~333ms at 30 FPS)
- **History Window**: 8 frames (~267ms at 30 FPS)

## 🎓 Learning Points

### 1. Temporal Smoothing
Penting untuk aplikasi real-time gesture detection:
- Mengurangi false positives
- Meningkatkan user experience
- Mencegah gesture flickering

### 2. Dual Window Pattern
Lebih baik daripada side-by-side dalam satu window:
- Cleaner separation
- Easier to focus pada masing-masing view
- Lebih flexible untuk positioning

### 3. Visual Feedback
Progress bar memberikan feedback yang jelas:
- User tahu kapan gesture terdeteksi
- User bisa adjust pose jika belum stable
- Meningkatkan interactivity

## 🔮 Possible Enhancements

1. **Multi-Gesture Sequences**: Detect kombinasi gestures
2. **Custom Gestures**: Add your own reference images
3. **Sound Feedback**: Audio cue saat gesture terdeteksi
4. **Recording Mode**: Record gesture sequences
5. **Confidence Threshold**: Adjustable similarity threshold

## ✨ Credits

- Base implementation: Custom development
- Dual Window Pattern: Inspired by [aaronhubhachen/learning-imagerecognition](https://github.com/aaronhubhachen/learning-imagerecognition)
- MediaPipe: Google's pose & hand tracking
- OpenCV: Computer vision library

---

**Status**: ✅ Fully Implemented & Tested
**Date**: 2024
**Version**: 1.0.0
