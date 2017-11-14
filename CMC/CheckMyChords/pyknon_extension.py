# this module extends the pyknon library
# TODO: extend also Midi class (from pyknon.genmidi) 

from pyknon.music import Note as OldNote, NoteSeq as OldNoteSeq

class PyknonExtensionError(Exception):
    pass

class Note(OldNote):
    
    @property
    def to_str(self):
        val = ("C","C#","D","D#","E","F","F#","G","G#","A","A#","B")[self.value]
        oct = ""
        if self.octave < 5:
            oct += "," * (5-self.octave)
        else:
            oct += "'" * (self.octave-4)
        return "{}{}".format(val,oct)
    
    @property
    def to_hrstr(self):
        # Human readable str of a note: in english notation ( C4 == 'middle' C)
        val = ("C","C#","D","D#","E","F","F#","G","G#","A","A#","B")[self.value]
        oct = str(self.octave - 1)
        space = "" if len(val) == 2 else " "
        return "{}{}{}".format(val,oct, space)

class NoteSeq(OldNoteSeq):
    
    @staticmethod
    def _make_note_or_rest(note_list):  # overridden
        if note_list[0] is not None:
            return Note(*note_list)
        else:
            # return Rest(note_list[2])
            return PyknonExtensionError("Rests not implemented")
    
    @property
    def to_str(self):
        string = " ".join([note.to_str for note in self.items])
        return string
    
    @property
    def to_hrstr(self):
        string = " ".join([note.to_hrstr for note in self.items])
        return string

