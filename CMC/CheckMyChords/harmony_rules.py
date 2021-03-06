# Stores classes & functions needed to check harmony of a piece
from pyknon.music import Note, NoteSeq

from CheckMyChords.models import MusicPiece
from CheckMyChords.pyknon_extension import *


class Chord(object):
    # a class storing a chord (as Note objects) and additional info about it
    # (as well as methods for getting that info)
    
    def __init__(self, soprano, alto, tenor, bass):  # TODO: pass more arguments (key)
        if (not isinstance(soprano, Note)) or \
           (not isinstance(alto, Note)) or \
           (not isinstance(tenor, Note)) or \
           (not isinstance(bass, Note)):
            raise TypeError(
                'A Chord object should be built using Note objects' 
                + ' as arguments.')
        # TODO: add an iterator (over parts) and delete self.parts
        self.soprano = soprano
        self.alto = alto
        self.tenor = tenor
        self.bass = bass
        self.parts = {"S": self.soprano, 
                      "A": self.alto, 
                      "T": self.tenor,
                      "B": self.bass}
        self.root = None  # int 0-11 or None
        self.mode = None  # 'M', 'm', 'M7', 'm7' or None
        self.structure = {"S": None,  # as intervals from the root
                          "A": None,  # in "standard" notation (e.g. 5==fifth)
                          "T": None,  # None == 'not recognised'
                          "B": None} 
        self._read_chord()
    
    def __str__(self):
        return "S:{s}, A:{a}, T:{t}, B:{b}".format(
            s = self.soprano.to_str,
            a = self.alto.to_str,
            t = self.tenor.to_str,
            b = self.bass.to_str)
    
    def _read_chord(self):
        # determines chord detailed info
        self._find_root()
        self._find_structure()
        self._find_mode()
    
    def _find_root(self):
        # method deducting chord details from the notes given
        # TODO: Rewrite it to use values instead of midi_numbers 
        #     (will possibly simplify conditions)
        b = self.bass.midi_number
        t = self.tenor.midi_number
        a = self.alto.midi_number
        s = self.soprano.midi_number
        # finding root
        #   ifs' condtions ordered by decreasing "importance"
        #     I. looking for a fifth (including crossed voices)
        if (t-b) in (7, 19, 31) \
                or (a-b) in (7, 19, 31, 43) \
                or (s-b) in (7, 19, 31, 43):
            self.root = self.bass.value
        elif (b-t) in (7,) \
                or (a-t) in (7, 19, 31) \
                or (s-t) in (7, 19, 31, 43):
            self.root = self.tenor.value
        elif (b-a) in (7,) \
                or (t-a) in (7, 19) \
                or (s-a) in (7, 19, 31):
            self.root = self.alto.value
        elif (b-s) in (7,) or (t-s) in (7,) or (a-s) in (7,):
            self.root = self.soprano.value
        #    II. looking for a fourth (tonic only above fifth)
        elif (b-t) in (5,) or (b-a) in (5,) or (b-s) in (5,):
            self.root = self.bass.value
        elif (t-b) in (5, 17, 29, 41) \
                or (t-a) in (5, 17) \
                or (t-s) in (5,):
            self.root = self.tenor.value
        elif (a-b) in (5, 17, 29, 41) \
                or (a-t) in (5, 17, 29, 41) \
                or (a-s) in (5,):
            self.root = self.alto.value
        elif (s-b) in (5, 17, 29, 41, 53) \
                or (s-t) in (5, 17, 29, 41) \
                or (s-a) in (5, 17, 29, 41):
            self.root = self.soprano.value
        #    III. the fifth is missing, looking for a doubled interval
        #        (1113 chord or similar)
        elif (b%12 == t%12) or (b%12 == a%12) or (b%12 == s%12):
            self.root = self.bass.value
        elif (t%12 == a%12) or (t%12 == s%12):
            self.root = self.tenor.value
        elif (a%12 == s%12):
            self.root = self.alto.value     
        #    IV. no note is dubled (and 5th missing), assuming bass 
        #        note is the root (to modify, should D9(>) be included)
        else:
            self.root = self.bass.value
    
    def _find_structure(self):
        # method deducting chord structure from notes given (needs root)
        # should leave initial (None) for unrecognised notes
        # minor/major thirds are distinguished
        if self.root == None:
            return
        intervals = {
            "0": "1",  # root
            "3": "3>",  # minor third
            "4": "3",  # major third
            "7": "5",  # fith
            "10": "7",  # minor seventh
        }
        for voice, note in self.parts.items():
            dist_from_root = str((note.midi_number - self.root) % 12)
            if dist_from_root in intervals:
                self.structure[voice] = intervals[dist_from_root]
    
    def _find_mode(self):
        # method determining chord mode (M, m, M7 or m7) from the chord
        # structure
        if "3>" in self.structure.values() and "3" in self.structure.values():
            # both minor and major thirds in a chord at the same time
            self.mode = None
        elif "3>" in self.structure.values():
            self.mode = "m7" if "7" in self.structure.values() else "m"
        elif "3" in self.structure.values():
            self.mode = "M7" if "7" in self.structure.values() else "M"
        else:  # no third in a chord (or find_structure failed)
            self.mode = None
    
    def harmonic_function(self, key):
        # Tonic must be of correct mode
        # Tonic6 must be of oposite mode (a minor in C major key)
        # Allows both minor and major subdominants in minor and major keys
        # Allows minor and major dominants in minor keys
        # Allows only major dominant in major keys
        # Allows sevenths in dominant only ("D7")
        # harm_fs = ("T", "S", "D", "D7", "T6")
        # NOTE - this method will recognise function if foreign notes are
        # present (C E F# G) will be recognised as a Tonic in C major,
        # but (C E G Bb) won't
        if self.root == key[0]:
            if key[1] == 1 and self.mode == "M":  # major
                return "T" 
            elif key[1] == 0 and self.mode =='m': # minor
                return "T"
            else:
                return ""  # unrecognised chord or seventh present
        elif (self.root - key[0]) % 12 == 5:
            if self.mode in ("M", "m"):
                return "S"
            else:
                return ""
        elif (self.root - key[0]) % 12 == 7:
            if key[1] == 1 and self.mode == "M":
                return "D"
            elif key[1] == 1 and self.mode == "M7":
                return "D7"
            elif key[1] == 0 and self.mode in ("M", "m"): 
                return "D"
            elif key[1] == 0 and self.mode in ("M7", "m7"):
                return "D7"
            else:
                return ""
        elif (self.root - key[0]) % 12 == 8:  #6th in minor scale
            if self.mode == "M":
                return "TVI"
            else:
                return ""
        elif (self.root - key[0]) % 12 == 9:  #6th in major key
            if self.mode == "m":
                return "TVI"
            else:
                return ""
        else:
            return ""


