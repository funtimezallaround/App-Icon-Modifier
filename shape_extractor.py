"""
Shape Extractor for App Icons
Extracts app icon shapes using masks from the masks folder
"""

import cv2
import numpy as np
import os
from typing import Tuple, Optional
import glob

def load_masks() -> Tuple[Optional[np.ndarray], Optional[np.ndarray]]:
    """
    Load the icon masks from the masks folder.
    
    Returns:
        Tuple of (big_mask, small_mask) as numpy arrays with alpha channel
    """
    masks_dir = "masks"
    
    big_mask_path = os.path.join(masks_dir, "iconmask_big.png")
    small_mask_path = os.path.join(masks_dir, "iconmask_small.png")
    
    big_mask = None
    small_mask = None
    
    if os.path.exists(big_mask_path):
        big_mask = cv2.imread(big_mask_path, cv2.IMREAD_UNCHANGED)
        print(f"✅ Loaded big mask: {big_mask.shape}")
    else:
        print(f"❌ Big mask not found: {big_mask_path}")
    
    if os.path.exists(small_mask_path):
        small_mask = cv2.imread(small_mask_path, cv2.IMREAD_UNCHANGED)
        print(f"✅ Loaded small mask: {small_mask.shape}")
    else:
        print(f"❌ Small mask not found: {small_mask_path}")
    
    return big_mask, small_mask


def extract_icon_shape(icon_path: str, mask: np.ndarray, output_path: str) -> bool:
    """
    Extract the shape of an app icon using the provided mask.
    
    Args:
        icon_path: Path to the input icon image
        mask: The mask to apply (should have alpha channel)
        output_path: Path where to save the extracted shape
        
    Returns:
        True if extraction was successful, False otherwise
    """
    try:
        # Load the icon
        icon = cv2.imread(icon_path, cv2.IMREAD_UNCHANGED)
        if icon is None:
            print(f"❌ Could not load icon: {icon_path}")
            return False
        
        # Get dimensions
        icon_h, icon_w = icon.shape[:2]
        mask_h, mask_w = mask.shape[:2]
        
        print(f"   📏 Icon size: {icon_w}x{icon_h}, Mask size: {mask_w}x{mask_h}")
        
        # Resize mask to match icon if needed
        if (mask_h != icon_h) or (mask_w != icon_w):
            resized_mask = cv2.resize(mask, (icon_w, icon_h), interpolation=cv2.INTER_NEAREST)
            print("   🔄 Resized mask to match icon dimensions")
        else:
            resized_mask = mask.copy()
        
        # Ensure icon has alpha channel
        if len(icon.shape) == 3 and icon.shape[2] == 3:
            # Add alpha channel (fully opaque)
            icon = cv2.cvtColor(icon, cv2.COLOR_BGR2BGRA)
        elif len(icon.shape) == 3 and icon.shape[2] == 4:
            # Already has alpha channel
            pass
        else:
            print(f"❌ Unsupported icon format: {icon.shape}")
            return False
        
        # Ensure mask has alpha channel
        if len(resized_mask.shape) == 3 and resized_mask.shape[2] == 3:
            # Convert grayscale or BGR mask to BGRA
            if len(np.unique(resized_mask)) <= 2:  # Binary mask
                # Convert to grayscale then to BGRA
                gray_mask = cv2.cvtColor(resized_mask, cv2.COLOR_BGR2GRAY)
                mask_alpha = np.where(gray_mask > 127, 255, 0).astype(np.uint8)
            else:
                # Use the mask as-is for alpha
                gray_mask = cv2.cvtColor(resized_mask, cv2.COLOR_BGR2GRAY)
                mask_alpha = gray_mask
        elif len(resized_mask.shape) == 3 and resized_mask.shape[2] == 4:
            # Use existing alpha channel
            mask_alpha = resized_mask[:, :, 3]
        elif len(resized_mask.shape) == 2:
            # Grayscale mask
            mask_alpha = resized_mask
        else:
            print(f"❌ Unsupported mask format: {resized_mask.shape}")
            return False
        
        # Create the result by applying the mask
        result = icon.copy()
        
        # Apply mask to alpha channel
        # Where mask is transparent (0), make result transparent
        # Where mask has content (>0), keep original icon alpha
        result[:, :, 3] = np.minimum(icon[:, :, 3], mask_alpha)
        
        # Save the result
        success = cv2.imwrite(output_path, result)
        if success:
            print(f"   ✅ Saved shape-extracted icon: {output_path}")
            return True
        else:
            print(f"   ❌ Failed to save: {output_path}")
            return False
            
    except Exception as e:
        print(f"❌ Error processing {icon_path}: {str(e)}")
        return False


def get_icon_size_category(icon_path: str) -> str:
    """
    Determine if an icon is 'large' or 'small' based on filename or dimensions.
    
    Args:
        icon_path: Path to the icon file
        
    Returns:
        'large' or 'small' category
    """
    filename = os.path.basename(icon_path).lower()
    
    # Check filename for size indicators
    if 'large' in filename or '160x160' in filename:
        return 'large'
    elif 'small' in filename or '90x90' in filename:
        return 'small'
    
    # Fallback: check actual dimensions
    try:
        icon = cv2.imread(icon_path)
        if icon is not None:
            h, w = icon.shape[:2]
            # Assume icons larger than 120px are 'large'
            if max(h, w) > 120:
                return 'large'
            else:
                return 'small'
    except Exception:
        pass
    
    # Default to large if can't determine
    return 'large'


