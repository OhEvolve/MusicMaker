
""" Builds a song from scratch """



# standard libraries

# nonstandard libraries

# homegrown libraries
from methods import *

# library modifications


settings = {
        'bpm':120,
        'measures':8,
        'layers':2
        }

sample = Sampler(settings)
print 'Waiting...'
raw_input('')
sample.start()
