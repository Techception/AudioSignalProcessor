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
# <main>
def main(input_note):
    MODE = 'hz'
    SAMPLERATE = 44100 # sample rate

    
    note = converter.noteBuilder(MODE, *input_note)
    #print(f'note {note}')
    
    waveData = calculations.wave(**note)
    #waveEquation, waveTimeRange, wavePCM = waveData['func'], waveData['timeRange'], waveData['bytes']
    
    sys.stdout.buffer.write(waveData['bytes'])
    sys.stdout.flush()
    # analysis.graph(
    #     title = note['frequency']
    #     ,wave = waveData['func']
    #     ,time = waveData['timeRange']
    #     ,timefinal = 1/note['frequency']
    #     )
    return None

if __name__ == '__main__':
    try:
        while True:
            input_note = input('duration, tone: ').split(',')
            main(input_note)
    except EOFError:
        pass