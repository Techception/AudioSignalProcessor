"""
Goal:
    - Generate a simple waveform
    - write it to a WAV file
"""

import numpy as np
import wave
import sys
import argparse 

def write_wav_mono(path: str, x: np.ndarray, sr: int) -> None:
    """write mono 16-bit PCM WAV. x is float32 in [-1,1]."""
    x = np.array(x, dtype=np.float32)
    x = np.clip(x, -1.0, 1.0) 
    x_i16 = (x*32767.0).astype(np.int16)

    with wave.open(path, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2) # 16-bit
        wf.setframerate(sr) 
        wf.writeframes(x_i16.tobytes())

def main(f_hz : int) -> None:
    sr = 48000 #sample rate
    dur_s = 10.0 #duration of play
    print(f_hz)
    
    n = int(sr * dur_s) #total number of samples required
    t = np.arange(n, dtype=np.float32) / sr #time index
    x = 1 * np.sin(2.0 * np.pi * f_hz *t) 
    print(x)

    write_wav_mono("out/out.wav", x, sr) 
    print("Wrote out.wav")

if __name__== "__main__":
    parser = argparse.ArgumentParser() 
    parser.add_argument("f_hz", type=int, help="frequency in Hz")
    args = parser.parser_args() 
    main(args.f_hz)

