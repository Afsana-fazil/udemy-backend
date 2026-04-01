import cloudinary.api
from rest_framework import serializers

class CloudinaryURLField(serializers.Field):
    cache = None  # store mapping once

    def __init__(self, resource_type="image", *args, **kwargs):
        self.resource_type = resource_type
        super().__init__(*args, **kwargs)

    def load_cloudinary_map(self):
        if CloudinaryURLField.cache is not None:
            return CloudinaryURLField.cache

        resources = cloudinary.api.resources(type="upload", max_results=500)

        mapping = {}
        for res in resources["resources"]:
            public_id = res["public_id"]
            filename = public_id.split("/")[-1]

            mapping[filename] = public_id

        CloudinaryURLField.cache = mapping
        return mapping

    def to_representation(self, value):
        if not value:
            return None

        url = str(value)

        # already full URL
        if url.startswith("http"):
            return url

        cloud_name = "djptbf0iw"

        filename = url.split("/")[-1].split(".")[0]

        mapping = self.load_cloudinary_map()

        if filename in mapping:
            public_id = mapping[filename]
            return f"https://res.cloudinary.com/{cloud_name}/{self.resource_type}/upload/{public_id}"

        # fallback (if not found)
        return f"https://res.cloudinary.com/{cloud_name}/{self.resource_type}/upload/{url}"