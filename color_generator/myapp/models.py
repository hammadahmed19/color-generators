from django.db import models

# Create your models here.

class Colours(models.Model):
    user_name = models.CharField(max_length=100)
    colours = models.JSONField(max_length=100)

    def __str__(self):
        return self.user_name