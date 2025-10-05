"""
Color Removal Comparison Tool
Compare exact vs tolerance-based color removal
"""

import cv2
import numpy as np
import os

def analyze_color_removal(image_path, tolerance=25):
    """Analyze the difference between exact and tolerance-based color removal"""
    
    if not os.path.exists(image_path):
        print(f"❌ Image not found: {image_path}")
        return
    
    print(f"🔍 Analyzing: {os.path.basename(image_path)}")
    
    # Load image
    img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        return
    
    # Ensure BGRA format
    if len(img.shape) == 3 and img.shape[2] == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    
    # Find most common color
    pixels = img.reshape(-1, img.shape[-1])
    unique, counts = np.unique(pixels, axis=0, return_counts=True)
    color_rank = unique[np.argsort(-counts)]
    most_common = color_rank[0][:3]
    
    print(f"  🎯 Most common color: {most_common}")
    
    # Method 1: Exact color match
    exact_mask = np.all(img[:, :, :3] == most_common, axis=-1)
    exact_pixels = np.sum(exact_mask)
    
    # Method 2: Tolerance-based match
    rgb_diff = np.abs(img[:, :, :3].astype(int) - most_common.astype(int))
    tolerance_mask = np.all(rgb_diff <= tolerance, axis=-1)
    tolerance_pixels = np.sum(tolerance_mask)
    
    total_pixels = img.shape[0] * img.shape[1]
    
    print(f"  📊 Exact match: {exact_pixels} pixels ({exact_pixels/total_pixels*100:.1f}%)")
    print(f"  📊 Tolerance ±{tolerance}: {tolerance_pixels} pixels ({tolerance_pixels/total_pixels*100:.1f}%)")
    print(f"  🔄 Difference: +{tolerance_pixels - exact_pixels} pixels")
    
    # Show color variations within tolerance
    if tolerance_pixels > exact_pixels:
        # Find colors within tolerance that aren't exact matches
        similar_but_different = tolerance_mask & ~exact_mask
        if np.any(similar_but_different):
            similar_colors = img[similar_but_different][:, :3]
            unique_similar = np.unique(similar_colors, axis=0)
            
            print(f"  🎨 Similar colors found:")
            for color in unique_similar[:5]:  # Show first 5
                diff = np.abs(color.astype(int) - most_common.astype(int))
                print(f"    {color} (diff: {diff})")
    
    print()

def compare_sample_icons():
    """Compare color removal on a few sample icons"""
    
    print("🔍 COLOR REMOVAL COMPARISON")
    print("=" * 50)
    
    sample_icons = [
        "build/extracted_shapes/icon_001_large_157x157_shape.png",
        "build/extracted_shapes/icon_006_small_86x86_shape.png", 
        "build/extracted_shapes/icon_011_small_86x86_shape.png"
    ]
    
    for icon_path in sample_icons:
        analyze_color_removal(icon_path, tolerance=25)
    
    print("💡 Benefits of tolerance-based removal:")
    print("  ✅ Removes color variations from compression/antialiasing")
    print("  ✅ Cleaner edges and better background removal") 
    print("  ✅ More robust against slight color variations")
    print("  ✅ Better results for logos with gradients near background color")

if __name__ == "__main__":
    compare_sample_icons()