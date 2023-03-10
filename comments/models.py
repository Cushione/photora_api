from django.db import models
from django.contrib.auth.models import User
from posts.models import Post


class Comment(models.Model):
    """
    Comment Model
    """

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.TextField()
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="post_comments"
    )

    class Meta:
        """
        Comment Meta Data
        """

        # Order comments by created date in descending order
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
