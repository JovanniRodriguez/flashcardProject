from django.db import models

# Create your models here.
NUM_BOXES = 4
BOXES = range(1, NUM_BOXES + 1)

class CardSet(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    date_created = models.DateTimeField(auto_now_add=True)
    card_setNumber = models.IntegerField(unique=True, editable=False, null=True)

    def __str__(self):
        return self.name
    
class Card(models.Model):
    card_setNumber = models.ForeignKey(CardSet, on_delete=models.CASCADE)
    question = models.CharField(max_length=100)
    answer = models.CharField(max_length=200)
    img = models.ImageField(upload_to="images/", default=None) # new
    audio = models.FileField(upload_to="audio/", default=None) # new
    box = models.IntegerField(
        choices=zip(BOXES, BOXES),
        default=BOXES[0],
    )
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question