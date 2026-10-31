import numpy as np 

####################################################################################
####################################################################################
# <Convertions>
# convert musical notation into frequency and seconds 

intervals_EqT = 440*2**(np.arange(12)/12)
intervals_spaced = np.linspace(440,880,12)
tones_12ToneChrome = ('a', 'a#', 'b', 'c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#')
# map note names to frequencies 
def pitchMap(intervals: np= intervals_EqT, tones: tuple= tones_12ToneChrome) -> dict:
    range = [int(i) for i in list(intervals)]
    tonesToFrequency = zip(tones,range)
    ToneMapFrequency = dict(tonesToFrequency)
    return ToneMapFrequency


def timeMap(noteValue: str, signature: str= '4/4', bpm: int= 60):
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
 

def noteBuilder(note: tuple) -> dict:
    duration, tone = note[0], note[1]
    converted_duration = timeMap(duration)
    frequency = pitchMap()[tone]
    note = {'duration': converted_duration, 'frequency':frequency}
    return note 

####################################################################################
####################################################################################
def debug_pitchMap():
    print('option 1', intervals_EqT)
    print('option 2', intervals_spaced)
    option = input('select option: ')
    if option == '1':
        frequency = pitchMap(intervals_EqT)
    elif option == '2':
        frequency = pitchMap(intervals_spaced)
    print(frequency)
    return None

def debug_timeMap():
    noteValue = input('enter note value e.g. 1/4 for quater-note/crotchet: ')
    time = timeMap(noteValue= noteValue, signature= '4/4', bpm= 60)
    print(f"\na {noteValue} note plays for {time} s")
    return None

def debug_noteToPitch():
    input_note = input('time, tone: ').split(',')
    note = noteBuilder(input_note)
    print('note: ',note)

def debug():
    #debug_pitchMap()
    #debug_timeMap()
    debug_noteToPitch()


if __name__ == '__main__':
    debug()