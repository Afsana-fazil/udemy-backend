from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MainCategoryViewSet,
    SubCategoryViewSet,
    CourseViewSet,
    CoursePurchaseViewSet,
    CourseProgressViewSet,
    CartItemViewSet,
    WishlistItemViewSet,
    VideoViewSet,
    VideoProgressViewSet
)

router = DefaultRouter()
router.register(r'main-categories', MainCategoryViewSet)
router.register(r'subcategories', SubCategoryViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'purchases', CoursePurchaseViewSet, basename='purchase')
router.register(r'progress', CourseProgressViewSet, basename='progress')
router.register(r'cart', CartItemViewSet, basename='cart')
router.register(r'wishlist', WishlistItemViewSet, basename='wishlist')
router.register(r'videos', VideoViewSet)
router.register(r'video-progress', VideoProgressViewSet)


urlpatterns = [
    path('', include(router.urls)),
    # Additional endpoints
    path('my-courses/', CoursePurchaseViewSet.as_view({'get': 'list'}), name='my-courses'),
    path('dashboard/', CourseProgressViewSet.as_view({'get': 'dashboard'}), name='dashboard'),
]
