#===============================================================================
# MakeFudge: PyFudge Brainfuck Control Script
#-------------------------------------------------------------------------------
# Version: 0.1.6
# Updated: 11-11-2013
# Author: Alex Crawford
# License: MIT
#===============================================================================

'''***REQUIRES PYFUDGE***

A script that displays the output of a Brainfuck program, and allows the 
user to toggle/change the settings of PyFudge. Also dumps the output, and
memory to two separate txt files ('output.txt', and 'memory.txt').

Just place PyFudge (as 'pyfudge.py'), and your Brainfuck programs (with a 
'.b' or '.bf' extension) in the same directory as this script, and the BF 
programs should be listed for loading when you run this script.
'''

#===============================================================================
# IMPORTS
#===============================================================================

from __future__ import print_function
import os
import glob
from pyfudge import Pyfudge

#===============================================================================
# MISC. FORMATTING VARIABLES
#===============================================================================

HR = '*' * 79
NL = '\n'

#===============================================================================
# MENU CLASS
#===============================================================================

class Menu(object):
    ''''''
    program = None
    progname = None

    memsize = Pyfudge.memsize
    cellsize = Pyfudge.cellsize
    cellwrap = True
    binmode = False
    debugmode = False
    memdisp = 0

    @classmethod
    def main(self):
        ''''''
        Display.osclear()

        if self.progname is None:
            opts = [
            'Load program',
            'Settings',
            'Exit'
            ]
        else:
            opts = [
            'Load program',
            'Run ' + self.progname,
            'Settings',
            'Exit'
            ]

        index = 1

        Display.title('Main Menu')

        Display.numlist(opts) 

        print(HR)
        
        cmd = raw_input('Choice: ')
        print()

        if self.progname is None:
            if cmd is '1':
                self.loadprog()
            elif cmd is '2':
                self.settings()
            elif cmd is '3' or cmd is '':
                return
        else:
            if cmd is '1':
                self.loadprog()
            elif cmd is '2':
                Display.output(self.program, self.memdisp)
            elif cmd is '3':
                self.settings()
            elif cmd is '4' or cmd is '':
                return

    @classmethod
    def loadprog(self):
        ''''''
        Display.osclear()

        filetypes = ['*.b', '*.bf']

        filelist = []

        Display.title('Load Program')

        for ftype in filetypes:
            filelist.extend(glob.glob(ftype))

        Display.numlist(filelist)

        print(HR)

        cmd = int(raw_input('Choice: '))
        print()

        with open(filelist[cmd-1], 'r') as afile:

            self.program = afile.read()
            self.progname = filelist[cmd-1]

        self.main()

    @classmethod
    def settings(self):
        ''''''
        # global pyfudge
        # global options

        Display.osclear()

        opts = [
            'Set memory size ' + '(' + str(Pyfudge.memsize) + ')',
            'Set cell size ' + '(' + str(Pyfudge.cellsize) + ')',
            'Toggle byte wrapping ' + '(' + str(self.cellwrap) + ')',
            'Toggle binary mode ' + '(' + str(self.binmode) + ')',
            'Toggle debug mode ' + '(' + str(self.debugmode) + ')',
            'Change byte display size ' + '(' + str(self.memdisp) + ')',
            'Back'
        ]

        Display.title('Settings')

        Display.numlist(opts)

        print(HR)

        cmd = raw_input('Choice: ')
        print()

        if cmd is '1':
            size = raw_input('Memory size: ')
            if size in ['a','A','auto','Auto']:
                Pyfudge.setmemory(memsize='auto')
            else:
                Pyfudge.setmemory(memsize=int(size))
            self.settings()
        if cmd is '2':
            pass
        if cmd is '3':
            if self.cellwrap:
                self.cellwrap = False
            else:
                self.cellwrap = True
            self.settings()
        elif cmd is '4':
            if self.binmode:
                self.binmode = False
            else:
                self.binmode = True
            self.settings()
        elif cmd is '5':
            if self.debugmode:
                self.debugmode = False
            else:
                self.debugmode = True
            self.settings()
        elif cmd is '6':
            self.memdisp = int(raw_input('Number of bytes: '))
            self.settings()
        elif cmd is '7' or cmd is '':
            self.main()

#===============================================================================
# DISPLAY CLASS
#===============================================================================

class Display(object):
    ''''''

    @classmethod
    def output(self, program, memdisp=Menu.memdisp):
        ''''''
        self.osclear()

        out = Pyfudge(program).run(wrap=Menu.cellwrap, binary=Menu.binmode)

        print('Done. Press enter to continue.')
        raw_input()

        self.osclear()

        if len(out[0]) is not 0:
            self.title('Output', newline=True)

            print(out[0] + NL)

            with open('output.txt', 'w') as outfile:
                outfile.write(out[0])

        if memdisp is not 0:
            self.title('Memory', newline=True)
            if memdisp is 'all':
                print(str(Pyfudge.memory) + NL)
            else:
                print(str(Pyfudge.memory[0:memdisp]) + NL)

        with open('memory.txt', 'w') as memfile:
            memfile.write(str(Pyfudge.memory))

    @staticmethod
    def title (title='', subtitle=None, upcase=True, newline=False):
        ''''''
        print(HR)
        if not upcase:
            print(title)
        else:
            print(title.upper())

        if subtitle is not None:
            print(subtitle)
        print(HR)

        if newline:
            print()

    @staticmethod
    def numlist (thelist=[], num=True, upcase=False):
        ''''''
        index = 1

        for item in thelist:
            if num and upcase:
                print("{0}. {1}".format(index, item.upper()))
            elif num and not upcase:
                print("{0}. {1}".format(index, item))
            elif not num and upcase:
                print(item.upper())
            elif not num and not upcase:
                print(item)
            index += 1

        # print()

    @staticmethod
    def osclear():
        ''''''
        if os.name in ['nt', 'dos']:
            os.system('cls')
        elif os.name is 'posix':
            os.system('clear')

    @staticmethod
    def bracket(text):
        ''''''
        return '{0}{1}{2}'.format('(', text, ')')

#===============================================================================
# IF MAIN
#===============================================================================

if __name__ == '__main__':
        Menu.main()

