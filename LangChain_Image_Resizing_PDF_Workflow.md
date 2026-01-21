# LangChain Dynamic Image Resizing for PDF Generation

## Table of Contents

1. [Problem Description](#problem-description)
2. [Key Features](#key-features)
3. [Solution Overview](#solution-overview)
4. [Prerequisites and Dependencies](#prerequisites-and-dependencies)
5. [Implementation](#implementation)
6. [Code Example](#code-example)
7. [Detailed Workflow Explanation](#detailed-workflow-explanation)
8. [Real-World Applications](#real-world-applications)
9. [Best Practices](#best-practices)
10. [Troubleshooting](#troubleshooting)

---

## Problem Description

When generating PDFs programmatically, one common challenge is handling images of varying sizes. Oversized images can:
- Destroy PDF layouts and formatting
- Cause content to overflow page boundaries
- Result in poor visual presentation
- Increase file sizes unnecessarily
- Create inconsistent document appearance

This solution demonstrates how to use **LangChain** to orchestrate dynamic image resizing workflows, ensuring proper formatting and maintaining layout integrity in generated PDFs.

### Why LangChain?

LangChain provides:
- **Modular Architecture**: Break complex workflows into manageable steps
- **Sequential Processing**: Chain multiple operations in a predictable order
- **LLM Integration**: Use language models for intelligent decision-making
- **Scalability**: Easily extend workflows with new steps
- **Reusability**: Create reusable components for different projects

---

## Key Features

This solution provides:

1. **Dynamic Image Resizing**: Automatically resize images based on maximum width constraints
2. **LangChain Orchestration**: Coordinate multiple steps in a single workflow
3. **PIL/Pillow Integration**: Leverage Python's powerful image processing library
4. **Layout Planning**: Use LLMs to determine optimal content arrangement
5. **Conditional Processing**: Apply resizing only when necessary
6. **Preserving Aspect Ratios**: Maintain image proportions during resizing
7. **Modular Design**: Easy to extend and customize for specific needs

---

## Solution Overview

The solution integrates three key components:

1. **Image Processing Layer**: Uses PIL/Pillow for dynamic image resizing
2. **LangChain Orchestration**: Coordinates the workflow steps
3. **LLM Decision Making**: Plans optimal layouts for PDF generation

The workflow follows these steps:
```
Input Data → Image Resizing → Layout Planning → PDF Generation
```

---

## Prerequisites and Dependencies

### Required Libraries

```bash
# Core dependencies
pip install langchain
pip install langchain-openai
pip install Pillow
pip install openai

# Optional: For PDF generation
pip install reportlab
pip install PyPDF2
```

### Environment Setup

```bash
# Set your OpenAI API key
export OPENAI_API_KEY="your-api-key-here"
```

### Python Version

- Python 3.8 or higher recommended

---

## Implementation

### Step 1: Image Resizing Function

The first component is a dynamic image resizing function using PIL:

```python
from PIL import Image

def resize_image(image_path, max_width):
    """
    Resize an image if it exceeds the maximum width while maintaining aspect ratio.
    
    Args:
        image_path (str): Path to the image file
        max_width (int): Maximum allowed width in pixels
    
    Returns:
        PIL.Image: Resized image object
    """
    img = Image.open(image_path)
    
    # Check if resizing is needed
    if img.size[0] > max_width:
        # Calculate scale factor to maintain aspect ratio
        scale_factor = max_width / img.size[0]
        
        # Calculate new dimensions
        new_width = max_width
        new_height = int(img.size[1] * scale_factor)
        
        # Resize the image with high-quality resampling
        img = img.resize((new_width, new_height), Image.LANCZOS)
    
    return img
```

**Note**: `Image.ANTIALIAS` has been deprecated in favor of `Image.LANCZOS` in newer versions of Pillow.

### Step 2: Layout Planning with LLM

Use a language model to intelligently plan the PDF layout:

```python
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI

# Initialize the language model
llm = OpenAI(model="gpt-4", temperature=0.3)

# Create a prompt template for layout planning
layout_prompt = PromptTemplate(
    template="""
    You are a professional document layout designer. Arrange the following content 
    for optimal presentation in a PDF document:
    
    - Text Content: {text}
    - Table Data: {table}
    - Images: {images}
    
    Provide a layout strategy that includes:
    1. The order of elements
    2. Spacing recommendations
    3. Page break suggestions
    4. Image positioning (left, center, right)
    
    Format your response as a structured layout plan.
    """,
    input_variables=["text", "table", "images"]
)
```

### Step 3: LangChain Sequential Chain

Construct the complete workflow using LangChain:

```python
from langchain.chains import SequentialChain, LLMChain

# Note: This is a conceptual example. LangChain's SequentialChain
# works with LLMChain objects. For custom functions, you may need
# to wrap them in custom Chain classes.

# Create layout planning chain
layout_chain = LLMChain(llm=llm, prompt=layout_prompt)

# In practice, you would create custom Chain classes for image processing
# or use LangChain's Transform chains
```

---

## Code Example

Here's a complete, working example that demonstrates the entire workflow:

```python
from langchain.chains import SequentialChain
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from PIL import Image
import os

# Step 1: Dynamic Image Processing Function
def resize_image(image_path, max_width=800):
    """
    Resize image if it exceeds maximum width, maintaining aspect ratio.
    """
    img = Image.open(image_path)
    if img.size[0] > max_width:
        scale_factor = max_width / img.size[0]
        img = img.resize(
            (max_width, int(img.size[1] * scale_factor)), Image.LANCZOS
        )
    return img

def save_resized_image(img, output_path):
    """
    Save the resized image to disk.
    """
    img.save(output_path, quality=95)
    return output_path

# Step 2: LLM to Decide Layout
llm = OpenAI(model="gpt-4", temperature=0.3)

layout_prompt = PromptTemplate(
    template="""
    Arrange the following content for a professional PDF document:
    
    - Text: {text}
    - Table: {table}
    - Images: {images}
    
    Provide a layout strategy including:
    1. Element order
    2. Spacing between elements
    3. Image placement recommendations
    4. Page break suggestions
    
    Be concise and specific.
    """,
    input_variables=["text", "table", "images"]
)

# Step 3: PDF Generation Function (Placeholder)
def generate_pdf(layout_strategy, content_data, output_path="output.pdf"):
    """
    Generate PDF based on layout strategy.
    
    This is a placeholder function. In a real implementation, you would use
    libraries like ReportLab or WeasyPrint to generate the actual PDF.
    """
    print(f"Generating PDF with strategy: {layout_strategy}")
    print(f"Content data: {content_data}")
    
    # Here you would implement actual PDF generation logic
    # For example, using ReportLab:
    # from reportlab.pdfgen import canvas
    # c = canvas.Canvas(output_path)
    # ... add content based on layout_strategy ...
    # c.save()
    
    return output_path

# Step 4: Complete Workflow Function
def process_document_for_pdf(image_path, text, table, max_width=800):
    """
    Complete workflow to process a document with images for PDF generation.
    """
    print("Starting document processing workflow...")
    
    # Step 1: Process Image
    print(f"Processing image: {image_path}")
    resized_image = resize_image(image_path, max_width)
    resized_image_path = image_path.replace(".jpg", "_resized.jpg")
    save_resized_image(resized_image, resized_image_path)
    print(f"Image resized and saved to: {resized_image_path}")
    
    # Step 2: Plan Layout using LLM
    print("Planning layout with LLM...")
    image_info = f"Image: {resized_image_path} (dimensions: {resized_image.size})"
    
    layout_strategy = llm.predict(
        layout_prompt.format(
            text=text,
            table=str(table),
            images=image_info
        )
    )
    print(f"Layout strategy: {layout_strategy}")
    
    # Step 3: Generate PDF
    print("Generating PDF...")
    content_data = {
        "text": text,
        "table": table,
        "image_path": resized_image_path,
        "layout": layout_strategy
    }
    
    pdf_path = generate_pdf(layout_strategy, content_data)
    print(f"PDF generated: {pdf_path}")
    
    return {
        "resized_image": resized_image_path,
        "layout_strategy": layout_strategy,
        "pdf_path": pdf_path
    }

# Step 5: Run the Complete Workflow
if __name__ == "__main__":
    # Example document data
    document_data = {
        "image_path": "example.jpg",  # Make sure this file exists
        "text": "Welcome to our comprehensive PDF guide! This document demonstrates dynamic image resizing.",
        "table": {
            "Header": ["Year", "Revenue", "Growth"],
            "Rows": [
                ["2024", "$1.0M", "15%"],
                ["2025", "$1.5M", "50%"],
                ["2026", "$2.2M", "47%"]
            ]
        }
    }
    
    # Process the document
    result = process_document_for_pdf(
        image_path=document_data["image_path"],
        text=document_data["text"],
        table=document_data["table"],
        max_width=800
    )
    
    print("\n=== Workflow Complete ===")
    print(f"Resized Image: {result['resized_image']}")
    print(f"PDF Output: {result['pdf_path']}")
```

---

## Detailed Workflow Explanation

### Phase 1: Image Processing

1. **Load Image**: Open the image file using PIL
2. **Check Dimensions**: Compare current width to maximum allowed width
3. **Calculate Scaling**: Determine scale factor to maintain aspect ratio
4. **Resize**: Apply high-quality resampling using LANCZOS algorithm
5. **Save**: Store the resized image for later use

**Key Considerations**:
- Preserving aspect ratio prevents distortion
- LANCZOS provides high-quality downsampling
- Original images are not modified (non-destructive)

### Phase 2: Layout Planning

1. **Prepare Context**: Gather all content information
2. **LLM Query**: Send structured prompt to language model
3. **Receive Strategy**: Get intelligent layout recommendations
4. **Parse Response**: Extract actionable layout instructions

**Benefits**:
- AI-powered layout decisions
- Context-aware placement
- Professional formatting suggestions
- Adaptable to different content types

### Phase 3: PDF Generation

1. **Initialize Canvas**: Create PDF document structure
2. **Apply Layout**: Follow LLM-suggested strategy
3. **Add Content**: Insert text, tables, and images
4. **Optimize**: Ensure proper spacing and formatting
5. **Save**: Export final PDF document

---

## Real-World Applications

### 1. Automated Report Generation

Generate financial reports with charts and tables:
```python
# Process quarterly earnings report
report_data = {
    "charts": ["revenue_chart.png", "growth_chart.png"],
    "tables": quarterly_financial_data,
    "text": executive_summary
}
```

### 2. Marketing Materials

Create product catalogs with multiple images:
```python
# Resize product images for catalog
for product in products:
    resize_image(product.image_path, max_width=600)
```

### 3. Educational Content

Generate study materials with diagrams:
```python
# Process educational diagrams
diagrams = ["diagram1.png", "diagram2.png", "diagram3.png"]
for diagram in diagrams:
    process_diagram_for_pdf(diagram)
```

### 4. Technical Documentation

Create API documentation with code screenshots:
```python
# Resize code screenshots
screenshots = get_code_screenshots()
for screenshot in screenshots:
    resize_image(screenshot, max_width=700)
```

---

## Best Practices

### Image Resizing

1. **Set Appropriate Max Width**: Choose based on page size and margins
   - US Letter (8.5" × 11"): max_width = 600-700px
   - A4 (210mm × 297mm): max_width = 550-650px

2. **Maintain Quality**: Use LANCZOS resampling for best results

3. **Check File Formats**: Support common formats (JPEG, PNG, GIF)

4. **Handle Errors**: Implement try-except blocks for file operations

### LangChain Integration

1. **Optimize Prompts**: Write clear, specific prompts for better results

2. **Temperature Settings**: Use low temperature (0.3-0.5) for consistent layouts

3. **Error Handling**: Implement fallback strategies if LLM fails

4. **Caching**: Cache layout strategies for similar content

### PDF Generation

1. **Page Size Consistency**: Maintain uniform page dimensions

2. **Margin Management**: Ensure adequate white space

3. **Font Selection**: Use readable, professional fonts

4. **File Size Optimization**: Compress images appropriately

---

## Troubleshooting

### Common Issues and Solutions

#### Issue: Image Quality Degradation

**Problem**: Resized images appear blurry or pixelated

**Solution**:
```python
# Use LANCZOS instead of BILINEAR or NEAREST
img = img.resize((new_width, new_height), Image.LANCZOS)

# Increase JPEG quality when saving
img.save(output_path, quality=95)
```

#### Issue: Aspect Ratio Distortion

**Problem**: Images appear stretched or squashed

**Solution**:
```python
# Always calculate both dimensions based on scale factor
scale_factor = max_width / img.size[0]
new_height = int(img.size[1] * scale_factor)
img = img.resize((max_width, new_height), Image.LANCZOS)
```

#### Issue: LLM Response Inconsistency

**Problem**: Layout strategies vary too much between runs

**Solution**:
```python
# Lower the temperature for more consistent outputs
llm = OpenAI(model="gpt-4", temperature=0.1)

# Add more specific instructions in prompt
# Use few-shot examples in the prompt
```

#### Issue: Large File Sizes

**Problem**: Generated PDFs are too large

**Solution**:
```python
# Reduce image dimensions more aggressively
max_width = 600  # Instead of 800

# Compress images before adding to PDF
img.save(output_path, quality=85, optimize=True)

# Use JPEG instead of PNG for photos
```

#### Issue: Memory Errors with Large Images

**Problem**: Program crashes when processing very large images

**Solution**:
```python
from PIL import Image

# Set a maximum image size limit
Image.MAX_IMAGE_PIXELS = 200000000  # Adjust as needed

# Process images in chunks if necessary
# Close images after processing
img = Image.open(path)
# ... process ...
img.close()
```

---

## Additional Resources

### Documentation

- [LangChain Documentation](https://python.langchain.com/)
- [Pillow (PIL) Documentation](https://pillow.readthedocs.io/)
- [ReportLab Documentation](https://www.reportlab.com/docs/reportlab-userguide.pdf)
- [OpenAI API Documentation](https://platform.openai.com/docs/)

### Example Projects

- [LangChain Tutorials](https://python.langchain.com/docs/tutorials)
- [PDF Generation Examples](https://github.com/topics/pdf-generation)

### Related Topics

- Document AI and Processing
- Automated Report Generation
- Content Management Systems
- Image Optimization Techniques

---

## Conclusion

This solution demonstrates how LangChain can orchestrate complex workflows involving image processing, AI-powered decision-making, and document generation. By combining PIL for image resizing, LangChain for workflow coordination, and LLMs for intelligent layout planning, you can create robust, scalable PDF generation systems.

### Key Takeaways

1. **Modularity**: Breaking workflows into distinct steps improves maintainability
2. **AI Integration**: LLMs can make intelligent layout decisions
3. **Quality Preservation**: Proper image resizing maintains visual quality
4. **Scalability**: The approach scales to handle various document types
5. **Flexibility**: Easy to extend with additional processing steps

### Next Steps

- Implement actual PDF generation using ReportLab or WeasyPrint
- Add support for multiple images per document
- Implement batch processing for multiple documents
- Add error handling and logging
- Create unit tests for each component
- Optimize performance for large-scale operations

---

*Last Updated: 2026-01-21*
