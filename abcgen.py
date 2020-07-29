#!/bin/python3

from random import choice
from random import randrange
header="""
X:1
T:Chromatic Triadic
M:4/4
C:Automated
K:C
L: 1/8
"""

notes = ["A,", "^A,", "B,","^B,",
         "C",  "^C",  "D", "^D",
         "E",   "F", "^F",  "G",
        "^G",   "A", "^A",  "B",
         "c",  "^c",  "d", "^d",
         "e",   "f", "^f",  "g",
        "^g",   "a", "^a",  "b",
        "c'",  "^c'", "d'","^d'",
        "e'",   "f'","^f'", "g'"]

octave = 12
intervals = [4, 7, 1]
direction = [-1, 1]
old_note = -1


def constrain(note):
    if note >= len(notes):
        note -= octave
    if note < 0:
        note += octave
    return note

def gen_intervals(note):
    #Add these values to the root to get the chord tone
    root = 0
    third = 4
    fifth = 7
    inversions = [[root, third, fifth],
                  [third, fifth, root],
                  [fifth, root, third]]
    inversion = randrange(3)

    find_root = constrain(note - inversions[inversion][0])
    
    note2 = constrain(find_root + inversions[inversion][1]
                      + randrange(-1, 0)  *  octave)
    note3 = constrain(find_root + inversions[inversion][2]
                      + randrange(-1, 0)  * octave)
    tones = [note, note2, note3]
    return tones

def print_note(note):
    global old_note
    
    if note == old_note:
        import pdb; pdb.set_trace()

    note = constrain(note)
    old_note = note
    return notes[note]

def gen_file():
    third = 4
    fifth = 7
    octave = 12
    note = 18
    body = ""

    count = 0
    while(count < 64):
        if 0 == count % 8:
            body += "|"
        elif 0 == count % 4:
            body += " "
        intervals = gen_intervals(note)
        for i in intervals:
            note = constrain(i)
            count += 1
            body += print_note(note)
        # generate one note ove the chromatic run here, and the second note
        # becomes the basis for the next triad 
        note = constrain(note + choice(direction))
        count += 1
        body += print_note(note)
        note = constrain(note + choice(direction))
    body += "|"
            
    with open('garzone.abc', 'w') as f:
        f.write(header)
        f.write(body)

def main():
    gen_file()
        
if __name__ == "__main__":
    # execute only if run as a script
    main()
