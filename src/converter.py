import numpy as np 

####################################################################################
####################################################################################
# <Convertions>
# convert musical notation into frequency and seconds 

# map note names to frequencies 
def pitchMap(range: np.linspace) -> dict:
    pitchs = ('a', 'a#', 'b', 'c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#')
    range = [int(i) for i in list(range)]
    pitchToFrequency = zip(pitchs,range)
    notesPitch = dict(pitchToFrequency)
    return notesPitch


def timeMap(noteValue: str, signature: str = '4/4', bpm: int = 60):
    # e.g. consider sig: 4/4 note_length: 1/4 how long in seconds? 
    # beatValue = 1/denominator(signature) = 1/denominator(4/4) = 1/4
    # beats = note_length / beatValue

    (noteNumerator , noteDenominator) = map(int, noteValue.split('/')) ## possibly an unnecesary step? 
    (_ , noteUnit) = map(int, signature.split('/'))                    ## beats per bar : note unit
    
    note = (noteNumerator / noteDenominator) # Convert to float e.g. 1-quater note = 1/4 = 0.25 
    beatUnit = 1/noteUnit                    # what note represents a single beat? 4/4 means beat unite is quarter-note = 1/4 
    noteBeats = note / beatUnit          # how long the note lasts in terms of beats 
    noteSeconds =  (60/bpm) * noteBeats  # how long the note lasts in terms of seconds
    return noteSeconds
 

def noteToPitch(range: np.linspace, pitch: str, length: str, bpm: int = 60) -> dict:
    #beat note to duration 
    notesLength = {
        '1': 60/bpm
        ,'1/2': 60/bpm/2
        ,'1/4': 60/bpm/4
        ,'1/8': 60/bpm/8
        ,'1/32': 60/bpm/32
        };
    range = np.linspace(440,880,12)
    notesPitch = pitchMap(range)
    notePitch = notesPitch[pitch]
    noteLength = notesLength[length]
    note = {'pitch':notePitch, 'length': noteLength}
    #print('note:', note)
    return note 

def debug():
    noteValue = input('enter note value: ')
    time = timeMap(noteValue= noteValue, signature= '4/4', bpm= 60)
    print(f"\na {noteValue} note plays for {time} s")

if __name__ == '__main__':
    debug()