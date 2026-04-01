from rest_framework import serializers

CLOUD_NAME = "djptbf0iw"

class CloudinaryURLField(serializers.Field):

    def __init__(self, resource_type="image", *args, **kwargs):
        self.resource_type = resource_type
        super().__init__(*args, **kwargs)

    def to_representation(self, value):
    if not value:
        return None

    url = str(value)

    if url.startswith("http"):
        return url

    public_id = url.rsplit(".", 1)[0]
    
    public_id = public_id.replace(".5-star", "5-star")

    return f"https://res.cloudinary.com/{CLOUD_NAME}/{self.resource_type}/upload/{public_id}"