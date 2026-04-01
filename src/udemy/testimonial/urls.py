from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TestimonialViewSet, StoryViewSet, ReviewListAPIView

router = DefaultRouter()
router.register(r'testimonials', TestimonialViewSet)
router.register(r'stories', StoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('reviews/', ReviewListAPIView.as_view(), name='review-list'),
]