import sys
import numpy as np
from numpy import pi, sin
import argparse
import matplotlib.pyplot as plt
####################################################################################
#STATICS
fs = 44100 # sample rate
#beat note to duration 
bpm = 60 # change in future 
notesLength = {'1': 60/bpm,'1/2': 60/bpm/2, '1/4': 60/bpm/4, '1/8': 60/bpm/8, '1/32': 60/bpm/32};
print("notesLength", notesLength)

#frequency to pitch: 
if sys.argv[1] == 'spaced':  # equal spaced notes
    range = np.linspace(440,880,12)
    range = [int(i) for i in list(range)]
    pitchs = ('a', 'a#', 'b', 'c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#')
    pitchToFrequency = zip(pitchs,range)
    notesPitch = dict(pitchToFrequency)
    print("notesPitch", notesPitch)

if sys.argv[1] == 'EqT':  # Equal Temperment
    range = 440*2**(np.arange(12)/12)
    range = [int(i) for i in list(range)]
    pitchs = ('a', 'a#', 'b', 'c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#')
    pitchToFrequency = zip(pitchs,range)
    notesPitch = dict(pitchToFrequency)
    print("notesPitch", notesPitch)
####################################################################################
#get frequency information from the commandline arguments
parser = argparse.ArgumentParser();
parser.add_argument("mode", type=str, help="music mode?");
parser.add_argument("f", type=str, help="tonic frequency in Hz");
parser.add_argument("t", type=str, help="Duration of note in seconds");
args = parser.parse_args();
#conditional
if sys.argv[1] == 'hz':            # time frequency description
    #arguments to variables 
    frequency = int(args.f)        # frequency in Hz
    duration = int(args.t)         # length of note in seconds 
    resolution = 1
else: #musical description
    #arguments to variables 
    frequency = notesPitch[args.f] # frequency in Hz
    duration = notesLength[args.t] # length of note in seconds 
    resultion = bpm*32
#end of conditional 
print("frequency",frequency)
print("duration", duration)
####################################################################################
#Calculations
def wave(sampleRate: int = 0, duration: float = 0, Amplitude: int = 1, frequency: int = 0):
    totalSamples = sampleRate*duration  # total datapoints (float)
    A = Amplitude;                      # Max Amplitude 
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
    data = {'func': wave, 'timeRange':time, 'bin': pcm}
    return data
    
    #Debugging
    print("total samples:", totalSamples);
    print('Time range:',time);

#Analysis
def graph (
        title: str = "waveform"
        ,wave: np.ndarray = np.linspace(0,0,0)
        ,time: np.ndarray = np.linspace(0,(2*np.pi),360)
        ,Timefinal: float = 1
        ) -> None:
    #plot graph with title and axis 
    plt.plot(time, wave)
    plt.xlabel("Time (seconds)")
    plt.ylabel("Amplitude")
    plt.title(f"{title} Hz sine wave")
    plt.xlim(0, Timefinal)  # show the first 0.01 seconds
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"wave.png", dpi=150)
    #plt.show()
    return None

if __name__ == '__main__':
    
    waveData = wave(sampleRate = fs, duration =  duration, Amplitude = 1, frequency = frequency)
    waveEquation = waveData['func']
    waveTimeRange = waveData['timeRange'] 
    wavePCM = waveData['bin']

    graph (title = frequency, wave = waveEquation, time = waveTimeRange, Timefinal = 0.25)
    sys.stdout.buffer.write(wavePCM.tobytes())
