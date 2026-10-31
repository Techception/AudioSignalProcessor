####################################################################################
####################################################################################
# Structure

"""
<render.py>
    <import/>
    <variables/>

    <def_functions>
        1.
        <Convertions>
            <def pitchMap(range)/>
            <def musicalConversion()/>
        </Convertions>
        
        2.
        <Calculations>
            <def wave(*defaults) -> dict>
                - wave equation
                - file data
            </def>
        <Calculations>
        
        3.
        <analysis>
            <def graph (*args) -> None/>
        </analysis>
    <def_functions>

    <main>
        - args = parseArguments()
        - note = musicalConversion(args)
        - waveData = wave(note)
        - graph(waveData)
        - stdout(waveData)
    </main>

</render.py>
"""


####################################################################################
####################################################################################
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
# <Calculations>

def arguments():
    parser = argparse.ArgumentParser();
    parser.add_argument("--mode", type=str, help="music mode?");    ## for converter 
    parser.add_argument("--sampleRate", type=str, help=""); ## todo ## for main program
    args = parser.parse_args();
    return args


####################################################################################
####################################################################################
# <main>
def main():
    args = arguments();
    #print('args:', args)
    SAMPLERATE = 44100 # sample rate

    input_note = (duration, tone) = input('duration, tone: ').split(',')
    print('')
    if args.mode == 'hz':                  # time frequency description
        note = {'duration': int(duration), 'frequency': int(tone)} ##e.g. {'pitch': 440, 'length: 1}
    else:
        note = converter.noteBuilder(note= input_note)
    print(f'note {note}')
    
    waveData = calculations.wave(**note)
    waveEquation, waveTimeRange, wavePCM = waveData['func'], waveData['timeRange'], waveData['bytes']
    
    #sys.stdout.buffer.write(wavePCM)
    analysis.graph(title = note['frequency'], wave = waveEquation, time = waveTimeRange, timefinal = 0.25)
    return None

if __name__ == '__main__':
    #get frequency information from the commandline arguments
    main()