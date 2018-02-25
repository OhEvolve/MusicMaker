
""" Builds a song from scratch """



# standard libraries

# nonstandard libraries

# homegrown libraries
from methods import *

# library modifications


settings = {
        'bpm':140,
        'measures':2,
        'layers':3,
        'samplerate':44100,
        'cannon':False
        }

sample = Sampler(settings)
print 'Waiting...'
raw_input('')
sample.start()
