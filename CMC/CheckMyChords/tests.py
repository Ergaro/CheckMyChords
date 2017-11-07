from django.test import TestCase

from pyknon.music import Note, NoteSeq

from CheckMyChords.harmony_rules import Chord
# Create your tests here.


class ChordTests(TestCase):
    def setUp(self):
        pass
    
    def test_chord_created_using_note_objects(self):
        # create notes
        soprano = Note("G'")
        alto = Note("E'")
        tenor = Note("C'")
        bass = Note("C,")
        # create chord from given notes
        c_chord = Chord(soprano, alto, tenor, bass)
        # check if chord consists of given notes
        self.assertEqual(c_chord.soprano, soprano)
        self.assertEqual(c_chord.alto, alto)
        self.assertEqual(c_chord.tenor, tenor)
        self.assertEqual(c_chord.bass, bass)
        
        self.assertIs(type(c_chord.soprano), Note)
        self.assertIs(type(c_chord.alto), Note)
        self.assertIs(type(c_chord.tenor), Note)
        self.assertIs(type(c_chord.bass), Note)
        
    def test_chord_created_using_wrong_data_types(self):
        # try to create chord object using different argument types
        with self.assertRaises(TypeError):
            c_chord=Chord(1,2,3,4)
            
        with self.assertRaises(TypeError):
            c_chord=Chord("w", "x", "y", "z")

    def test_chord_created_using_strings(self):
        # chord object should be able to get proper strings as arguments
        # should just try - Note(given_string) - not yet implemented
        
        # create chord from given notes
        c_chord = Chord("G'", "E'", "C'", "C,")
        # check if chord consists of given notes
        self.assertEqual(c_chord.soprano, "G'")
        self.assertEqual(c_chord.alto, "E'")
        self.assertEqual(c_chord.tenor, "C'")
        self.assertEqual(c_chord.bass, "C,")
        
        self.assertIs(type(c_chord.soprano), Note)
        self.assertIs(type(c_chord.alto), Note)
        self.assertIs(type(c_chord.tenor), Note)
        self.assertIs(type(c_chord.bass), Note)



class HarmonyRulesTests(TestCase):
    # not yet implemented
    pass

