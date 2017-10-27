from django.db import models
from django.contrib.auth.models import User


class MusicPiece(models.Model):
    date_added = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=64)
    soprano = models.TextField()
    alto = models.TextField()
    tenor = models.TextField()
    bass = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
        related_name = 'uploaded_pieces'
    )
    is_public = models.BooleanField(default=False)
    # The TODOs below are TODO when rewriting Note class ("leaving" pyknon)
    #     add a CharField storing a key
    #     ? add a filefield? (and store a midi?)

