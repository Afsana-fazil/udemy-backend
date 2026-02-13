from rest_framework import serializers
from .models import Section, Lecture

class LectureSerializer(serializers.ModelSerializer):
    duration = serializers.SerializerMethodField()
    
    class Meta:
        model = Lecture
        fields = ['id', 'title', 'duration', 'is_preview']
    
    def get_duration(self, obj):
        """Convert duration to string format expected by frontend"""
        if obj.duration:
            total_seconds = int(obj.duration.total_seconds())
            minutes = total_seconds // 60
            return str(minutes)
        return "0"

class SectionSerializer(serializers.ModelSerializer):
    lectures = LectureSerializer(many=True, read_only=True)
    total_lectures = serializers.IntegerField(read_only=True)
    total_duration = serializers.SerializerMethodField()

    class Meta:
        model = Section
        fields = ['id', 'title', 'lectures', 'total_lectures', 'total_duration']
    
    def get_total_duration(self, obj):
        """Convert total duration to HH:MM:SS format"""
        if hasattr(obj, 'total_duration') and obj.total_duration:
            total_seconds = int(obj.total_duration.total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        return "00:00:00"
    
    def to_representation(self, instance):
        """Add error handling for section serialization"""
        try:
            data = super().to_representation(instance)
            # Ensure lectures is always an array
            if 'lectures' not in data or data['lectures'] is None:
                data['lectures'] = []
            return data
        except Exception as e:
            print(f"Error serializing section {instance.id}: {str(e)}")
            # Return basic section data if serialization fails
            return {
                'id': instance.id,
                'title': instance.title,
                'lectures': [],
                'total_lectures': 0,
                'total_duration': "00:00:00"
            }
