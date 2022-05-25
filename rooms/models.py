from unicodedata import name
from django.db import models
from django.conf import settings
from django.db.models import Q

from topics.models import Topic

User = settings.AUTH_USER_MODEL

# Create your models here.
class RoomQuerySet(models.QuerySet):
    def search(self, query=None):
        if query is None or query == "":
            return self.none()
        lookups = (
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(topic__name__icontains=query)
        )
        return self.filter(lookups) 

class RoomManager(models.Manager):
    def get_queryset(self):
        return RoomQuerySet(self.model, using=self._db)

    def search(self, query=None):
        return self.get_queryset().search(query=query)

class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = RoomManager()

    def __str__(self):
        return self.name
