from django.test import TestCase

from pyknon.music import Note, NoteSeq

from CheckMyChords.harmony_rules import Chord


class NoteTests(TestCase):
    # not yet implemented
    pass

class ChordTests(TestCase):
    # TODO: add more descriptive fail messages
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
        # chord object should be able to handle proper strings as arguments
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

    def test_chord_find_root_simple_chords(self):
        c_chord = Chord(Note("G'"), Note("E'"), Note("C'"), Note("C,"))
        d_chord = Chord(Note("A'"), Note("F#'"), Note("D'"), Note("D,"))
        e_min_chord = Chord(Note("B'"), Note("G'"), Note("E'"), Note("E,"))
        f_min_chord = Chord(Note("C''"), Note("Ab'"), Note("F'"), Note("F,"))
        
        c_chord._read_chord()
        d_chord._read_chord()
        e_min_chord._read_chord()
        f_min_chord._read_chord()
        
        self.assertEqual(c_chord.root, 0)       
        self.assertEqual(d_chord.root, 2)
        self.assertEqual(e_min_chord.root, 4)
        self.assertEqual(f_min_chord.root, 5)
        
    def test_chord_find_root_simple_chords_inversions(self):
        c_firs_inv = Chord(Note("C''"), Note("C'"), Note("G,"), Note("E,"))
        d_sec_inv = Chord(Note("F#'"), Note("D'"), Note("D'"), Note("A,"))
        e_min_first_inv = Chord(Note("E''"), Note("B'"), Note("E'"), Note("G,"))
        f_min_sec_inv = Chord(Note("F'"), Note("F'"), Note("Ab,"), Note("C,"))
        
        c_firs_inv._read_chord()
        d_sec_inv._read_chord()
        e_min_first_inv._read_chord()
        f_min_sec_inv._read_chord()
        
        self.assertEqual(c_firs_inv.root, 0)       
        self.assertEqual(d_sec_inv.root, 2)
        self.assertEqual(e_min_first_inv.root, 4)
        self.assertEqual(f_min_sec_inv.root, 5)
    
    def test_chord_find_root_simple_septimal_chords(self):
        # Major chords only (Dominant seventh chord)
        # minor chords have a perfect fith between 3 and 7, which leads
        # to multiple interpretations
        a_septimal = Chord(Note("G'"), Note("C#'"), Note("E,"), Note("A,,"))
        bb_septimal = Chord(Note("F'"), Note("D'"), Note("Ab,"), Note("Bb,,"))
        b_septimal = Chord(Note("D#'"), Note("A,"), Note("F#,"), Note("B,,"))
    
        a_septimal._read_chord()
        bb_septimal._read_chord()
        b_septimal._read_chord()
        
        self.assertEqual(a_septimal.root, 9)       
        self.assertEqual(bb_septimal.root, 10)
        self.assertEqual(b_septimal.root, 11)
        
    def test_chord_find_root_septimal_chords_inversions(self):
        # Major chords only (Dominant seventh chords)
        fs_septimal_fi = Chord(Note("F#'"), Note("E'"), Note("C#'"), Note("A#,"))
        g_septimal_si = Chord(Note("F'"), Note("B,"), Note("G,"), Note("D,"))
        ab_septimal_ti = Chord(Note("Eb'"), Note("C'"), Note("Ab,"), Note("Gb,"))
    
        fs_septimal_fi._read_chord()
        g_septimal_si._read_chord()
        ab_septimal_ti._read_chord()
        
        self.assertEqual(fs_septimal_fi.root, 6)       
        self.assertEqual(g_septimal_si.root, 7)
        self.assertEqual(ab_septimal_ti.root, 8)
    
    def test_chord_find_root_simple_ninth_chords(self):
        # Major chords only (Dominant ninth chord - like in septimal chords)
        c_major_ninth = Chord(Note("D''"), Note("E'"), Note("Bb,"), Note("C,"))
        cs_minor_ninth = Chord(Note("E#'"), Note("D'"), Note("B,"), Note("C#,"))
        d_minor_ninth = Chord(Note("Eb'"), Note("C'"), Note("F#,"), Note("D,"))
        eb_major_ninth = Chord(Note("Db''"), Note("F'"), Note("G,"), Note("Eb,"))
        
        c_major_ninth._read_chord()
        cs_minor_ninth._read_chord()
        d_minor_ninth._read_chord()
        eb_major_ninth._read_chord()
        
        self.assertEqual(c_major_ninth.root, 0)       
        self.assertEqual(cs_minor_ninth.root, 1)
        self.assertEqual(d_minor_ninth.root, 2)
        self.assertEqual(eb_major_ninth.root, 3)
        
    def test_chord_find_root_ninth_chords_inversions(self):
        # Major chords only (Dominant ninth chords)
        # Not yet implemented
        f_maj_ninth_fi = Chord(Note("G'"), Note("Eb'"), Note("F,"), Note("A,,"))
        ab_min_ninth_fi = Chord(Note("Bbb'"), Note("Gb'"), Note("Ab,"), Note("C,"))
        b_maj_ninth_ti = Chord(Note("C#''"), Note("D#'"), Note("B,"), Note("A,"))
        ds_min_ninth_ti = Chord(Note("E''"), Note("F##'"), Note("D#'"), Note("C#,"))
        
        f_maj_ninth_fi._read_chord()
        ab_min_ninth_fi._read_chord()
        b_maj_ninth_ti._read_chord()
        ds_min_ninth_ti._read_chord()
        
        self.assertEqual(f_maj_ninth_fi.root, 5)
        self.assertEqual(ab_min_ninth_fi.root, 8)
        self.assertEqual(b_maj_ninth_ti.root, 11)
        self.assertEqual(ds_min_ninth_ti.root, 3)
    
    
    def test_chord_find_root_incomplete_chords(self):
        # 1 1 1 3 and 1 1 1 3> chords (should be recognized even if inverted)
        f_min_1113 = Chord(Note("Ab'"), Note("F'"), Note("F,"), Note("F,,"))
        g_major_1113 = Chord(Note("G'"), Note("B,"), Note("G,"), Note("G,,"))
        a_major_1113_fi = Chord(Note("A'"), Note("A'"), Note("A,"), Note("C#,"))
        # 1 1 3 7 chord
        db_major_1137 = Chord(Note("F'"), Note("Db'"), Note("Cb'"), Note("Db,"))
        db_major_1137_fi = Chord(Note("Db''"), Note("Db'"), Note("Cb'"), Note("F,"))
        db_major_1137_si = Chord(Note("Db''"), Note("F'"), Note("Db'"), Note("Cb'"))
        # 1 5 chord
        fs_15 = Chord(Note("F#'"), Note("C#'"), Note("C#'"), Note("F#,"))
        fs_15_inverted = Chord(Note("F#'"), Note("C#'"), Note("F#,"), Note("C#,"))
        # 1111 chord
        db_1111 = Chord(Note("Db'"), Note("Db'"), Note("Db'"), Note("Db'"))
        
        f_min_1113._read_chord()
        g_major_1113._read_chord()
        a_major_1113_fi._read_chord()
        db_major_1137._read_chord()
        db_major_1137_fi._read_chord()
        db_major_1137_si._read_chord()
        fs_15._read_chord()
        fs_15_inverted._read_chord()
        db_1111._read_chord()
        
        self.assertEqual(f_min_1113.root, 5)
        self.assertEqual(g_major_1113.root, 7)
        self.assertEqual(a_major_1113_fi.root, 9)
        self.assertEqual(db_major_1137.root, 1)
        self.assertEqual(db_major_1137_fi.root, 1)
        self.assertEqual(db_major_1137_si.root, 1)
        self.assertEqual(fs_15.root, 6)
        self.assertEqual(fs_15_inverted.root, 6)
        self.assertEqual(db_1111.root, 1)
        
    def test_chord_find_root_wrongly_named_chords(self):
        # Some basic chords should be recognized even if wrongly written
        # e.g. F-G#-C
        pass
    
    def test_chord_find_root_other_chords(self):
        # D64 or similar? - in context?
        # D9 w/o 1 - multiple interpretations??
        # diminished chord
        # minor chord with added 7th
        pass
    
    def test_chord_structure_for_simple_chords(self):
        pass
    
    def test_chord_structure_for_chords_with_added_seventh(self):
        pass
    
    def test_chord_structure_for_chords_with_fith_ommited(self):
        pass


class HarmonyRulesTests(TestCase):
    # not yet implemented
    pass

