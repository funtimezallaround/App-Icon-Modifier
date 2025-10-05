"""
Alignment Comparison Tool
Compare original vs improved mask alignment
"""

import cv2
import numpy as np
import os
import glob

def create_alignment_comparison():
    """Create a side-by-side comparison of mask alignment"""
    
    print("🔍 Creating alignment comparison...")
    
    # Get some sample icons from build folder
    icon_files = sorted(glob.glob("build/output/icon_*.png"))[:6]  # First 6 icons
    
    if not icon_files:
        print("❌ No icons found")
        return
    
    # Create comparison grid
    cell_width = 200
    cell_height = 150
    cols = 3  # 3 comparisons per row
    rows = len(icon_files) // cols + (1 if len(icon_files) % cols else 0)
    
    grid_width = cols * cell_width * 3  # Original, Old Method, New Method
    grid_height = rows * cell_height
    
    comparison = np.ones((grid_height, grid_width, 3), dtype=np.uint8) * 240
    
    # Load masks
    big_mask_path = "masks/iconmask_big.png"
    small_mask_path = "masks/iconmask_small.png"
    
    for idx, icon_file in enumerate(icon_files):
        row = idx // cols
        col = idx % cols
        
        filename = os.path.basename(icon_file)
        print(f"Processing: {filename}")
        
        # Load icon
        icon = cv2.imread(icon_file)
        if icon is None:
            continue
        
        # Determine mask
        if 'large' in filename:
            mask_path = big_mask_path
        else:
            mask_path = small_mask_path
        
        mask = cv2.imread(mask_path, cv2.IMREAD_UNCHANGED)
        if mask is None:
            continue
        
        # Create old method (stretched mask)
        icon_h, icon_w = icon.shape[:2]
        old_mask = cv2.resize(mask, (icon_w, icon_h), interpolation=cv2.INTER_NEAREST)
        
        if len(old_mask.shape) == 3:
            old_mask_gray = cv2.cvtColor(old_mask, cv2.COLOR_BGR2GRAY)
        else:
            old_mask_gray = old_mask
        
        # Apply old mask overlay (for visualization)
        mask_overlay = np.where(old_mask_gray > 127, [0, 255, 0], [255, 0, 0])  # Green inside, red outside
        old_result = cv2.addWeighted(icon, 0.7, mask_overlay.astype(np.uint8), 0.3, 0)
        
        # Create new method (centered mask)
        mask_h, mask_w = mask.shape[:2]
        scale_factor = min(icon_w / mask_w, icon_h / mask_h) * 0.9
        
        new_mask_w = int(mask_w * scale_factor)
        new_mask_h = int(mask_h * scale_factor)
        scaled_mask = cv2.resize(mask, (new_mask_w, new_mask_h), interpolation=cv2.INTER_NEAREST)
        
        full_mask = np.zeros((icon_h, icon_w), dtype=np.uint8)
        start_x = (icon_w - new_mask_w) // 2
        start_y = (icon_h - new_mask_h) // 2
        end_x = start_x + new_mask_w
        end_y = start_y + new_mask_h
        
        if len(scaled_mask.shape) == 3:
            scaled_mask_gray = cv2.cvtColor(scaled_mask, cv2.COLOR_BGR2GRAY)
        else:
            scaled_mask_gray = scaled_mask
        
        full_mask[start_y:end_y, start_x:end_x] = scaled_mask_gray
        
        # Apply new mask overlay (for visualization)
        mask_overlay_new = np.where(full_mask > 127, [0, 255, 0], [255, 0, 0])  # Green inside, red outside
        new_result = cv2.addWeighted(icon, 0.7, mask_overlay_new.astype(np.uint8), 0.3, 0)
        
        # Resize for grid
        display_size = (cell_width - 10, cell_height - 30)
        icon_resized = cv2.resize(icon, display_size)
        old_resized = cv2.resize(old_result, display_size)
        new_resized = cv2.resize(new_result, display_size)
        
        # Calculate positions in grid
        y_start = row * cell_height + 10
        y_end = y_start + display_size[1]
        
        # Original
        x_start = col * cell_width * 3 + 5
        x_end = x_start + display_size[0]
        comparison[y_start:y_end, x_start:x_end] = icon_resized
        
        # Old method
        x_start = col * cell_width * 3 + cell_width + 5
        x_end = x_start + display_size[0]
        comparison[y_start:y_end, x_start:x_end] = old_resized
        
        # New method
        x_start = col * cell_width * 3 + cell_width * 2 + 5
        x_end = x_start + display_size[0]
        comparison[y_start:y_end, x_start:x_end] = new_resized
        
        # Add labels
        label_y = y_start - 5
        cv2.putText(comparison, "Original", (col * cell_width * 3 + 5, label_y), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1)
        cv2.putText(comparison, "Old (Stretched)", (col * cell_width * 3 + cell_width + 5, label_y), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 200), 1)
        cv2.putText(comparison, "New (Centered)", (col * cell_width * 3 + cell_width * 2 + 5, label_y), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 150, 0), 1)
    
    # Save comparison to build folder
    build_dir = "build"
    os.makedirs(build_dir, exist_ok=True)
    comparison_path = os.path.join(build_dir, "alignment_comparison.png")
    cv2.imwrite(comparison_path, comparison)
    print(f"✅ Alignment comparison saved: {comparison_path}")
    print("🟢 Green = mask area, 🔴 Red = outside mask")

if __name__ == "__main__":
    create_alignment_comparison()