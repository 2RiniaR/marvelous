import sys
import os


base = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(base, "../src"))
print(sys.path)
