import sys
import tty

tty.setcbreak(sys.stdin.fileno())

while True:
    key = sys.stdin.read(1)
    print(key)
