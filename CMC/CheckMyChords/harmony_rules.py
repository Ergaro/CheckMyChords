# Stores functions that check harmony of a piece
from pyknon.music import Note, NoteSeq

from .models import MusicPiece


class Piece(object):
    # A class analogous to MusicPiece, but stores parts as NoteSeqs objects
    # also stores harmony rules functions and results of their "work"
    
    def __init__(self, piece):
        if isinstance(piece, MusicPiece):
            self.title = piece.title
            self.soprano = NoteSeq(piece.soprano)
            self.alto = NoteSeq(piece.alto)
            self.tenor = NoteSeq(piece.tenor)
            self.bass = NoteSeq(piece.bass)
            self.parts = {"S": self.soprano, 
                           "A": self.alto, 
                           "T": self.tenor,
                           "B": self.bass}
            self.set_key()
            self.err_count = 0
            self.war_count = 0
            self.err_detailed = []
            self.war_detailed = []
            # self.identify_cords()
            # initialize other properties (?? - err_count already initiated)
        else:
            raise TypeError(
                'A Piece object should be built using MusicPiece object' 
                + ' as an argument.')
        
        # turn the if statement below into validator and add it to the form
        if not (len(self.soprano) 
                == len(self.alto) 
                == len(self.tenor)
                == len(self.bass)):
            raise Exception("Parts have different length!")

    def set_key(self):
        # method should identify key (basing on the first chord)
        # key is stored as a touple - first element determinines the tonic,
        # (integer 0-11) second detemines the mode (1 or 0)
        # method should return C major if failed to read the chord
        # self.key = (2, 0)  # D minor
        self.key = (0, 1)  # C major
        
    def identify_cords(self):
        pass

    def check_harmony(self):
        # main method for checking harmony of a piece, should call methods
        # for checking each rule
        self.check_range()  
        self.check_intervals()
        self.check_distances()
        self.check_paralels()
        self.check_chords()
        
    # Methods checking individual rules. Each method should:
    # Increase self.err_count by number of mistakes found
    # Append a 3-element touple to self.err_detailed, matching the pattern:
    # ( <Mistake type (str)> , <err_count (int)>, <list of str-s with details
    # about each mistake> ) 
        
    def check_range(self):
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
            self.err_count += err_count
            self.err_detailed.append(("Voice range errors", err_count, errs))

    def check_intervals(self):
        # checking for "restricted" intervals: leaps of a 7th, or >=9th
        # Note: this isn't a strict rule
        war_count = 0
        wars = []
        for voice, part in self.parts.items():
            for i in range(len(part)-1):
                distance = abs(part[i+1].midi_number - part[i].midi_number)
                if  distance in [10,11] or distance > 12:
                    war_count +=1
                    wars.append("Chords {0}/{1}: 'Restricted' leap in {2}".
                                format(i+1, i+2, voice))
        if war_count:
            wars.sort()
            self.war_count += war_count
            self.war_detailed.append(("'Restricted' leaps", war_count, wars))
            

    def check_distances(self):
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
            elif self.alto[i].midi_number - self.tenor[i].midi_number < 0:
                err_count += 1
                errs.append("Chord {0}: T/B overlap".format(i+1))
        
        if err_count:
            self.err_count += err_count
            self.err_detailed.append(("Voice distance errors", err_count, errs))
        if war_count:
            self.war_count += war_count
            self.war_detailed.append(("Voice distance warnings", war_count, wars))
        
        

    def check_paralels(self):
        # checking for restricted (anti)consecutive intervals (1, 5, 8)
        err_count = 0
        errs = []
        war_count = 0
        wars = []
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
            # The distances extended above allowed by check_distance 
            # (by a reasonable amount to identify both errors if occur 
            # simultaneously
            # paralels should be checked only when note changes, hence:
            if s1 != s2 and a1 != a2:
                if (s1 - a1) % 12 == 0 and (s2 - a2) % 12 == 0:
                    err_count += 1
                    errs.append("Chords {0}{1} : S/A consecutive Unison/Octave".
                                format(i+1, i+2))
                elif s1 - a1 in (7, 19, 31) and s2 - a2 in (7, 19, 31):
                    err_count += 1
                    errs.append("Chords {0}{1} : S/A consecutive Fifths".
                                format(i+1, i+2))
            
            if s1 != s2 and t1 != t2:
                if (s1 - t1) % 12 == 0 and (s2 - t2) % 12 == 0:
                    err_count += 1
                    errs.append("Chords {0}{1} : S/T consecutive Unison/Octave".
                                format(i+1, i+2))
                elif s1 - t1 in (7, 19, 31, 43) and s2 - t2 in (7, 19, 31, 43):
                    err_count += 1
                    errs.append("Chords {0}{1} : S/T consecutive Fifths".
                                format(i+1, i+2))
                    
            if s1 != s2 and b1 != b2:
                if (s1 - b1) % 12 == 0 and (s2 - b2) % 12 == 0:
                    err_count += 1
                    errs.append("Chords {0}{1} : S/B consecutive Unison/Octave".
                                format(i+1, i+2))
                elif s1 - b1 in (7, 19, 31, 43) and s2 - b2 in (7, 19, 31, 43):
                    err_count += 1
                    errs.append("Chords {0}{1} : S/B consecutive Fifths".
                                format(i+1, i+2))

            if a1 != a2 and t1 != t2:
                if (a1 - t1) % 12 == 0 and (a2 - t2) % 12 == 0:
                    err_count += 1
                    errs.append("Chords {0}{1} : A/T consecutive Unison/Octave".
                                format(i+1, i+2))
                elif a1 - t1 in (7, 19, 31) and a2 - t2 in (7, 19, 31):
                    err_count += 1
                    errs.append("Chords {0}{1} : A/T consecutive Fifths".
                                format(i+1, i+2))
                    
            if a1 != a2 and b1 != b2:
                if (a1 - b1) % 12 == 0 and (a2 - b2) % 12 == 0:
                    err_count += 1
                    errs.append("Chords {0}{1} : A/B consecutive Unison/Octave".
                                format(i+1, i+2))
                elif a1 - b1 in (7, 19, 31, 43) and a2 - b2 in (7, 19, 31, 43):
                    err_count += 1
                    errs.append("Chords {0}{1} : A/B consecutive Fifths".
                                format(i+1, i+2))
                    
            if t1 != t2 and b1 != b2:
                if (t1 - b1) % 12 == 0 and (t2 - b2) % 12 == 0:
                    err_count += 1
                    errs.append("Chords {0}{1} : T/B consecutive Unison/Octave".
                                format(i+1, i+2))
                elif t1 - b1 in (7, 19, 31) and t2 - b2 in (7, 19, 31):
                    err_count += 1
                    errs.append("Chords {0}{1} : T/B consecutive Fifths".
                                format(i+1, i+2))
                    
        if err_count:
            self.err_count += err_count
            self.err_detailed.append(("Consecutive intervals", err_count, errs))

    def check_chords(self):
        # checking for wrong chords (unrecognisable, or wrong dubling)
        pass






def check_harmony_rules(music_piece):
    piece = Piece(music_piece)
    piece.check_harmony()
    return piece
    
    


