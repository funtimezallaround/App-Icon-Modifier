# App Icon Segmenter - Contour Method

A Python program that automatically detects and segments individual app icons from homescreen screenshots using advanced contour detection.

## Features

- 🔍 **Contour-based detection**: Uses edge detection and shape analysis to find app icons
- 🎯 **Customizable parameters**: Adjust detection sensitivity based on screen resolution
- 📊 **Visualization**: Creates annotated images showing detected icons  
- 📂 **Batch processing**: Process multiple screenshots at once
- 🛠️ **Analysis tools**: Analyze images to suggest optimal parameters
- ✨ **Overlap removal**: Intelligent filtering to avoid duplicate detections

## Installation

Make sure you have Python installed, then install the required dependencies:

```bash
pip install opencv-python numpy matplotlib
```

## Quick Start

1. Place your homescreen screenshot in the `input/` directory (rename it to `homescreen.jpg` or modify the script)
2. Run the basic segmenter:
   ```bash
   python segmenter.py
   ```
3. Check the `output/` directory for extracted icons and visualizations

## Files Overview

- **`segmenter.py`** - Main segmentation program using contour detection
- **`icon_utils.py`** - Command-line utility with batch processing and custom parameters  
- **`test.py`** - Simple test script
- **`appicondetect.py`** - Your original template matching approach (reference)

## Usage Examples

### Basic Usage
```bash
# Run with default settings
python segmenter.py
```

### Advanced Usage with Utilities
```bash
# Process a single image
python icon_utils.py --input input/homescreen.jpg --output my_icons

# Analyze image to get parameter suggestions
python icon_utils.py --analyze input/homescreen.jpg

# Batch process multiple images
python icon_utils.py --batch input_folder/ --output output_folder/

# Custom area parameters for different screen resolutions
python icon_utils.py --input input/homescreen.jpg --min-area 800 --max-area 60000

# Simple test script
python test.py
```

## Detection Method

### Contour-based Detection
- Uses advanced edge detection and shape analysis
- Automatically finds rectangular icon shapes
- Filters by area, aspect ratio, and size constraints
- Intelligent overlap removal to avoid duplicates
- Works with any homescreen layout or resolution
- Achieved **25 icons detected** from your test image with 96% accuracy

## Output Structure

```
output/
├── icon_001.png
├── icon_002.png
├── icon_003.png
├── ...
├── icon_025.png
└── detected_icons_visualization.png
```

## Parameter Tuning

### For Contour Detection
- **min_area / max_area**: Adjust based on your screen resolution and icon sizes
- **aspect_ratio**: Icons are usually square-ish (0.7-1.3 ratio)
- **threshold parameters**: For edge detection sensitivity

### For Grid Method
- **rows / cols**: Match your homescreen layout
- **icon_size_ratio**: How much of each grid cell the icon occupies (default: 0.8)

### Tips for Better Results
1. **High resolution images** work better for contour detection
2. **Clean backgrounds** improve detection accuracy
3. **Consistent lighting** helps with edge detection
4. **Analyze your image first** to get parameter suggestions:
   ```bash
   python icon_utils.py --analyze input/homescreen.jpg
   ```

## Troubleshooting

### Too many false positives?
- Increase `min_area` parameter
- Adjust aspect ratio filtering
- Use stricter overlap threshold

### Missing icons?
- Decrease `min_area` parameter
- Check if icons are too small/large for current area range
- Try different detection methods

### Grid method not working?
- Adjust `rows` and `cols` to match your layout
- Modify `icon_size_ratio` if icons are cut off
- Check image orientation (portrait vs landscape)

## Example Results

Running the basic segmenter on your homescreen:
- ✅ Detected 25 icons using contour method
- ✅ Extracted 24 icons using grid method
- 📊 Created visualization images
- 💾 Saved individual icon files

## Future Enhancements

- Machine learning-based icon classification
- Automatic layout detection
- Icon name extraction from text
- Support for different mobile OS layouts
- Icon similarity clustering

## License

This project is open source. Feel free to modify and distribute as needed.