#!/usr/bin/env python3

# <import>
from numpy import array, int16
from math import sin, pi
import time;
import threading;
import sys;
# </import>

# <variables>
SAMPLE_RATE = 44100; # sample rate
frequency_hz = 320; # default frequency in Hz
chunk = 441 # number of samples to generate at a time
wait = chunk / SAMPLE_RATE # time to wait between chunks in seconds
index = 0
# </variables>

# <functions>
# <generator>  
amplitude = lambda f, t: sin(2 * pi * f * t)
def generator():
    t_i = [(index + i) / SAMPLE_RATE for i in range(chunk)]
    waveChunk = [amplitude(frequency_hz, t) for t in t_i]
    sound_chunk = (array(waveChunk) * 32767).astype(int16).tobytes()
    # <send wave samples to stdout/>
    sys.stdout.buffer.write(sound_chunk)
    sys.stdout.buffer.flush()
# </generator>

# <console_input> read user input and update frequency
def console_input():
    global frequency_hz

    #promt_in = None
    #promt_out = None
    promt_in = "Enter new frequency in Hz (or 'q' to quit): "
    promt_out = f"Current frequency: {frequency_hz} Hz. Enter new frequency in Hz (or 'q' to quit): "
    print(promt_in, file=sys.stderr, flush=True)
    user_input = input()
    try:
        new_frequency = 100*float(user_input)
    except ValueError:
        new_frequency = 0 
    frequency_hz = new_frequency
    print(promt_out, file=sys.stderr, flush=True)
    return None
# </console_input>
# </functions> 

# <thread 1> play_thread: generates wave samples and sends them to stdout
def play_thread():
    global index
    # <range of time points to generate wave samples for/>
    while True:
        generator()
        # <update index and wait for next chunk/>
        index += chunk
        time.sleep(wait)  # Sleep for the duration of the chunk
# </thread 1>

# <thread 2> input_thread: reads user input and updates frequency
def input_thread():
    while True:
        console_input()
# </thread 2>

# <main>
def main():
    # <define threads>
    threads = {};
    threads['play'] = threading.Thread(target=play_thread)
    threads['input'] = threading.Thread(target=input_thread)
    # </define threads>

    # <start threads>
    threads['play'].start()
    threads['input'].start()
    # </start threads>
    return 0

if __name__ == '__main__':
    main()
# </main>

# <usage>
# python3 src/render.py | ffplay -f s16le -ar 44100 -ch_layout mono -nodisp - 2> /dev/null 
# ./experiment/input.sh | ./src/render.py | ffplay -f s16le -ar 44100 -ch_layout mono -nodisp -
# ./program/src/interface/input.sh | ./src/render.py | ffplay -f s16le -ar 44100 -ch_layout mono -nodisp -fflags nobuffer -flags low_delay -
# </usage>