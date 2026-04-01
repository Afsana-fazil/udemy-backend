from django.db import models
from datetime import timedelta

class Section(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

    @property
    def total_lectures(self):
        return self.lectures.count()

    @property
    def total_duration(self):
        total = timedelta()
        for lecture in self.lectures.all():
            total += lecture.duration
        return total


class Lecture(models.Model):
    section = models.ForeignKey(Section, related_name='lectures', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    duration = models.DurationField()
    is_preview = models.BooleanField(default=False)

    def __str__(self):
        return self.title
