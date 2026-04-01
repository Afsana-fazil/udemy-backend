import cloudinary
import cloudinary.uploader
import os

# 🔐 Your Cloudinary config
cloudinary.config(
    cloud_name="djptbf0iw",
    api_key="531437327887678",
    api_secret="ansmFJ8NmKgyRKip8AKRjLUlRn8"
)


MEDIA_ROOT = "media"

for root, dirs, files in os.walk(MEDIA_ROOT):
    for file in files:
        file_path = os.path.join(root, file)
        
        # This creates public_id like: courses/course1  (no extension)
        relative = os.path.relpath(file_path, MEDIA_ROOT)
        public_id = os.path.splitext(relative)[0].replace("\\", "/")
        
        print(f"Uploading: {file_path} → {public_id}")
        
        try:
            cloudinary.uploader.upload(
                file_path,
                public_id=public_id,
                overwrite=True,
                resource_type="auto"
            )
            print(f"✅ Done: {public_id}")
        except Exception as e:
            print(f"❌ Error: {e}")

print("✅ All uploads complete!")