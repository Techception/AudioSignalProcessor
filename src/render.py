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
VOLUME = 1
def waveEquation(time, frequency):
    w = (2*np.pi) * frequency    # Angular frequency 
    arg = w * time
    return VOLUME * np.sin(arg)



# <main>
def main():

    waves = list()
    time = 0 

    for frequency in sys.stdin:
        print(time, frequency)
        print(type(frequency))
        frequency = int(frequency.strip())
        a = waveEquation(time, frequency)
        waves.append(a)
        time += 1/SAMPLERATE;

    #print(len(waves), file=sys.stderr)
    #analysis.graph(**waves[-1],timefinal = 0.25)
    return None

if __name__ == '__main__':
    main()