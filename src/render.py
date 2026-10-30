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
#<import/>

import sys;
import argparse;
import matplotlib.pyplot as plt;
import numpy as np;
from numpy import pi, sin;



####################################################################################
####################################################################################

#STATICS
fs = 44100 # sample rate

####################################################################################
####################################################################################
# <Convertions>
# convert musical notation into frequency and seconds 

bpm = 60 # change in future 
def pitchMap(range) -> dict:
    pitchs = ('a', 'a#', 'b', 'c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#')
    range = [int(i) for i in list(range)]
    pitchToFrequency = zip(pitchs,range)
    notesPitch = dict(pitchToFrequency)
    return notesPitch

def noteToPitch(range: np.linspace, pitch: str, length: str, notesLength: dict) -> dict:
        range = np.linspace(440,880,12)
        notesPitch = pitchMap(range)
        notePitch = notesPitch[pitch]
        noteLength = notesLength[length]
        note = {'pitch':notePitch, 'length': noteLength}
        #print('note:', note)
        return note 

def musicalConversion(mode:str, pitch: str, length: str) -> dict:
    #beat note to duration 
    notesLength = {'1': 60/bpm,'1/2': 60/bpm/2, '1/4': 60/bpm/4, '1/8': 60/bpm/8, '1/32': 60/bpm/32};

    #wave frequency and time description of sound 
    if mode == 'hz':                  # time frequency description
        #print("mode:", mode)
        notePitch = int(pitch)        # frequency in Hz
        noteLength = int(length)      # length of note in seconds 
        note = {'pitch':notePitch, 'length': noteLength} ##e.g. {'pitch': 440, 'length: 1}
        return note

    #Musical Tone to concert frequency (spaced interval): 
    if mode == 'spaced':  # equal spaced notes
        #print("mode:", mode)
        spaced = np.linspace(440,880,12)
        note = noteToPitch(range= spaced, pitch= pitch, length= length, notesLength= notesLength)
        return note
    
    #Musical Tone to concert frequency (Equal Temperment):
    if mode == 'EqT':  # Equal Temperment
        #print("mode:", mode)
        EqT = 440*2**(np.arange(12)/12)
        note = noteToPitch(range= EqT, pitch= pitch, length= length, notesLength=notesLength)
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
# <Analysis>

def graph (
        title: str = "waveform"
        ,wave: np.ndarray = np.linspace(0,0,0)
        ,time: np.ndarray = np.linspace(0,(2*pi),360)
        ,timefinal: float = 1
        ) -> None:
    #plot graph with title and axis 
    plt.plot(time, wave)
    plt.xlabel("Time (seconds)")
    plt.ylabel("Amplitude")
    plt.title(f"{title} Hz sine wave")
    plt.xlim(0, timefinal)  # show the first 0.01 seconds
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"wave.png", dpi=150)
    #plt.show()
    return None

####################################################################################
####################################################################################
#<main>

if __name__ == '__main__':
    #get frequency information from the commandline arguments
    parser = argparse.ArgumentParser();
    parser.add_argument("--mode", type=str, help="music mode?");
    parser.add_argument("--pitch", type=str, help="tonic frequency in Hz");
    parser.add_argument("--length", type=str, help="Duration of note in seconds");
    args = parser.parse_args();
    print(args)

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

    #graph (title = frequency, wave = waveEquation, time = waveTimeRange, timefinal = 0.25)
    sys.stdout.buffer.write(wavePCM)
