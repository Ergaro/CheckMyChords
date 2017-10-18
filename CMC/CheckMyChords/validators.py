import re

from django.core.exceptions import ValidationError

    
def NotesValidator(input):
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
    pass
    
# add a validator to check if lengths of the parts match