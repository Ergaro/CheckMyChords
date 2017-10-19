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
        cleaned_data = super(NewPieceForm, self).clean()
        try:
            s = len(NoteSeq(cleaned_data['soprano']))
            a = len(NoteSeq(cleaned_data['alto']))
            t = len(NoteSeq(cleaned_data['tenor']))
            b = len(NoteSeq(cleaned_data['bass']))
            print([s,a,t,b])
            if not (s == a == t == b != 0):
                msg = ValidationError("All parts must have the same length" + 
                                    " and have more than 0 notes")
                self.add_error(None, msg)
        except Exception:
            pass
        return cleaned_data
    
class SelectRulesForm(forms.Form):
    RULES = (
        ("RANGE", 'Default voice ranges'),
        ("LEAPS", 'Leaps of a seventh or above octave forbidden'),
        ("DISTANCES", 'Distances allowed: S/A - max 8, A/T - less than 8, T/B - preferably below 12, max 15'),
        ("PARALELS", '(Anti)consecutive unisons, perfect fifths and octaves forbidden'),
        ("CHORDS", "Chords - in implementation"),
        ("CHORDS_IN_CTX", "Chords (in musical context) -Not yet implemented")
    )  
    rules = forms.MultipleChoiceField(
        choices=RULES,
        widget=forms.CheckboxSelectMultiple(attrs={'checked' : 'checked'})
    )
