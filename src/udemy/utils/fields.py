from rest_framework import serializers

CLOUD_NAME = "djptbf0iw"

try:
    from .cloudinary_map import CLOUDINARY_MAP
except ImportError:
    CLOUDINARY_MAP = {}


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

        filename = url.split("/")[-1].split(".")[0]

        if filename in CLOUDINARY_MAP:
            public_id = CLOUDINARY_MAP[filename]
            return f"https://res.cloudinary.com/{CLOUD_NAME}/{self.resource_type}/upload/{public_id}"
        return f"https://res.cloudinary.com/{CLOUD_NAME}/{self.resource_type}/upload/{url}"