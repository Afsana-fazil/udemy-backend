from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class MainCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "Main categories"

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    main_category = models.ForeignKey(MainCategory, on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    learners_count = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Sub categories"

    def __str__(self):
        return f"{self.main_category.name} → {self.name}"


class Course(models.Model):
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='courses')
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=0)
    rating = models.ImageField(upload_to="courses/rating/", blank=True, null=True)
    rating_point = models.CharField(max_length=25, blank=True, null=True, help_text="Course rating points")
    reviews = models.CharField(
        max_length=25, blank=True, null=True, verbose_name="Course reviews"
    )
    video = models.FileField(upload_to='videos/', blank=True, null=True)
    image = models.ImageField(upload_to='courses/')
    premium = models.BooleanField(default=False)
    best_seller = models.BooleanField(default=False)
    created_by = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @property
    def main_category(self):
        return self.sub_category.main_category.name

    @property
    def average_rating(self):
        reviews = self.course_reviews.all()
        if reviews:
            return sum(review.rating for review in reviews) / len(reviews)
        return 0

    @property
    def total_reviews(self):
        return self.course_reviews.count()


class CoursePurchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='purchases')
    purchased_at = models.DateTimeField(auto_now_add=True)
    amount_paid = models.DecimalField(max_digits=8, decimal_places=2)
    payment_method = models.CharField(max_length=50, default='online')
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ['user', 'course']

    def __str__(self):
        return f"{self.user.username} - {self.course.title}"



class CourseReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_reviews')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'course']

    def __str__(self):
        return f"{self.user.username} - {self.course.title} - {self.rating} stars"


class CourseProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='course_progress')
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='user_progress')
    progress_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    completed_videos = models.PositiveIntegerField(default=0)
    total_videos = models.PositiveIntegerField(default=0)
    last_accessed = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'course']

    def __str__(self):
        return f"{self.user.username} - {self.course.title} - {self.progress_percentage}%"

    def update_progress(self):
        total_videos = self.course.videos.count()
        completed_videos = VideoProgress.objects.filter(
            user=self.user,
            video__course=self.course,
            is_completed=True
        ).count()
        self.total_videos = total_videos
        self.completed_videos = completed_videos
        self.progress_percentage = (completed_videos / total_videos * 100) if total_videos > 0 else 0
        self.save()


class Video(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='videos')
    title = models.CharField(max_length=255)
    video_file = models.FileField(upload_to='course_videos/')
    thumbnail = models.ImageField(upload_to='video_thumbnails/', blank=True, null=True)
    duration = models.DurationField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_preview = models.BooleanField(default=False)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.course.title} - {self.title}"

class VideoProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='video_progress')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='progress')
    watched_duration = models.DurationField(default=0)
    is_completed = models.BooleanField(default=False)
    last_watched = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'video')

    def __str__(self):
        return f"{self.user.username} - {self.video.title} - {'Completed' if self.is_completed else 'In Progress'}"
    

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'course')


class WishlistItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist_items')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'course')