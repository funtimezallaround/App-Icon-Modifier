"""
Simple test for shape extraction
"""

import cv2
import numpy as np
import os

def test_masks():
    """Test loading masks"""
    print("Testing mask loading...")
    
    big_mask_path = "masks/iconmask_big.png" 
    small_mask_path = "masks/iconmask_small.png"
    
    print(f"Checking: {big_mask_path}")
    print(f"Exists: {os.path.exists(big_mask_path)}")
    
    print(f"Checking: {small_mask_path}")  
    print(f"Exists: {os.path.exists(small_mask_path)}")
    
    if os.path.exists(big_mask_path):
        big_mask = cv2.imread(big_mask_path, cv2.IMREAD_UNCHANGED)
        print(f"Big mask shape: {big_mask.shape if big_mask is not None else 'None'}")
        
    if os.path.exists(small_mask_path):
        small_mask = cv2.imread(small_mask_path, cv2.IMREAD_UNCHANGED) 
        print(f"Small mask shape: {small_mask.shape if small_mask is not None else 'None'}")

if __name__ == "__main__":
    test_masks()