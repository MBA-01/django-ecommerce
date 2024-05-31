from django.db import models

# Create your models here.

class Domain(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField(unique=True)

    def __str__(self):
        return self.name

class ScraperProduct(models.Model):
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    price = models.CharField(max_length=100)
    description = models.TextField()
    images = models.JSONField()
    link = models.URLField()

    def __str__(self):
        return self.title
