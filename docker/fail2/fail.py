import time
import sys

if __name__ == "__main__":
    time.sleep(1)
    print("Programm is about to exit", file = sys.stdout)
    print("Programm exiting", file = sys.stderr)
    exit(1)


