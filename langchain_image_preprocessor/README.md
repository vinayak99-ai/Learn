# LangChain Image Preprocessor for PDF Generation

## Overview

This workflow preprocesses JSON files containing image links, text, and tables to optimize images for PDF generation. The pipeline downloads images from URLs, resizes them while maintaining aspect ratios, and updates the JSON with optimized dimensions and placement details.

## Purpose

When generating PDFs programmatically, images of varying sizes can cause layout issues, overflow page boundaries, and result in poor visual presentation. This preprocessing workflow ensures:

- **Consistent image sizing**: All images are resized to fit within a maximum width while maintaining aspect ratios
- **Optimized file sizes**: Images are compressed for efficient PDF generation
- **Layout planning**: Intelligent suggestions for image placement and page breaks
- **Metadata enrichment**: Updated JSON includes dimensions and processed image paths

## Features

- ✅ Downloads images from URLs
- ✅ Dynamic image resizing with aspect ratio preservation (max_width=600px)
- ✅ High-quality image resampling using LANCZOS algorithm
- ✅ Automatic directory management for processed images
- ✅ Layout planning with intelligent suggestions
- ✅ Comprehensive error handling
- ✅ Detailed processing logs

## Input JSON Structure

The input JSON file should follow this structure:

```json
{
    "title": "Sample PDF",
    "images": [
        {
            "url": "https://example.com/image1.jpg",
            "alt_text": "Image 1"
        },
        {
            "url": "https://example.com/image2.jpg",
            "alt_text": "Image 2"
        }
    ],
    "content": [
        {
            "type": "text",
            "value": "Welcome to the Sample PDF document!"
        },
        {
            "type": "table",
            "headers": ["Year", "Sales"],
            "rows": [
                ["2020", "$1M"],
                ["2021", "$1.5M"]
            ]
        }
    ]
}
```

### Input Fields

- **title** (string): Title of the PDF document
- **images** (array): List of image objects, each containing:
  - **url** (string): URL of the image to download
  - **alt_text** (string): Alternative text description
- **content** (array): List of content items, each with:
  - **type** (string): Type of content ("text" or "table")
  - **value** (string): Text content (for type="text")
  - **headers** (array): Table column headers (for type="table")
  - **rows** (array): Table rows (for type="table")

## Output JSON Structure

The output JSON includes optimized image information:

```json
{
    "title": "Sample PDF",
    "images": [
        {
            "url": "processed_images/image1.jpg",
            "alt_text": "Image 1",
            "dimensions": [600, 400]
        },
        {
            "url": "processed_images/image2.jpg",
            "alt_text": "Image 2",
            "dimensions": [600, 350]
        }
    ],
    "content": [
        {
            "type": "text",
            "value": "Welcome to the Sample PDF document!"
        },
        {
            "type": "table",
            "headers": ["Year", "Sales"],
            "rows": [
                ["2020", "$1M"],
                ["2021", "$1.5M"]
            ]
        }
    ],
    "layout": {
        "image_alignment": "center",
        "page_breaks": []
    }
}
```

### Output Fields

All input fields are preserved, with the following additions:

- **images[].dimensions** (array): Image dimensions as [width, height] in pixels
- **images[].url** (string): Updated to point to the processed image path
- **layout** (object): Layout planning information:
  - **image_alignment** (string): Suggested image alignment ("center", "left", "right")
  - **page_breaks** (array): Suggested locations for page breaks

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Dependencies

Install the required Python packages:

```bash
pip install Pillow requests
```

Or use the requirements file from the parent directory:

```bash
cd /home/runner/work/Learn/Learn
pip install -r requirements.txt
```

## Usage

### Basic Usage

Run the preprocessing pipeline:

```bash
cd langchain_image_preprocessor
python preprocessing_pipeline.py
```

This will:
1. Read `sample_input.json`
2. Download and process images
3. Generate `optimized_output.json`
4. Save processed images to `processed_images/` directory

### Custom Usage

You can also use the pipeline as a Python module:

```python
from preprocessing_pipeline import PreprocessingPipeline

# Create pipeline instance
pipeline = PreprocessingPipeline(
    max_image_width=600,
    output_dir="processed_images"
)

# Process your JSON file
result = pipeline.process(
    input_json_path="your_input.json",
    output_json_path="your_output.json"
)

print(f"Processed {result['processed_images']} images successfully")
```

## File Structure

```
langchain_image_preprocessor/
├── README.md                    # This file
├── sample_input.json            # Sample input file
├── optimized_output.json        # Generated output (after running)
├── preprocessing_pipeline.py    # Main Python script
└── processed_images/            # Directory for processed images (created automatically)
    ├── image1.jpg
    └── image2.jpg
```

## Configuration

### Image Processing Settings

You can customize the image processing behavior by modifying the `PreprocessingPipeline` initialization:

