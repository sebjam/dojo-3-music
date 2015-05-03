'''
Requires Musescore and timidity 
'''

import random
import os
import sys
from subprocess import call

from music21 import note, stream, instrument

VALID_NOTES = [i+k+str(j)  for j in [3,4,5] for i in 'abcdefg' for k in ['', '#']]

KEYS = {
        'c-major':
    [
        {'c', 'e', 'g'},
        {'d', 'f', 'a'},
        {'e', 'g', 'b'},
        {'f', 'a', 'c'},
        {'g', 'b', 'd'},
        {'a', 'c', 'e'},
    ]
}

def progression(key, bars=8):
    first = None
    for bar in range(bars):
        if bar == bars - 1:
            chord = first
        else:
            chord = random.choice(KEYS[key])
        if first is None:
            first = chord
        yield chord

def notes(prog):
    for bar in prog:
        beats = 0
        while beats < 4:
            n = random.choice(VALID_NOTES)
            while n[:-1] not in bar:
                n = random.choice(VALID_NOTES)
            beats += 1
            yield note.Note(n)

def random_score(key='c-major'):
    meas1 = stream.Measure()
    meas2 = stream.Measure()
    prog = list(progression(key))
    n1 = notes(prog)
    n2 = notes(prog)
    for curr_note1, curr_note2 in zip(n1, n2):
        meas1.append(curr_note1)
        meas2.append(curr_note2)
        print (curr_note1, curr_note2),

    score = stream.Score()

    part1 = stream.Part()
    part1.insert(instrument.Piano())
    part1.append(meas1)
    score.append(part1)

    part2 = stream.Part()
    part2.insert(instrument.Viola())
    part2.append(meas2)
    score.append(part2)

    return score

if __name__ == '__main__':
    filename = sys.argv[1]

    random_score().write(fp="{}.xml".format(filename))

    # Musescore to convert xml to midi
    call(["mscore", "{}.xml".format(filename), "-o", "{}.mid".format(filename)])

    # Musescore to convert xml to midi
    call(["mscore", "{}.xml".format(filename), "-o", "{}.pdf".format(filename)])

    # Play with Timidity
    call(["timidity", "{}.mid".format(filename)])

