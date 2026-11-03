source code in src/ 
to execute the program: python3 src/render.py 
render.py combines:
    -   converter.py    for musical functions to convert stave notation into pulse time and wave frequency 
    -   calculations.py to calculate the wave mathematically and generate the byte data 
    -   analysis.py     for graphing the wave visually 

run_test.sh: 
    - create an output folder in form out/testxx containing: 
        -   the scripts
        -   output waves graphic
        -   pcm file 
    - pipe output to ffplay that does the physical sound making 
    - can be used alone or pipe in a musical score 

scores:
    - contains score/compositions 
    - can be in the music form e.g. 1/1,E represents a whole note E 
    - can be in time-frequency form e.g. 1,440 represents a 1 second pulse of a 440hz wave 

environment.sh: 
    -  build the python .venv and pip install requirements 

docs: 
    - project charter 
    - analisys of code and physics 

example run: 
cat scores/music.composer | python3 src/render.py 2> /dev/null | tee "wave.pcm" | ffplay -f s16le -ar 44100 -ac 1 -nodisp -autoexit -

explaination: 
input: score file -> generator (no stdErr output) -> branched pipe to file and to ffplay -> output: sound generated from ffplay reading pcm 

