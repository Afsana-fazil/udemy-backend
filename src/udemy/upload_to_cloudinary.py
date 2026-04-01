import cloudinary
import cloudinary.uploader
import os

# 🔐 Your Cloudinary config
cloudinary.config(
    cloud_name="djptbf0iw",
    api_key="531437327887678",
    api_secret="ansmFJ8NmKgyRKip8AKRjLUlRn8"
)

# 📁 Your media folder path
MEDIA_ROOT = "media"   # change if needed

def upload_folder(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)

            # Keep folder structure in Cloudinary
            relative_path = os.path.relpath(root, folder_path)

            print(f"Uploading: {file_path}")

            try:
                cloudinary.uploader.upload(
                    file_path,
                    folder=relative_path,
                    resource_type="auto"
                )
            except Exception as e:
                print(f"Error uploading {file_path}: {e}")

upload_folder(MEDIA_ROOT)