```python
pipeline = PreprocessingPipeline(
    max_image_width=600,     # Maximum width in pixels (default: 600)
    output_dir="processed_images"  # Output directory (default: "processed_images")
)
```

### Image Quality

To adjust image quality, modify the `ImagePreprocessor` initialization in the pipeline:

```python
self.image_preprocessor = ImagePreprocessor(
    max_width=max_image_width,
    output_quality=95,  # JPEG quality: 1-100 (default: 95)
    save_dir=output_dir
)
```

## Workflow Steps

### Step 1: Image Processing

1. Downloads images from URLs using `requests`
2. Opens images using PIL (Pillow)
3. Checks image dimensions
4. Resizes if width exceeds maximum (maintains aspect ratio)
5. Saves processed images with high quality (JPEG quality=95)
6. Returns file path and dimensions

### Step 2: Layout Planning

1. Analyzes document content (images, text, tables)
2. Determines optimal image alignment (currently: center)
3. Suggests page breaks for documents with multiple images
4. Returns layout recommendations

### Step 3: JSON Generation

1. Combines original content with processed image data
2. Adds layout planning information
3. Writes optimized JSON to output file
4. Preserves all original content and metadata

## Error Handling

The pipeline includes robust error handling:

- **Network errors**: If image download fails, the error is logged and processing continues
- **Invalid images**: If an image cannot be processed, the original URL is kept
- **Missing files**: Clear error messages if input file is not found
- **Processing errors**: Full stack traces for debugging

## Integration with PDF Generation

This preprocessor is designed to work with PDF generation APIs or libraries. The output JSON can be passed to:

- **ReportLab**: Python PDF generation library
- **WeasyPrint**: HTML to PDF converter
- **Licensed POS APIs**: Commercial PDF generation services
- **Custom PDF generators**: Any system that accepts JSON input

Example integration:

```python
from preprocessing_pipeline import PreprocessingPipeline
# from your_pdf_library import PDFGenerator

# Step 1: Preprocess images
pipeline = PreprocessingPipeline()
result = pipeline.process("input.json", "optimized.json")

# Step 2: Load optimized JSON
with open("optimized.json", "r") as f:
    optimized_data = json.load(f)

# Step 3: Generate PDF
# pdf_generator = PDFGenerator()
# pdf_generator.create_from_json(optimized_data, "output.pdf")
```

## Troubleshooting

### Common Issues

#### Issue: Images not downloading

**Symptoms**: Network errors or timeout messages

**Solutions**:
- Check internet connectivity
- Verify image URLs are accessible
- Increase timeout in `resize_image()` method
- Check firewall settings

#### Issue: Poor image quality

**Symptoms**: Processed images appear blurry

**Solutions**:
- Increase `output_quality` parameter (default: 95)
- Ensure `Image.LANCZOS` resampling is used
- Check original image quality

#### Issue: Images too large or too small

**Symptoms**: Processed images don't fit well in PDFs

**Solutions**:
- Adjust `max_image_width` parameter
- Consider page size and margins when setting max width
- Use different widths for different PDF page sizes

## Best Practices

1. **Image URLs**: Use HTTPS URLs for better security
2. **Image Formats**: Support JPEG, PNG, GIF formats
3. **File Naming**: Use descriptive filenames in URLs
4. **Error Handling**: Always check the output JSON for errors
5. **Backup**: Keep original input JSON files
6. **Testing**: Test with various image sizes and formats
7. **Performance**: For large batches, consider parallel processing

## Future Enhancements

Potential improvements for this workflow:

- [ ] LLM integration for intelligent layout planning (using LangChain)
- [ ] Support for multiple image size profiles
- [ ] Batch processing for multiple JSON files
- [ ] Progress tracking and reporting
- [ ] Caching for previously downloaded images
- [ ] Image format conversion options
- [ ] Watermarking support
- [ ] OCR for images with text
- [ ] Automatic image optimization
- [ ] Cloud storage integration

## Resources

### Documentation

- [Pillow (PIL) Documentation](https://pillow.readthedocs.io/)
- [Requests Library](https://requests.readthedocs.io/)
- [LangChain Documentation](https://python.langchain.com/)
- [JSON Format Specification](https://www.json.org/)

### Related Projects

- [langchain_pdf_image_resizer.py](../langchain_pdf_image_resizer.py) - Related PDF processing script in parent directory
- [LangChain_Image_Resizing_PDF_Workflow.md](../LangChain_Image_Resizing_PDF_Workflow.md) - Comprehensive workflow documentation

## License

This project is part of the Learn repository. See the parent repository for license information.

## Contributing

Contributions are welcome! Please ensure:
- Code follows PEP 8 style guidelines
- Documentation is updated
- Error handling is robust
- Tests are included for new features

## Support

For issues or questions:
1. Check this README for common solutions
2. Review the troubleshooting section
3. Check the parent repository's documentation
4. Open an issue in the GitHub repository

---

*Last Updated: 2026-01-21*
*Version: 1.0.0*
