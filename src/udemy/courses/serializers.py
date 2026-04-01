from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    MainCategory, 
    SubCategory, 
    Course, 
    CoursePurchase, 
    CourseReview, 
    CourseProgress,
    CartItem,
    WishlistItem,
    Video,
    VideoProgress
)
from content.serializers import SectionSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from datetime import timedelta
from django.shortcuts import get_object_or_404

# ✅ IMPORT THIS
from utils.fields import CloudinaryURLField


# ------------------ VIDEO ------------------

class VideoSerializer(serializers.ModelSerializer):
    video = CloudinaryURLField(resource_type="video")

    class Meta:
        model = Video
        fields = '__all__'


class VideoProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoProgress
        fields = '__all__'


# ------------------ CATEGORY ------------------

class MainCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MainCategory
        fields = '__all__'


class MainCategoryDetailSerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()
    
    class Meta:
        model = MainCategory
        fields = '__all__'
    
    def get_subcategories(self, obj):
        return SubCategorySerializer(obj.subcategories.all(), many=True).data


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'


# ------------------ REVIEWS ------------------

class CourseReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.first_name', read_only=True)
    
    class Meta:
        model = CourseReview
        fields = ['id', 'user', 'user_name', 'rating', 'comment', 'created_at']
        read_only_fields = ['user']


# ------------------ COURSE ------------------

class CourseSerializer(serializers.ModelSerializer):
    main_category = serializers.CharField(source='sub_category.main_category.name', read_only=True)
    sub_category_name = serializers.CharField(source='sub_category.name', read_only=True)
    average_rating = serializers.ReadOnlyField()
    total_reviews = serializers.ReadOnlyField()
    purchased = serializers.SerializerMethodField()
    progress = serializers.SerializerMethodField()

    videos = VideoSerializer(many=True, read_only=True)
    course_reviews = CourseReviewSerializer(many=True, read_only=True)

    sub_category = serializers.PrimaryKeyRelatedField(queryset=SubCategory.objects.all())

    # ✅ FIXED FIELDS
    image = CloudinaryURLField(resource_type="image")
    video = CloudinaryURLField(resource_type="video")

    title = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    price = serializers.DecimalField(max_digits=8, decimal_places=0, required=True)
    created_by = serializers.CharField(required=True)

    class Meta:
        model = Course
        fields = '__all__'

    def validate(self, data):
        errors = {}
        required_fields = ['title', 'description', 'price', 'sub_category', 'image', 'created_by']
        for field in required_fields:
            if not data.get(field):
                errors[field] = f"{field.replace('_', ' ').capitalize()} is required."
        if errors:
            raise serializers.ValidationError(errors)
        return data

    def get_purchased(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return CoursePurchase.objects.filter(user=request.user, course=obj, is_active=True).exists()
        return False
    
    def get_progress(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                progress = CourseProgress.objects.get(user=request.user, course=obj)
                return float(progress.progress_percentage)
            except CourseProgress.DoesNotExist:
                return 0
        return 0


# ------------------ PURCHASE ------------------

class CoursePurchaseSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course.title', read_only=True)

    # ✅ FIXED
    course_image = CloudinaryURLField(resource_type="image", source='course.image', read_only=True)
    
    class Meta:
        model = CoursePurchase
        fields = ['id', 'course', 'course_title', 'course_image', 'purchased_at', 'amount_paid', 'payment_method']
        read_only_fields = ['user']


# ------------------ PROGRESS ------------------

class CourseProgressSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course.title', read_only=True)

    # ✅ FIXED
    course_image = CloudinaryURLField(resource_type="image", source='course.image', read_only=True)
    
    class Meta:
        model = CourseProgress
        fields = ['id', 'course', 'course_title', 'course_image', 'progress_percentage', 'completed_videos', 'total_videos', 'last_accessed']
        read_only_fields = ['user']


# ------------------ CART ------------------

class CartItemSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    course_id = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(), source='course', write_only=True
    )

    class Meta:
        model = CartItem
        fields = ['id', 'course', 'course_id', 'added_at']


# ------------------ WISHLIST ------------------

class WishlistItemSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    course_id = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(), source='course', write_only=True
    )

    class Meta:
        model = WishlistItem
        fields = ['id', 'course', 'course_id', 'added_at']


# ------------------ VIDEO VIEWSET ------------------

class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        video = get_object_or_404(Video, pk=pk)
        progress, created = VideoProgress.objects.get_or_create(
            user=request.user,
            video=video,
            defaults={'is_completed': True}
        )
        if not created:
            progress.is_completed = True
            progress.save()

        course_progress, created = CourseProgress.objects.get_or_create(
            user=request.user,
            course=video.course,
            defaults={'progress_percentage': 0, 'completed_videos': 0, 'total_videos': video.course.videos.count()}
        )
        course_progress.update_progress()

        return Response({
            'message': 'Video marked as completed',
            'progress': float(course_progress.progress_percentage)
        })

    @action(detail=True, methods=['post'])
    def update_progress(self, request, pk=None):
        video = get_object_or_404(Video, pk=pk)
        current_time = request.data.get('current_time', 0)

        progress, created = VideoProgress.objects.get_or_create(
            user=request.user,
            video=video,
            defaults={'watched_duration': timedelta(seconds=current_time)}
        )

        if not created:
            progress.watched_duration = timedelta(seconds=current_time)
            progress.save()

        video_duration = video.duration.total_seconds() if video.duration else 0

        if video_duration and current_time / video_duration > 0.9 and not progress.is_completed:
            progress.is_completed = True
            progress.save()
            course_progress = CourseProgress.objects.get(user=request.user, course=video.course)
            course_progress.update_progress()

        return Response({
            'message': 'Progress updated',
            'watched_duration': current_time,
            'is_completed': progress.is_completed
        })


class VideoProgressViewSet(viewsets.ModelViewSet):
    queryset = VideoProgress.objects.all()
    serializer_class = VideoProgressSerializer
    permission_classes = [IsAuthenticated]