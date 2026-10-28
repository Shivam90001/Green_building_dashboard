import os
import shutil
from PIL import Image

# Path to generated image
src_img_path = r"C:\Users\abc\.gemini\antigravity\brain\019013a7-f503-420a-8104-5c86fb67e5c1\dashboard_icon_1785825237642.jpg"
dest_folder = os.path.dirname(os.path.abspath(__file__))
dest_jpg = os.path.join(dest_folder, "icon.jpg")
dest_ico = os.path.join(dest_folder, "icon.ico")

print(f"Copying {src_img_path} to {dest_jpg}...")
shutil.copy(src_img_path, dest_jpg)

print("Converting icon.jpg to multi-size icon.ico using Pillow...")
try:
    img = Image.open(dest_jpg)
    # Convert and save as ICO with standard sizes
    img.save(dest_ico, format="ICO", sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)])
    print("icon.ico created successfully!")
except Exception as e:
    print(f"Error during conversion: {str(e)}")
