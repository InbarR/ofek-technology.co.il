import requests
from PIL import Image
from io import BytesIO
import os

def download_and_save_image(url, save_path, width, height):
    try:
        # Create images directory if it doesn't exist
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        # Download image
        response = requests.get(url)
        response.raise_for_status()
        
        # Open and process image
        img = Image.open(BytesIO(response.content))
        
        # Convert to RGB if image is in RGBA mode
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        
        # Calculate dimensions to maintain aspect ratio
        aspect_ratio = width / height
        original_ratio = img.width / img.height
        
        if original_ratio > aspect_ratio:
            # Image is wider than target ratio
            new_width = int(height * original_ratio)
            new_height = height
        else:
            # Image is taller than target ratio
            new_width = width
            new_height = int(width / original_ratio)
            
        # Resize image
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Center crop to target size
        left = (new_width - width) // 2
        top = (new_height - height) // 2
        right = left + width
        bottom = top + height
        img = img.crop((left, top, right, bottom))
        
        # Save image
        img.save(save_path, quality=95)
        print(f"Successfully saved {save_path}")
        
    except Exception as e:
        print(f"Error downloading {url}: {str(e)}")

# Download both images with specific dimensions
images = [
    {
        "url": "https://media.licdn.com/dms/image/v2/C5603AQH_g04AfCkm9A/profile-displayphoto-shrink_800_800/profile-displayphoto-shrink_800_800/0/1516457393706?e=1752105600&v=beta&t=i3Uc_BalDTzLcnHVbDS_nKhz_BEZJdlYWh25lLzMBc0",
        "save_path": "images/doron-rotem.jpg",
        "width": 200,
        "height": 200
    },
    {
        "url": "https://static.wixstatic.com/media/9db776_99a18cc5aa17468aa85146f6029db707~mv2.jpg/v1/fill/w_1321,h_1980,al_c,q_90/264A0812.jpg",
        "save_path": "images/oded-rotem.jpg",
        "width": 300,  # Wider to prevent face cutoff
        "height": 200
    }
]

for image in images:
    download_and_save_image(
        image["url"],
        image["save_path"],
        image["width"],
        image["height"]
    )
