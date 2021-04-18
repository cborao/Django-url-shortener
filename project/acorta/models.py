from django.db import models

class Content(models.Model):
    key = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    def __str__(self):
        return self.key + ": " + self.url
