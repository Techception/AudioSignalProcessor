####################################################################################
####################################################################################

import sys
import argparse
import matplotlib.pyplot as plt
import numpy as np
from numpy import pi, sin

####################################################################################
####################################################################################

#get frequency information from the commandline arguments
parser = argparse.ArgumentParser();
parser.add_argument("--mode", type=str, help="music mode?");
parser.add_argument("--pitch", type=str, help="tonic frequency in Hz");
parser.add_argument("--length", type=str, help="Duration of note in seconds");
args = parser.parse_args();
print(args.mode)

####################################################################################
####################################################################################

#STATICS
fs = 44100 # sample rate

####################################################################################
####################################################################################

bpm = 60 # change in future 
def pitchMap(range):
    pitchs = ('a', 'a#', 'b', 'c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#')
    range = [int(i) for i in list(range)]
    pitchToFrequency = zip(pitchs,range)
    notesPitch = dict(pitchToFrequency)
    return notesPitch

def musicalConversion():
    #beat note to duration 
    notesLength = {'1': 60/bpm,'1/2': 60/bpm/2, '1/4': 60/bpm/4, '1/8': 60/bpm/8, '1/32': 60/bpm/32};

    #wave frequency and time description of sound 
    if args.mode == 'hz':                  # time frequency description
        notePitch = int(args.pitch)        # frequency in Hz
        noteLength = int(args.length)      # length of note in seconds 
        return {'pitch':notePitch, 'length': noteLength} ##e.g. {'pitch': 440, 'length: 1}

    #Musical Tone to concert frequency (spaced interval): 
    if args.mode == 'spaced':  # equal spaced notes
        range = np.linspace(440,880,12)
        notesPitch = pitchMap(range)
        notePitch = notesPitch[args.pitch]
        noteLength = notesLength[args.length]
        return {'pitch':notePitch, 'length': noteLength}
    
    #Musical Tone to concert frequency (Equal Temperment):
    if args.mode == 'EqT':  # Equal Temperment
        range = 440*2**(np.arange(12)/12)
        notesPitch = pitchMap(range)
        notePitch = notesPitch[args.pitch]
        noteLength = notesLength[args.length]
        return {'pitch':notePitch, 'length': noteLength}

####################################################################################
####################################################################################

note = musicalConversion()
frequency = note['pitch'] # frequency in Hz
duration = note['length'] # length of note in seconds 
#end of conditional 
print("frequency",frequency)
print("duration", duration)

####################################################################################
####################################################################################

#Calculations
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

#Analysis
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

if __name__ == '__main__':
    
    waveData = wave(sampleRate = fs, duration =  duration, frequency = frequency, amplitude = 1)
    waveEquation = waveData['func']
    waveTimeRange = waveData['timeRange'] 
    wavePCM = waveData['bytes']

    #graph (title = frequency, wave = waveEquation, time = waveTimeRange, timefinal = 0.25)
    sys.stdout.buffer.write(wavePCM)
