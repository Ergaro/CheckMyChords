from django import forms

from pyknon.music import NoteSeq

from .models import (
    MusicPiece
)
from .validators import NotesValidator
from django.core.exceptions import ValidationError



class NewPieceForm(forms.Form):
    title = forms.CharField(max_length=64, label="Title")
    soprano = forms.CharField(validators = [NotesValidator])
    alto = forms.CharField(validators = [NotesValidator])
    tenor = forms.CharField(validators = [NotesValidator])
    bass = forms.CharField(validators = [NotesValidator])
    # TODO: add a key field (not required), turn set_key into a fallback
    # key = forms.CharField(validaators = [KeyValidator], required=False)
    
    # TODO: make it possible to add parts in English notation (C4 for middle C)
    #        (just need to change numbers to ' or ,-s)

    def clean(self):
        # enforces equal length of each part
        cleaned_data = super(NewPieceForm, self).clean()
        s = len(NoteSeq(cleaned_data['soprano']))
        a = len(NoteSeq(cleaned_data['alto']))
        t = len(NoteSeq(cleaned_data['tenor']))
        b = len(NoteSeq(cleaned_data['bass']))
        
        if not (s == a == t == b != 0):
            raise ValidationError("All parts must have the same length" + 
                                  " and have more than 0 notes")
        
        return(cleaned_data)