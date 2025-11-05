# Gesture Matching - Simple Version

## 📋 Overview
Versi simplified dari gesture matching application, diadaptasi dari struktur **simple-mediapipe-project** dengan layout **side-by-side** (kiri: webcam + skeleton, kanan: reference image).

Repository reference: https://github.com/aaronhubhachen/simple-mediapipe-project.git

## 🎯 Key Features

### 1. **Simple Structure**
- Mengikuti struktur dari simple-mediapipe-project
- Single file main application (`main_simple.py`)
- Clean, readable code dengan extensive comments

### 2. **Side-by-Side Display**
```
┌──────────────────────────────────────────────────────────────┐
│  YOUR POSE          │          MATCH: MONKEY1                │
├─────────────────────┼────────────────────────────────────────┤
│                     │                                        │
│   [Webcam Feed]     │     [Reference Image]                  │
│   + Skeleton        │                                        │
│                     │                                        │
├─────────────────────┴────────────────────────────────────────┤
│  FPS: 30.0          │  Similarity: 85%  │  Q: Quit | S: Save │
└──────────────────────────────────────────────────────────────┘
```

**Layout:**
- **LEFT**: Webcam real-time + skeleton overlay (pose + hands)
- **RIGHT**: Reference image yang match (atau placeholder)

### 3. **Real-time Detection**
- MediaPipe Pose: 33 landmarks
- MediaPipe Hands: 21 landmarks per hand (max 2 hands)
- Cosine similarity matching
- Threshold: 85% similarity untuk match

## 🚀 Quick Start

### Running the Application:
```bash
cd e:\make_meme_with_Python1
python main_simple.py
```

### Expected Output:
```
============================================================
GESTURE MATCHING - SIDE BY SIDE DISPLAY
============================================================
Adaptasi dari: simple-mediapipe-project

[LOADING] Memuat gambar referensi dari: reference_images
INFO: Created TensorFlow Lite XNNPACK delegate for CPU.
  Processing: monkey1.jpg...
    ✓ Pose 'monkey1' berhasil dimuat
  Processing: monkey2.jpg...
    ✓ Pose 'monkey2' berhasil dimuat

[OK] Total 2 pose referensi berhasil dimuat
Pose: monkey1, monkey2
[OK] Webcam initialized successfully!

============================================================
[OK] Application started successfully!
============================================================

[DISPLAY] Side by Side Layout:
  LEFT  : Webcam + Skeleton Overlay
  RIGHT : Reference Image (when matched)

[CONTROLS]
  Q : Quit
  S : Save screenshot

[GESTURE] Strike a pose to match with reference images!
```

## 🎮 Controls

| Key | Action |
|-----|--------|
| `Q` | Quit aplikasi |
| `S` | Save screenshot |

## 📁 Project Structure

```
make_meme_with_Python1/
├── main_simple.py              # ← NEW: Simplified main application
├── main.py                     # Old: Dual window version
├── gesture_detector.py         # MediaPipe detector
├── pose_matcher.py            # Similarity matcher
├── config.py                  # Configuration
├── reference_images/          # Reference gesture images
│   ├── monkey1.jpg
│   ├── monkey2.jpg
│   └── ...
└── outputs/                   # Saved screenshots
    └── gesture_match_*.jpg
```

## 🔧 Configuration

### Window Settings (in main_simple.py):
```python
WINDOW_WIDTH = 640          # Width masing-masing side
WINDOW_HEIGHT = 480         # Height window
COMBINED_WIDTH = 1300       # Total width (640*2 + 20px gap)
```

### Detection Settings (in config.py):
```python
SIMILARITY_THRESHOLD = 0.85    # 85% similarity untuk match
CAMERA_INDEX = 0               # Webcam index
MIN_DETECTION_CONFIDENCE = 0.5 # MediaPipe confidence
```

## 🎨 Differences from Original

### From simple-mediapipe-project:
| Original | Our Version |
|----------|-------------|
| Tongue detection | Gesture/Pose detection |
| Face Mesh (468 landmarks) | Pose (33) + Hands (21x2) |
| 2 separate windows | 1 window side-by-side |
| apple.png / appletongue.png | Multiple reference images |

### From Our Dual Window Version:
| Dual Window | Simple Version |
|-------------|----------------|
| 2 separate windows | 1 window side-by-side |
| Gesture smoothing | Direct matching |
| Stability progress bar | Simple match display |
| Complex state management | Straightforward logic |