def extract_all_icon_shapes(input_dir: str = "output", output_dir: str = "extracted_shapes") -> None:
    """
    Extract shapes from all icons in the input directory using appropriate masks.
    
    Args:
        input_dir: Directory containing the original icons
        output_dir: Directory to save the shape-extracted icons
    """
    print("🔍 Starting Icon Shape Extraction")
    print("=" * 50)
    
    # Load masks
    big_mask, small_mask = load_masks()
    
    if big_mask is None and small_mask is None:
        print("❌ No masks available! Please ensure mask files exist in the masks folder.")
        return
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    print(f"📁 Output directory: {output_dir}")
    
    # Find all icon files
    icon_patterns = [
        os.path.join(input_dir, "*.png"),
        os.path.join(input_dir, "*.jpg"),
        os.path.join(input_dir, "*.jpeg")
    ]
    
    icon_files = []
    for pattern in icon_patterns:
        icon_files.extend(glob.glob(pattern))
    
    if not icon_files:
        print(f"❌ No icon files found in {input_dir}")
        return
    
    print(f"🎯 Found {len(icon_files)} icon files")
    print()
    
    success_count = 0
    
    for icon_file in sorted(icon_files):
        filename = os.path.basename(icon_file)
        name_without_ext = os.path.splitext(filename)[0]
        
        print(f"🔄 Processing: {filename}")
        
        # Skip visualization files
        if 'visualization' in filename.lower():
            print("   ⏭️  Skipping visualization file")
            continue
        
        # Determine size category and select appropriate mask
        size_category = get_icon_size_category(icon_file)
        
        # Select appropriate mask
        if size_category == 'large' and big_mask is not None:
            selected_mask = big_mask
            mask_type = "big"
        elif size_category == 'small' and small_mask is not None:
            selected_mask = small_mask
            mask_type = "small"
        elif big_mask is not None:
            # Fallback to big mask if preferred size not available
            selected_mask = big_mask
            mask_type = "big (fallback)"
        elif small_mask is not None:
            # Fallback to small mask if big not available
            selected_mask = small_mask
            mask_type = "small (fallback)"
        else:
            print(f"   ❌ No suitable mask available for {filename}")
            continue
        
        print(f"   🎭 Using {mask_type} mask for {size_category} icon")
        
        # Create output filename
        output_filename = f"{name_without_ext}_shape_extracted.png"
        output_path = os.path.join(output_dir, output_filename)
        
        # Extract the shape
        if extract_icon_shape(icon_file, selected_mask, output_path):
            success_count += 1
        
        print()
    
    print("=" * 50)
    print("✅ Shape extraction complete!")
    print(f"📊 Successfully processed: {success_count}/{len(icon_files)} icons")
    print(f"📁 Results saved to: {output_dir}")


def create_shape_preview(input_dir: str = "output", output_dir: str = "extracted_shapes") -> None:
    """
    Create a preview grid showing original icons vs shape-extracted versions.
    
    Args:
        input_dir: Directory with original icons
        output_dir: Directory with shape-extracted icons
    """
    print("\n🖼️  Creating shape extraction preview...")
    
    # Find matching pairs
    original_files = glob.glob(os.path.join(input_dir, "icon_*.png"))
    extracted_files = glob.glob(os.path.join(output_dir, "*_shape_extracted.png"))
    
    if not original_files or not extracted_files:
        print("❌ No matching icon pairs found for preview")
        return
    
    # Take first 6 icons for preview
    preview_count = min(6, len(original_files))
    
    # Create preview grid (2 rows x preview_count columns)
    # Top row: originals, Bottom row: shape-extracted
    cell_size = 120
    grid_width = preview_count * cell_size
    grid_height = 2 * cell_size
    
    preview = np.zeros((grid_height, grid_width, 3), dtype=np.uint8)
    preview.fill(64)  # Dark gray background
    
    for i in range(preview_count):
        original_file = original_files[i]
        filename = os.path.basename(original_file)
        name_without_ext = os.path.splitext(filename)[0]
        extracted_file = os.path.join(output_dir, f"{name_without_ext}_shape_extracted.png")
        
        if not os.path.exists(extracted_file):
            continue
        
        # Load images
        original = cv2.imread(original_file)
        extracted = cv2.imread(extracted_file, cv2.IMREAD_UNCHANGED)
        
        if original is None or extracted is None:
            continue
        
        # Resize to cell size
        original_resized = cv2.resize(original, (cell_size-10, cell_size-10))
        
        # Handle extracted image with alpha channel
        if len(extracted.shape) == 4:
            # Convert BGRA to BGR for preview (with white background)
            alpha = extracted[:, :, 3] / 255.0
            extracted_bgr = extracted[:, :, :3]
            white_bg = np.ones_like(extracted_bgr) * 255
            extracted_preview = (extracted_bgr * alpha[:, :, np.newaxis] + 
                               white_bg * (1 - alpha[:, :, np.newaxis])).astype(np.uint8)
        else:
            extracted_preview = extracted
        
        extracted_resized = cv2.resize(extracted_preview, (cell_size-10, cell_size-10))
        
        # Place in grid
        x_offset = i * cell_size + 5
        
        # Original (top row)
        y_offset = 5
        preview[y_offset:y_offset+cell_size-10, x_offset:x_offset+cell_size-10] = original_resized
        
        # Extracted (bottom row)
        y_offset = cell_size + 5
        preview[y_offset:y_offset+cell_size-10, x_offset:x_offset+cell_size-10] = extracted_resized
    
    # Save preview
    preview_path = "shape_extraction_preview.png"
    cv2.imwrite(preview_path, preview)
    print(f"✅ Preview saved: {preview_path}")


def main():
    """Main function to run the shape extraction process."""
    extract_all_icon_shapes()
    create_shape_preview()


if __name__ == "__main__":
    main()