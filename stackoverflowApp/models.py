from django.db import models

# Create your models here.
class Stackoverflow(models.Model):
    page = models.IntegerField()
    title = models.TextField()
    # slug = models.SlugField()

    def __str__(self):
        return self.title