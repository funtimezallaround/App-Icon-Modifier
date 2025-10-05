"""
Cleanup Script for App Icon Processor
====================================

This script organizes the workspace by:
1. Moving old/development files to an archive folder
2. Replacing the old README with the new one
3. Cleaning up temporary files
4. Organizing the project structure

Run this to clean up the project for end users.
"""

import os
import shutil
from pathlib import Path

def create_archive():
    """Create archive folder for old files."""
    archive_dir = "archive"
    os.makedirs(archive_dir, exist_ok=True)
    return archive_dir

def move_to_archive(files_to_archive, archive_dir):
    """Move specified files to archive folder."""
    moved_files = []
    
    for file_path in files_to_archive:
        if os.path.exists(file_path):
            try:
                destination = os.path.join(archive_dir, os.path.basename(file_path))
                # If file already exists in archive, add number suffix
                counter = 1
                base_dest = destination
                while os.path.exists(destination):
                    name, ext = os.path.splitext(base_dest)
                    destination = f"{name}_{counter}{ext}"
                    counter += 1
                
                shutil.move(file_path, destination)
                moved_files.append(f"{file_path} → {destination}")
                print(f"📦 Moved: {file_path} → archive/")
            except Exception as e:
                print(f"❌ Failed to move {file_path}: {e}")
    
    return moved_files

def cleanup_temp_files():
    """Remove temporary and cache files."""
    temp_files = [
        "test_shape.png",
        "test_cropped.png", 
        "mask_extraction_preview.png",
        "__pycache__"
    ]
    
    removed_files = []
    
    for file_path in temp_files:
        if os.path.exists(file_path):
            try:
                if os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                else:
                    os.remove(file_path)
                removed_files.append(file_path)
                print(f"🗑️  Removed: {file_path}")
            except Exception as e:
                print(f"❌ Failed to remove {file_path}: {e}")
    
    return removed_files

def replace_readme():
    """Replace old README with new one."""
    if os.path.exists("NEW_README.md"):
        try:
            if os.path.exists("README.md"):
                shutil.move("README.md", "archive/OLD_README.md")
                print("📦 Moved: README.md → archive/OLD_README.md")
            
            shutil.move("NEW_README.md", "README.md") 
            print("✅ Updated: NEW_README.md → README.md")
            return True
        except Exception as e:
            print(f"❌ Failed to update README: {e}")
            return False
    return False

def main():
    """Main cleanup function."""
    print("🧹 WORKSPACE CLEANUP")
    print("=" * 50)
    
    # Create archive directory
    archive_dir = create_archive()
    print(f"📁 Created archive directory: {archive_dir}/")
    
    # Files to archive (development/test files)
    files_to_archive = [
        "alignment_checker.py",
        "appicondetect.py", 
        "build_manager.py",
        "color_analysis.py",
        "icon_utils.py",
        "shape_extractor.py", 
        "test_alignment.py",
        "test_masks.py",
        "DIRECTORY_INFO.md"
    ]
    
    print(f"\n📦 Archiving development files...")
    moved_files = move_to_archive(files_to_archive, archive_dir)
    
    print(f"\n🗑️  Cleaning temporary files...")
    removed_files = cleanup_temp_files()
    
    print(f"\n📄 Updating README...")
    readme_updated = replace_readme()
    
    # Summary
    print("\n" + "=" * 50)
    print("✅ CLEANUP COMPLETE!")
    print("=" * 50)
    print(f"📦 Archived {len(moved_files)} development files")
    print(f"🗑️  Removed {len(removed_files)} temporary files")
    print(f"📄 README updated: {'Yes' if readme_updated else 'No'}")
    
    print(f"\n🎯 Project Structure Now:")
    print("├── 📄 process_icons.py     # 👈 MAIN SCRIPT - Run this!")
    print("├── 📄 segmenter.py         # Icon detection")
    print("├── 📄 cookiecutter.py      # Shape extraction")  
    print("├── 📄 final_assembly.py    # Background removal")
    print("├── 📄 README.md           # Documentation")
    print("├── 📂 input/              # Your screenshots here")
    print("├── 📂 masks/              # Icon masks")
    print("├── 📂 build/              # Processing outputs") 
    print("├── 📂 new_icons/          # 🎯 Final results")
    print("└── 📂 archive/            # Old development files")
    
    print(f"\n💡 Ready for users! Just run: python process_icons.py")

if __name__ == "__main__":
    main()