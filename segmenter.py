import os
import cv2
import numpy as np
from typing import List, Tuple

def detect_app_icons(image_path: str, output_dir: str = "output", 
                    min_area: int = 1000, max_area: int = 50000) -> List[Tuple]:
    """
    Detect and segment app icons from a homescreen screenshot using contour detection
    
    Args:
        image_path: Path to the homescreen screenshot
        output_dir: Directory to save extracted icons
        min_area: Minimum area for icon detection (adjust based on screen resolution)
        max_area: Maximum area for icon detection (adjust based on screen resolution)
        
    Returns:
        List of bounding boxes (x, y, w, h) for detected icons
    """
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Load image
    img = cv2.imread(image_path)
    if img is None:
        print(f"❌ Could not load image: {image_path}")
        return []
    
    print(f"✅ Loaded image: {img.shape}")
    
    # Convert to grayscale for processing
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Use adaptive threshold to create binary image
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                 cv2.THRESH_BINARY_INV, 11, 2)
    
    # Morphological operations to clean up
    kernel = np.ones((3, 3), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    
    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Filter contours by area and aspect ratio
    icon_boxes = []
    for contour in contours:
        area = cv2.contourArea(contour)
        
        # Filter by area (adjustable parameters)
        if min_area < area < max_area:
            x, y, w, h = cv2.boundingRect(contour)
            
            # Filter by aspect ratio (icons are usually square-ish)
            aspect_ratio = w / h
            if 0.7 < aspect_ratio < 1.3 and w > 30 and h > 30:
                icon_boxes.append((x, y, w, h))
    
    print(f"🔍 Found {len(icon_boxes)} potential app icons")
    
    # Remove overlapping boxes (simple but effective approach)
    filtered_boxes = []
    for box in icon_boxes:
        x, y, w, h = box
        overlap = False
        
        for existing_box in filtered_boxes:
            ex, ey, ew, eh = existing_box
            
            # Check if boxes overlap significantly
            if (x < ex + ew and x + w > ex and y < ey + eh and y + h > ey):
                # Calculate overlap area
                overlap_x = max(0, min(x + w, ex + ew) - max(x, ex))
                overlap_y = max(0, min(y + h, ey + eh) - max(y, ey))
                overlap_area = overlap_x * overlap_y
                
                # If overlap is more than 50% of smaller box, skip this box
                smaller_area = min(w * h, ew * eh)
                if overlap_area > 0.5 * smaller_area:
                    overlap = True
                    break
        
        if not overlap:
            filtered_boxes.append(box)
    
    print(f"✨ After filtering overlaps: {len(filtered_boxes)} icons")
    
    # Analyze sizes and determine two standard sizes
    sizes = [(w, h) for x, y, w, h in filtered_boxes]
    areas = [w * h for w, h in sizes]
    
    # Determine two size categories based on area
    median_area = np.median(areas)
    

    
    # Determine two standard square sizes based on detected sizes
    small_size = 86  # Small square size
    large_size = 157  # Large square size
    
    print("📏 Standardizing to two square sizes:")
    print(f"   Small icons: {small_size}×{small_size}")
    print(f"   Large icons: {large_size}×{large_size}")
    
    # Create standardized bounding boxes
    standardized_boxes = []
    for i, (x, y, w, h) in enumerate(filtered_boxes):
        # Determine if this should be small or large based on original area
        area = w * h
        if area <= median_area:
            box_size = small_size
            size_type = "small"
        else:
            box_size = large_size 
            size_type = "large"
        
        # Calculate center of original detection
        center_x = x + w // 2
        center_y = y + h // 2
        
        # Create square bounding box centered on the original detection
        new_x = center_x - box_size // 2
        new_y = center_y - box_size // 2
        
        # Ensure the box stays within image bounds
        new_x = max(0, min(new_x, img.shape[1] - box_size))
        new_y = max(0, min(new_y, img.shape[0] - box_size))
        
        standardized_boxes.append((new_x, new_y, box_size, box_size, size_type))
    
    # Extract and save each icon with standardized square boxes
    for i, (x, y, box_size, _, size_type) in enumerate(standardized_boxes):
        # Extract the square region (no scaling, original resolution)
        icon = img[y:y+box_size, x:x+box_size]
        
        # Save icon with size info in filename
        output_path = os.path.join(output_dir, f"icon_{i+1:03d}_{size_type}_{box_size}x{box_size}.png")
        cv2.imwrite(output_path, icon)
    
    # Update filtered_boxes for visualization with standardized boxes
    filtered_boxes = [(x, y, box_size, box_size) for x, y, box_size, _, _ in standardized_boxes]
    
    # Create visualization
    vis_img = img.copy()
    for i, (x, y, w, h) in enumerate(filtered_boxes):
        cv2.rectangle(vis_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(vis_img, str(i+1), (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    
    # Save visualization
    vis_path = os.path.join(output_dir, "detected_icons_visualization.png")
    cv2.imwrite(vis_path, vis_img)
    
    print(f"💾 Saved {len(filtered_boxes)} icons to '{output_dir}' directory")
    print(f"📊 Saved visualization to '{vis_path}'")
    
    return filtered_boxes

def analyze_image(image_path: str) -> None:
    """
    Analyze image to suggest optimal parameters for icon detection
    
    Args:
        image_path: Path to the homescreen screenshot
    """
    img = cv2.imread(image_path)
    if img is None:
        print(f"❌ Could not load image: {image_path}")
        return
    
    h, w, channels = img.shape
    
    print(f"📊 Image Analysis: {os.path.basename(image_path)}")
    print(f"   📐 Dimensions: {w} × {h} pixels")
    print(f"   🎨 Channels: {channels}")
    print(f"   � File size: {os.path.getsize(image_path) / 1024:.1f} KB")
    
    # Basic color analysis for threshold suggestions
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    brightness = np.mean(gray)
    contrast = np.std(gray)
    
    print(f"   💡 Average brightness: {brightness:.1f}")
    print(f"   🌓 Contrast (std dev): {contrast:.1f}")
    
    # Suggest parameters based on image size
    if w * h > 2000000:  # High resolution
        suggested_min = 1500
        suggested_max = 60000
    elif w * h > 1000000:  # Medium resolution
        suggested_min = 1000
        suggested_max = 40000
    else:  # Lower resolution
        suggested_min = 500
        suggested_max = 20000
    
    print(f"   🎯 Suggested area range: {suggested_min} - {suggested_max}")
    
    if brightness < 100:
        print("   💡 Dark image - consider adjusting threshold parameters")
    elif brightness > 200:
        print("   ☀️ Bright image - may need different edge detection settings")

def main():
    """Main function to run icon detection"""
    
    # Configuration
    input_image = "input/homescreen.jpg"
    output_dir = "output"
    
    print("🎯 APP ICON SEGMENTER - CONTOUR METHOD")
    print("=" * 50)
    
    # Check if input image exists
    if not os.path.exists(input_image):
        print(f"❌ Input image not found: {input_image}")
        print("📝 Please make sure you have a homescreen screenshot in the 'input' directory")
        return
    
    # Analyze image first
    print("🔍 Analyzing image...")
    analyze_image(input_image)
    
    print("\n" + "-" * 50)
    
    # Run contour-based detection
    print("� Running contour-based icon detection...")
    detected_icons = detect_app_icons(input_image, output_dir)
    
    print("\n" + "=" * 50)
    print("✅ Icon detection complete!")
    print(f"📱 Successfully extracted {len(detected_icons)} app icons")
    print(f"📁 Check the '{output_dir}' folder for:")
    print("   • Individual app icon images (icon_001.png, icon_002.png, etc.)")
    print("   • Detection visualization (detected_icons_visualization.png)")
    print("\n💡 Tip: If results aren't perfect, you can adjust the min_area and max_area parameters")

if __name__ == "__main__":
    main()