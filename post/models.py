from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=120)
    content = models.TextField()
    image = models.ImageField(null=True)
    created_at = models.DateTimeField()

    def __str__(self) -> str:
        return self.title