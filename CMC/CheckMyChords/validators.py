import re

from django.core.exceptions import ValidationError

    
def NotesValidator(input):
    # TODO : make this validator 'stronger' (should try to convert input into
    # a NoteSeq and see if it works)
    try:
        str(input)
    except Exception:
        raise ValidationError("Wrong datatype")
    
    if 'h' in input or 'H' in input:
        raise ValidationError("Use english notation!")
    elif 'r' in input or 'R' in input:
        raise ValidationError("Rests not allowed!")
    elif re.search(r"[^a-gA-G#,' ]", input) is not None:
        raise ValidationError("Wrong notation")

def KeyValidator(input):
    # Not yet implemented (will be used to validate key given by the user)
    pass
    
