from django.apps import AppConfig

from pyknon.music import NoteSeq
from pyknon.music import Note


from pyknon_extension import * 


class CheckmychordsConfig(AppConfig):
    name = 'CheckMyChords'
    

# a = Note("F#''")
# b = NoteSeq("Ab,, C'' Eb'")
# c = NoteSeq(b.to_str)
# 
# print(a)
# print(b)
# print(c)
# 
# print(a.to_str)
# print(b.to_str)
# print(c.to_str)


