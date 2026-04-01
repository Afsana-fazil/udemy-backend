from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import UserProfile
from .serializers import (
    UserSerializer, 
    UserProfileSerializer, 
    UserRegistrationSerializer,
    AvatarUploadSerializer,
    MyTokenObtainPairSerializer
)

class UserRegistrationView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Use custom serializer to get token with full_name
            token = MyTokenObtainPairSerializer.get_token(user)
            access_token = str(token.access_token)
            refresh_token = str(token)
            return Response({
                'status': 'success',
                'message': 'User registered successfully',
                'data': {
                    'user': UserSerializer(user).data,
                    'token': access_token,
                    'refresh': refresh_token
                }
            }, status=status.HTTP_201_CREATED)
        return Response({
            'status': 'error',
            'message': 'Registration failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response({
                'status': 'error',
                'message': 'Username and password are required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(username=username, password=password)
        
        if user:
            # Use your custom serializer to get the token with full_name
            serializer = MyTokenObtainPairSerializer(data={
                'username': username,
                'password': password
            })
            if serializer.is_valid():
                return Response({
                    'status': 'success',
                    'message': 'Login successful',
                    'data': {
                        'user': UserSerializer(user).data,
                        'token': serializer.validated_data['access'],
                        'refresh': serializer.validated_data['refresh']
                    }
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'status': 'error',
                    'message': 'Invalid credentials'
                }, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({
                'status': 'error',
                'message': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        profile = get_object_or_404(UserProfile, user=request.user)
        serializer = UserProfileSerializer(profile)
        return Response({
            'status': 'success',
            'data': serializer.data
        })
    
    def put(self, request):
        profile = get_object_or_404(UserProfile, user=request.user)
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'success',
                'message': 'Profile updated successfully',
                'data': serializer.data
            })
        return Response({
            'status': 'error',
            'message': 'Update failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class AvatarUploadView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        profile = get_object_or_404(UserProfile, user=request.user)
        serializer = AvatarUploadSerializer(profile, data=request.data, partial=True)
        
        if serializer.is_valid():
            # Delete old avatar if exists
            if profile.avatar:
                profile.avatar.delete(save=False)
            
            serializer.save()
            return Response({
                'status': 'success',
                'message': 'Avatar uploaded successfully',
                'data': {
                    'avatar': request.build_absolute_uri(profile.avatar.url) if profile.avatar else None
                }
            })
        return Response({
            'status': 'error',
            'message': 'Upload failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        refresh_token = request.data.get('refresh_token')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        return Response({
            'status': 'success',
            'message': 'Logout successful'
        })
    except Exception as e:
        return Response({
            'status': 'error',
            'message': 'Logout failed'
        }, status=status.HTTP_400_BAD_REQUEST)

# Keep the old signup view for backward compatibility
@api_view(['POST'])
def signup(request):
    email = request.data.get('email')
    password = request.data.get('password')
    first_name = request.data.get('first_name')
    
    if email and password and first_name:
        if not User.objects.filter(username=email).exists():
            user = User.objects.create_user(
                username=email, 
                password=password,
                first_name=first_name,
                email=email
            )
            refresh = RefreshToken.for_user(user)
            return Response({
                'status': 200,
                'message': 'User created successfully',
                'data': {
                    'user': UserSerializer(user).data,
                    'token': str(refresh.access_token),
                    'refresh': str(refresh)
                }
            })
        else:
            return Response({
                'status': 6001,
                'message': 'User already exists'
            }, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({
            'status': 6001,
            'message': 'All fields are required'
        }, status=status.HTTP_400_BAD_REQUEST)
    


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
