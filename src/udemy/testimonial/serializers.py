from rest_framework import serializers
from .models import Testimonial, Story, Review
from courses.serializers import SubCategorySerializer
from utils.fields import CloudinaryURLField

class TestimonialSerializer(serializers.ModelSerializer):
    course = SubCategorySerializer(read_only=True)
    profile = CloudinaryURLField(resource_type="image")
    
    class Meta:
        model = Testimonial
        fields = ['id', 'name', 'content', 'course', 'profile']


class StorySerializer(serializers.ModelSerializer):
    image = CloudinaryURLField(resource_type="image")
    company_icon = CloudinaryURLField(resource_type="image")

    class Meta:
        model = Story
        fields = ['id', 'title', 'stat_1_percent', 'stat_1_text', 'stat_2_percent', 'stat_2_text', 'image', 'company_icon', 'created_at', 'description']


class ReviewSerializer(serializers.ModelSerializer):
    rating = CloudinaryURLField(resource_type="image")
    
    class Meta:
        model = Review
        fields = '__all__'