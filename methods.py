
""" Builds a song from scratch """

# standard libraries
import termios, fcntl, sys, os
import argparse
import logging
import time
import pickle

# nonstandard libraries
import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# library modifications
sys.setcheckinterval(1)

############################
# -- command line catch -- #
############################

# outsourced to internal function

class Sampler:

    def __init__(self,*args,**kwargs):

        """ Initialize sampler """

        self.settings = {
                'bpm':120,
                'time_signature':(4,4),
                'measures':4,
                'countdown':3,
                'layers':2,
                # recording settings
                'samplerate':44100,
                'channels':1,
                'cannon':False
                }
        
        # update settings
        for arg in args: self.settings.update(arg)
        self.settings.update(kwargs)

    def start(self):

        """ Start sample program """

        # move to local namespace
        bpm = self.settings['bpm']
        ts = self.settings['time_signature']
        measures = self.settings['measures']
        layers = self.settings['layers']
        samplerate = self.settings['samplerate']
        channels = self.settings['channels']
        cannon = self.settings['cannon']          # boolean

        # precalculate useful values
        entrysize = samplerate*measures*ts[0]*(60./bpm)

        # countdown
        for b in xrange(1,ts[0]+1):
            print 'Down measure {}/{}...'.format(b,ts[0])
            time.sleep(60./bpm)

        self.recording = np.zeros((layers,int(entrysize),channels))

        print 'Recording...'

        for phrase in xrange(100): # set with variable

            # define condition for writing new layers of music
            if cannon:
                condition = True
            else:
                condition = phrase < layers

            sd.stop()

            # Catch layers...
            if condition:
                print 'RECORDING...'
                temp_recording = sd.playrec(
                        np.sum(self.recording,axis=0), 
                        samplerate=samplerate, 
                        channels=channels)
    
            else:
                sd.play(np.sum(self.recording,axis=0),samplerate,
                        loop=False,blocking=False)

            for m in xrange(1,measures+1):

                #clear_screen()
                print 'Measure {}/{}...'.format(m,measures)

                ### On the beat ###
                for b in xrange(1,ts[0]+1):
                    print 'Beat {}/{}'.format(b,ts[0])
                    time.sleep(60./bpm)

            if condition:

                pickle.dump(temp_recording,open('data.p','wb'))
                #filtered_recording = butter_highpass_filter(temp_recording,5,samplerate)
                filtered_recording = my_filter(temp_recording)
                self.recording[phrase%layers,:,:] = filtered_recording 
                    
                #plt.plot(filtered_recording)
                #plt.show()

        print 'End recording.'


        # play looped track
        #sd.play(self.recording,loop=False,blocking=False)

        for m in xrange(1,measures+1):
            print 'Measure {}/{}...'.format(m,measures)

            for b in xrange(1,ts[0]+1):
                print 'Beat {}/{}'.format(b,ts[0])
                time.sleep(60./bpm)



############################
# --- internal methods --- #
############################

def get_input():
    """ returns character string of most recent input """
    return repr(sys.stdin.read()).strip("'")

def int_or_str(text):
    """helper function for argument parsing."""
    try:
        return int(text)
    except valueerror:
        return text

def callback(indata, outdata, frames, time, status):
    if status:
        print(status)
    outdata[:] = indata


############################
# ---       main       --- #
############################

# main testing function
"""#
class main():

    def __init__(self,args):

        # actual execution loop
        try:

            self.max_duration = 20.0
            self.exit = false # initialize exit
            self.active_recording = false

            # start streaming device
            while true: # with sd.stream(device=(args.input_device, args.output_device),
                           #samplerate=args.samplerate, blocksize=args.blocksize,
                           #dtype=args.dtype, latency=args.latency,
                           #channels=args.channels, callback=callback) as stream:

                self.samplerate = 2*44100 #stream.samplerate    
                #self.samplerate = 48000 #stream.samplerate    
                self.channels = 1 #stream.channels

                while not self.exit:

                    try:
                        # process inputs
                        c = get_input()
                        self.interpret(c)

                    except ioerror: 
                        pass

                    time.sleep(0.01) # give time for inp/out to sync

        finally:
            # closing backend safely
            termios.tcsetattr(fd, termios.tcsaflush, oldterm)
            fcntl.fcntl(fd, fcntl.f_setfl, oldflags)

    def interpret(self,val):
        "" interprets user protocols ""
        if val == 'q':
            print 'exiting...'
            self.exit = true
        elif val == ' ':

            if self.active_recording == false:
                print 'recording loop:'
                self.active_recording= true
                sd.stop()
                self.recording = sd.rec(int(self.max_duration * self.samplerate), 
                        samplerate=self.samplerate, 
                        channels=1)

            elif self.active_recording == true:
                print 'playing loop:'
                self.active_recording = false 
                self.recording = np.trim_zeros(self.recording)

                # static filter

                def f(x):
                    return abs(x)

                #f = np.vectorize(f)

                #std = np.std(self.recording)
                #self.recording[abs(self.recording) < std] = 0

                '''
                plt.plot(self.recording)
                plt.plot(np.std(self.recording)*np.ones(self.recording.shape))
                plt.plot(-np.std(self.recording)*np.ones(self.recording.shape))
                plt.show()
                '''
                

                sd.stop()
                sd.play(self.recording,loop=true)

        elif val == 'm':
            print 'starting tone...'
            pitch = 440 # hz
            myarray = np.sin(2*np.pi*pitch*np.arange(int(1.0*self.samplerate))/self.samplerate)
            sd.play(myarray)
        else:
            print "got character <{}>".format(val)
"""#

def clear_screen():
    os.system('clear')

def my_filter(data):

    # data load
    final_shape = data.shape
    data = np.array(data).flatten()
    N = len(data)
    # fft 
    data_fft = np.fft.fft(data)
    data_fft_mod = [d if 2*abs(i - N/2) < 0.99*N else 0.0 for i,d in enumerate(data_fft)]
    data_mod = np.real(np.fft.ifft(data_fft_mod))

    return np.reshape(data_mod,final_shape)

def butter_highpass(cutoff, fs, order=20):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = signal.butter(order, normal_cutoff, btype='high', analog=False)
    return b, a

def butter_highpass_filter(data, cutoff, fs, order=5):
    b, a = butter_highpass(cutoff, fs, order=order)
    y = signal.filtfilt(b, a, data, axis=0)
    return y

if __name__ == "__main__":
    args = get_args()
    main = main(args)




