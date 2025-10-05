'''
Cookie Cutter - Shape Extraction for App Icons
Take the closeups of the app icons and use the masks to cut out the squircle shapes.
'''

# imports
import os
import cv2
import numpy as np
import glob


def apply_mask_to_icon(icon_path: str, mask_path: str, output_path: str) -> bool:
    """
    Apply a mask to an icon to extract its shape.
    
    Args:
        icon_path: Path to the source icon
        mask_path: Path to the mask file  
        output_path: Where to save the result
        
    Returns:
        True if successful, False otherwise
    """
    try:
        print(f"Processing: {os.path.basename(icon_path)}")
        
        # Load icon and mask
        icon = cv2.imread(icon_path, cv2.IMREAD_UNCHANGED)
        mask = cv2.imread(mask_path, cv2.IMREAD_UNCHANGED)
        
        if icon is None:
            print(f"  ❌ Could not load icon: {icon_path}")
            return False
            
        if mask is None:
            print(f"  ❌ Could not load mask: {mask_path}")
            return False
        
        print(f"  📏 Icon: {icon.shape}, Mask: {mask.shape}")
        
        # Store original icon dimensions for later scaling
        original_icon_h, original_icon_w = icon.shape[:2]
        
        # Get mask dimensions
        mask_h, mask_w = mask.shape[:2]
        
        # Crop icon to match mask size (center crop)
        start_y = (original_icon_h - mask_h) // 2
        start_x = (original_icon_w - mask_w) // 2
        end_y = start_y + mask_h
        end_x = start_x + mask_w
        
        # Ensure crop boundaries are within image bounds
        start_y = max(0, start_y)
        start_x = max(0, start_x)
        end_y = min(original_icon_h, end_y)
        end_x = min(original_icon_w, end_x)
        
        icon_cropped = icon[start_y:end_y, start_x:end_x]
        print(f"  ✂️ Cropped icon from {original_icon_w}x{original_icon_h} to {icon_cropped.shape[1]}x{icon_cropped.shape[0]}")
        
        # If cropped size doesn't match mask exactly, resize to match
        if icon_cropped.shape[:2] != (mask_h, mask_w):
            icon_cropped = cv2.resize(icon_cropped, (mask_w, mask_h), interpolation=cv2.INTER_CUBIC)
            print(f"  📏 Adjusted crop to exactly {mask_w}x{mask_h}")
        
        # Convert mask to grayscale if needed
        if len(mask.shape) == 3:
            mask_gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
        else:
            mask_gray = mask
        
        print(f"  🎯 Applying {mask_w}x{mask_h} mask to {mask_w}x{mask_h} cropped icon")
        
        # Ensure cropped icon has alpha channel
        if len(icon_cropped.shape) == 3 and icon_cropped.shape[2] == 3:
            icon_cropped = cv2.cvtColor(icon_cropped, cv2.COLOR_BGR2BGRA)
        
        # Apply mask to cropped icon's alpha channel
        result = icon_cropped.copy()
        
        # Where mask is white (255), keep icon; where black (0), make transparent
        alpha_mask = np.where(mask_gray > 127, 255, 0).astype(np.uint8)
        result[:, :, 3] = np.minimum(icon_cropped[:, :, 3], alpha_mask)
        
        # Determine target size based on original icon filename
        filename = os.path.basename(icon_path)
        if 'large' in filename or '157x157' in filename:
            target_size = (157, 157)
        else:
            target_size = (86, 86)
        
        # Scale result back to target size
        result = cv2.resize(result, target_size, interpolation=cv2.INTER_CUBIC)
        print(f"  📏 Scaled result back to {target_size[0]}x{target_size[1]}")
        
        # Save result
        success = cv2.imwrite(output_path, result)
        if success:
            print(f"  ✅ Saved: {os.path.basename(output_path)}")
            return True
        else:
            print(f"  ❌ Failed to save: {output_path}")
            return False
            
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def extract_shapes_from_output_folder(input_dir="build/output"):
    """Extract shapes from all icons in the output folder using masks."""
    
    print("🔍 Cookie Cutter - Shape Extraction")
    print("=" * 40)
    
    # Check if masks exist
    big_mask = "masks/iconmask_big.png"
    small_mask = "masks/iconmask_small.png"
    
    if not os.path.exists(big_mask) and not os.path.exists(small_mask):
        print("❌ No mask files found in masks/ folder")
        return
    
    print("🎭 Available masks:")
    if os.path.exists(big_mask):
        print(f"  - Big mask: {big_mask}")
    if os.path.exists(small_mask):  
        print(f"  - Small mask: {small_mask}")
    
    # Create build directory
    build_dir = "build"
    output_dir = os.path.join(build_dir, "extracted_shapes")
    os.makedirs(output_dir, exist_ok=True)
    print(f"📁 Output: {output_dir}")
    
    # Find icons in the specified input folder
    icon_files = glob.glob(f"{input_dir}/icon_*.png")
    print(f"🎯 Found {len(icon_files)} icons")
    print()
    
    if not icon_files:
        print("❌ No icons found in output/ folder")
        return
    
    success_count = 0
    
    for icon_file in sorted(icon_files):
        filename = os.path.basename(icon_file)
        base_name = os.path.splitext(filename)[0]
        
        # Skip visualization files
        if 'visualization' in filename:
            continue
        
        # Determine which mask to use based on size in filename
        if 'large' in filename or '160x160' in filename:
            if os.path.exists(big_mask):
                selected_mask = big_mask
                mask_name = "big"
            else:
                selected_mask = small_mask  
                mask_name = "small"
        else:
            if os.path.exists(small_mask):
                selected_mask = small_mask
                mask_name = "small"  
            else:
                selected_mask = big_mask
                mask_name = "big"
        
        print(f"🎭 Using {mask_name} mask for {filename}")
        
        # Create output filename
        output_filename = f"{base_name}_shape.png"
        output_path = os.path.join(output_dir, output_filename)
        
        # Apply mask
        if apply_mask_to_icon(icon_file, selected_mask, output_path):
            success_count += 1
        
        print()
    
    print("=" * 40)
    print(f"✅ Complete! Processed {success_count}/{len(icon_files)} icons")
    print(f"📁 Results in: {output_dir}")


