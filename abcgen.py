#!/bin/python3

from random import choice

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

intervals = [4, 7, 1]
direction = [-1, 1]







def main():

    third = 4
    fifth = 7
    octave = 12
    note = 18
    body = ""
    num_notes = len(notes)
    
    for count in range(32):
        if 0 == count % 8:
            body += "|"
        elif 0 == count % 4:
            body += " "            
        note = note +  intervals[  (count % 3)] * choice(direction)
        if note >= num_notes:
            note -= num_notes
        if note < 0:
            note += num_notes
        body += notes[note]
    
    with open('garzone.abc', 'w') as f:
        f.write(header)
        f.write(body)

if __name__ == "__main__":
    # execute only if run as a script
    main()
