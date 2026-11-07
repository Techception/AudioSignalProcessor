# <import/>
from numpy import array, int16
from math import sin, pi
import time;
import threading;
import sys;
####################################################################################
####################################################################################

# <variables>
SAMPLE_RATE = 44100; # sample rate
frequency_hz = 320; # default frequency in Hz
# </variables>

# <Calculations>
""" 
generate amplitude of wave at time t 
A(t) = A x sin(2 x pi x f x t)
t = index/SAMPLE_RATE # time in seconds related to number of samples
"""
sample = lambda f,index : sin(2*pi * f * index/SAMPLE_RATE );
# </Calculations>

# <generator> perpetuates the wave generation over time
def play_thread():
    global frequency_hz
    index = 0
    chunk = 2000 # number of samples to generate at a time
    while True:
        sound_chunk = array([sample(frequency_hz, index + i) * 32767 for i in range(chunk)], dtype=int16)
        sys.stdout.buffer.write(sound_chunk.tobytes())
        sys.stdout.buffer.flush()
        index += chunk
        #time.sleep(chunk / 2*SAMPLE_RATE)  # Sleep for the duration of the chunk

def input_thread():
    global frequency_hz
    while True:
        #user_input = input("Enter new frequency in Hz (or 'exit' to quit): ")
        user_input = input()
        if user_input.lower() == 'exit':
            quit()
        try:
            new_frequency = float(user_input)
            frequency_hz = new_frequency
            #print(f"Frequency changed to {frequency_hz} Hz", file=sys.stderr)
        except ValueError:
            #print("Invalid input. Please enter a valid number.", file=sys.stderr, flush=True)
            pass

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

#python3 src/render.py | ffplay -f s16le -ar 44100 -ch_layout mono -nodisp - 2> /dev/null 