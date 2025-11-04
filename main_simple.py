"""
Gesture Matching Application
Adaptasi dari simple-mediapipe-project dengan gesture detection
Side-by-side display: Kiri (Webcam + Skeleton), Kanan (Reference Image)

Repository reference: https://github.com/aaronhubhachen/simple-mediapipe-project.git
"""

import cv2
import numpy as np
import os
from pathlib import Path
import time
from gesture_detector import GestureDetector
from pose_matcher import PoseMatcher
import config

# ============================================================================
# CONFIGURATION SETTINGS
# ============================================================================

# Window settings - side by side display
WINDOW_WIDTH = 640   # Width untuk masing-masing side
WINDOW_HEIGHT = 480
COMBINED_WIDTH = WINDOW_WIDTH * 2 + 20  # Gap 20px di tengah

# Gesture detection threshold
SIMILARITY_THRESHOLD = config.SIMILARITY_THRESHOLD

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """
    Main application loop - mengikuti struktur dari simple-mediapipe-project
    
    Steps:
    1. Load reference images
    2. Initialize webcam
    3. Initialize MediaPipe detector
    4. Run detection loop
    5. Display side-by-side (left: webcam, right: reference)
    """
    
    print("=" * 60)
    print("GESTURE MATCHING - SIDE BY SIDE DISPLAY")
    print("=" * 60)
    print("Adaptasi dari: simple-mediapipe-project")
    print()
    
    # ========================================================================
    # STEP 1: Load reference images
    # ========================================================================
    
    reference_path = Path(config.REFERENCE_IMAGES_PATH)
    
    if not reference_path.exists():
        print(f"\n[ERROR] Folder referensi tidak ditemukan: {reference_path}")
        print("Silakan buat folder 'reference_images/' dan tambahkan gambar pose referensi.")
        return
    
    # Load all images from reference folder
    reference_images = {}
    reference_poses = {}
    
    print(f"[LOADING] Memuat gambar referensi dari: {reference_path}")
    
    image_files = list(reference_path.glob('*.jpg')) + \
                  list(reference_path.glob('*.png')) + \
                  list(reference_path.glob('*.jpeg'))
    
    if not image_files:
        print(f"\n[ERROR] Tidak ada gambar di folder: {reference_path}")
        print("Silakan tambahkan file gambar (.jpg, .png, .jpeg)")
        return
    
    # Initialize detector untuk process reference images
    detector = GestureDetector()
    
    for img_file in image_files:
        pose_name = img_file.stem  # Nama file tanpa extension
        
        print(f"  Processing: {img_file.name}...")
        
        # Load image
        img = cv2.imread(str(img_file))
        if img is None:
            print(f"    ✗ Gagal membaca: {img_file.name}")
            continue
        
        # Store original image untuk display
        reference_images[pose_name] = img.copy()
        
        # Extract landmarks dari reference image (pass path string)
        _, landmarks = detector.process_image(str(img_file))
        
        if landmarks is not None:
            reference_poses[pose_name] = landmarks
            print(f"    ✓ Pose '{pose_name}' berhasil dimuat")
        else:
            print(f"    ✗ Tidak ada pose terdeteksi di {img_file.name}")
    
    if not reference_poses:
        print("\n[ERROR] Tidak ada pose referensi yang berhasil dimuat!")
        print("Pastikan gambar memiliki pose/gesture yang jelas.")
        return
    
    print(f"\n[OK] Total {len(reference_poses)} pose referensi berhasil dimuat")
    print(f"Pose: {', '.join(reference_poses.keys())}")
    
    # Initialize matcher
    matcher = PoseMatcher(reference_poses)
    
    # ========================================================================
    # STEP 2: Initialize webcam
    # ========================================================================
    
    cap = cv2.VideoCapture(config.CAMERA_INDEX)
    
    if not cap.isOpened():
        print("\n[ERROR] Tidak bisa membuka webcam!")
        print("Cek:")
        print("  - Webcam terhubung dengan benar")
        print("  - Tidak ada aplikasi lain yang menggunakan webcam")
        print("  - Permission webcam sudah diaktifkan")
        return
    
    # Set webcam resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, WINDOW_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, WINDOW_HEIGHT)
    
    print("[OK] Webcam initialized successfully!")
    
    # ========================================================================
    # STEP 3: Create display window
    # ========================================================================
    
    # Single window untuk side-by-side display
    window_name = 'Gesture Matching - Side by Side'
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    
    print("\n" + "=" * 60)
    print("[OK] Application started successfully!")
    print("=" * 60)
    print("\n[DISPLAY] Side by Side Layout:")
    print("  LEFT  : Webcam + Skeleton Overlay")
    print("  RIGHT : Reference Image (when matched)")
    print("\n[CONTROLS]")
    print("  Q : Quit")
    print("  S : Save screenshot")
    print("\n[GESTURE] Strike a pose to match with reference images!\n")
    
    # Default - no match yet
    current_reference = None
    current_match_name = None
    
    # Variables untuk FPS
    prev_time = time.time()
    fps = 0
    
    # ========================================================================
    # STEP 4: Main detection loop
    # ========================================================================
    
    try:
        while True:
            # Read frame from webcam
            ret, frame = cap.read()
            
            if not ret:
                print("\n[ERROR] Tidak bisa membaca frame dari webcam.")
                break
            
            # Flip horizontally untuk mirror effect
            frame = cv2.flip(frame, 1)
            
            # Resize to match target size
            frame = cv2.resize(frame, (WINDOW_WIDTH, WINDOW_HEIGHT))
            
            # ==============================================================
            # Detect pose/gesture menggunakan MediaPipe
            # ==============================================================
            
            frame_with_skeleton, landmarks = detector.process_frame(frame)
            
            # ==============================================================
            # Match dengan reference poses
            # ==============================================================
            
            match_name = None
            similarity = 0.0
            
            if landmarks is not None and matcher is not None:
                match_name, similarity = matcher.find_best_match(landmarks)
                
                if match_name:
                    current_match_name = match_name
                    current_reference = reference_images[match_name]
            
            # Calculate FPS
            current_time = time.time()
            fps = 1 / (current_time - prev_time)
            prev_time = current_time
            
            # ==============================================================
            # Create side-by-side display
            # ==============================================================
            
            # Left side: Webcam with skeleton
            left_frame = frame_with_skeleton.copy()
            
            # Right side: Reference image atau placeholder
            if current_reference is not None:
                right_frame = cv2.resize(current_reference, (WINDOW_WIDTH, WINDOW_HEIGHT))
            else:
                # Placeholder ketika tidak ada match
                right_frame = np.zeros((WINDOW_HEIGHT, WINDOW_WIDTH, 3), dtype=np.uint8)
                cv2.putText(right_frame, "No Match Yet", 
                           (WINDOW_WIDTH//2 - 100, WINDOW_HEIGHT//2),
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                cv2.putText(right_frame, "Strike a Pose!", 
                           (WINDOW_WIDTH//2 - 100, WINDOW_HEIGHT//2 + 50),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
            
            # Create combined canvas
            gap = 20
            combined = np.zeros((WINDOW_HEIGHT, COMBINED_WIDTH, 3), dtype=np.uint8)
            
            # Paste left frame
            combined[0:WINDOW_HEIGHT, 0:WINDOW_WIDTH] = left_frame
            
            # Paste right frame
            combined[0:WINDOW_HEIGHT, WINDOW_WIDTH+gap:WINDOW_WIDTH*2+gap] = right_frame
            
            # Draw separator lines
            cv2.line(combined, (WINDOW_WIDTH, 0), (WINDOW_WIDTH, WINDOW_HEIGHT), 
                    (255, 255, 255), 2)
            cv2.line(combined, (WINDOW_WIDTH+gap, 0), (WINDOW_WIDTH+gap, WINDOW_HEIGHT), 
                    (255, 255, 255), 2)
            
            # ==============================================================
            # Add text overlays
            # ==============================================================
            
            # Header labels
            cv2.rectangle(combined, (0, 0), (WINDOW_WIDTH, 60), (0, 0, 0), -1)
            cv2.rectangle(combined, (WINDOW_WIDTH+gap, 0), (COMBINED_WIDTH, 60), (0, 0, 0), -1)
            
            cv2.putText(combined, "YOUR POSE", (20, 40),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            if current_match_name:
                cv2.putText(combined, f"MATCH: {current_match_name.upper()}", 
                           (WINDOW_WIDTH+gap+20, 40),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            else:
                cv2.putText(combined, "REFERENCE", 
                           (WINDOW_WIDTH+gap+20, 40),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            
            # Bottom info bar
            info_y = WINDOW_HEIGHT - 60
            cv2.rectangle(combined, (0, info_y), (COMBINED_WIDTH, WINDOW_HEIGHT), (0, 0, 0), -1)
            
            # FPS
            cv2.putText(combined, f"FPS: {fps:.1f}", (20, info_y + 35),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            # Similarity
            if match_name and similarity > 0:
                cv2.putText(combined, f"Similarity: {similarity:.1%}", 
                           (WINDOW_WIDTH+gap+20, info_y + 35),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            
            # Controls
            cv2.putText(combined, "Q: Quit | S: Save", 
                       (COMBINED_WIDTH//2 - 120, info_y + 35),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            # ==============================================================
            # Display window
            # ==============================================================
            
            cv2.imshow(window_name, combined)
            
            # ==============================================================
            # Handle keyboard input
            # ==============================================================
            
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('q'):
                print("\n[QUIT] Keluar dari aplikasi...")
                break
            elif key == ord('s'):
                # Save screenshot
                output_path = Path(config.OUTPUT_PATH)
                output_path.mkdir(parents=True, exist_ok=True)
                
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                filename = output_path / f"gesture_match_{timestamp}.jpg"
                
                cv2.imwrite(str(filename), combined)
                print(f"[SAVE] Screenshot saved: {filename}")
    
    finally:
        # ====================================================================
        # STEP 5: Cleanup
        # ====================================================================
        
        print("\n[CLEANUP] Menutup aplikasi...")
        
        # Release webcam
        cap.release()
        
        # Close all windows
        cv2.destroyAllWindows()
        
        # Close MediaPipe detector
        detector.close()
        
        print("[OK] Application closed successfully.")
        print("Thanks for using Gesture Matching!\n")


if __name__ == "__main__":
    main()
