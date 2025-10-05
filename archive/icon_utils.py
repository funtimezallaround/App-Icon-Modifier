#!/usr/bin/env python3
"""
App Icon Segmenter Utility - Contour Method
A simple utility to extract app icons from homescreen screenshots using contour detection

Usage:
    python icon_utils.py --input <image_path> --output <output_dir>
    python icon_utils.py --batch <input_dir> --output <output_dir>
    python icon_utils.py --analyze <image_path>
"""

import os
import sys
import argparse
import cv2
import numpy as np
from pathlib import Path

# Import our segmenter functions
from segmenter import detect_app_icons, analyze_image

def process_single_image(image_path: str, output_dir: str, 
                        min_area: int = 1000, max_area: int = 50000):
    """Process a single homescreen image using contour detection"""
    
    if not os.path.exists(image_path):
        print(f"❌ Image not found: {image_path}")
        return False
    
    print(f"🖼️  Processing: {image_path}")
    print("🔍 Running contour-based detection...")
    
    icons = detect_app_icons(image_path, output_dir, min_area, max_area)
    return len(icons) > 0

def process_batch(input_dir: str, output_dir: str, 
                 min_area: int = 1000, max_area: int = 50000):
    """Process multiple images in a directory"""
    
    if not os.path.exists(input_dir):
        print(f"❌ Input directory not found: {input_dir}")
        return False
    
    # Supported image extensions
    extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif'}
    
    # Find all image files
    image_files = []
    for ext in extensions:
        image_files.extend(Path(input_dir).glob(f"*{ext}"))
        image_files.extend(Path(input_dir).glob(f"*{ext.upper()}"))
    
    if not image_files:
        print(f"❌ No image files found in: {input_dir}")
        return False
    
    print(f"📂 Found {len(image_files)} images to process")
    
    for i, image_file in enumerate(image_files, 1):
        print(f"\n[{i}/{len(image_files)}] Processing: {image_file.name}")
        
        # Create output subdirectory for this image
        image_output_dir = os.path.join(output_dir, image_file.stem)
        
        process_single_image(str(image_file), image_output_dir, min_area, max_area)
    
    return True





def main():
    parser = argparse.ArgumentParser(description="App Icon Segmenter Utility")
    
    # Input options
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--input", "-i", help="Input image file")
    group.add_argument("--batch", "-b", help="Input directory for batch processing")
    group.add_argument("--analyze", "-a", help="Analyze image to suggest parameters")
    
    # Output options
    parser.add_argument("--output", "-o", default="output", help="Output directory")
    
    # Detection parameters
    parser.add_argument("--min-area", type=int, default=1000, 
                       help="Minimum area for contour detection")
    parser.add_argument("--max-area", type=int, default=50000, 
                       help="Maximum area for contour detection")
    
    args = parser.parse_args()
    
    print("🎯 App Icon Segmenter Utility")
    print("=" * 50)
    
    try:
        if args.analyze:
            analyze_image(args.analyze)
        elif args.input:
            process_single_image(args.input, args.output, args.min_area, args.max_area)
        elif args.batch:
            process_batch(args.batch, args.output, args.min_area, args.max_area)
            
        print("\n✅ Processing complete!")
        
    except KeyboardInterrupt:
        print("\n⚠️  Processing interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())