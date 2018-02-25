
import numpy as np


indata = np.ones((3,2))

dampening = 0.5
echo_count = 4

outdata = np.concatenate([(dampening**i)*indata for i in xrange(echo_count)],axis=0)
print outdata.shape

