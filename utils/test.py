import time
import sys
import numpy as np

np.set_printoptions(formatter={'int': '{:3d}'.format})
count = [i*2 for i in range(64)]
count = np.array(count)

for i in range(10):
    time.sleep(1)
    sys.stdout.write(f"something_{i}\n")
    for j in range(0, len(count), 16):
        sys.stdout.write(f"{count[j:j+16]}\n")
    sys.stdout.flush()
    if i < 9:
        sys.stdout.write("\x1b[1A\x1b[2K" * 5)