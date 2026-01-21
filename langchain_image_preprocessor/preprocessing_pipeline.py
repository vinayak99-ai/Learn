#!/usr/bin/env python3
"""
LangChain Image Preprocessing Pipeline for PDF Generation

This script preprocesses JSON files containing image links, text, and tables
to optimize images for PDF generation. It downloads images, resizes them,
and updates the JSON with optimized dimensions and placement details.

Author: Learn Repository Contributors
Date: 2026-01-21
"""

import os
import json
import requests
from io import BytesIO
from typing import Dict, List, Tuple, Optional
from PIL import Image


class ImagePreprocessor:
    """Handle image downloading and resizing operations."""
    
    def __init__(self, max_width: int = 600, output_quality: int = 95, save_dir: str = "processed_images"):
        """
        Initialize the image preprocessor.
        
        Args:
            max_width: Maximum width for resized images in pixels
            output_quality: JPEG quality for output (1-100)
            save_dir: Directory to save processed images
        """
        self.max_width = max_width
        self.output_quality = output_quality
        self.save_dir = save_dir
        
        # Create output directory if it doesn't exist
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
    
    def resize_image(self, url: str, save_dir: str) -> Tuple[str, List[int]]:
        """
        Download and resize an image from a URL or local file path.
        
        Args:
            url: URL or local file path of the image
            save_dir: Directory to save the resized image
        
        Returns:
            Tuple of (save_path, dimensions) where dimensions is [width, height]
        
        Raises:
            requests.RequestException: If image download fails
            ValueError: If image format is not supported
        """
        try:
            # Check if it's a local file or URL
            is_url = url.startswith(('http://', 'https://'))
            
            if is_url:
                # Download the image from URL
                print(f"Downloading image from: {url}")
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
                response = requests.get(url, timeout=10, headers=headers)
                response.raise_for_status()
                img = Image.open(BytesIO(response.content))
            else:
                # Handle local file
                print(f"Loading local image: {url}")
                if not os.path.exists(url):
                    raise FileNotFoundError(f"Local image file not found: {url}")
                img = Image.open(url)
            
            original_size = img.size
            print(f"  Original size: {original_size[0]}x{original_size[1]} pixels")
            
            # Resize if needed
            if img.size[0] > self.max_width:
                ratio = self.max_width / float(img.size[0])
                new_height = int(img.size[1] * ratio)
                img = img.resize((self.max_width, new_height), Image.LANCZOS)
                print(f"  Resized to: {self.max_width}x{new_height} pixels (ratio: {ratio:.2f})")
            else:
                print(f"  No resize needed (width <= {self.max_width}px)")
            
            # Create save directory if it doesn't exist
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
            
            # Generate filename from URL or path
            filename = url.split("/")[-1]
            if not filename or '.' not in filename:
                # Use hashlib for consistent unique filenames
                import hashlib
                url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
                filename = f"image_{url_hash}.jpg"
            
            save_path = os.path.join(save_dir, filename)
            
            # Convert to RGB if necessary (for PNG with transparency, etc.)
            if img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Save the image with explicit format
            img.save(save_path, format='JPEG', quality=self.output_quality)
            print(f"  Saved to: {save_path}")
            
            final_size = img.size
            img.close()
            
            return save_path, [final_size[0], final_size[1]]
            
        except requests.RequestException as e:
            print(f"  Error downloading image: {e}")
            raise
        except FileNotFoundError as e:
            print(f"  Error: {e}")
            raise
        except Exception as e:
            print(f"  Error processing image: {e}")
            raise


class LayoutPlanner:
    """Plan document layouts for optimal PDF generation."""
    
    def __init__(self):
        """Initialize the layout planner."""
        pass
    
    def plan_layout(self, content_data: Dict) -> Dict:
        """
        Plan the layout for PDF generation based on content.
        
        This is a rule-based implementation. In a full LangChain implementation,
        this would use an LLM to make intelligent layout decisions.
        
        Args:
            content_data: Dictionary containing document content
        
        Returns:
            Dictionary with layout planning details
        """
        print("\nPlanning document layout...")
        
        images = content_data.get('images', [])
        content = content_data.get('content', [])
        
        # Analyze content
        has_text = any(item.get('type') == 'text' for item in content)
        has_table = any(item.get('type') == 'table' for item in content)
        has_images = len(images) > 0
        
        # Create layout plan
        layout = {
            'image_alignment': 'center',
            'page_breaks': []
        }
        
        # Add page break suggestions for multiple images
        if len(images) > 2:
            # Suggest page breaks after every 2 images
            for i in range(2, len(images), 2):
                layout['page_breaks'].append(f"after_image_{i}")
        
        print(f"  Layout plan created:")
        print(f"    - Image alignment: {layout['image_alignment']}")
        print(f"    - Page breaks: {layout['page_breaks'] if layout['page_breaks'] else 'None'}")
        
        return layout


