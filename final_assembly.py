import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

appicon = cv2.imread('input/autumn_bg.png', cv2.IMREAD_UNCHANGED)

appicon = cv2.resize(appicon, (157, 157), interpolation=cv2.INTER_AREA)

# Cut out the icon shape:
mask = cv2.imread('masks/iconmask_big.png', cv2.IMREAD_GRAYSCALE)
mask = cv2.resize(mask, (157, 157), interpolation=cv2.INTER_AREA)
icon_shape = cv2.bitwise_and(appicon, appicon, mask=mask)

# make black background transparent
# Check if image has alpha channel, if not add one
if icon_shape.shape[2] == 3:
	icon_shape = cv2.cvtColor(icon_shape, cv2.COLOR_BGR2BGRA)

icon_shape[np.all(icon_shape == [0, 0, 0, 255], axis=-1)] = [0, 0, 0, 0]

output_dir = 'new_icons'
os.makedirs(output_dir, exist_ok=True)

for path in os.listdir("build/extracted_shapes"):
    if not path.endswith('.png'):
        continue
        
    # load the image
    shape = cv2.imread(os.path.join("build/extracted_shapes", path), cv2.IMREAD_UNCHANGED)
    # Stretch the image to fill the entire 157x157 size (ignores aspect ratio)
    shape = cv2.resize(shape, (157, 157), interpolation=cv2.INTER_CUBIC)
    
    # Ensure shape has alpha channel
    if shape.shape[2] == 3:
        shape = cv2.cvtColor(shape, cv2.COLOR_BGR2BGRA)
    
    # Enhanced color ranking with tolerance-based grouping
    tolerance = 60
    
    # Get all pixels and their unique colors
    pixels = shape.reshape(-1, shape.shape[-1])
    unique_colors, counts = np.unique(pixels, axis=0, return_counts=True)
    
    print(f"  📊 Found {len(unique_colors)} unique colors before grouping")
    
    # Group similar colors together
    color_groups = []
    remaining_colors = list(zip(unique_colors, counts))
    
    while remaining_colors:
        # Take the most frequent remaining color as group representative
        remaining_colors.sort(key=lambda x: x[1], reverse=True)
        representative_color, rep_count = remaining_colors.pop(0)
        
        # Find all similar colors within tolerance
        group_colors = [(representative_color, rep_count)]
        total_count = rep_count
        
        i = 0
        while i < len(remaining_colors):
            color, count = remaining_colors[i]
            
            # Check if this color is similar to the representative
            rgb_diff = np.abs(color[:3].astype(int) - representative_color[:3].astype(int))
            if np.all(rgb_diff <= tolerance):
                # Add to this group and remove from remaining
                group_colors.append((color, count))
                total_count += count
                remaining_colors.pop(i)
            else:
                i += 1
        
        # Store the group (representative color and total count)
        color_groups.append((representative_color, total_count, len(group_colors)))
    
    # Sort groups by total frequency
    color_groups.sort(key=lambda x: x[1], reverse=True)
    
    # Extract the ranked colors (representatives only)
    color_rank = np.array([group[0] for group in color_groups])
    group_counts = [group[1] for group in color_groups]
    group_sizes = [group[2] for group in color_groups]
    
    print(f"  📈 Grouped into {len(color_groups)} color families")
    print(f"Top color groups in {path}:")
    for i, (rep_color, total_count, group_size) in enumerate(color_groups[:3]):
        percentage = (total_count / pixels.shape[0]) * 100
        print(f"    #{i+1}: {rep_color[:3]} - {total_count} pixels ({percentage:.1f}%) - {group_size} variants")
    
    # Remove background color and all similar colors (within tolerance)
    background_color = color_rank[0][:3]  # Get RGB, ignore alpha
    
    print(f"  🎯 Target color: {background_color}, tolerance: ±{tolerance}")
    
    # Create mask for similar colors using tolerance
    # Calculate the absolute difference for each RGB channel
    rgb_diff = np.abs(shape[:, :, :3].astype(int) - background_color.astype(int))
    
    # Check if all RGB channels are within tolerance
    similar_color_mask = np.all(rgb_diff <= tolerance, axis=-1)
    
    # Count how many pixels will be removed
    pixels_to_remove = np.sum(similar_color_mask)
    total_pixels = shape.shape[0] * shape.shape[1]
    removal_percentage = (pixels_to_remove / total_pixels) * 100
    
    print(f"  📊 Removing {pixels_to_remove}/{total_pixels} pixels ({removal_percentage:.1f}%)")
    
    # Set similar color pixels to transparent (alpha = 0)
    shape[similar_color_mask] = [0, 0, 0, 0]
    
    # Optional: Also remove any remaining transparent or near-transparent pixels
    # This helps clean up any existing transparency artifacts
    alpha_threshold = 50  # Remove pixels with alpha < 50
    low_alpha_mask = shape[:, :, 3] < alpha_threshold
    shape[low_alpha_mask] = [0, 0, 0, 0]
    
    remaining_pixels = np.sum(shape[:, :, 3] > 0)
    print(f"  ✨ {remaining_pixels} pixels remaining after cleanup")
    
    # Alternative: Remove specific color (e.g., gray background)
    # gray_color = [119, 145, 161]  # Example gray
    # gray_mask = np.all(shape[:, :, :3] == gray_color, axis=-1)
    # shape[gray_mask] = [0, 0, 0, 0]  # Make transparent
    
    # Merge with the app icon background using alpha blending
    result = icon_shape.copy()
    
    # Blend the shape onto the icon background
    shape_alpha = shape[:, :, 3] / 255.0
    
    for c in range(3):  # RGB channels
        result[:, :, c] = (
            shape_alpha * shape[:, :, c] + 
            (1 - shape_alpha) * result[:, :, c]
        )
    
    # Update alpha channel
    result[:, :, 3] = np.maximum(result[:, :, 3], shape[:, :, 3])
    
    # Save merged result
    output_path = os.path.join(output_dir, f"merged_{path}")
    cv2.imwrite(output_path, result)
    print(f"✅ Saved merged icon: merged_{path}")