"""
Quick alignment test
"""

import cv2
import os

def test_alignment():
    """Test the alignment of a specific icon"""
    
    # Test with first icon
    icon_path = "output/icon_001_large_157x157.png" 
    mask_path = "masks/iconmask_big.png"
    
    if not os.path.exists(icon_path) or not os.path.exists(mask_path):
        print("Files not found for testing")
        return
    
    print("Testing alignment with improved cookiecutter method...")
    
    icon = cv2.imread(icon_path)
    mask = cv2.imread(mask_path, cv2.IMREAD_UNCHANGED)
    
    print(f"Icon shape: {icon.shape}")
    print(f"Mask shape: {mask.shape}")
    
    # Apply improved centering logic
    icon_h, icon_w = icon.shape[:2]
    mask_h, mask_w = mask.shape[:2]
    
    scale_factor = min(icon_w / mask_w, icon_h / mask_h) * 0.9
    print(f"Scale factor: {scale_factor:.2f}")
    
    new_mask_w = int(mask_w * scale_factor)
    new_mask_h = int(mask_h * scale_factor)
    print(f"Scaled mask size: {new_mask_w}x{new_mask_h}")
    
    # Center calculation
    start_x = (icon_w - new_mask_w) // 2
    start_y = (icon_h - new_mask_h) // 2
    print(f"Mask position: ({start_x}, {start_y})")
    
    print("✅ Alignment calculations completed")

if __name__ == "__main__":
    test_alignment()