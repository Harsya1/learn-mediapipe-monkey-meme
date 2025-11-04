"""
Main Application - Gesture Detection with Pose Matching
Deteksi pose dari webcam dan cocokkan dengan gambar referensi
"""

import cv2
import os
import sys
from pathlib import Path
import time
import numpy as np
from gesture_detector import GestureDetector
from pose_matcher import PoseMatcher
import config


class GestureMatchingApp:
    """Aplikasi utama untuk gesture detection dan matching"""
    
    def __init__(self):
        """Inisialisasi aplikasi"""
        self.detector = GestureDetector()
        self.reference_poses = {}
        self.reference_images = {}  # Menyimpan gambar referensi asli
        self.matcher = None
        self.last_match_time = 0
        self.last_match_name = None
        
        # Gesture smoothing (dari repository referensi)
        self.gesture_history = []
        self.HISTORY_SIZE = 8
        self.last_stable_gesture = None
        self.gesture_hold_frames = 0
        self.MIN_HOLD_FRAMES = 10  # Perlu hold 10 frames untuk stabilitas
        
    def load_reference_images(self):
        """Load semua gambar referensi dari folder reference_images"""
        ref_path = Path(config.REFERENCE_IMAGES_PATH)
        
        if not ref_path.exists():
            print(f"Folder {config.REFERENCE_IMAGES_PATH} tidak ditemukan!")
            print("Membuat folder...")
            ref_path.mkdir(parents=True, exist_ok=True)
            print(f"Silakan tambahkan gambar referensi ke folder {config.REFERENCE_IMAGES_PATH}")
            return False
        
        # Cari semua file gambar
        image_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
        image_files = []
        for ext in image_extensions:
            image_files.extend(ref_path.glob(f'*{ext}'))
            image_files.extend(ref_path.glob(f'*{ext.upper()}'))
        
        if len(image_files) == 0:
            print(f"Tidak ada gambar referensi di folder {config.REFERENCE_IMAGES_PATH}!")
            print("Silakan tambahkan gambar referensi dengan format: .jpg, .jpeg, .png, atau .bmp")
            return False
        
        print(f"\nMemuat {len(image_files)} gambar referensi...")
        
        for img_path in image_files:
            pose_name = img_path.stem  # Nama file tanpa ekstensi
            print(f"  Processing: {img_path.name}...")
            
            # Load gambar asli untuk display
            original_img = cv2.imread(str(img_path))
            
            _, landmarks = self.detector.process_image(str(img_path))
            
            if landmarks is not None:
                self.reference_poses[pose_name] = landmarks
                self.reference_images[pose_name] = original_img  # Simpan gambar asli
                print(f"    ✓ Pose '{pose_name}' berhasil dimuat")
            else:
                print(f"    ✗ Gagal mendeteksi pose di '{pose_name}'")
        
        if len(self.reference_poses) == 0:
            print("\nTidak ada pose yang berhasil dimuat!")
            print("Pastikan gambar referensi menunjukkan pose tubuh yang jelas.")
            return False
        
        print(f"\n✓ Total {len(self.reference_poses)} pose referensi berhasil dimuat")
        print(f"Pose: {', '.join(self.reference_poses.keys())}\n")
        
        # Inisialisasi matcher
        self.matcher = PoseMatcher(self.reference_poses)
        return True
    
    def smooth_gesture(self, gesture_name):
        """
        Smooth gesture detection untuk menghindari flickering
        Implementasi dari repository referensi
        
        Args:
            gesture_name: Nama gesture yang terdeteksi (atau None)
            
        Returns:
            Stable gesture name (atau None)
        """
        self.gesture_history.append(gesture_name)
        if len(self.gesture_history) > self.HISTORY_SIZE:
            self.gesture_history.pop(0)
        
        # Count occurrences di recent history
        gesture_count = self.gesture_history.count(gesture_name)
        threshold = self.HISTORY_SIZE * 0.6
        
        # Check apakah gesture stable
        if gesture_name is not None and gesture_count > threshold:
            self.gesture_hold_frames += 1
            if self.gesture_hold_frames >= self.MIN_HOLD_FRAMES:
                self.last_stable_gesture = gesture_name
        else:
            self.gesture_hold_frames = max(0, self.gesture_hold_frames - 1)
            if gesture_name is None and self.gesture_hold_frames == 0:
                none_count = self.gesture_history.count(None)
                if none_count > self.HISTORY_SIZE * 0.7:
                    self.last_stable_gesture = None
        
        return self.last_stable_gesture
    
    def draw_info(self, frame, match_name=None, similarity=0.0, fps=0):
        """
        Gambar informasi di frame
        
        Args:
            frame: Frame untuk digambar
            match_name: Nama pose yang cocok
            similarity: Score similarity
            fps: Frame per second
        """
        h, w = frame.shape[:2]
        
        # Background untuk text
        cv2.rectangle(frame, (10, 10), (w - 10, 120), (0, 0, 0), -1)
        cv2.rectangle(frame, (10, 10), (w - 10, 120), config.COLOR_WHITE, 2)
        
        # FPS
        cv2.putText(frame, f"FPS: {fps:.1f}", (20, 35),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, config.COLOR_WHITE, 2)
        
        # Match status
        if match_name:
            text = f"MATCH: {match_name}"
            color = config.COLOR_GREEN
            cv2.putText(frame, text, (20, 65),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
            cv2.putText(frame, f"Similarity: {similarity:.2%}", (20, 95),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        else:
            cv2.putText(frame, "No Match", (20, 65),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, config.COLOR_RED, 2)
            if similarity > 0:
                cv2.putText(frame, f"Best: {similarity:.2%}", (20, 95),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, config.COLOR_RED, 2)
        
        # Instructions
        cv2.putText(frame, "Press 'q' to quit, 's' to save", (20, h - 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, config.COLOR_WHITE, 1)
    
    def create_side_by_side_view(self, frame_left, frame_right, match_name=None, similarity=0.0, fps=0):
        """
        Gabungkan 2 frame side-by-side dengan label dan info
        
        Args:
            frame_left: Frame kiri (webcam dengan skeleton)
            frame_right: Frame kanan (gambar referensi atau placeholder)
            match_name: Nama pose yang cocok
            similarity: Score similarity
            fps: Frame per second
            
        Returns:
            Combined frame
        """
        h, w = frame_left.shape[:2]
        
        # Resize frame_right untuk match ukuran frame_left
        if frame_right is not None:
            frame_right = cv2.resize(frame_right, (w, h))
        else:
            # Buat placeholder jika tidak ada match
            frame_right = np.zeros((h, w, 3), dtype=np.uint8)
            cv2.putText(frame_right, "No Match Yet", (w//2 - 100, h//2),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, config.COLOR_WHITE, 2)
            cv2.putText(frame_right, "Strike a Pose!", (w//2 - 100, h//2 + 50),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, config.COLOR_BLUE, 2)
        
        # Buat canvas untuk side-by-side
        gap = 20  # Gap antara 2 frame
        combined_width = w * 2 + gap
        combined = np.zeros((h, combined_width, 3), dtype=np.uint8)
        
        # Paste frame kiri
        combined[0:h, 0:w] = frame_left
        
        # Paste frame kanan
        combined[0:h, w+gap:w*2+gap] = frame_right
        
        # Garis pemisah
        cv2.line(combined, (w, 0), (w, h), config.COLOR_WHITE, 2)
        cv2.line(combined, (w+gap, 0), (w+gap, h), config.COLOR_WHITE, 2)
        
        # Background untuk header
        cv2.rectangle(combined, (0, 0), (w, 60), (0, 0, 0), -1)
        cv2.rectangle(combined, (w+gap, 0), (combined_width, 60), (0, 0, 0), -1)
        
        # Label untuk masing-masing side
        cv2.putText(combined, "YOUR POSE", (20, 35),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, config.COLOR_GREEN, 2)
        
        if match_name:
            cv2.putText(combined, f"MATCHED: {match_name.upper()}", (w+gap+20, 35),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, config.COLOR_GREEN, 2)
        else:
            cv2.putText(combined, "REFERENCE IMAGE", (w+gap+20, 35),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, config.COLOR_RED, 2)
        
        # Info di bottom
        info_y = h - 60
        cv2.rectangle(combined, (0, info_y), (combined_width, h), (0, 0, 0), -1)
        
        cv2.putText(combined, f"FPS: {fps:.1f}", (20, info_y + 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, config.COLOR_WHITE, 2)
        
        if match_name:
            cv2.putText(combined, f"Similarity: {similarity:.1%}", (w+gap+20, info_y + 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, config.COLOR_GREEN, 2)
        
        cv2.putText(combined, "Q: Quit | S: Save Screenshot", 
                   (combined_width//2 - 150, info_y + 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, config.COLOR_WHITE, 1)
        
        return combined
    
    def run(self):
        """Jalankan aplikasi utama"""
        # Load reference images
        if not self.load_reference_images():
            print("\nTidak bisa melanjutkan tanpa gambar referensi.")
            print(f"\nCara menggunakan:")
            print(f"1. Tambahkan gambar pose referensi ke folder '{config.REFERENCE_IMAGES_PATH}'")
            print(f"2. Beri nama file sesuai pose (contoh: 'tpose.jpg', 'wave.png')")
            print(f"3. Jalankan ulang program ini")
            return
        
        # Buka webcam
        cap = cv2.VideoCapture(config.CAMERA_INDEX)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.CAMERA_WIDTH)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.CAMERA_HEIGHT)
        
        if not cap.isOpened():
            print("Error: Tidak bisa membuka webcam!")
            return
        
        print("Webcam terbuka. Mulai deteksi pose + hand tracking...")
        print("Tekan 'q' untuk keluar, 's' untuk save screenshot")
        print("\nWindow Layout:")
        print("  - Camera Feed: Webcam + Skeleton (Pose + Hand Tracking)")
        print("  - Detected Gesture: Gambar Referensi yang Match")
        
        # Create dual windows (pattern dari repository referensi)
        cv2.namedWindow('Camera Feed', cv2.WINDOW_NORMAL)
        cv2.namedWindow('Detected Gesture', cv2.WINDOW_NORMAL)
        
        # Variables untuk FPS
        prev_time = time.time()
        fps = 0
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    print("Error: Tidak bisa membaca frame dari webcam")
                    break
                
                # Flip frame horizontal (mirror)
                frame = cv2.flip(frame, 1)
                
                # Detect pose + hands
                camera_display, landmarks = self.detector.process_frame(frame)
                
                # Match dengan reference poses
                raw_match_name = None
                similarity = 0.0
                
                if landmarks is not None and self.matcher is not None:
                    raw_match_name, similarity = self.matcher.find_best_match(landmarks)
                
                # Apply gesture smoothing (dari repository referensi)
                stable_gesture = self.smooth_gesture(raw_match_name)
                
                # Calculate FPS
                current_time = time.time()
                fps = 1 / (current_time - prev_time)
                prev_time = current_time
                
                # Draw FPS dan info di camera feed
                h, w = camera_display.shape[:2]
                
                # Info box background
                cv2.rectangle(camera_display, (10, 10), (w - 10, 100), (0, 0, 0), -1)
                cv2.rectangle(camera_display, (10, 10), (w - 10, 100), config.COLOR_WHITE, 2)
                
                # FPS
                cv2.putText(camera_display, f"FPS: {fps:.1f}", (20, 35),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, config.COLOR_WHITE, 2)
                
                # Gesture info
                if stable_gesture:
                    cv2.putText(camera_display, f"Gesture: {stable_gesture}", (20, 65),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, config.COLOR_GREEN, 2)
                else:
                    cv2.putText(camera_display, "No Gesture", (20, 65),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, config.COLOR_RED, 2)
                
                # Stability progress bar (dari repository referensi)
                bar_width = w - 40
                bar_height = 10
                bar_x = 20
                bar_y = 80
                
                # Background bar
                cv2.rectangle(camera_display, (bar_x, bar_y), 
                             (bar_x + bar_width, bar_y + bar_height),
                             config.COLOR_WHITE, 1)
                
                # Progress bar
                progress = min(self.gesture_hold_frames / self.MIN_HOLD_FRAMES, 1.0)
                progress_width = int(bar_width * progress)
                
                if progress >= 1.0:
                    bar_color = config.COLOR_GREEN  # Stable
                elif progress > 0.5:
                    bar_color = config.COLOR_BLUE   # Getting stable
                else:
                    bar_color = config.COLOR_RED    # Not stable
                
                if progress_width > 0:
                    cv2.rectangle(camera_display, (bar_x, bar_y),
                                 (bar_x + progress_width, bar_y + bar_height),
                                 bar_color, -1)
                
                # Gesture display window
                if stable_gesture and stable_gesture in self.reference_images:
                    gesture_display = self.reference_images[stable_gesture].copy()
                    
                    # Resize to match camera display
                    gesture_display = cv2.resize(gesture_display, (w, h))
                    
                    # Add label
                    cv2.rectangle(gesture_display, (0, 0), (w, 60), (0, 0, 0), -1)
                    cv2.putText(gesture_display, f"DETECTED: {stable_gesture.upper()}", 
                               (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.0, 
                               config.COLOR_GREEN, 2)
                else:
                    # Create placeholder
                    gesture_display = np.zeros((h, w, 3), dtype=np.uint8)
                    cv2.putText(gesture_display, "No Gesture Detected", 
                               (w//2 - 150, h//2),
                               cv2.FONT_HERSHEY_SIMPLEX, 1, config.COLOR_WHITE, 2)
                    cv2.putText(gesture_display, "Strike a Pose!", 
                               (w//2 - 100, h//2 + 50),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.8, config.COLOR_BLUE, 2)
                
                # Show dual windows (pattern dari repository)
                cv2.imshow('Camera Feed', camera_display)
                cv2.imshow('Detected Gesture', gesture_display)
                
                # Handle keyboard input
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    print("\nKeluar dari aplikasi...")
                    break
                elif key == ord('s'):
                    # Save screenshot (both windows)
                    output_path = Path(config.OUTPUT_PATH)
                    output_path.mkdir(parents=True, exist_ok=True)
                    
                    timestamp = time.strftime("%Y%m%d_%H%M%S")
                    
                    # Save camera feed
                    filename_camera = output_path / f"camera_{timestamp}.jpg"
                    cv2.imwrite(str(filename_camera), camera_display)
                    
                    # Save gesture display
                    filename_gesture = output_path / f"gesture_{timestamp}.jpg"
                    cv2.imwrite(str(filename_gesture), gesture_display)
                    
                    print(f"Screenshots saved:")
                    print(f"  - {filename_camera}")
                    print(f"  - {filename_gesture}")
        
        finally:
            # Cleanup
            cap.release()
            cv2.destroyAllWindows()
            self.detector.close()
            print("Aplikasi ditutup.")


def main():
    """Entry point"""
    print("=" * 60)
    print("GESTURE DETECTION - POSE MATCHING")
    print("=" * 60)
    print("Aplikasi untuk mendeteksi pose dan mencocokkan dengan gambar referensi")
    print()
    
    app = GestureMatchingApp()
    app.run()


if __name__ == "__main__":
    main()