## ✨ Advantages of Simple Version

1. **Cleaner Code**: Mengikuti struktur simple-mediapipe-project yang clean
2. **Single Window**: Lebih mudah untuk positioning dan management
3. **Straightforward**: Tanpa smoothing complexity, langsung show hasil
4. **Easy to Understand**: Perfect untuk learning dan modification

## 🔍 How It Works

### Step-by-Step Flow:

1. **Load Reference Images**
   ```python
   # Scan reference_images/ folder
   # Load all .jpg, .png, .jpeg files
   # Extract pose landmarks from each image
   ```

2. **Initialize Webcam**
   ```python
   # Open camera (index 0)
   # Set resolution to 640x480
   # Ready for frame capture
   ```

3. **Main Loop**
   ```python
   while True:
       # Capture frame from webcam
       # Process with MediaPipe (pose + hands)
       # Match dengan reference poses
       # Create side-by-side display
       # Show combined window
   ```

4. **Display Logic**
   ```python
   # LEFT: webcam frame + skeleton overlay
   # RIGHT: matched reference image (or placeholder)
   # Add labels, FPS, similarity info
   ```

## 📊 Performance

- **FPS**: ~30 FPS (hardware dependent)
- **Latency**: ~33ms per frame
- **Accuracy**: Depends on similarity threshold (default 85%)
- **Memory**: Lightweight, similar to simple-mediapipe-project

## 🎓 Learning Points

### 1. Structure from simple-mediapipe-project
- Clean main() function with clear steps
- Extensive comments for learning
- Step-by-step initialization
- Proper error handling

### 2. Side-by-Side Display
- Single window lebih simple than dual windows
- Easy canvas composition with numpy
- Clear visual separation

### 3. MediaPipe Integration
- Pose detection (33 landmarks)
- Hand tracking (21 landmarks per hand)
- Combined detection for full gesture

## 🔮 Possible Enhancements

1. **Add Gesture Smoothing**: Borrow from our dual window version
2. **Multiple References**: Show top 3 matches instead of just best
3. **Confidence Indicator**: Visual bar showing match confidence
4. **Recording Mode**: Record gesture sequences
5. **Custom Gestures**: Easy UI to add new reference poses

## 🆚 Version Comparison

### When to Use Simple Version:
- ✅ Learning gesture detection basics
- ✅ Quick prototyping
- ✅ Single monitor setup
- ✅ Prefer side-by-side visualization
- ✅ Want straightforward code

### When to Use Dual Window Version:
- ✅ Need gesture smoothing (anti-flicker)
- ✅ Multi-monitor setup available
- ✅ Want stability progress feedback
- ✅ Production-ready application
- ✅ Need temporal consistency

## 🎯 Tips for Best Results

### 1. Good Lighting
- Well-lit environment
- Avoid backlight
- Consistent lighting

### 2. Clear Gestures
- Distinct poses/gestures
- Hold pose steady for 1-2 seconds
- Avoid rapid movements

### 3. Camera Position
- Distance: 1-2 meters from camera
- Position: Upper body visible
- Background: Plain/solid better

### 4. Reference Images
- Clear, high-quality images
- Distinct poses that are easy to differentiate
- Similar angle/perspective to webcam

## 📝 Code Structure

### Main Steps (Commented in Code):

```python
# STEP 1: Load reference images
#   - Scan reference_images/ folder
#   - Extract landmarks from each image
#   - Store both image and landmarks

# STEP 2: Initialize webcam
#   - Open camera device
#   - Set resolution
#   - Verify successful opening

# STEP 3: Create display window
#   - Single window for side-by-side
#   - Set window properties

# STEP 4: Main detection loop
#   - Capture frame
#   - Process with MediaPipe
#   - Match with references
#   - Create side-by-side display
#   - Handle user input

# STEP 5: Cleanup
#   - Release webcam
#   - Close windows
#   - Close MediaPipe
```

## 🙏 Credits

- **Structure**: Inspired by [simple-mediapipe-project](https://github.com/aaronhubhachen/simple-mediapipe-project.git)
- **Detection**: MediaPipe by Google
- **CV Library**: OpenCV
- **Matching**: Custom cosine similarity implementation

---

**Version**: 1.0.0 (Simple)  
**Date**: November 4, 2025  
**Status**: ✅ Fully Functional  
**Recommended for**: Learning & Quick Prototyping
