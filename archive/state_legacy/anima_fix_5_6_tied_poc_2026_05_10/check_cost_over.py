"""Exit 0 if cost > threshold, exit 1 otherwise. argv: cost threshold"""
import sys
cost = float(sys.argv[1])
thresh = float(sys.argv[2])
sys.exit(0 if cost > thresh else 1)