class Piece(object):
    # A class analogous to MusicPiece, but stores parts as NoteSeqs objects
    # also stores harmony rules functions and results of their "work"
    # TODO: add an iterator (over parts) and delete self.parts
    
    def __init__(self, piece):
        if not isinstance(piece, MusicPiece):
            raise TypeError(
                'A Piece object should be built using MusicPiece object' 
                + ' as an argument.')
        self.soprano = NoteSeq(piece.soprano)
        self.alto = NoteSeq(piece.alto)
        self.tenor = NoteSeq(piece.tenor)
        self.bass = NoteSeq(piece.bass)
        self.title = piece.title
        self.parts = {"S": self.soprano, 
                      "A": self.alto, 
                      "T": self.tenor,
                      "B": self.bass}
        self._key = [None, None]
        self._chords = []
        self._err_count = 0
        self._war_count = 0
        self._err_detailed = []
        self._war_detailed = []
        self._read_chords()
        self._set_key()
    
    @property
    def err_count(self):
        return self._err_count
    
    @property
    def war_count(self):
        return self._war_count
    
    @property
    def err_detailed(self):
        return self._err_detailed
    
    @property
    def war_detailed(self):
        return self._war_detailed
    
    @property
    def key(self):
        return self._key
    
    @property
    def chords(self):
        return self._chords
    
    @property
    def parts_hr(self):
        # human-readable representation of the part
        result = {}
        for voice, part in self.parts.items():
            result[voice] = "|" + part.to_hrstr + "||"
        return result
    
    @property
    def key_hr(self):
        # human-readable version of key
        if None in self.key:
            return "Unknown key"
        else:
            result =" ".join((
                ("C","C#","D","D#","E","F","F#","G","G#","A",
                                                        "A#","B")[self.key[0]],
                ("minor", "major")[self.key[1]]
            ))
            return result
    
    @property
    def functions_hr(self):
        # gives harmonic functions set to print under score (compatible with
        # parts_hr)
        result = "|"
        for chord in self.chords:
            ch = chord.harmonic_function(self.key)
            while len(ch) < 4:
                ch += " "  # ensures correct spacing
            result += ch
        result = result[:-1] + "||"
        return result
    
    @property
    def chord_n_hr(self):
        # chord numbers to print above score (compatible with parts_hr)
        result = " "
        for idx in enumerate(self.chords, 1):
            num = str(idx[0])
            while len(num) < 4:
                num += " "
            result += num
        return result
    
    def _read_chords(self):
        # converts noteSeqs to chords
        for i in range(len(self.soprano)):
            chord = Chord(self.soprano[i], 
                          self.alto[i], 
                          self.tenor[i], 
                          self.bass[i])
            self._chords.append(chord)
    
    def _set_key(self):
        # method dentifies key (basing on the first chord)
        # key is stored as a touple - first element determinines the tonic,
        # (integer 0-11) second detemines the mode (1 == major or 0 == minor)
        # method should return C major if failed to read the chord
        if self.chords[0].root != None:
            self._key[0] = self.chords[0].root
        else:
            self._key[0] = 0  # C as a fallback value
        if self.chords[0].mode in ("M","M7"):
            self._key[1] = 1
        elif self.chords[0].mode in ("m", "m7"):
            self._key[1] = 0
        else:
            self._key[1] = 1  # major as a fallback value
    
    def check_harmony(self, rules=['ALL']):
        # main method for checking harmony of a piece, should call methods
        # for checking each rule
        if 'ALL' in rules or 'RANGE' in rules:
            self._check_range()
        if 'ALL' in rules or 'LEAPS' in rules:
            self._check_leaps()
        if 'ALL' in rules or 'DISTANCES' in rules:
            self._check_distances()
        if 'ALL' in rules or 'PARALELS' in rules:
            self._check_paralels()
        if 'ALL' in rules or 'CHORDS' in rules:
            self._check_chords()
        if 'ALL' in rules or "CHORDS_IN_CTX" in rules:
            self._check_chords_in_context()
    
    # Methods checking individual rules. Each method should:
    # Increase self.err_count by number of mistakes found
    # Append a 3-element touple to self.err_detailed, matching the pattern:
    # ( <Mistake type (str)> , <err_count (int)>, <list of str-s with details
    # about each mistake> )
    
    def _check_range(self):
        # checking vocal range for each voice in the piece
        err_count = 0
        errs = []
        ranges = {
            "S" : (58, 81),
            "A" : (53, 74),
            "T" : (46, 69),
            "B" : (40, 62)
        }
        for voice, part in self.parts.items():
            v_range = ranges[voice]
            for idx, note in enumerate(part, 1):
                if note.midi_number > v_range[1]:
                    err_count += 1
                    errs.append("Chord {0}: {1} too high".format(idx, voice))
                elif note.midi_number < v_range[0]:
                    err_count += 1
                    errs.append("Chord {0}: {1} too low".format(idx, voice))
        if err_count:
            errs.sort()
            self._err_count += err_count
            self._err_detailed.append(("Voice range errors", err_count, errs))
    
    def _check_leaps(self):
        # checking for restricted intervals: leaps of a 7th, or >=9th
        err_count = 0
        errs = []
        for voice, part in self.parts.items():
            for i in range(len(part)-1):
                distance = abs(part[i+1].midi_number - part[i].midi_number)
                if  distance == 10:
                    err_count +=1
                    errs.append("Chords {0}/{1}: Restricted leap in {2} - 7".
                                format(i+1, i+2, voice))
                elif distance == 11:
                    err_count +=1
                    errs.append("Chords {0}/{1}: Restricted leap in {2} - 7<".
                                format(i+1, i+2, voice))
                elif distance > 12:
                    err_count +=1
                    errs.append(
                        "Chords {0}/{1}: Restricted leap in {2} - over an octave".
                            format(i+1, i+2, voice))
        if err_count:
            errs.sort()
            self._err_count += err_count
            self._err_detailed.append(("Restricted leaps", err_count, errs))
    
    def _check_distances(self):
        # checking each chord for too high distances between voices and 
        # too low distances (overlaps == crossing voices)
        err_count = 0
        errs = []
        war_count = 0
        wars = []
        for i in range(len(self.soprano)):
            if self.soprano[i].midi_number - self.alto[i].midi_number > 12:
                err_count += 1
                errs.append("Chord {0}: S/A interval to wide".format(i+1))
            elif self.soprano[i].midi_number - self.alto[i].midi_number < 0:
                err_count += 1
                errs.append("Chord {0}: S/A overlap".format(i+1))
                
            if self.alto[i].midi_number - self.tenor[i].midi_number >= 12:
                err_count += 1
                errs.append("Chord {0}: A/T interval to wide".format(i+1))
            elif self.alto[i].midi_number - self.tenor[i].midi_number < 0:
                err_count += 1
                errs.append("Chord {0}: A/T overlap".format(i+1))
                
            if self.tenor[i].midi_number - self.bass[i].midi_number > 24:
                err_count += 1
                errs.append("Chord {0}: T/B interval to wide".format(i+1))
            elif self.tenor[i].midi_number - self.bass[i].midi_number > 19:
                war_count += 1
                wars.append("Chord {0}: T/B interval to wide".format(i+1))
            elif self.tenor[i].midi_number - self.bass[i].midi_number < 0:
                err_count += 1
                errs.append("Chord {0}: T/B overlap".format(i+1))
        if err_count:
            self._err_count += err_count
            self._err_detailed.append(
                ("Voice distance errors", err_count, errs)
            )
        if war_count:
            self._war_count += war_count
            self._war_detailed.append(
                ("Voice distance warnings", war_count, wars)
            )
    
    def _check_paralels(self):
        # checking for restricted (anti)consecutive intervals (1, 5, 8)
        err_count = 0
        errs = []
        for i in range(len(self.soprano)-1):
            s1 = self.soprano[i].midi_number
            s2 = self.soprano[i+1].midi_number
            a1 = self.alto[i].midi_number
            a2 = self.alto[i+1].midi_number
            t1 = self.tenor[i].midi_number
            t2 = self.tenor[i+1].midi_number
            b1 = self.bass[i].midi_number
            b2 = self.bass[i+1].midi_number
            # conditions writen usin "in" to not falsly trigger it when
            # voices move in consecutive forths, A above S
            # REVISE IT!
            # The distances extended above allowed by check_distance 
            # (by a reasonable amount to identify both errors if occur 
            # simultaneously
            # paralels should be checked only when note changes, hence:
            if s1 != s2 and a1 != a2:
                if (s1 - a1) % 12 == 0 and (s2 - a2) % 12 == 0:
                    err_count += 1
                    errs.append("Chords {0}/{1}: S/A consecutive Unison/Octave".
                                format(i+1, i+2))
                elif s1 - a1 in (7, 19, 31) and s2 - a2 in (7, 19, 31):
                    err_count += 1
                    errs.append("Chords {0}/{1}: S/A consecutive Fifths".
                                format(i+1, i+2))
            
            if s1 != s2 and t1 != t2:
                if (s1 - t1) % 12 == 0 and (s2 - t2) % 12 == 0:
                    err_count += 1
                    errs.append("Chords {0}/{1}: S/T consecutive Unison/Octave".
                                format(i+1, i+2))
                elif s1 - t1 in (7, 19, 31, 43) and s2 - t2 in (7, 19, 31, 43):
                    err_count += 1
                    errs.append("Chords {0}/{1}: S/T consecutive Fifths".
                                format(i+1, i+2))
            
            if s1 != s2 and b1 != b2:
                if (s1 - b1) % 12 == 0 and (s2 - b2) % 12 == 0:
                    err_count += 1
                    errs.append("Chords {0}/{1}: S/B consecutive Unison/Octave".
                                format(i+1, i+2))
                elif s1 - b1 in (7, 19, 31, 43) and s2 - b2 in (7, 19, 31, 43):
                    err_count += 1
                    errs.append("Chords {0}/{1}: S/B consecutive Fifths".
                                format(i+1, i+2))
            
            if a1 != a2 and t1 != t2:
                if (a1 - t1) % 12 == 0 and (a2 - t2) % 12 == 0:
                    err_count += 1
                    errs.append("Chords {0}/{1}: A/T consecutive Unison/Octave".
                                format(i+1, i+2))
                elif a1 - t1 in (7, 19, 31) and a2 - t2 in (7, 19, 31):
                    err_count += 1
                    errs.append("Chords {0}/{1}: A/T consecutive Fifths".
                                format(i+1, i+2))
            
            if a1 != a2 and b1 != b2:
                if (a1 - b1) % 12 == 0 and (a2 - b2) % 12 == 0:
                    err_count += 1
                    errs.append("Chords {0}/{1}: A/B consecutive Unison/Octave".
                                format(i+1, i+2))
                elif a1 - b1 in (7, 19, 31, 43) and a2 - b2 in (7, 19, 31, 43):
                    err_count += 1
                    errs.append("Chords {0}/{1}: A/B consecutive Fifths".
                                format(i+1, i+2))
            
            if t1 != t2 and b1 != b2:
                if (t1 - b1) % 12 == 0 and (t2 - b2) % 12 == 0:
                    err_count += 1
                    errs.append("Chords {0}/{1}: T/B consecutive Unison/Octave".
                                format(i+1, i+2))
                elif t1 - b1 in (7, 19, 31) and t2 - b2 in (7, 19, 31):
                    err_count += 1
                    errs.append("Chords {0}/{1}: T/B consecutive Fifths".
                                format(i+1, i+2))
            
        if err_count:
            self._err_count += err_count
            self._err_detailed.append(
                ("Consecutive intervals", err_count, errs)
            )
    
    def _check_chords(self):
        # checking for wrong chords (unrecognisable, or wrong dubling)
        # if chord is unrecognisable, other conditions aren't checked
        # e.g - chord c,d,e,g, will get warning (d doesn't belong to C chord)
        # but c,d,g,c will not get warning, but will get an error - 
        # chord mode unknown) 
        err_count = 0
        errs = []
        war_count = 0
        wars = []
        for idx, chord in enumerate(self.chords, 1):
            if chord.mode == None:
                err_count += 1
                errs.append("Chord {0}: Chord mode unknown".format(idx))
            else:  
                roots = 0
                thirds = 0
                fifths = 0
                sevenths = 0
                for voice, interval in chord.structure.items():
                    if interval == "1":
                        roots += 1
                    elif interval == "3>" or interval == "3":
                        thirds += 1
                    elif interval == "5":
                        fifths += 1
                    elif interval == "7":
                        sevenths += 1
                    else:
                        war_count += 1
                        wars.append(
                            "Chord {0}: {1} note doesn't belong to the chord".
                                format(idx, voice)
                        )
                if thirds > 1 and (not chord.harmonic_function(self.key) == "TVI"):
                    war_count += 1
                    wars.append("Chord {0}: more than one third in the chord".
                                    format(idx))
                elif fifths >1:
                    war_count += 1
                    wars.append("Chord {0}: more than one fifth in the chord".
                                    format(idx))
                elif sevenths > 1:
                    err_count += 1
                    errs.append("Chord {0}: more than one seventh in the chord".
                                    format(idx))
        if err_count:
            self._err_count += err_count
            self._err_detailed.append(("Unnown chords", err_count, errs))
        
        if war_count:
            self._war_count += war_count
            self._war_detailed.append(
                ("Foreign notes in chords and wrong doubling", war_count, wars)
            )
    
    def _check_chords_in_context(self):
        err_count = 0
        errs = []
        war_count = 0
        wars = []
        war_count += 1
        wars.append("Checking chords in context not yet implemented!")
        self._war_count += war_count
        self._war_detailed.append(
            ("Checking chords in context", war_count, wars)
        )


def check_harmony_rules(music_piece, rules=['ALL']):
    piece = Piece(music_piece)
    piece.check_harmony(rules)
    return piece

def make_piece(music_piece):
    # turns a Music_Piece object into a Piece object (without checking rules)
    piece = Piece(music_piece)
    return piece
    
