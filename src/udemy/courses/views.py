from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, Avg, Count
from django.utils import timezone
from datetime import timedelta
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
from .serializers import (
    MainCategoryDetailSerializer,
    SubCategorySerializer,
    CourseSerializer,
    CoursePurchaseSerializer,
    CourseReviewSerializer,
    CourseProgressSerializer,
    CartItemSerializer,
    WishlistItemSerializer,
    VideoSerializer,
    VideoProgressSerializer
)

class MainCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MainCategory.objects.prefetch_related('subcategories')
    serializer_class = MainCategoryDetailSerializer

class SubCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_queryset(self):
        queryset = self.queryset
        main_category = self.request.query_params.get('main_category')
        sub_slug = self.request.query_params.get('subcategory')
        created_by = self.request.query_params.get('created_by')
        limit = self.request.query_params.get('limit')
        search = self.request.query_params.get('search')
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        min_rating = self.request.query_params.get('min_rating')
        sort_by = self.request.query_params.get('sort_by', 'newest')

        if main_category:
            queryset = queryset.filter(sub_category__main_category_id=main_category)

        if sub_slug:
            queryset = queryset.filter(sub_category__slug=sub_slug)

        if created_by:
            queryset = queryset.filter(created_by__icontains=created_by)

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(created_by__icontains=search)
            )

        if min_price:
            queryset = queryset.filter(price__gte=min_price)

        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        if min_rating:
            queryset = queryset.filter(rating_point__gte=min_rating)

        # Sorting
        if sort_by == 'price-low':
            queryset = queryset.order_by('price')
        elif sort_by == 'price-high':
            queryset = queryset.order_by('-price')
        elif sort_by == 'rating':
            queryset = queryset.order_by('-rating_point')
        elif sort_by == 'newest':
            queryset = queryset.order_by('-created_at')
        else:
            queryset = queryset.order_by('-created_at')

        if limit:
            try:
                queryset = queryset[:int(limit)]
            except ValueError:
                pass

        return queryset

    def retrieve(self, request, *args, **kwargs):
        try:
            course_id = kwargs.get('pk')
            instance = get_object_or_404(Course, id=course_id)
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': f'Error retrieving course: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['get', 'post'], permission_classes=[IsAuthenticated])
    def reviews(self, request, pk=None):
        """Get or create course reviews"""
        course = get_object_or_404(Course, pk=pk)
        
        if request.method == 'GET':
            reviews = course.course_reviews.all().order_by('-created_at')
            serializer = CourseReviewSerializer(reviews, many=True)
            return Response(serializer.data)
        
        elif request.method == 'POST':
            # Check if user has already reviewed
            if CourseReview.objects.filter(user=request.user, course=course).exists():
                return Response(
                    {'error': 'You have already reviewed this course'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            serializer = CourseReviewSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user, course=course)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def purchase(self, request, pk=None):
        course = get_object_or_404(Course, pk=pk)
        user = request.user

        # Check if already purchased
        if CoursePurchase.objects.filter(user=user, course=course).exists():
            return Response({'error': 'You have already purchased this course.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create purchase
        purchase = CoursePurchase.objects.create(
            user=user,
            course=course,
            amount_paid=course.price,
            payment_method=request.data.get('payment_method', 'online'),
            transaction_id=request.data.get('transaction_id', '')
        )
        return Response({'success': True, 'purchase_id': purchase.id}, status=status.HTTP_201_CREATED)


class CoursePurchaseViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CoursePurchaseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CoursePurchase.objects.filter(user=self.request.user, is_active=True)

class CourseProgressViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CourseProgressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CourseProgress.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        """Get user's learning dashboard data"""
        progress_list = self.get_queryset()
        
        total_courses = progress_list.count()
        total_progress = sum(p.progress_percentage for p in progress_list)
        average_progress = total_progress / total_courses if total_courses > 0 else 0
        completed_courses = progress_list.filter(progress_percentage=100).count()
        
        return Response({
            'total_courses': total_courses,
            'average_progress': float(average_progress),
            'completed_courses': completed_courses,
            'courses': CourseProgressSerializer(progress_list, many=True).data
        })


class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class WishlistItemViewSet(viewsets.ModelViewSet):
    serializer_class = WishlistItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WishlistItem.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

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