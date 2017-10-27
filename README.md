# Introduction

CMC v. 0.1.0

CheckMyChords is a simple Django app that enables user to add short choral sequences to database and check if they obey some basic harmony rules.
The piece can be checked using some (or all) selected rules. The rules covered so far include:
* Natural vocal ranges of voices
* Some of restricted intervals (leaps of a seventh and leaps bigger than an octave)
* Correct distances between voices and not crossing voices
* Restricted paralels: consecutive and anticonsecutive unisons, perfect fifths and octaves
The most basic chord modes (minor, major, with added minor seventh) and functions (T, S, D, D7, Tvi) are recognised:
* Using unrecognised chord
* Wrong doubling (in Tvi the third CAN be doubled)
* Using foreign notes in a chord (apart from minor seventh)
Are treated as a mistake. 
The user can then see a list of all mistakes made with proper description (where and what rule has been broken)
The user can always recheck any piece from database using different set of rules.

It's also possible to generate (and download) a midi file of the piece. (Uses JQuery & AJAX to do it without reloading the page).
The midi file is then also stored on the server and isn't generated again if needed.

CMC started as a CodersLab school final project

CMC uses pyknon library (https://github.com/kroger/pyknon)

# Major TODOs

* Adding more harmony rules&logic!
  * All voices going in the same direction
  * Add more recognised chords (Dvii, D9>, D64)
  * Checking chords in context (e.g. subdominant shouldn't occur after a dominant)
* Add tests and demo
* Limit pyknon libraty usage to midi generation and write own Note class instead, that should distinguish enharmonic equivalent notes. Currently it's impossible and that leads to major problems - e.g. treating (D, E#, A) as a legitimate D minor chord, which makes some harmonic rules impossible to implement.

# License

This library is released under a MIT license. See the [LICENSE](LICENSE.md) file for
more details.


