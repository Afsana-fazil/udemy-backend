from django.urls import path
from .views import (
    signup, 
    UserRegistrationView, 
    UserLoginView, 
    UserProfileView, 
    AvatarUploadView,
    logout,
    MyTokenObtainPairView
)

from rest_framework_simplejwt.views import (TokenRefreshView,)

urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', signup, name='signup'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', logout, name='logout'),
    path('profile/', UserProfileView.as_view(), name='profile'),
]
