#!/usr/bin/env python3
"""
LangChain PDF Image Resizer - Dynamic Image Resizing for PDF Generation

This script demonstrates how to use LangChain to orchestrate dynamic image
resizing workflows for PDF generation, ensuring proper formatting and layout.

Author: Learn Repository Contributors
Date: 2026-01-21
"""

import os
import sys
from typing import Dict, List, Optional, Tuple
from PIL import Image


class ImageProcessor:
    """Handle image resizing and processing operations."""
    
    def __init__(self, max_width: int = 800, output_quality: int = 95):
        """
        Initialize the image processor.
        
        Args:
            max_width: Maximum width for resized images in pixels
            output_quality: JPEG quality for output (1-100)
        """
        self.max_width = max_width
        self.output_quality = output_quality
    
    def resize_image(self, image_path: str, output_path: Optional[str] = None) -> Tuple[str, Tuple[int, int]]:
        """
        Resize an image if it exceeds the maximum width while maintaining aspect ratio.
        
        Args:
            image_path: Path to the input image file
            output_path: Optional path for output (auto-generated if not provided)
        
        Returns:
            Tuple of (output_path, new_dimensions)
        
        Raises:
            FileNotFoundError: If input image doesn't exist
            ValueError: If image format is not supported
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")
        
        try:
            img = Image.open(image_path)
        except Exception as e:
            raise ValueError(f"Cannot open image {image_path}: {e}")
        
        original_size = img.size
        print(f"Original image size: {original_size[0]}x{original_size[1]} pixels")
        
        # Check if resizing is needed
        if img.size[0] > self.max_width:
            # Calculate scale factor to maintain aspect ratio
            scale_factor = self.max_width / img.size[0]
            
            # Calculate new dimensions
            new_width = self.max_width
            new_height = int(img.size[1] * scale_factor)
            
            print(f"Resizing image to {new_width}x{new_height} pixels (scale: {scale_factor:.2f})")
            
            # Resize the image with high-quality resampling
            img = img.resize((new_width, new_height), Image.LANCZOS)
        else:
            print(f"Image width ({img.size[0]}px) is within limit ({self.max_width}px), no resize needed")
        
        # Generate output path if not provided
        if output_path is None:
            base, ext = os.path.splitext(image_path)
            output_path = f"{base}_resized{ext}"
        
        # Save the image
        img.save(output_path, quality=self.output_quality, optimize=True)
        print(f"Saved resized image to: {output_path}")
        
        final_size = img.size
        img.close()
        
        return output_path, final_size
    
    def batch_resize(self, image_paths: List[str]) -> List[Tuple[str, Tuple[int, int]]]:
        """
        Resize multiple images.
        
        Args:
            image_paths: List of paths to image files
        
        Returns:
            List of tuples (output_path, dimensions) for each image
        """
        results = []
        for i, path in enumerate(image_paths, 1):
            print(f"\nProcessing image {i}/{len(image_paths)}: {path}")
            try:
                result = self.resize_image(path)
                results.append(result)
            except Exception as e:
                print(f"Error processing {path}: {e}")
                results.append((None, None))
        
        return results


class LayoutPlanner:
    """Plan document layouts using intelligent strategies."""
    
    def __init__(self):
        """Initialize the layout planner."""
        pass
    
    def plan_layout(self, text: str, table: Dict, images: List[str]) -> str:
        """
        Plan the layout for a PDF document.
        
        This is a simplified version. In a full implementation, this would
        use a language model (LLM) to make intelligent layout decisions.
        
        Args:
            text: Text content for the document
            table: Table data as a dictionary
            images: List of image paths
        
        Returns:
            Layout strategy as a formatted string
        """
        print("\nPlanning document layout...")
        
        # Simple rule-based layout planning
        layout = []
        layout.append("=== Document Layout Strategy ===\n")
        
        # Analyze content
        has_text = bool(text and text.strip())
        has_table = bool(table)
        has_images = bool(images)
        
        layout.append("Content Elements:")
        if has_text:
            layout.append(f"  - Text: {len(text)} characters")
        if has_table:
            layout.append(f"  - Table: {len(table.get('Rows', []))} rows")
        if has_images:
            layout.append(f"  - Images: {len(images)} image(s)")
        
        layout.append("\nRecommended Layout Order:")
        order = 1
        
        # Title and introduction text first
        if has_text:
            layout.append(f"{order}. Text content (top of page)")
            order += 1
        
        # Images in the middle
        if has_images:
            for i, img in enumerate(images, 1):
                layout.append(f"{order}. Image {i}: Center-aligned with caption")
                order += 1
        
        # Tables last
        if has_table:
            layout.append(f"{order}. Table: Full width, with borders")
            order += 1
        
        layout.append("\nSpacing Recommendations:")
        layout.append("  - Top margin: 1 inch")
        layout.append("  - Bottom margin: 1 inch")
        layout.append("  - Left/Right margins: 0.75 inches")
        layout.append("  - Space between elements: 0.25 inches")
        
        layout.append("\nPage Break Suggestions:")
        if has_images and len(images) > 2:
            layout.append("  - Consider page break after every 2 images")
        else:
            layout.append("  - Single page layout should suffice")
        
        strategy = "\n".join(layout)
        print(strategy)
        
        return strategy


class PDFGenerator:
    """Generate PDF documents (placeholder implementation)."""
    
    def __init__(self):
        """Initialize the PDF generator."""
        pass
    
    def generate(self, layout_strategy: str, content_data: Dict, output_path: str = "output.pdf") -> str:
        """
        Generate a PDF based on the layout strategy.
        
        This is a placeholder implementation. A full implementation would use
        libraries like ReportLab, WeasyPrint, or PyPDF2.
        
        Args:
            layout_strategy: Layout plan from LayoutPlanner
            content_data: Dictionary containing all content elements
            output_path: Path for the output PDF file
        
        Returns:
            Path to generated PDF file
        """
        print(f"\n{'='*60}")
        print("PDF Generation (Placeholder)")
        print(f"{'='*60}")
        print(f"Output file: {output_path}")
        print(f"\nLayout Strategy:\n{layout_strategy}")
        print(f"\nContent Summary:")
        print(f"  - Text: {len(content_data.get('text', ''))} characters")
        print(f"  - Images: {len(content_data.get('images', []))} image(s)")
        print(f"  - Table rows: {len(content_data.get('table', {}).get('Rows', []))}")
        
        print("\n[NOTE: Actual PDF generation would happen here]")
        print("[To implement: Install reportlab and add PDF creation logic]")
        
        # In a real implementation, you would:
        # 1. Create a canvas with reportlab
        # 2. Parse the layout strategy
        # 3. Add content elements in the recommended order
        # 4. Apply spacing and margins
        # 5. Handle page breaks
        # 6. Save the PDF
        
        # Example code (commented out):
        # from reportlab.pdfgen import canvas
        # from reportlab.lib.pagesizes import letter
        # 
        # c = canvas.Canvas(output_path, pagesize=letter)
        # width, height = letter
        # 
        # # Add text
        # c.drawString(100, height - 100, content_data['text'])
        # 
        # # Add images
        # for img_path in content_data['images']:
        #     c.drawImage(img_path, 100, 400, width=400, height=300)
        # 
        # c.save()
        
        return output_path


class DocumentProcessor:
    """Main workflow coordinator for document processing."""
    
    def __init__(self, max_image_width: int = 800):
        """
        Initialize the document processor.
        
        Args:
            max_image_width: Maximum width for images in pixels
        """
        self.image_processor = ImageProcessor(max_width=max_image_width)
        self.layout_planner = LayoutPlanner()
        self.pdf_generator = PDFGenerator()
    
    def process(self, document_data: Dict) -> Dict:
        """
        Process a complete document from input data to PDF.
        
        Args:
            document_data: Dictionary containing:
                - images: List of image paths (required)
                - text: Text content (optional)
                - table: Table data (optional)
                - output_path: PDF output path (optional)
        
        Returns:
            Dictionary with processing results
        """
        print(f"\n{'='*60}")
        print("Starting Document Processing Workflow")
        print(f"{'='*60}\n")
        
        # Extract data
        images = document_data.get('images', [])
        text = document_data.get('text', '')
        table = document_data.get('table', {})
        output_path = document_data.get('output_path', 'output.pdf')
        
        if not images:
            print("Warning: No images provided")
        
        # Step 1: Process Images
        print("STEP 1: Image Processing")
        print("-" * 60)
        resized_images = []
        
        for image_path in images:
            try:
                resized_path, dimensions = self.image_processor.resize_image(image_path)
                resized_images.append(resized_path)
            except Exception as e:
                print(f"Error processing image {image_path}: {e}")
        
        # Step 2: Plan Layout
        print(f"\n{'='*60}")
        print("STEP 2: Layout Planning")
        print("-" * 60)
        layout_strategy = self.layout_planner.plan_layout(text, table, resized_images)
        
        # Step 3: Generate PDF
        print(f"\n{'='*60}")
        print("STEP 3: PDF Generation")
        print("-" * 60)
        content_data = {
            'text': text,
            'table': table,
            'images': resized_images,
            'layout': layout_strategy
        }
        
        pdf_path = self.pdf_generator.generate(layout_strategy, content_data, output_path)
        
        # Return results
        result = {
            'original_images': images,
            'resized_images': resized_images,
            'layout_strategy': layout_strategy,
            'pdf_path': pdf_path,
            'success': True
        }
        
        print(f"\n{'='*60}")
        print("Workflow Complete!")
        print(f"{'='*60}")
        print(f"Resized images: {len(resized_images)}")
        print(f"PDF output: {pdf_path}")
        
        return result


def main():
    """Main entry point for the script."""
    print("LangChain PDF Image Resizer - Dynamic Image Resizing Workflow\n")
    
    # Example usage
    print("This script demonstrates dynamic image resizing for PDF generation.")
    print("Note: This is a demonstration. Actual PDF generation requires reportlab.\n")
    
    # Example document data
    document_data = {
        'images': [
            'example.jpg',  # Note: These files need to exist for real processing
            'sample.png'
        ],
        'text': '''
Welcome to Our Comprehensive PDF Guide!

This document demonstrates dynamic image resizing using LangChain orchestration.
The images in this document have been automatically resized to fit within 
optimal dimensions while maintaining their aspect ratios.

Key Features:
- Automatic image resizing
- Layout planning
- Professional formatting
- Modular architecture
        '''.strip(),
        'table': {
            'Header': ['Year', 'Revenue', 'Growth Rate', 'Market Share'],
            'Rows': [
                ['2024', '$1.0M', '15%', '5%'],
                ['2025', '$1.5M', '50%', '7%'],
                ['2026', '$2.2M', '47%', '10%']
            ]
        },
        'output_path': 'example_output.pdf'
    }
    
    # Check if example images exist
    missing_images = [img for img in document_data['images'] if not os.path.exists(img)]
    
    if missing_images:
        print("⚠️  Warning: Example images not found:")
        for img in missing_images:
            print(f"   - {img}")
        print("\nTo run this script with actual images:")
        print("1. Create or provide image files (e.g., example.jpg, sample.png)")
        print("2. Update the 'images' list in document_data")
        print("3. Run the script again\n")
        
        print("Proceeding with demonstration using placeholder data...\n")
        # Use empty list for demo
        document_data['images'] = []
    
    # Process the document
    processor = DocumentProcessor(max_image_width=800)
    
    try:
        result = processor.process(document_data)
        
        print("\n" + "="*60)
        print("RESULTS SUMMARY")
        print("="*60)
        print(f"Success: {result['success']}")
        print(f"Original images: {len(result['original_images'])}")
        print(f"Processed images: {len(result['resized_images'])}")
        print(f"PDF output path: {result['pdf_path']}")
        
        if result['resized_images']:
            print("\nResized images:")
            for img in result['resized_images']:
                print(f"  - {img}")
        
    except Exception as e:
        print(f"\n❌ Error during processing: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    print("\n✓ Script completed successfully!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
