from django.db import models
from django.contrib.auth.models import User
from django.conf import settings



class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()             
    time = models.TimeField()
    location = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    rsvps = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='rsvped_events', blank=True)


    image = models.ImageField(
        upload_to='event_images/', 
        blank=True,
        null=True,
        default='event_images/Default.jpg'
    )

    def __str__(self):
        return self.name


class Participant(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    events = models.ManyToManyField(Event, related_name="participants")

    def __str__(self):
        return self.name