#!/usr/bin/env python3
"""
App Icon Processor - Complete Pipeline
======================================

A comprehensive tool for processing app icons from screenshots:
1. Detects icons from homescreen screenshots
2. Extracts icon shapes using masks
3. Removes backgrounds with intelligent color analysis
4. Creates final processed icons ready for use

Usage:
    python process_icons.py

Requirements:
    - Input screenshot in input/ folder
    - Mask files in masks/ folder
    - Python with OpenCV and NumPy
"""

import os
import sys
import time
from pathlib import Path


def print_banner():
    """Display welcome banner."""
    print("=" * 60)
    print("🎨 APP ICON PROCESSOR - Complete Pipeline")
    print("=" * 60)
    print("🔍 Detects icons from screenshots")
    print("✂️  Extracts shapes using masks")
    print("🎯 Removes backgrounds intelligently")
    print("✨ Creates final processed icons")
    print("=" * 60)
    print()


def check_prerequisites():
    """Check if all required files and folders exist."""
    print("📋 Checking prerequisites...")

    required_dirs = ['input', 'masks']
    required_files = [
        'input/homescreen.jpg',
        'masks/iconmask_big.png',
        'masks/iconmask_small.png'
    ]

    missing = []

    # Check directories
    for dir_name in required_dirs:
        if not os.path.exists(dir_name):
            missing.append(f"Directory: {dir_name}/")

    # Check files
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing.append(f"File: {file_path}")

    if missing:
        print("❌ Missing required files/directories:")
        for item in missing:
            print(f"   - {item}")
        print()
        print("📁 Please ensure you have:")
        print("   - input/homescreen.jpg (your screenshot)")
        print("   - masks/iconmask_big.png (large icon mask)")
        print("   - masks/iconmask_small.png (small icon mask)")
        return False

    print("✅ All prerequisites found!")
    return True


def run_step(step_name, module_name, description):
    """Run a processing step and handle errors."""
    print(f"\n🚀 Step {step_name}: {description}")
    print("-" * 50)

    try:
        # Import and run the module
        if module_name == 'segmenter':
            import segmenter
            segmenter.main()
        elif module_name == 'cookiecutter':
            import cookiecutter
            cookiecutter.extract_shapes_from_output_folder()
        elif module_name == 'final_assembly':
            import final_assembly
            # final_assembly runs automatically when imported

        print(f"✅ {step_name} completed successfully!")
        return True

    except Exception as e:
        print(f"❌ {step_name} failed: {str(e)}")
        return False


def create_build_structure():
    """Ensure build directory structure exists."""
    build_dirs = [
        'build',
        'build/output',
        'build/extracted_shapes',
        'new_icons'
    ]

    for dir_path in build_dirs:
        os.makedirs(dir_path, exist_ok=True)


def display_results():
    """Show processing results and file locations."""
    print("\n" + "=" * 60)
    print("🎉 PROCESSING COMPLETE!")
    print("=" * 60)

    # Count files in each directory
    output_icons = len([f for f in os.listdir(
        'build/output') if f.startswith('icon_')])
    extracted_shapes = len([f for f in os.listdir(
        'build/extracted_shapes') if f.endswith('_shape.png')])

    if os.path.exists('new_icons'):
        final_icons = len([f for f in os.listdir('new_icons')
                          if f.startswith('merged_icon_')])
    else:
        final_icons = 0

    print("📊 Processing Summary:")
    print(f"   🔍 Detected icons: {output_icons}")
    print(f"   ✂️  Extracted shapes: {extracted_shapes}")
    print(f"   ✨ Final processed icons: {final_icons}")
    print()

    print("📁 Output Locations:")
    print("   📂 build/output/ - Detected icons from screenshot")
    print("   📂 build/extracted_shapes/ - Icons with shape masks applied")
    print("   📂 new_icons/ - Final processed icons (backgrounds removed)")
    print()

    if final_icons > 0:
        print("🎯 Your processed icons are ready in the new_icons/ folder!")
    else:
        print("⚠️  No final icons were created. Check the extracted_shapes folder.")


def main():
    """Main processing pipeline."""
    start_time = time.time()

    print_banner()

    # Check prerequisites
    if not check_prerequisites():
        print("\n❌ Cannot proceed without required files.")
        print("📖 See README.md for setup instructions.")
        sys.exit(1)

    # Create build structure
    create_build_structure()

    print("\n🎬 Starting processing pipeline...")

    # Step 1: Detect icons from screenshot
    success = run_step(
        "1/3",
        "segmenter",
        "Detecting app icons from screenshot"
    )
    if not success:
        sys.exit(1)

    # Step 2: Extract shapes using masks
    success = run_step(
        "2/3",
        "cookiecutter",
        "Extracting icon shapes with masks"
    )
    if not success:
        sys.exit(1)

    # Calculate processing time
    end_time = time.time()
    processing_time = end_time - start_time

    # Display results
    display_results()
    print(f"⏱️  Total processing time: {processing_time:.1f} seconds")
    print("=" * 60)


if __name__ == "__main__":
    main()
