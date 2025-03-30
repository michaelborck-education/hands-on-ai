# Image Gallery Creator

**Difficulty**: Intermediate  
**Time**: 45-60 minutes  
**Learning Focus**: File handling, HTML generation, metadata management, API integration  
**Module**: chat

## Overview

Create a tool that generates an HTML gallery from a collection of images. The tool manages image metadata, generates descriptions (optionally with AI assistance), and creates a responsive web gallery to showcase the images.

## Instructions

```python
import os
import json
from ailabkit.chat import get_response
from datetime import datetime

def create_image_gallery():
    """
    Creates an HTML image gallery from a collection of images.
    Students can add their own images to the 'gallery_images' folder.
    """
    
    print("=== Image Gallery Creator ===")
    
    # Create necessary directories
    image_dir = "gallery_images"
    output_dir = "gallery_output"
    os.makedirs(image_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    
    # Check if there are images to process
    image_files = [f for f in os.listdir(image_dir) 
                  if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]
    
    if not image_files:
        print(f"No images found in '{image_dir}' folder.")
        print(f"Please add some image files (JPG, PNG, GIF) to the '{image_dir}' folder.")
        return
    
    print(f"Found {len(image_files)} images.")
    
    # Load existing metadata or create new
    metadata_file = os.path.join(output_dir, "gallery_metadata.json")
    if os.path.exists(metadata_file):
        with open(metadata_file, 'r') as f:
            try:
                gallery_data = json.load(f)
            except json.JSONDecodeError:
                gallery_data = {"title": "My Image Gallery", "images": []}
    else:
        gallery_data = {"title": "My Image Gallery", "images": []}
    
    # Update gallery title
    gallery_title = input(f"Gallery title [{gallery_data['title']}]: ")
    if gallery_title:
        gallery_data["title"] = gallery_title
    
    # Process each image
    existing_images = {img["filename"]: img for img in gallery_data["images"]}
    
    for image_file in image_files:
        if image_file in existing_images:
            # Image already has metadata
            print(f"\nImage {image_file} already has metadata:")
            print(f"Title: {existing_images[image_file]['title']}")
            print(f"Description: {existing_images[image_file]['description']}")
            
            update = input("Update this image's information? (y/n): ").lower() == 'y'
            if not update:
                continue
        
        print(f"\nProcessing: {image_file}")
        
        # Get metadata for this image
        default_title = os.path.splitext(image_file)[0].replace('_', ' ').title()
        title = input(f"Image title [{default_title}]: ") or default_title
        
        description = input("Image description: ")
        
        # Optionally generate description using AI
        if not description:
            generate_ai = input("Generate description with AI? (y/n): ").lower() == 'y'
            if generate_ai:
                try:
                    prompt = f"Generate a brief, interesting description for an image named '{image_file}'. Create something imaginative based on the filename, without stating that you're guessing or that you haven't seen the image."
                    description = get_response(prompt)
                    print(f"AI-generated description: {description}")
                    use_desc = input("Use this description? (y/n): ").lower() == 'y'
                    if not use_desc:
                        description = input("Enter alternative description: ")
                except Exception as e:
                    print(f"Error generating AI description: {e}")
                    description = input("Enter description manually: ")
        
        # Add or update metadata
        image_data = {
            "filename": image_file,
            "title": title,
            "description": description,
            "date_added": datetime.now().strftime("%Y-%m-%d")
        }
        
        if image_file in existing_images:
            # Update existing entry
            for i, img in enumerate(gallery_data["images"]):
                if img["filename"] == image_file:
                    gallery_data["images"][i] = image_data
                    break
        else:
            # Add new entry
            gallery_data["images"].append(image_data)
    
    # Save updated metadata
    with open(metadata_file, 'w') as f:
        json.dump(gallery_data, f, indent=2)
    
    print("\nGenerating HTML gallery...")
    
    # Generate HTML gallery
    html_output = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{gallery_data['title']}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        h1 {{
            text-align: center;
            color: #333;
        }}
        .gallery {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            grid-gap: 20px;
            max-width: 1200px;
            margin: 0 auto;
        }}
        .gallery-item {{
            border-radius: 5px;
            overflow: hidden;
            box-shadow: 0 3px 6px rgba(0, 0, 0, 0.16);
            background-color: white;
            transition: transform 0.3s;
        }}
        .gallery-item:hover {{
            transform: translateY(-5px);
        }}
        .gallery-image {{
            width: 100%;
            height: 200px;
            object-fit: cover;
        }}
        .gallery-content {{
            padding: 15px;
        }}
        .gallery-title {{
            margin-top: 0;
            color: #333;
        }}
        .gallery-description {{
            color: #666;
            font-size: 0.9em;
        }}
        .gallery-date {{
            color: #999;
            font-size: 0.8em;
            text-align: right;
            margin-top: 10px;
        }}
        footer {{
            text-align: center;
            margin-top: 30px;
            color: #999;
            font-size: 0.8em;
        }}
    </style>
</head>
<body>
    <h1>{gallery_data['title']}</h1>
    
    <div class="gallery">
"""
    
    # Add each image to the gallery
    for img in gallery_data["images"]:
        html_output += f"""        <div class="gallery-item">
            <img src="../{image_dir}/{img['filename']}" alt="{img['title']}" class="gallery-image">
            <div class="gallery-content">
                <h3 class="gallery-title">{img['title']}</h3>
                <p class="gallery-description">{img['description']}</p>
                <p class="gallery-date">Added: {img['date_added']}</p>
            </div>
        </div>
"""
    
    # Complete the HTML
    html_output += """    </div>
    
    <footer>
        <p>Created with Image Gallery Creator</p>
    </footer>
</body>
</html>
"""
    
    # Save the HTML file
    html_file = os.path.join(output_dir, "index.html")
    with open(html_file, 'w') as f:
        f.write(html_output)
    
    print(f"\nGallery created successfully!")
    print(f"HTML file saved to: {html_file}")
    print(f"Open this file in a web browser to view your gallery.")
    
    # Optional: Open the gallery in the default browser
    try_open = input("\nOpen gallery in browser? (y/n): ").lower() == 'y'
    if try_open:
        try:
            import webbrowser
            webbrowser.open('file://' + os.path.abspath(html_file))
        except Exception as e:
            print(f"Could not open browser: {e}")

# Run the gallery creator
if __name__ == "__main__":
    create_image_gallery()
```

## Extension Ideas

- Add image filtering by tags or categories
- Implement image resising and thumbnail generation
- Create a lightbox effect for viewing full-sise images
- Add EXIF data extraction to display camera information
- Implement a theme selector with different gallery styles
- Create a server-side component to host the gallery online

---