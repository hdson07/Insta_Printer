#!/usr/bin/env python
import os

filename = "sample_mask.png "
os.system("lpr -o media=Upper,letter,Custom.76x126mm -o orientation-requested=6  %s" %(filename))    

# os.system("lpr -P 165.194.35.209 /sample-out.jpg")
# fn = 'path/to/file.ext'
# printer = 'ps'
# print_cmd = 'lpr -P %s %s'
# os.system(print_cmd % (printer, fn))