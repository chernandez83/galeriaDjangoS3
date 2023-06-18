from django.db import models

class Album(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False)
    description = models.TextField()
    bucket = models.CharField(max_length=100, null=False, blank=False)
    key = models.CharField(max_length=50, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title