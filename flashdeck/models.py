from django.db import models
from django.contrib.auth.models import AbstractUser
from flashcardProject import settings

# Create your models here.

class CustomUser(AbstractUser):
    pass

    def __str__(self):
        return self.username


NUM_BOXES = 4
BOXES = range(1, NUM_BOXES + 1)

class CardSet(models.Model):
    name = models.CharField(max_length=100, default=None)
    description = models.CharField(max_length=500, default=None)
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # numCards = models.IntegerField(default=None)

    def __str__(self):
        return self.name
    
class Card(models.Model):
    card_setNumber = models.ForeignKey(CardSet, on_delete=models.CASCADE, default=None)
    question = models.CharField(max_length=100, default=None)
    answer = models.CharField(max_length=200, default=None)
    #img = models.ImageField(upload_to="images/", default=None, blank=True, null=True)
    #audio = models.FileField(upload_to="audio/", default=None, blank=True, null=True) 
    box = models.IntegerField(
        choices=zip(BOXES, BOXES),
        default=BOXES[0],
    )
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question