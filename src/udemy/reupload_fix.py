import cloudinary.uploader
import os
from django.apps import apps

for model in apps.get_models():
    for obj in model.objects.all():
        for field in model._meta.fields:

            if field.get_internal_type() in ['FileField', 'ImageField']:
                file_field = getattr(obj, field.name)

                if file_field and str(file_field).startswith('media/'):
                    file_path = os.path.join('media', str(file_field).replace('media/', ''))

                    if os.path.exists(file_path):
                        print(f"Uploading: {file_path}")

                        try:
                            public_id = str(file_field).replace("media/", "").rsplit(".", 1)[0]

                            cloudinary.uploader.upload(
                                file_path,
                                resource_type="auto",
                                public_id=public_id,
                                overwrite=True
                            )

                            print(f"Uploaded as: {public_id}")

                        except Exception as e:
                            print(f"Error: {e}")