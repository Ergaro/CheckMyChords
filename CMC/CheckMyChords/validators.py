import re

from django.core.exceptions import ValidationError

    
def NotesValidator(input):
    try:
        str(input)
    except Exception:
        raise ValidationError("Wrong datatype")
    
    if 'h' in input or 'H' in input:
        raise ValidationError("Use english notation!")
    elif re.search(r"[^a-gA-GrR#,' ]", input) is not None:
        # kick rests out of the regex above...
        raise ValidationError("Wrong notation")
    
# add a validator to check if lengths of the parts match