#!/usr/bin/env python3

# <import>
from numpy import array, int16
from math import exp, sin, pi
import time;
import threading;
import sys;
from dataclasses import dataclass;
# </import>

# <variables>
@dataclass
class AudioState:
    PLAY: bool = True
    SAMPLE_RATE: int = 44100
    frequency_hz: float = 320
    chunk: int = 441
    wait: float = 441 / 44100
    index: int = 0
    decay: int = 0
    sustain: int = 10
    current: str = ""
# </variables>

# <functions>
# <generator>  
amplitude = lambda f, t: sin(2 * pi * f * t)
def generator(state):
    t_i = [(state.index + i) / state.SAMPLE_RATE for i in range(state.chunk)]
    waveChunk = [exp(-state.decay / 50) * amplitude(state.frequency_hz, t) for t in t_i]
    sound_chunk = (array(waveChunk) * 32767).astype(int16).tobytes()
    # <send wave samples to stdout/>
    sys.stdout.buffer.write(sound_chunk)
    sys.stdout.buffer.flush()
# </generator>

# <console_input> read user input and update frequency
def console_input(state):
    exitCode = 1

    user_input = input()
    if user_input != state.current:
        state.decay = 0 #reset decay when user input is received
    state.current = user_input.strip()
    state.sustain = 10 #reset sustain when user input is received
    
    # <check for quit command>
    if user_input.lower() == 'q':
        state.PLAY = False
        print("\nExiting...", file=sys.stderr, flush=True)
        exitCode = 0
        return exitCode

    # <try to convert user input to float and update frequency>
    try:
        new_frequency = 100*float(user_input)
    except ValueError:
        new_frequency = 0 
    
    state.frequency_hz = new_frequency

    promt_out = f"Current frequency: {state.frequency_hz} Hz. Enter new frequency in Hz (or 'q' to quit): "
    print(promt_out, end='\r', file=sys.stderr, flush=True)
    
    exitCode = 0
    return exitCode
# </console_input>
# </functions> 

# <thread 1> play_thread: generates wave samples and sends them to stdout
def play_thread(state):
    # <range of time points to generate wave samples for/>
    while state.PLAY:
        generator(state)
        state.sustain -= 1
        if state.sustain <= 0:
            state.decay += 1 #increment decay for each chunk generated
        print(state.decay, end='\r', file=sys.stderr, flush=True)
        # <update index and wait for next chunk/>
        state.index += state.chunk
        time.sleep(state.wait*22/23)  # Sleep for the duration of the chunk

    return None
# </thread 1>

# <thread 2> input_thread: reads user input and updates frequency
def input_thread(state):
    #global PLAY
    while state.PLAY:
        console_input(state)
# </thread 2>

# <main>
def main():
    playstate = AudioState()
    # <define threads>
    threads = {};
    threads['play'] = threading.Thread(target=play_thread, args=(playstate,))
    threads['input'] = threading.Thread(target=input_thread, args=(playstate,))
    # </define threads>

    # <threads>
    threads['play'].start()
    threads['input'].start()
    # </threads>
# </main>

if __name__ == '__main__':
    main()
