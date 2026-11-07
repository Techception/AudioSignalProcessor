# <import/>


import numpy as np;

####################################################################################
####################################################################################

SAMPLE_RATE = 44100; # sample rate
frequency_hz = 440;


sample = lambda f,index : np.sin(2 * np.pi * f * index/SAMPLE_RATE );

# <main>
def main():

    samples = list()
    for index in range(SAMPLE_RATE):
        a = sample(frequency_hz, index)
        samples.append(a)

        print(a)

    return None

if __name__ == '__main__':
    main()