def create_mask_visualization():
    """Create a visualization showing the masks being applied."""
    
    print("\n🖼️ Creating mask visualization...")
    
    big_mask_path = "masks/iconmask_big.png"
    small_mask_path = "masks/iconmask_small.png"
    
    # Load first few icons for demo
    icon_files = sorted(glob.glob("build/output/icon_*.png"))[:4]
    
    if not icon_files:
        print("❌ No icons found for visualization")
        return
    
    # Create visualization grid
    cell_size = 150
    cols = 4
    rows = 2  # Original icons on top, masked on bottom
    
    viz_width = cols * cell_size
    viz_height = rows * cell_size
    
    visualization = np.ones((viz_height, viz_width, 3), dtype=np.uint8) * 240  # Light gray background
    
    for i, icon_file in enumerate(icon_files):
        if i >= cols:
            break
            
        # Load icon
        icon = cv2.imread(icon_file)
        if icon is None:
            continue
        
        # Determine mask
        filename = os.path.basename(icon_file)
        if 'large' in filename or '160x160' in filename:
            mask_path = big_mask_path if os.path.exists(big_mask_path) else small_mask_path
        else:
            mask_path = small_mask_path if os.path.exists(small_mask_path) else big_mask_path
        
        # Apply mask (simplified for visualization)
        mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
        if mask is not None:
            # Resize to match icon
            mask_resized = cv2.resize(mask, (icon.shape[1], icon.shape[0]))
            
            # Apply mask
            masked_icon = icon.copy()
            mask_3channel = cv2.cvtColor(mask_resized, cv2.COLOR_GRAY2BGR)
            masked_icon = cv2.bitwise_and(masked_icon, mask_3channel)
        else:
            masked_icon = icon
        
        # Resize for visualization
        icon_resized = cv2.resize(icon, (cell_size-10, cell_size-10))
        masked_resized = cv2.resize(masked_icon, (cell_size-10, cell_size-10))
        
        # Place in grid
        x_offset = i * cell_size + 5
        
        # Original (top row)
        y_start = 5
        y_end = y_start + cell_size - 10
        x_start = x_offset
        x_end = x_start + cell_size - 10
        visualization[y_start:y_end, x_start:x_end] = icon_resized
        
        # Masked (bottom row)
        y_start = cell_size + 5
        y_end = y_start + cell_size - 10
        visualization[y_start:y_end, x_start:x_end] = masked_resized
    
    # Save visualization
    viz_path = "mask_extraction_preview.png"
    cv2.imwrite(viz_path, visualization)
    print(f"✅ Visualization saved: {viz_path}")


if __name__ == "__main__":
    extract_shapes_from_output_folder()
    create_mask_visualization()

