
# standard libraries
import termios, fcntl, sys, os

# nonstandard libraries
import pygame

# library modifications
pygame.init()

# --- Internal Methods --- #

def get_input():
    """ Returns character string of most recent input """
    return repr(sys.stdin.read()).strip("'")

# Main testing function
class Main():

    def __init__(self):

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

            self.exit = False # initialize exit



            while not self.exit:

                try:
                    # process inputs
                    c = get_input()
                    self.interpret(c)

                except IOError: 
                    pass

        finally:
            # closing backend safely
            termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
            fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)

    def interpret(self,val):
        """ Interprets user protocols """
        print type(val)
        if val == 'q':
            print 'Exiting...'
            self.exit = True
        else:
            print "Got character <{}>".format(val)


if __name__ == "__main__":
    main = Main()


