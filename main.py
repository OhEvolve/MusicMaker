
# standard libraries
import termios, fcntl, sys, os
import argparse
import logging
import time

# nonstandard libraries
import pygame
import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt

# library modifications
pygame.init()


############################
# -- Command Line Catch -- #
############################

# outsourced to internal function

############################
# --- Internal Methods --- #
############################

def get_input():
    """ Returns character string of most recent input """
    return repr(sys.stdin.read()).strip("'")

def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text

def callback(indata, outdata, frames, time, status):
    if status:
        print(status)
    outdata[:] = indata

def get_args():
    """ Capture command line arguments """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-i', '--input-device', type=int_or_str,
                        help='input device ID or substring')
    parser.add_argument('-o', '--output-device', type=int_or_str,
                        help='output device ID or substring')
    parser.add_argument('-c', '--channels', type=int, default=2,
                        help='number of channels')
    parser.add_argument('-t', '--dtype', help='audio data type')
    parser.add_argument('-s', '--samplerate', type=float, help='sampling rate')
    parser.add_argument('-b', '--blocksize', type=int, help='block size')
    parser.add_argument('-l', '--latency', type=float, help='latency in seconds')
    return parser.parse_args()

############################
# ---       Main       --- #
############################

# Main testing function
class Main():

    def __init__(self,args):

        # some backend hooks
        fd = sys.stdin.fileno()
        oldterm = termios.tcgetattr(fd)
        newattr = termios.tcgetattr(fd)
        newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
        termios.tcsetattr(fd, termios.TCSANOW, newattr)
        oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

        # actual execution loop
        try:

            self.max_duration = 20.0
            self.exit = False # initialize exit
            self.active_recording = False

            # Start streaming device
            while True: # with sd.Stream(device=(args.input_device, args.output_device),
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

                    except IOError: 
                        pass

                    time.sleep(0.01) # give time for inp/out to sync

        finally:
            # closing backend safely
            termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
            fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)

    def interpret(self,val):
        """ Interprets user protocols """
        if val == 'q':
            print 'Exiting...'
            self.exit = True
        elif val == ' ':

            if self.active_recording == False:
                print 'Recording loop:'
                self.active_recording= True
                sd.stop()
                self.recording = sd.rec(int(self.max_duration * self.samplerate), 
                        samplerate=self.samplerate, 
                        channels=1)

            elif self.active_recording == True:
                print 'Playing loop:'
                self.active_recording = False 
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
                sd.play(self.recording,loop=True)

        elif val == 'm':
            print 'Starting tone...'
            pitch = 440 # hz
            myarray = np.sin(2*np.pi*pitch*np.arange(int(1.0*self.samplerate))/self.samplerate)
            sd.play(myarray)
        else:
            print "Got character <{}>".format(val)


if __name__ == "__main__":
    args = get_args()
    main = Main(args)


