#===============================================================================
# MakeFudge: PyFudge Brainfuck Output Script
#-------------------------------------------------------------------------------
# Version: 0.1.1
# Updated: 05-11-2013
# Author: Alex Crawford
# License: MIT
#===============================================================================

'''A very simple script for outputting the results of running a Brainfuck
program.

Just place Pyfudge, and your Brainfuck programs (with a '.bf' extension) 
in the same directory as this script, and it should be listed for loading 
when you run the script.

'''

#===============================================================================
# IMPORTS
#===============================================================================

from __future__ import print_function

import glob

from pyfudge import Pyfudge

#===============================================================================
# CONSTANTS
#===============================================================================

HR = ("*" * 79)
NL = ("\n")

#===============================================================================
# FUDGE MAKER
#===============================================================================

class Makefudge(object):
    ''''''

    @classmethod
    def make(self, program, memlen=100):
        ''''''

        self.title('Output')

        Pyfudge.interp(program)
        print(NL)

        self.title('Memory')

        if memlen is 'all':
            print(Pyfudge.MEMORY)
        else:
            print(Pyfudge.MEMORY[0:memlen])

    @staticmethod
    def title (*args):
        ''''''
        
        argl = len(args)

        print(HR)
        if argl == 1:
            print(args[0])
        elif argl == 2:
            print(args[0] + " (" + args[1] + ")")
        print(HR + NL)

    @staticmethod
    def numlist (thelist, upper=False):
        """"""

        index = 1

        if not upper:
          for item in thelist:
              print("[{0}] {1}".format(index, item))
              index += 1
        elif upper:
          for item in thelist:
              print("[{0}] {1}".format(index, item.upper()))
              index += 1
        print()

#===============================================================================
# IF MAIN
#===============================================================================

if __name__ == '__main__':

    print()

    filelist = glob.glob("*.bf")

    Makefudge.numlist(filelist)

    cmd = int(raw_input('Load which program? '))

    afile = open(filelist[cmd-1], 'r')

    program = afile.read()

    Makefudge.make(program)
