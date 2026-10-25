n=1
while [ -e "out/test$(printf '%02d' "$n")" ]; do
    n=$((n + 1))
done

test_dir="out/test$(printf '%02d' "$n")"
mkdir -p "$test_dir"
cp src/render.py "$test_dir/"

python3 $test_dir/render.py "$1" | tee "wave.pcm" | ffplay -f s16le -ar 44100 -ac 1 -nodisp -autoexit -
