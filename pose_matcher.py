"""
Pose Matcher Module
Mencocokkan pose dari webcam dengan pose di gambar referensi
"""

import numpy as np
from typing import List, Tuple, Optional
import os
import config


class PoseMatcher:
    """Class untuk mencocokkan pose dengan gambar referensi"""
    
    def __init__(self, reference_poses: dict):
        """
        Inisialisasi PoseMatcher
        
        Args:
            reference_poses: Dictionary dengan format {nama_pose: landmarks}
        """
        self.reference_poses = reference_poses
        
    def calculate_similarity(self, landmarks1, landmarks2) -> float:
        """
        Hitung similarity antara dua pose menggunakan cosine similarity
        Mendukung dict (pose + hands) atau list (pose saja)
        
        Args:
            landmarks1: Dict atau List landmarks pertama
            landmarks2: Dict atau List landmarks kedua
            
        Returns:
            Similarity score (0-1, semakin tinggi semakin mirip)
        """
        if landmarks1 is None or landmarks2 is None:
            return 0.0
        
        # Extract pose landmarks saja untuk comparison
        pose1 = landmarks1.get('pose_landmarks') if isinstance(landmarks1, dict) else landmarks1
        pose2 = landmarks2.get('pose_landmarks') if isinstance(landmarks2, dict) else landmarks2
        
        if pose1 is None or pose2 is None:
            return 0.0
        
        if len(pose1) != len(pose2):
            return 0.0
        
        # Ekstrak koordinat x, y saja (abaikan visibility)
        coords1 = np.array([(lm[0], lm[1]) for lm in pose1])
        coords2 = np.array([(lm[0], lm[1]) for lm in pose2])
        
        # Normalisasi koordinat (center dan scale)
        coords1_norm = self._normalize_pose(coords1)
        coords2_norm = self._normalize_pose(coords2)
        
        # Flatten arrays
        vec1 = coords1_norm.flatten()
        vec2 = coords2_norm.flatten()
        
        # Hitung cosine similarity
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        similarity = dot_product / (norm1 * norm2)
        
        # Convert ke range 0-1
        similarity = (similarity + 1) / 2
        
        return similarity
    
    def _normalize_pose(self, coords: np.ndarray) -> np.ndarray:
        """
        Normalisasi koordinat pose (center dan scale)
        
        Args:
            coords: Array koordinat (N, 2)
            
        Returns:
            Normalized coordinates
        """
        # Center: kurangi dengan mean
        centered = coords - np.mean(coords, axis=0)
        
        # Scale: bagi dengan standard deviation
        std = np.std(centered)
        if std > 0:
            normalized = centered / std
        else:
            normalized = centered
            
        return normalized
    
    def find_best_match(self, current_landmarks) -> Tuple[Optional[str], float]:
        """
        Temukan pose referensi yang paling cocok dengan pose saat ini
        
        Args:
            current_landmarks: Dict atau List landmarks dari pose saat ini
            
        Returns:
            Tuple berisi:
            - Nama pose yang paling cocok (atau None)
            - Similarity score
        """
        if current_landmarks is None:
            return None, 0.0
        
        best_match = None
        best_score = 0.0
        
        for pose_name, ref_landmarks in self.reference_poses.items():
            if ref_landmarks is None:
                continue
                
            score = self.calculate_similarity(current_landmarks, ref_landmarks)
            
            if score > best_score:
                best_score = score
                best_match = pose_name
        
        # Hanya return match jika score lebih dari threshold
        if best_score >= config.SIMILARITY_THRESHOLD:
            return best_match, best_score
        else:
            return None, best_score
    
    def get_all_similarities(self, current_landmarks) -> dict:
        """
        Hitung similarity dengan semua pose referensi
        
        Args:
            current_landmarks: Dict atau List landmarks dari pose saat ini
            
        Returns:
            Dictionary {pose_name: similarity_score}
        """
        if current_landmarks is None:
            return {}
        
        similarities = {}
        for pose_name, ref_landmarks in self.reference_poses.items():
            if ref_landmarks is None:
                similarities[pose_name] = 0.0
            else:
                score = self.calculate_similarity(current_landmarks, ref_landmarks)
                similarities[pose_name] = score
        
        return similarities
