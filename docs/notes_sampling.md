2025-02-01

create a function that can generate a .wav file. 
it creates the wave file by using numpy arrays 
- I don't know why numpy is better than a normal array yet 

And by using the wave module that can read or write WAV files 
this file is written in 16 bit 
- I need to find out more about the benefits and/or cost of different bits 16 vs 32 etc. 
- Is this the same as the bit rate? 
- Does more bits mean more quality? 

What I found was when using a sample rate of 48000: 
> the number of samples per cycle of the wave is given fs/f 
> where fs is the sample rate (e.g. 48000 samples per second) 
> and f is the frequency of the wave (e.g. cycles per second) 

so for a low frequency sound e.g. 220hz
there would be 48000/220 ~= 218 samples per wave cycle 
which gives a smooth sound. 

But for a higher frequency e.g. 12000hz 
there would be 48000/12000 = 4 samples per wave cycle 
which gives a choppy cound - almost like hearing bells 

This also means the nyquist frequency, that is the maximum frequency sound that can be analysed without aliasing is fs/2 = 24000hz.

So when I tried the experiment with a 30000hz sound this aliased to a 18000hz sound. 

Corrections to make:
> Bit depth vs bit rate 
> Why python list are inferior to numpy arrays due to memory management and loops 
> As well as numpy in built sin function 

Also tidy up that its dense sampling and metalic sounds and add some more equations on aliasing 
