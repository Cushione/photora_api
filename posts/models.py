from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, max_length=500)
    image = models.ImageField(
        upload_to='images/' 
    )
    likes = models.ManyToManyField(
        User, related_name='liked_posts', blank=True
    )


    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def number_of_likes(self):
        return self.likes.count()

    def number_of_comments(self):
        return self.post_comments.count()
