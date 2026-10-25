import sys
import numpy as np
import argparse
import matplotlib.pyplot as plt

#get frequency information from the commandline arguments
parser = argparse.ArgumentParser();
parser.add_argument("f", type=int, help="tonic frequency in Hz");
args = parser.parse_args();

#statics 
#for now just a 10 second wave at 44100 sampling 
duration = 10 #length of note in seconds 
fs = 44100 #sample rate

#this defines the numberline on which the wave is rendered 
totalSamples = fs*duration
t = np.linspace(
    0, #beginning of number line in this case t = 0 
    duration, #total duration that the sound plays 
    totalSamples #the number of samples will determine the resolution of the time index 
) #time index 

tone = np.sin((2)*(np.pi)*(args.f)*(t)) #the sound wave

plt.plot(t,tone) #plot of the wave for illustration 

pcm = (tone*32767).astype(np.int16)
#sys.stdout.buffer.write(pcm.tobytes())
