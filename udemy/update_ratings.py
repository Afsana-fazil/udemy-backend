import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'udemy.settings')
django.setup()

from courses.models import Course

# Get all available rating images
rating_dir = os.path.join('media', 'courses', 'rating')
available_ratings = [f for f in os.listdir(rating_dir) if f.endswith('.png')]

# Update each course's rating image
for course in Course.objects.all():
    # Extract the rating point from the current rating image path
    try:
        rating_point = float(course.rating_point)
        # Choose appropriate rating image based on rating point
        if rating_point >= 4.5:
            new_rating = '4.5-star.png'
        else:
            new_rating = '4-star.png'
        
        # Update the rating image path
        course.rating = f'http://localhost:8000/media/courses/rating/{new_rating}'
        course.save()
        print(f"Updated rating for course {course.id}: {course.title}")
    except (ValueError, AttributeError) as e:
        print(f"Error updating course {course.id}: {e}")

print("Rating update complete!") 