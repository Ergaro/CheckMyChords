from django import forms
from .models import (
    MusicPiece
)
from .validators import NotesValidator
from django.core.validators import RegexValidator


class NewPieceForm(forms.Form):
    title = forms.CharField(max_length=64, label="Title")
    soprano = forms.CharField(validators = [NotesValidator])
    # soprano = forms.CharField(widget=forms.TextInput(attrs={'placeholder':"soprano part here"}))
    # soprano = forms.CharField(widget=forms.Textarea(attrs={'rows':1}))
    alto = forms.CharField(validators = [NotesValidator])
    tenor = forms.CharField(validators = [NotesValidator])
    bass = forms.CharField(validators = [NotesValidator])

