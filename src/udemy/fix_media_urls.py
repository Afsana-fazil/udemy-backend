import cloudinary.uploader
import os
from django.apps import apps

# loop through all models
for model in apps.get_models():
    for obj in model.objects.all():
        for field in model._meta.fields:
            
            # check if it's a file/image field
            if field.get_internal_type() in ['FileField', 'ImageField']:
                file_field = getattr(obj, field.name)

                if file_field and str(file_field).startswith('media/'):
                    file_path = os.path.join('media', str(file_field).replace('media/', ''))

                    if os.path.exists(file_path):
                        print(f"Uploading: {file_path}")

                        try:
                            response = cloudinary.uploader.upload(
                                file_path,
                                resource_type="auto"
                            )

                            # update DB with Cloudinary URL
                            setattr(obj, field.name, response['secure_url'])
                            obj.save()

                            print(f"Updated: {response['secure_url']}")

                        except Exception as e:
                            print(f"Error: {e}")