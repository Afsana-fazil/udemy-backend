from django.db import models

# Create your models here.

class DemoSubmission(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    work_email = models.EmailField()
    phone_number = models.CharField(max_length=30)
    location = models.CharField(max_length=100)
    company_name = models.CharField(max_length=200)
    company_size = models.CharField(max_length=100)
    num_people_to_train = models.CharField(max_length=100)
    job_title = models.CharField(max_length=100)
    job_level = models.CharField(max_length=100)
    training_needs = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.company_name}"
