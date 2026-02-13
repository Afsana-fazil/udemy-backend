from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import DemoSubmission
from rest_framework import serializers
from django.views.decorators.csrf import csrf_exempt


class DemoSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemoSubmission
        fields = '__all__'

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def submit_demo(request):
    serializer = DemoSubmissionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'success': True, 'message': 'Demo submitted successfully!'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
