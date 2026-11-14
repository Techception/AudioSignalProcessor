#!/usr/bin/env python3

# <import>
from numpy import array, int16
from math import exp, sin, pi
import time;
import threading;
import sys;
# </import>

# <variables>
PLAY = True; # flag to control playback
SAMPLE_RATE = 44100; # sample rate
frequency_hz = 320; # default frequency in Hz
chunk = 441 # number of samples to generate at a time
wait = chunk / SAMPLE_RATE # time to wait between chunks in seconds
index = 0
decay = 0
sustain = 10 # number of chunks to sustain before decaying
# </variables>

# <functions>
# <generator>  
amplitude = lambda f, t: exp(-decay/50)*sin(2 * pi * f * t)
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
    global PLAY
    global frequency_hz
    global decay
    global sustain
    exitCode = 1

    #promt_in = None
    #promt_out = None
    promt_in = "Enter new frequency in Hz (or 'q' to quit): "
    #print(promt_in, file=sys.stderr, flush=True)
    user_input = input()
    decay = 0 #reset decay when user input is received
    sustain = 10 #reset sustain when user input is received
    # <check for quit command>
    if user_input.lower() == 'q':
        PLAY = False
        print("\nExiting...", file=sys.stderr, flush=True)
        exitCode = 0
        return exitCode

    # <try to convert user input to float and update frequency>
    try:
        new_frequency = 100*float(user_input)
    except ValueError:
        new_frequency = 0 
    
    frequency_hz = new_frequency

    promt_out = f"Current frequency: {frequency_hz} Hz. Enter new frequency in Hz (or 'q' to quit): "
    print(promt_out, end='\r', file=sys.stderr, flush=True)
    
    exitCode = 0
    return exitCode
# </console_input>
# </functions> 

# <thread 1> play_thread: generates wave samples and sends them to stdout
def play_thread():
    global PLAY
    global index
    global decay
    global sustain
    # <range of time points to generate wave samples for/>
    while PLAY:
        generator()
        sustain -= 1
        if sustain <= 0:
            decay += 1 #increment decay for each chunk generated
        #print(decay, end='\r', file=sys.stderr, flush=True)
        # <update index and wait for next chunk/>
        index += chunk
        time.sleep(wait*22/23)  # Sleep for the duration of the chunk

    return None
# </thread 1>

# <thread 2> input_thread: reads user input and updates frequency
def input_thread():
    global PLAY
    while PLAY:
        console_input()
# </thread 2>

# <main>
def main():
    # <define threads>
    threads = {};
    threads['play'] = threading.Thread(target=play_thread)
    threads['input'] = threading.Thread(target=input_thread)
    # </define threads>

    # <threads>
    threads['play'].start()
    threads['input'].start()
    # </threads>
# </main>

if __name__ == '__main__':
    main()


# <usage>
# python3 src/render.py | ffplay -f s16le -ar 44100 -ch_layout mono -nodisp - 2> /dev/null 
# ./experiment/input.sh | ./src/render.py | ffplay -f s16le -ar 44100 -ch_layout mono -nodisp -
# ./program/src/interface/input.sh | ./src/render.py | ffplay -f s16le -ar 44100 -ch_layout mono -nodisp -fflags nobuffer -flags low_delay -
# </usage>