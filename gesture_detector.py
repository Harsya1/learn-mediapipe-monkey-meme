"""
Gesture Detector Module
Menggunakan MediaPipe untuk mendeteksi pose tubuh dan tangan dari webcam
"""

import cv2
import mediapipe as mp
import numpy as np
from typing import Optional, List, Tuple, Dict
import config


class GestureDetector:
    """Class untuk mendeteksi pose dan hand tracking menggunakan MediaPipe"""
    
    def __init__(self):
        """Inisialisasi MediaPipe Pose dan Hands"""
        self.mp_pose = mp.solutions.pose
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=config.MIN_DETECTION_CONFIDENCE,
            min_tracking_confidence=config.MIN_TRACKING_CONFIDENCE
        )
        
        # Inisialisasi hand tracking
        self.hands = self.mp_hands.Hands(
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7,
            max_num_hands=2
        )
        
    def process_frame(self, frame: np.ndarray) -> Tuple[np.ndarray, Optional[Dict]]:
        """
        Proses frame untuk mendeteksi pose dan hands
        
        Args:
            frame: Frame dari webcam (BGR format)
            
        Returns:
            Tuple berisi:
            - Frame yang sudah digambar skeleton pose dan hands
            - Dict dengan 'pose_landmarks' dan 'hand_landmarks' (atau None jika tidak terdeteksi)
        """
        # Convert BGR to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_rgb.flags.writeable = False
        
        # Process pose dengan MediaPipe
        pose_results = self.pose.process(frame_rgb)
        
        # Process hands dengan MediaPipe
        hands_results = self.hands.process(frame_rgb)
        
        # Convert back to BGR
        frame_rgb.flags.writeable = True
        frame_bgr = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)
        
        landmarks_data = {
            'pose_landmarks': None,
            'hand_landmarks': []
        }
        
        # Gambar pose landmarks jika terdeteksi
        if pose_results.pose_landmarks:
            self.mp_drawing.draw_landmarks(
                frame_bgr,
                pose_results.pose_landmarks,
                self.mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=self.mp_drawing_styles.get_default_pose_landmarks_style()
            )
            
            # Extract pose landmarks
            landmarks_data['pose_landmarks'] = self._extract_landmarks(pose_results.pose_landmarks)
        
        # Gambar hand landmarks jika terdeteksi
        if hands_results.multi_hand_landmarks:
            for hand_landmarks in hands_results.multi_hand_landmarks:
                # Gambar hand skeleton dengan warna berbeda
                self.mp_drawing.draw_landmarks(
                    frame_bgr,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing_styles.get_default_hand_landmarks_style(),
                    self.mp_drawing_styles.get_default_hand_connections_style()
                )
                
                # Extract hand landmarks
                hand_lm = self._extract_landmarks(hand_landmarks)
                landmarks_data['hand_landmarks'].append(hand_lm)
        
        # Return frame dan landmarks (atau None jika tidak ada yang terdeteksi)
        if landmarks_data['pose_landmarks'] is not None or len(landmarks_data['hand_landmarks']) > 0:
            return frame_bgr, landmarks_data
        
        return frame_bgr, None
    
    def _extract_landmarks(self, pose_landmarks) -> List[Tuple[float, float, float]]:
        """
        Extract pose landmarks sebagai list koordinat
        
        Args:
            pose_landmarks: MediaPipe pose landmarks object
            
        Returns:
            List of tuples (x, y, visibility)
        """
        landmarks = []
        for landmark in pose_landmarks.landmark:
            landmarks.append((landmark.x, landmark.y, landmark.visibility))
        return landmarks
    
    def process_image(self, image_path: str) -> Tuple[Optional[np.ndarray], Optional[Dict]]:
        """
        Proses gambar untuk mendeteksi pose dan hands
        
        Args:
            image_path: Path ke file gambar
            
        Returns:
            Tuple berisi:
            - Image yang sudah digambar skeleton pose dan hands (atau None)
            - Dict landmarks pose dan hands (atau None)
        """
        try:
            image = cv2.imread(image_path)
            if image is None:
                print(f"Error: Tidak bisa membaca gambar {image_path}")
                return None, None
            
            # Convert BGR to RGB
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image_rgb.flags.writeable = False
            
            # Process pose dengan MediaPipe
            pose_results = self.pose.process(image_rgb)
            
            # Process hands dengan MediaPipe
            hands_results = self.hands.process(image_rgb)
            
            # Convert back to BGR
            image_rgb.flags.writeable = True
            image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
            
            landmarks_data = {
                'pose_landmarks': None,
                'hand_landmarks': []
            }
            
            if pose_results.pose_landmarks:
                # Gambar pose landmarks
                self.mp_drawing.draw_landmarks(
                    image_bgr,
                    pose_results.pose_landmarks,
                    self.mp_pose.POSE_CONNECTIONS,
                    landmark_drawing_spec=self.mp_drawing_styles.get_default_pose_landmarks_style()
                )
                
                landmarks_data['pose_landmarks'] = self._extract_landmarks(pose_results.pose_landmarks)
            
            # Gambar hand landmarks jika terdeteksi
            if hands_results.multi_hand_landmarks:
                for hand_landmarks in hands_results.multi_hand_landmarks:
                    self.mp_drawing.draw_landmarks(
                        image_bgr,
                        hand_landmarks,
                        self.mp_hands.HAND_CONNECTIONS,
                        self.mp_drawing_styles.get_default_hand_landmarks_style(),
                        self.mp_drawing_styles.get_default_hand_connections_style()
                    )
                    
                    hand_lm = self._extract_landmarks(hand_landmarks)
                    landmarks_data['hand_landmarks'].append(hand_lm)
            
            if landmarks_data['pose_landmarks'] is not None or len(landmarks_data['hand_landmarks']) > 0:
                return image_bgr, landmarks_data
            else:
                print(f"Warning: Tidak ada pose/hand terdeteksi di {image_path}")
                return image_bgr, None
                
        except Exception as e:
            print(f"Error processing image {image_path}: {e}")
            return None, None
    
    def close(self):
        """Tutup MediaPipe Pose dan Hands"""
        self.pose.close()
        self.hands.close()
