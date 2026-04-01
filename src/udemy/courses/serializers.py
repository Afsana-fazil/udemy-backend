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


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'


class VideoProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoProgress
        fields = '__all__'


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


class CourseReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.first_name', read_only=True)
    
    class Meta:
        model = CourseReview
        fields = ['id', 'user', 'user_name', 'rating', 'comment', 'created_at']
        read_only_fields = ['user']


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
    image = serializers.ImageField(required=True)
    title = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    price = serializers.DecimalField(max_digits=8, decimal_places=0, required=True)
    created_by = serializers.CharField(required=True)
    video = serializers.FileField(required=False, allow_null=True)

    class Meta:
        model = Course
        fields = '__all__'
        # Add sub_category_name to the output
        extra_fields = ['sub_category_name']

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


class CoursePurchaseSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course.title', read_only=True)
    course_image = serializers.CharField(source='course.image', read_only=True)
    
    class Meta:
        model = CoursePurchase
        fields = ['id', 'course', 'course_title', 'course_image', 'purchased_at', 'amount_paid', 'payment_method']
        read_only_fields = ['user']


class CourseProgressSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course.title', read_only=True)
    course_image = serializers.CharField(source='course.image', read_only=True)
    
    class Meta:
        model = CourseProgress
        fields = ['id', 'course', 'course_title', 'course_image', 'progress_percentage', 'completed_videos', 'total_videos', 'last_accessed']
        read_only_fields = ['user']


class CartItemSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    course_id = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(), source='course', write_only=True
    )

    class Meta:
        model = CartItem
        fields = ['id', 'course', 'course_id', 'added_at']

class WishlistItemSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    course_id = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(), source='course', write_only=True
    )

    class Meta:
        model = WishlistItem
        fields = ['id', 'course', 'course_id', 'added_at']

def update_progress(self):
    total_videos = self.course.videos.count()
    completed_videos = VideoProgress.objects.filter(
        user=self.user,
        video__course=self.course,
        is_completed=True
    ).count()
    self.total_videos = total_videos
    self.completed_videos = completed_videos
    self.progress_percentage = (completed_videos / total_videos * 100) if total_videos > 0 else 0
    self.save()

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
        # Update course progress
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
        # Auto-complete if watched more than 90%
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