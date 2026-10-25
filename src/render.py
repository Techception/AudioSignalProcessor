import sys
import numpy as np
import argparse

parser = argparse.ArgumentParser();
parser.add_argument("f", type=int, help="tonic frequency in Hz");
args = parser.parse_args();

duration = 10 #length of note in seconds 

fs = 44100 #sample rate
t = np.linspace(0,duration,fs*duration) #time index 

tone = np.sin((2)*(np.pi)*(args.f)*(t)) #the sound wave

pcm = (tone*32767).astype(np.int16)
sys.stdout.buffer.write(pcm.tobytes())
