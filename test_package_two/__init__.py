import sys
import os


print('print from TWO')
dir_name = os.path.dirname(os.path.abspath(__file__))
print(dir_name)
sys.path.append(os.path.dirname(dir_name))
print(sys.path)