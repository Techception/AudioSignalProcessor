import numpy as np;

####################################################################################
####################################################################################
# <Calculations>


def wave(duration: float, frequency: int, sampleRate: int = 44100, amplitude: int = 1) -> dict:
    totalSamples = sampleRate*duration  # total datapoints (float)
    A = amplitude;                      # Max Amplitude 
    F = frequency;
    W = (2*np.pi) * F;                     # Angular frequency
    
    #this defines the numberline on which the wave is rendered 
    totalSamples = int(totalSamples)    # total datapoints (integer)
    #Get the time range = duration of wave
    time = np.linspace( 
        0,           # beginning of number line in this case t = 0 
        duration,    # total duration that the sound plays 
        totalSamples # the number of samples will determine the resolution of the time index 
    ) # time index 

    #Generate waves
    #A(t) = A x sin(2 x pi x f x t)
    wave = A*np.sin(W * time)           # Mathematical wave
    pcm = (wave*32767).astype(np.int16) # the digital file data
    pcm = pcm.tobytes()
    data = {'func': wave, 'timeRange':time, 'bytes': pcm}
    
    #Debugging
    #print("total samples:", totalSamples);
    #print('Time range:',time);
    return data