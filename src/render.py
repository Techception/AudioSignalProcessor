import sys
import numpy as np
import argparse
import matplotlib.pyplot as plt

#STATICS
fs = 44100 #sample rate
#frequency to pitch: 
range = np.linspace(440,880,12)
range = [int(i) for i in list(range)]
pitchs = ('a', 'a#', 'b', 'c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#')
pitchToFrequency = zip(pitchs,range)
notesPitch = dict(pitchToFrequency)
#beat note to duration 
bpm = 60 #change in future 
notesLength = {'1': 60/bpm,'1/2': 60/bpm/2, '1/4': 60/bpm/4, '1/8': 60/bpm/8, '1/32': 60/bpm/32};

#get frequency information from the commandline arguments
parser = argparse.ArgumentParser();
parser.add_argument("mode", type=int, help="music mode?");
#conditional
if sys.argv[1] == 0:
    #time frequency description
    parser.add_argument("f", type=int, help="tonic frequency in Hz");
    parser.add_argument("t", type=int, help="Duration of note in seconds");
    args = parser.parse_args();
    #arguments to variables 
    frequency = args.f #frequency in Hz
    duration = args.t #length of note in seconds 
    
else:
    #musical description
    parser.add_argument("f", type=str, help="note key in musical notation");
    parser.add_argument("t", type=int, help="Duration as relative musical notes");
    args = parser.parse_args();
    #arguments to variables 
    frequency = notesPitch[args.f] #frequency in Hz
    duration = notesLength[args.t] #length of note in seconds 
#end of conditional 




#this defines the numberline on which the wave is rendered 
totalSamples = fs*duration
t = np.linspace(
    0, #beginning of number line in this case t = 0 
    duration, #total duration that the sound plays 
    totalSamples #the number of samples will determine the resolution of the time index 
) #time index 

tone = np.sin((2)*(np.pi)*frequency*(t)) #the sound wave

plt.plot(t, tone)
plt.xlabel("Time (seconds)")
plt.ylabel("Amplitude")
plt.title(f"{frequency} Hz sine wave")
plt.xlim(0, 0.25)  # show the first 0.01 seconds
plt.grid(True)
plt.tight_layout()
plt.savefig(f"wave.png", dpi=150)
#plt.show()

pcm = (tone*32767).astype(np.int16)
sys.stdout.buffer.write(pcm.tobytes())
