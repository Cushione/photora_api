from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """
    Profile Model
    """

    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=35)
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to="images/", default="../user_nbfhis")
    followers = models.ManyToManyField(
        User, related_name="followed_profiles", blank=True
    )

    class Meta:
        """
        Comment Meta Data
        """

        # Order profiles by created date in descending order
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.owner}'s profile"


def create_profile(sender, instance, created, **kwargs):
    """
    Creates a profile when a user is created
    """
    if created:
        Profile.objects.create(owner=instance, name=instance.username[0:50])


# Create Profile when a user is created
models.signals.post_save.connect(create_profile, sender=User)
