from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True)
    age = models.IntegerField(blank=True,
                              validators=[
                                  MinValueValidator(10),
                                  MaxValueValidator(100)
                              ])
    profile_picture = models.ImageField(upload_to='media/members/profile_pictures', blank=True, null=True)

    def __str__(self):
        return self.name
