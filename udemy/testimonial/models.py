from django.db import models
from courses.models import SubCategory

class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    content = models.TextField()
    course = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='testimonials')
    profile = models.ImageField(upload_to="testimonial/")
    
    def __str__(self):
        return f"{self.name}'s testimonial for {self.course.name}"
    

class Story(models.Model):
    title = models.CharField(max_length=255)
    stat_1_percent = models.CharField(max_length=25)
    stat_1_text = models.CharField(max_length=255)
    stat_2_percent = models.CharField(max_length=25)
    stat_2_text = models.CharField(max_length=255)
    image = models.ImageField(upload_to="story/")
    description = models.TextField()
    company_icon = models.ImageField(upload_to="story/icons/")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Stories"

    def __str__(self):
        return self.title


class Review(models.Model):
    name = models.CharField(max_length=100)
    initials = models.CharField(max_length=2) 
    rating = models.ImageField(upload_to="reviews/")
    time_ago = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255) 

    def __str__(self):
        return f"{self.name}"
    



