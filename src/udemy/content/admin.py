from django.contrib import admin
from .models import Section, Lecture

class LectureInline(admin.TabularInline):
    model = Lecture
    extra = 1

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'total_lectures', 'formatted_total_duration')
    inlines = [LectureInline]

    def formatted_total_duration(self, obj):
        total_seconds = int(obj.total_duration.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        if hours > 0:
            return f"{hours}:{minutes:02}:{seconds:02}"
        return f"{minutes}:{seconds:02}"

    formatted_total_duration.short_description = 'Total Duration'
