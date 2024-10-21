from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    bio = models.TextField(max_length=500, blank=True)
    image = models.ImageField(
        default="profile_pics/default-profile.png", upload_to="profile_pics"
    )
    phone = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f"{self.user.username} Profile"
