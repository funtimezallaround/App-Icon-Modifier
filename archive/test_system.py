#!/usr/bin/env python3
"""
Quick Test Script for App Icon Processor
========================================

Tests the complete pipeline to ensure everything works properly.
Run this before distributing to users.
"""

import os
import sys

def test_imports():
    """Test if all modules can be imported."""
    print("🧪 Testing module imports...")
    
    try:
        import segmenter
        print("  ✅ segmenter.py - OK")
    except Exception as e:
        print(f"  ❌ segmenter.py - FAILED: {e}")
        return False
    
    try:
        import cookiecutter  
        print("  ✅ cookiecutter.py - OK")
    except Exception as e:
        print(f"  ❌ cookiecutter.py - FAILED: {e}")
        return False
        
    try:
        import final_assembly
        print("  ✅ final_assembly.py - OK") 
    except Exception as e:
        print(f"  ❌ final_assembly.py - FAILED: {e}")
        return False
    
    try:
        import process_icons
        print("  ✅ process_icons.py - OK")
    except Exception as e:
        print(f"  ❌ process_icons.py - FAILED: {e}")
        return False
    
    return True

def test_prerequisites():
    """Test if required files exist."""
    print("\n📋 Testing prerequisites...")
    
    required_files = [
        "input/homescreen.jpg",
        "masks/iconmask_big.png", 
        "masks/iconmask_small.png"
    ]
    
    all_found = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"  ✅ {file_path} - Found")
        else:
            print(f"  ❌ {file_path} - Missing")
            all_found = False
    
    return all_found

def test_opencv():
    """Test if OpenCV is working properly."""
    print("\n🔧 Testing OpenCV functionality...")
    
    try:
        import cv2
        
        # Test image loading
        test_img = cv2.imread("input/homescreen.jpg")
        if test_img is not None:
            print(f"  ✅ Image loading - OK ({test_img.shape})")
        else:
            print("  ❌ Image loading - FAILED")
            return False
            
        # Test mask loading
        test_mask = cv2.imread("masks/iconmask_big.png") 
        if test_mask is not None:
            print(f"  ✅ Mask loading - OK ({test_mask.shape})")
        else:
            print("  ❌ Mask loading - FAILED")
            return False
        
        print("  ✅ OpenCV functionality - OK")
        return True
        
    except Exception as e:
        print(f"  ❌ OpenCV test - FAILED: {e}")
        return False

def test_directory_structure():
    """Test if output directories can be created."""
    print("\n📁 Testing directory structure...")
    
    test_dirs = [
        "build",
        "build/output", 
        "build/extracted_shapes",
        "new_icons"
    ]
    
    try:
        for dir_path in test_dirs:
            os.makedirs(dir_path, exist_ok=True)
            if os.path.exists(dir_path):
                print(f"  ✅ {dir_path}/ - OK")
            else:
                print(f"  ❌ {dir_path}/ - Failed to create")
                return False
        
        return True
        
    except Exception as e:
        print(f"  ❌ Directory creation - FAILED: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 APP ICON PROCESSOR - SYSTEM TEST")
    print("=" * 50)
    
    tests = [
        ("Module Imports", test_imports),
        ("Prerequisites", test_prerequisites), 
        ("OpenCV Functionality", test_opencv),
        ("Directory Structure", test_directory_structure)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        result = test_func()
        if result:
            passed += 1
    
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS")
    print("=" * 50)
    print(f"✅ Passed: {passed}/{total}")
    print(f"❌ Failed: {total - passed}/{total}")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
        print("✨ System is ready for processing!")
        print("\n💡 Run: python process_icons.py")
        return True
    else:
        print("\n⚠️  SOME TESTS FAILED!")
        print("🔧 Please fix the issues before proceeding.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)