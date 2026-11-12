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
# </variables>

# <Calculations>
# generate amplitude of wave at time t 
# A(t) = A x sin(2 x pi x f x t)
# t = index/SAMPLE_RATE # time in seconds related to number of samples
def sample(f, index):
    return sin(2 * pi * f * index / SAMPLE_RATE)
# </Calculations>

# <generator> 
# perpetuates the wave generation over time
def play_thread():
    global frequency_hz
    index = 0
    chunk = 441 # number of samples to generate at a time
    while True:
        sound_chunk = array([sample(frequency_hz, index + i) * 32767 for i in range(chunk)], dtype=int16)
        sys.stdout.buffer.write(sound_chunk.tobytes())
        sys.stdout.buffer.flush()
        index += chunk
        #time.sleep(1)  # Sleep for the duration of the chunk

# </generator>

# <input thread>
def input_thread():
    global frequency_hz
    
    while True:
        print('enter: ')
        user_input = input()

        if user_input == 'q':
            quit()

        try:
            new_frequency = 100*float(user_input)
            frequency_hz = new_frequency
            print(f"Frequency changed to {frequency_hz} Hz")
        except ValueError:
            pass
# </input thread>

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
# </usage>