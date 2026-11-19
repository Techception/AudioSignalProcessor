#!/usr/bin/env python3

# <import>
from numpy import array, int16
from math import exp, sin, pi
import time;
import threading;
import sys;
from dataclasses import dataclass;

import math
# </import>

# <variables>
@dataclass
class AudioState:
    is_playing: bool = True
    sample_rate: int = 44100
    frequency_hz: float = 320
    chunk_size_samples: int = 441
    chunk_duration_seconds: float = 441 / 44100
    sample_index: int = 0
    decay_steps: int = 0
    sustain_chunks_remaining: int = 10
    attack_chunks_remaining: int = 5
    previous_input: str = ""
    released: int = 0
# </variables>
# to do: separate golbal variables from sound pulse 
# perhaps the audio pulse should be a class of its own 

# <functions>
# <audio generation>
WAVEFORMS = {
    "sin": lambda angle_radians: math.sin(angle_radians),
    "square": lambda angle_radians: 1.0 if angle_radians < math.pi else -1.0,
    "sawtooth": lambda angle_radians: 1.0 - angle_radians / math.pi,
}
# to do: triangle wave, square wave duty cycle 

AMPLITUDE = lambda t,k,a: a*math.exp(-t*(1/k))
# to do: entire ASDR profile in this function 

def asdr(state: AudioState):
    state.attack_chunks_remaining -= 1
    if state.attack_chunks_remaining <= 0 and state.released <= 50:
        state.sustain_chunks_remaining -= 1
    else: 
        state.decay_steps += 1


def waveform_sample(
    frequency_hz: float,
    time_seconds: float,
    waveform: str = "sin",
    phi: float = 0.0,
) -> float:
    # Return a waveform sample; phi is a phase offset in radians.
    angle_radians = (2*math.pi * frequency_hz*time_seconds + phi) % (2*math.pi)
    waveform_name = waveform.lower()
    sample_function = WAVEFORMS.get(waveform_name)
    if sample_function is None:
        raise ValueError(f"Unknown waveform: {waveform}")
    return sample_function(angle_radians)

def write_audio_chunk(state: AudioState) -> None:
    decaytime = state.decay_steps   
    attack = 1 if state.attack_chunks_remaining <= 0 else 1/state.attack_chunks_remaining**2
    sample_times = [
        (state.sample_index + offset) / state.sample_rate
        for offset in range(state.chunk_size_samples)
    ]
    samples = [
        AMPLITUDE(decaytime,50,attack) * waveform_sample(state.frequency_hz, time_seconds)
        for time_seconds in sample_times
    ]
    pcm_bytes = (array(samples) * 32767).astype(int16).tobytes()
    # <send wave samples to stdout/>
    sys.stdout.buffer.write(pcm_bytes)
    sys.stdout.buffer.flush()
# </audio generation>

# <frequency input>
def read_frequency_input(state: AudioState) -> int:
    user_input = input()
    if state.released > 50 or user_input != state.previous_input:
        state.decay_steps = 0
        state.sustain_chunks_remaining = 50
        state.attack_chunks_remaining = 10
    # elif user_input == state.previous_input:
    #     if state.sustain_chunks_remaining == 0:
    #         state.decay_steps = 0
    #state.sustain_chunks_remaining = 10
    state.released = 0
    state.previous_input = user_input.strip()
    #state.sustain_chunks_remaining = 10
    
    # <check for quit command>
    if user_input.lower() == 'q':
        state.is_playing = False
        print("\nExiting...", file=sys.stderr, flush=True)
        return 0

    # <try to convert user input to float and update frequency>
    try:
        new_frequency_hz = 100 * float(user_input)
    except ValueError:
        new_frequency_hz = 0
    
    state.frequency_hz = new_frequency_hz

    prompt = f"Current frequency: {state.frequency_hz} Hz. Enter new frequency in Hz (or 'q' to quit): "
    print(prompt, end='\r', file=sys.stderr, flush=True)
    
    return 0
# </frequency input>
# </functions> 

# <thread 1> playback_worker: generates wave samples and sends them to stdout
def playback_worker(state: AudioState) -> None:
    # <range of time points to generate wave samples for/>
    while state.is_playing:
        write_audio_chunk(state)
        asdr(state)
        # <advance sample position and wait for next chunk/>
        state.sample_index += state.chunk_size_samples
        state.released += 1
        #print(state.decay_steps, end='\r', file=sys.stderr, flush=True)
        print(state.released, end='\r', file=sys.stderr, flush=True)
        time.sleep(state.chunk_duration_seconds * 22 / 23)

    return None
# </thread 1>

# <thread 2> input_worker: reads user input and updates frequency
def input_worker(state: AudioState) -> None:
    while state.is_playing:
        read_frequency_input(state)
# </thread 2>

# <main>
def main():
    audio_state = AudioState()
    
    # <define threads>
    playback_thread = threading.Thread(target=playback_worker, args=(audio_state,))
    input_thread = threading.Thread(target=input_worker, args=(audio_state,))
    # </define threads>

    # <threads>
    playback_thread.start()
    input_thread.start()
    # </threads>
# </main>

if __name__ == '__main__':
    main()
