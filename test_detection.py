"""
Test script untuk gesture detection tanpa gambar referensi
Hanya untuk test webcam + skeleton + hand tracking
"""

import cv2
import time
from gesture_detector import GestureDetector
import config


def main():
    print("=" * 60)
    print("TEST GESTURE DETECTION - Webcam + Skeleton + Hand Tracking")
    print("=" * 60)
    print("\nTekan 'q' untuk keluar\n")
    
    # Inisialisasi detector
    detector = GestureDetector()
    
    # Buka webcam
    cap = cv2.VideoCapture(config.CAMERA_INDEX)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.CAMERA_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.CAMERA_HEIGHT)
    
    if not cap.isOpened():
        print("Error: Tidak bisa membuka webcam!")
        return
    
    print("✓ Webcam terbuka")
    print("✓ Deteksi pose + hand tracking aktif")
    print("\nFitur yang terdeteksi:")
    print("  - 33 Pose landmarks (tubuh)")
    print("  - 21 Hand landmarks per tangan (max 2 tangan)")
    
    # Variables untuk FPS
    prev_time = time.time()
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Tidak bisa membaca frame")
                break
            
            # Flip horizontal (mirror)
            frame = cv2.flip(frame, 1)
            
            # Process frame
            frame, landmarks = detector.process_frame(frame)
            
            # Calculate FPS
            current_time = time.time()
            fps = 1 / (current_time - prev_time)
            prev_time = current_time
            
            # Display info
            info_text = []
            info_text.append(f"FPS: {fps:.1f}")
            
            if landmarks:
                if landmarks.get('pose_landmarks'):
                    info_text.append("Pose: DETECTED")
                else:
                    info_text.append("Pose: NOT FOUND")
                
                num_hands = len(landmarks.get('hand_landmarks', []))
                info_text.append(f"Hands: {num_hands}")
            else:
                info_text.append("Pose: NOT FOUND")
                info_text.append("Hands: 0")
            
            # Draw info
            y_offset = 30
            for text in info_text:
                cv2.putText(frame, text, (20, y_offset),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                y_offset += 35
            
            cv2.putText(frame, "Press 'q' to quit", (20, frame.shape[0] - 20),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            # Show frame
            cv2.imshow('Test: Pose + Hand Detection', frame)
            
            # Handle keyboard
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    finally:
        cap.release()
        cv2.destroyAllWindows()
        detector.close()
        print("\n✓ Test selesai")


if __name__ == "__main__":
    main()
