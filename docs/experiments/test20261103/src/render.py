# <import/>

import sys;
import argparse;
import matplotlib.pyplot as plt;
import numpy as np;
from numpy import pi, sin;
# synth modules:
import converter
import analysis
import calculations
####################################################################################
####################################################################################

MODE = 'eqt'
SAMPLERATE = 44100 # sample rate
TEMPERMENT = converter.pitchMap(MODE)

# <main>
def main():

    waves = list()
    try:
        while True:
            print('Enter note in format: duration,tone', file=sys.stderr)
            input_note = input().split(',')
            note = converter.noteBuilder(MODE, TEMPERMENT, *input_note)
            waveData = calculations.wave(**note)
            waves.append(waveData)
            sys.stdout.buffer.write(waveData['bytes'])
            sys.stdout.flush()
    except EOFError:
        pass

    #print(len(waves), file=sys.stderr)
    #analysis.graph(**waves[-1],timefinal = 0.25)
    return None

if __name__ == '__main__':
    main()