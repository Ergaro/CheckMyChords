# this module extends the pyknon library - should be imported wherever
# the oryginal pyknon is used

# theese functions add @properties of Note and NoteSeq from pyknon library
# they return notes and noteSeq-s in a form that is parsable back to Note
# and NoteSeq objects (to store them in db)

# TODO - make sure this code runs only once

from pyknon.music import Note
from pyknon.music import NoteSeq


def note_to_str(self):
    val = ("C","C#","D","D#","E","F","F#","G","G#","A","A#","B")[self.value]
    oct = ""
    if self.octave < 5:
        oct += "," * (5-self.octave)
    else:
        oct += "'" * (self.octave-4)
    return "{}{}".format(val,oct)

def note_to_hrstr(self):
    # Human readable str of a note: in english notation ( C4 == 'middle' C)
    val = ("C","C#","D","D#","E","F","F#","G","G#","A","A#","B")[self.value]
    oct = str(self.octave - 1)
    space = "" if len(val) == 2 else " "
    return "{}{}{}".format(val,oct, space)

def seq_to_str(self):
    string = " ".join([note.to_str for note in self.items])
    return string

def seq_to_hrstr(self):
    string = " ".join([note.to_hrstr for note in self.items])
    return string


Note.to_str = property(note_to_str)
Note.to_hrstr = property(note_to_hrstr)
NoteSeq.to_str = property(seq_to_str)
NoteSeq.to_hrstr = property(seq_to_hrstr)
