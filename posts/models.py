from django.db import models
from tinymce.models import HTMLField  # To use TinyMce editor
from django.contrib.auth.models import User

# Create your models here.

class Tweets(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  #'User' is table by default which have users who are logged in.
    text = HTMLField(null=True)
    photo = models.ImageField(upload_to="photo/", blank=True, null=True) # Django is already saving into MEDIA_ROOT whic specifies the /media/ folder
    created_at = models.DateTimeField(auto_now_add=True)
    # Sets the field only once, when the object is first created.
    # Django automatically fills it with the current timestamp at creation time.
    updated_at = models.DateTimeField(auto_now= True, null=True)
    # Updates the field every time the object is saved (even if you don’t change anything else).
    # Automatically sets the timestamp to the current time on each save.

    def __str__(self):
        return f'{self.user.username} - {self.text[:10]}'
