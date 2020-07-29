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

accidents = {}


def constrain(note):
    if note >= len(notes):
        print("dropping\n")
        note -= octave
    if note < 0:
        print("raising\n")
        note += octave
    return note

def gen_intervals(note):
    #Add these values to the root to get the chord tone
    root = 0
    up_third = 4
    up_fifth = 7
    up_root = octave
    down_root = -octave
    down_fifth = -5
    down_third = -8
    
    inversions = [[root, up_third, up_fifth],
                  [root, up_fifth, up_third],
                  [up_third, up_fifth, root],
                  [up_third, root, up_fifth],
                  [up_fifth, root, up_third],
                  [up_fifth, up_third, root],


                  [up_third, down_fifth, root],
                  [up_third, root, down_fifth],
                  [down_fifth, root, up_third],
                  [down_fifth, up_third, root],


                  [down_third, up_fifth, root],
                  [down_third, root, up_fifth],
                  [up_fifth, root, down_third],
                  [up_fifth, down_third, root],

                  
                  [up_third, up_fifth, up_root],
                  [up_third, up_root, up_fifth],
                  [up_fifth, up_root, up_third],
                  [up_fifth, up_third, up_root],
                  
                  [root, down_third, down_fifth],
                  [root, down_fifth, down_third],
                  [down_third, down_fifth, root],
                  [down_third, root, down_fifth],
                  [down_fifth, root, down_third],
                  [down_fifth, down_third, root],

                  [down_third, down_fifth, down_root],
                  [down_third, down_root, down_fifth],
                  [down_fifth, down_root, down_third],
                  [down_fifth, down_third, down_root],                  
                  
    ]
    
    inversion = randrange(len(inversions))
#+ randrange(-1, 0)  *  octave
    find_root = constrain(note - inversions[inversion][0])    
    note2 = constrain(find_root + inversions[inversion][1])
    note3 = constrain(find_root + inversions[inversion][2])
    tones = [note, note2, note3]
    return tones

def print_note(note, count):

    global accidents
    calculated = notes[note]
    letter = calculated[0]
    if calculated[0]  == "^":
        letter = calculated[1] 
        accidents[letter] = "^"
    elif accidents.get(letter) == "^":
        accidents[letter] = ""
        calculated = "=" + calculated

    if 0 == count % 8:
        calculated = "|" + calculated
        accidents = {}
    elif 0 == count % 4:
        calculated = " " + calculated
        
    return calculated

def gen_file():
    global accidents
    note = 18
    body = ""
    count = 0
    while(count < 64):
        intervals = gen_intervals(note)
        for i in intervals:
            body += print_note(i, count)
            count += 1
        # generate 1-3 chromatic notes.  The last chromatic note
        # becomes the basis for the next triad
        num_chroms =  randrange(2)

        for i in range(num_chroms):
            note = constrain(note + choice(direction))
            body += print_note(note, count)
            count += 1
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
