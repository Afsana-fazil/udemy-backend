from django.db import models


class ServiceCategory(models.Model):
    title = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Service categories"

    def __str__(self):
        return self.title

class Service(models.Model):
    service_category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name='services')
    title = models.CharField(max_length=255)
    stat_1_percent = models.CharField(max_length=25)
    stat_1_text = models.CharField(max_length=255)
    brand_1 = models.CharField(max_length=125)
    stat_2_percent = models.CharField(max_length=25)
    stat_2_text = models.CharField(max_length=255)
    brand_2 = models.CharField(max_length=125)
    image = models.ImageField(upload_to="story/")

    def __str__(self):
        return self.title

