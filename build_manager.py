"""
Build Manager - Organize All Icon Processing Outputs
Manages the build directory structure for all icon processing workflows.
"""

import os
import shutil
import glob
from datetime import datetime

def create_build_structure():
    """Create the build directory structure."""
    
    build_dirs = [
        "build",
        "build/output",           # Raw extracted icons from segmenter
        "build/extracted_shapes", # Shape-cut icons from cookiecutter  
        "build/processed_icons",  # Autumn squircle icons
        "build/previews",         # All visualization/preview images
        "build/logs"              # Processing logs
    ]
    
    print("📁 Creating build directory structure...")
    
    for directory in build_dirs:
        os.makedirs(directory, exist_ok=True)
        print(f"  ✅ {directory}")
    
    print("✨ Build structure ready!")


def clean_build():
    """Clean the build directory."""
    
    if os.path.exists("build"):
        print("🧹 Cleaning build directory...")
        shutil.rmtree("build")
        print("✅ Build directory cleaned")
    else:
        print("ℹ️ No build directory to clean")


def move_legacy_outputs():
    """Move any existing outputs from old locations to build folder."""
    
    print("📦 Moving legacy outputs to build folder...")
    
    # Create build structure first
    create_build_structure()
    
    moves = [
        # (source_pattern, destination_dir)
        ("output/icon_*.png", "build/output"),
        ("output/detected_icons_visualization.png", "build/previews"),
        ("extracted_shapes/*", "build/extracted_shapes"),
        ("processed_icons/*", "build/processed_icons"),
        ("*.png", "build/previews"),  # Move any loose preview files
    ]
    
    moved_count = 0
    
    for source_pattern, dest_dir in moves:
        files_to_move = glob.glob(source_pattern)
        
        if files_to_move:
            os.makedirs(dest_dir, exist_ok=True)
            
            for file_path in files_to_move:
                filename = os.path.basename(file_path)
                dest_path = os.path.join(dest_dir, filename)
                
                # Skip if it's already in build folder or is a system file
                if file_path.startswith("build/") or filename.startswith(("README", "DIRECTORY")):
                    continue
                
                try:
                    shutil.move(file_path, dest_path)
                    print(f"  📦 Moved: {file_path} → {dest_path}")
                    moved_count += 1
                except Exception as e:
                    print(f"  ❌ Failed to move {file_path}: {e}")
    
    print(f"✅ Moved {moved_count} files to build directory")
    
    # Clean up empty directories
    cleanup_dirs = ["output", "extracted_shapes", "processed_icons"]
    for directory in cleanup_dirs:
        if os.path.exists(directory) and not os.listdir(directory):
            os.rmdir(directory)
            print(f"  🗑️ Removed empty directory: {directory}")


def create_build_summary():
    """Create a summary of what's in the build directory."""
    
    if not os.path.exists("build"):
        print("❌ No build directory found")
        return
    
    print("\n📊 BUILD DIRECTORY SUMMARY")
    print("=" * 50)
    
    subdirs = [
        ("build/output", "Raw extracted icons"),
        ("build/extracted_shapes", "Shape-cut icons (cookiecutter)"),
        ("build/processed_icons", "Autumn squircle icons"),
        ("build/previews", "Visualization/preview images"),
        ("build/logs", "Processing logs")
    ]
    
    total_files = 0
    
    for subdir, description in subdirs:
        if os.path.exists(subdir):
            files = glob.glob(f"{subdir}/*")
            count = len(files)
            total_files += count
            
            status = "✅" if count > 0 else "📂"
            print(f"{status} {description:30} {count:3d} files")
            
            if count > 0 and count <= 5:
                for file_path in files[:3]:
                    filename = os.path.basename(file_path)
                    print(f"    • {filename}")
                if count > 3:
                    print(f"    • ... and {count - 3} more")
        else:
            print(f"❌ {description:30}   - missing")
    
    print("-" * 50)
    print(f"📁 Total files in build: {total_files}")
    
    # Check build folder size
    total_size = 0
    for root, dirs, files in os.walk("build"):
        for file in files:
            file_path = os.path.join(root, file)
            total_size += os.path.getsize(file_path)
    
    size_mb = total_size / (1024 * 1024)
    print(f"💾 Total build size: {size_mb:.1f} MB")


def create_build_log():
    """Create a log file with build information."""
    
    log_dir = "build/logs"
    os.makedirs(log_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f"build_{timestamp}.log")
    
    with open(log_file, 'w') as f:
        f.write(f"Icon Processing Build Log\n")
        f.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"=" * 40 + "\n\n")
        
        # Count files in each directory
        for subdir in ["output", "extracted_shapes", "processed_icons", "previews"]:
            full_path = f"build/{subdir}"
            if os.path.exists(full_path):
                files = glob.glob(f"{full_path}/*")
                f.write(f"{subdir}: {len(files)} files\n")
        
        f.write(f"\nBuild completed successfully!\n")
    
    print(f"📝 Build log saved: {log_file}")


def main():
    """Main function for build management."""
    
    print("🔧 ICON PROCESSING BUILD MANAGER")
    print("=" * 40)
    
    # Create build structure
    create_build_structure()
    
    # Move any legacy outputs
    move_legacy_outputs()
    
    # Create summary
    create_build_summary()
    
    # Create log
    create_build_log()
    
    print("\n✅ Build management complete!")
    print("💡 All future processing will save to the 'build' folder")


if __name__ == "__main__":
    main()