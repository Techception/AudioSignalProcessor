import sys
import numpy as np

duration = sys.argv[1] 
duration = int(duration)
fs = 44100
t = np.linspace(0,duration,fs*duration)
tone = np.sin(2*np.pi*440*t)

pcm = (tone*32767).astype(np.int16)
sys.stdout.buffer.write(pcm.tobytes())
