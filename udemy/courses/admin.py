from django.contrib import admin
from .models import (
    MainCategory, 
    SubCategory, 
    Course, 
    # CoursePurchase, 
    # CourseReview, 
    # CourseProgress,
    # video,
    # VideoProgress
)

@admin.register(MainCategory)
class MainCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'main_category', 'slug', 'learners_count')
    list_filter = ('main_category',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'price', 'premium', 'best_seller', 'created_at')
    list_filter = ('premium', 'best_seller', 'created_at', 'sub_category__main_category')
    search_fields = ('title', 'description', 'created_by')
    readonly_fields = ('created_at', 'updated_at')

# @admin.register(CoursePurchase)
# class CoursePurchaseAdmin(admin.ModelAdmin):
#     list_display = ('user', 'course', 'amount_paid', 'payment_method', 'purchased_at', 'is_active')
#     list_filter = ('payment_method', 'is_active', 'purchased_at')
#     search_fields = ('user__username', 'course__title')
#     readonly_fields = ('purchased_at',)

# @admin.register(CourseReview)
# class CourseReviewAdmin(admin.ModelAdmin):
#     list_display = ('user', 'course', 'rating', 'created_at')
#     list_filter = ('rating', 'created_at')
#     search_fields = ('user__username', 'course__title', 'comment')
#     readonly_fields = ('created_at', 'updated_at')

# @admin.register(CourseProgress)
# class CourseProgressAdmin(admin.ModelAdmin):
#     list_display = ('user', 'course', 'progress_percentage', 'completed_videos', 'total_videos', 'last_accessed')
#     list_filter = ('last_accessed',)
#     search_fields = ('user__username', 'course__title')
#     readonly_fields = ('created_at', 'last_accessed')

# @admin.register(Video)
# class VideoAdmin(admin.ModelAdmin):
#     list_display = ('title', 'course', 'order', 'is_preview')
#     list_filter = ('is_preview', 'course')
#     search_fields = ('title', 'course__title')
#     ordering = ('course', 'order')

# @admin.register(VideoProgress)
# class VideoProgressAdmin(admin.ModelAdmin):
#     list_display = ('user', 'video', 'is_completed', 'last_watched')
#     list_filter = ('is_completed', 'last_watched')
#     search_fields = ('user__username', 'video__title')
#     readonly_fields = ('created_at', 'last_watched')

