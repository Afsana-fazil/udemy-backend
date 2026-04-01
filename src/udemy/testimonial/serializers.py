from rest_framework import serializers
from .models import Testimonial, Story, Review
from courses.serializers import SubCategorySerializer

class TestimonialSerializer(serializers.ModelSerializer):
    course = SubCategorySerializer(read_only=True)
    
    class Meta:
        model = Testimonial
        fields = ['id', 'name', 'content', 'course', 'profile']


class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = ['id', 'title', 'stat_1_percent', 'stat_1_text', 'stat_2_percent', 'stat_2_text', 'image', 'company_icon', 'created_at', 'description']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'