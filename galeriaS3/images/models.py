from django.db import models

from albums.models import Album

class Image(models.Model):
    key = models.CharField(max_length=100, null=False, blank=False)
    bucket = models.CharField(max_length=100, null=False, blank=False)
    name = models.CharField(max_length=50, null=False, blank=False)
    content_type = models.CharField(max_length=20, null=False, blank=False)
    size = models.IntegerField()
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    @property
    def url(self):
        return f'https://{self.bucket}.s3.amazonaws.com/{self.key}'
    
    @property
    def title(self):
        return self.name.rsplit('.', 1)[0]
    
    @property
    def extension(self):
        return self.name.rsplit('.', 1)[-1]
    
    def __str__(self):
        return self.name
    
    def set_name(self, new_name):
        new_name = new_name + '.' + self.extension
        new_key = self.album.key + new_name
        
        if new_key:
            self.key = new_key
            self.name = new_name
            
            self.save()