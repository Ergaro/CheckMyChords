from django.db import models


# Create your models here.

class MusicPiece(models.Model):
    date_added = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=64)
    soprano = models.TextField()
    alto = models.TextField()
    tenor = models.TextField()
    bass = models.TextField()
    # add a CharField storing a key
    # add a filefield? (and store a midi?)