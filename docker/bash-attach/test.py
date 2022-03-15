import time
import sys

print("python test stdout", file = sys.stdout)
print("python test stderr", file = sys.stderr)

print("python test stdout with flush", file = sys.stdout, flush=True)
print("python test stderr with flush", file = sys.stderr, flush=True)

while True:
    time.sleep(60)