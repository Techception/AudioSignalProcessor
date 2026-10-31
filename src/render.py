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
import converter
import analysis

####################################################################################
####################################################################################

#STATICS
fs = 44100 # sample rate

####################################################################################
####################################################################################
# <Convertions>
# convert musical notation into frequency and seconds 

def musicalConversion(mode:str, pitch: str, length: str) -> dict:
    #wave frequency and time description of sound 
    #print("mode:", mode)

    #Musical Tone to concert frequency (spaced interval): 
    if mode == 'spaced':  # equal spaced notes
        spaced = np.linspace(440,880,12)
        note = converter.noteToPitch(range= spaced, pitch= pitch, length= length)
        return note
    
    #Musical Tone to concert frequency (Equal Temperment):
    if mode == 'EqT':  # Equal Temperment
        EqT = 440*2**(np.arange(12)/12)
        note = converter.noteToPitch(range= EqT, pitch= pitch, length= length)
        return note

####################################################################################
####################################################################################
# <Calculations>

def wave(sampleRate: int = 0, duration: float = 0, frequency: int = 0, amplitude: int = 1) -> dict:
    totalSamples = sampleRate*duration  # total datapoints (float)
    A = amplitude;                      # Max Amplitude 
    F = frequency;
    W = (2*pi) * F;                     # Angular frequency
    
    #this defines the numberline on which the wave is rendered 
    totalSamples = int(totalSamples)    # total datapoints (integer)
    #Get the time range = duration of wave
    time = np.linspace( 
        0,           # beginning of number line in this case t = 0 
        duration,    # total duration that the sound plays 
        totalSamples # the number of samples will determine the resolution of the time index 
    ) # time index 

    #Generate waves
    #A(t) = A x sin(2 x pi x f x t)
    wave = A*sin(W * time)           # Mathematical wave
    pcm = (wave*32767).astype(np.int16) # the digital file data
    pcm = pcm.tobytes()
    data = {'func': wave, 'timeRange':time, 'bytes': pcm}
    
    #Debugging
    #print("total samples:", totalSamples);
    #print('Time range:',time);
    return data

####################################################################################
####################################################################################
def arguments():
    parser = argparse.ArgumentParser();
    parser.add_argument("--mode", type=str, help="music mode?");    ## for converter 
    parser.add_argument("--temperment", type=str, help=""); ## todo ## for converter 
    parser.add_argument("--sampleRate", type=str, help=""); ## todo ## for main program
    parser.add_argument("--pitch", type=str, help="tonic frequency in Hz");        ## change to stdin 
    parser.add_argument("--length", type=str, help="Duration of note in seconds"); ## change to stdin 
    args = parser.parse_args();
    return args


####################################################################################
####################################################################################
# <main>
def main():
    args = arguments();
    #print('args:', args)

    if args.mode == 'hz':                  # time frequency description
        notePitch = int(args.pitch)        # frequency in Hz
        noteLength = int(args.length)      # length of note in seconds 
        note = {'pitch':notePitch, 'length': noteLength} ##e.g. {'pitch': 440, 'length: 1}
    else:
        note = musicalConversion(mode= args.mode, pitch= args.pitch, length= args.length)
    
    frequency = note['pitch'] # frequency in Hz
    duration = note['length'] # length of note in seconds 
    #end of conditional 
    #print("frequency",frequency)
    #print("duration", duration)
    
    waveData = wave(sampleRate = fs, duration =  duration, frequency = frequency, amplitude = 1)
    waveEquation = waveData['func']
    waveTimeRange = waveData['timeRange'] 
    wavePCM = waveData['bytes']
    
    sys.stdout.buffer.write(wavePCM)
    #analysis.graph(title = frequency, wave = waveEquation, time = waveTimeRange, timefinal = 0.25)
    return None

if __name__ == '__main__':
    #get frequency information from the commandline arguments
    main()



