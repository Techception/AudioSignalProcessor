n=1
while [ -e "out/test$(printf '%02d' "$n")" ]; do
    n=$((n + 1))
done

test_dir="out/test$(printf '%02d' "$n")"
mkdir -p "$test_dir"
cp src/render.py "$test_dir/"

cd $test_dir
python3 render.py "$@" | tee "wave.pcm" | ffplay -f s16le -ar 44100 -ac 1 -nodisp -autoexit -

cd ../..

cat > "$test_dir/README.md" <<'EOF'
# Test notes

## Purpose
What am I testing?

## Settings
- Frequency:
- Duration:
- Sample rate: 44,100 Hz

## How the code represents the sound
Explain what the code does and how it relates to the wave.

## Graph
![Waveform](wave.png)

## Audio samples
[wave.pcm](wave.pcm)

## Observations
What did I hear or notice?
EOF
