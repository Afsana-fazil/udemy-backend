from django.urls import path
from .views import submit_demo

urlpatterns = [
    path('submit/', submit_demo, name='submit_demo'),
] 