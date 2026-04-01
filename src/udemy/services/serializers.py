from rest_framework import serializers
from .models import ServiceCategory, Service

class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = ['id', 'title']

class ServiceSerializer(serializers.ModelSerializer):
    service_category = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Service
        fields = [
            'id', 'title', 'stat_1_percent', 'stat_1_text', 'brand_1',
            'stat_2_percent', 'stat_2_text', 'brand_2', 'image', 'service_category'
        ]
