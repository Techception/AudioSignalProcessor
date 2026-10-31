import numpy as np 
import matplotlib.pyplot as plt;

####################################################################################
####################################################################################
# <Analysis>

def graph (
        title: str = "waveform"
        ,wave: np.ndarray = np.linspace(0,0,0)
        ,time: np.ndarray = np.linspace(0,(2*np.pi),360)
        ,timefinal: float = 1
        ) -> None:
    #plot graph with title and axis 
    plt.plot(time, wave)
    plt.xlabel("Time (seconds)")
    plt.ylabel("Amplitude")
    plt.title(f"{title} Hz sine wave")
    plt.xlim(0, timefinal)  # show the first 0.01 seconds
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"wave.png", dpi=150)
    #plt.show()
    return None