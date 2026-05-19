"""Compute current cost given $1=ELAPSED_S $2=$/hr."""
import sys
elapsed_s = int(sys.argv[1])
rate = float(sys.argv[2])
print(round(elapsed_s * rate / 3600, 2))