class PreprocessingPipeline:
    """Main preprocessing pipeline coordinator."""
    
    def __init__(self, max_image_width: int = 600, output_dir: str = "processed_images"):
        """
        Initialize the preprocessing pipeline.
        
        Args:
            max_image_width: Maximum width for images in pixels
            output_dir: Directory to save processed images
        """
        self.image_preprocessor = ImagePreprocessor(max_width=max_image_width, save_dir=output_dir)
        self.layout_planner = LayoutPlanner()
        self.output_dir = output_dir
    
    def process(self, input_json_path: str, output_json_path: str) -> Dict:
        """
        Process a JSON file containing document data.
        
        Args:
            input_json_path: Path to input JSON file
            output_json_path: Path to save optimized output JSON
        
        Returns:
            Dictionary with processing results
        """
        print(f"\n{'='*60}")
        print("Starting Image Preprocessing Pipeline")
        print(f"{'='*60}\n")
        
        # Load input JSON
        print(f"Loading input from: {input_json_path}")
        with open(input_json_path, 'r') as f:
            data = json.load(f)
        
        print(f"  Title: {data.get('title', 'N/A')}")
        print(f"  Images: {len(data.get('images', []))}")
        print(f"  Content items: {len(data.get('content', []))}")
        
        # Process images
        print(f"\n{'='*60}")
        print("STEP 1: Image Processing")
        print(f"{'='*60}")
        
        processed_images = []
        for i, image_info in enumerate(data.get('images', []), 1):
            print(f"\nProcessing image {i}/{len(data.get('images', []))}:")
            url = image_info.get('url')
            alt_text = image_info.get('alt_text', '')
            
            try:
                save_path, dimensions = self.image_preprocessor.resize_image(url, self.output_dir)
                processed_images.append({
                    'url': save_path,
                    'alt_text': alt_text,
                    'dimensions': dimensions
                })
            except Exception as e:
                print(f"  Failed to process image: {e}")
                # Keep original image info if processing fails
                processed_images.append({
                    'url': url,
                    'alt_text': alt_text,
                    'dimensions': None,
                    'error': str(e)
                })
        
        # Plan layout
        print(f"\n{'='*60}")
        print("STEP 2: Layout Planning")
        print(f"{'='*60}")
        
        layout = self.layout_planner.plan_layout({
            'images': processed_images,
            'content': data.get('content', [])
        })
        
        # Create output JSON
        output_data = {
            'title': data.get('title', ''),
            'images': processed_images,
            'content': data.get('content', []),
            'layout': layout
        }
        
        # Save output JSON
        print(f"\n{'='*60}")
        print("STEP 3: Saving Output")
        print(f"{'='*60}")
        
        print(f"Writing output to: {output_json_path}")
        with open(output_json_path, 'w') as f:
            json.dump(output_data, f, indent=4)
        
        print(f"\n{'='*60}")
        print("Pipeline Complete!")
        print(f"{'='*60}")
        print(f"Processed images: {len([img for img in processed_images if img.get('dimensions')])}")
        print(f"Failed images: {len([img for img in processed_images if img.get('error')])}")
        print(f"Output file: {output_json_path}")
        
        return {
            'success': True,
            'processed_images': len([img for img in processed_images if img.get('dimensions')]),
            'failed_images': len([img for img in processed_images if img.get('error')]),
            'output_path': output_json_path
        }


def main():
    """Main entry point for the script."""
    print("LangChain Image Preprocessing Pipeline\n")
    
    # Get script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define file paths
    input_json = os.path.join(script_dir, "sample_input.json")
    output_json = os.path.join(script_dir, "optimized_output.json")
    output_dir = os.path.join(script_dir, "processed_images")
    
    # Check if input file exists
    if not os.path.exists(input_json):
        print(f"Error: Input file not found: {input_json}")
        print("Please create a sample_input.json file with the required structure.")
        return 1
    
    # Create and run the pipeline
    pipeline = PreprocessingPipeline(max_image_width=600, output_dir=output_dir)
    
    try:
        result = pipeline.process(input_json, output_json)
        
        print("\n" + "="*60)
        print("RESULTS SUMMARY")
        print("="*60)
        print(f"Success: {result['success']}")
        print(f"Processed images: {result['processed_images']}")
        print(f"Failed images: {result['failed_images']}")
        print(f"Output file: {result['output_path']}")
        
        print("\n✓ Pipeline completed successfully!")
        return 0
        
    except Exception as e:
        print(f"\n❌ Error during processing: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
