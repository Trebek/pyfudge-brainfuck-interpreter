#===============================================================================
# MakeFudge: PyFudge Brainfuck Control Script
#-------------------------------------------------------------------------------
# Version: 0.1.4
# Updated: 08-11-2013
# Author: Alex Crawford
# License: MIT
#===============================================================================

'''***REQUIRES PYFUDGE***

A script that displays the output of a Brainfuck program, and allows 
the user to toggle/change the settings of PyFudge.

Just place PyFudge (as 'pyfudge.py'), and your Brainfuck programs 
(with a '.b' or '.bf' extension) in the same directory as this script, 
and the BF programs should be listed for loading when you run this script.

'''

#===============================================================================
# IMPORTS
#===============================================================================

from __future__ import print_function
import os
import glob
import pyfudge

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

    memsize = pyfudge.MEMSIZE
    cellsize = pyfudge.CELLSIZE
    bytewrap = True
    binmode = False
    debugmode = False
    bytenum = 32

    @classmethod
    def main(self):
        ''''''

        Display.osclear()

        opts = [
            'Load program',
            'Run program',
            'Settings',
            'Exit'
        ]

        index = 1

        Display.title('Main Menu')

        Display.numlist(opts) 

        if self.progname is not None:
            print(HR + NL)
            print('Program: ' + self.progname + NL)

        print(HR + NL)

        cmd = raw_input('Choice: ')
        print()

        if cmd is '1':
            self.loadprog()
        elif cmd is '2':
            Display.output(self.program, memlen=self.bytenum)
        elif cmd is '3':
            self.settings()
        elif cmd is '4' or cmd is '':
            pass

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

        print(HR + NL)

        cmd = int(raw_input('Choice: '))
        print()

        with open(filelist[cmd-1], 'r') as afile:

            self.program = afile.read()
            self.progname = filelist[cmd-1]

        self.main()

    @classmethod
    def settings(self):
        ''''''

        Display.osclear()

        opts = [
            'Set memory size',
            'Set cell size',
            'Toggle byte wrapping',
            'Toggle binary mode',
            'Toggle debug mode',
            'Change byte display size',
            'Back'
        ]

        Display.title('Settings')

        Display.numlist(opts)

        print(HR + NL)

        dispopts = [
            ['Memory size: ', str(pyfudge.MEMSIZE)],
            ['Cell size: ', str(pyfudge.CELLSIZE)],
            ['Byte wrapping: ', str(self.bytewrap)],
            ['Binary mode: ', str(self.binmode)],
            ['Debug mode: ', str(self.debugmode)],
            ['Bytes to display: ', str(self.bytenum)]
        ]

        for item in dispopts:
            print(item[0] + item[1])
        print()

        print(HR + NL)

        cmd = raw_input('Choice: ')
        print()

        if cmd is '1':
            size = raw_input('Memory size: ')
            if size in ['a','A','auto','Auto']:
                pyfudge.setmemory(memsize='Auto')
            else:
                pyfudge.setmemory(memsize=int(size))
            self.settings()
        if cmd is '2':
            pass
        if cmd is '3':
            if self.bytewrap:
                self.bytewrap = False
            else:
                self.bytewrap = True
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
            self.bytenum = int(raw_input('Number of bytes: '))
            self.settings()
        elif cmd is '7' or cmd is '':
            self.main()

#===============================================================================
# DISPLAY CLASS
#===============================================================================

class Display(object):
    ''''''

    @classmethod
    def output(self, program, memlen=32):
        ''''''
    
        self.osclear()

        out = pyfudge.run(program, wrap=Menu.bytewrap, binary=Menu.binmode)

        if out[0] is not '':
            self.title('Output')

            print(out[0] + NL)
            # print()

        self.title('Memory')

        if memlen is 'all':
            print(pyfudge.MEMORY)
        else:
            print(pyfudge.MEMORY[0:memlen])

    @staticmethod
    def title (title='', subtitle='', upcase=True):
        ''''''
        
        # argl = len(args)

        print(HR)
        if not upcase:
            print(title)
        else:
            print(title.upper())

        if subtitle is not '':
            print(subtitle)
        print(HR + NL)

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

        print()

    @staticmethod
    def osclear():
        ''''''

        if os.name in ['nt', 'dos']:
            os.system('cls')
        elif os.name is 'posix':
            os.system('clear')

#===============================================================================
# IF MAIN
#===============================================================================

if __name__ == '__main__':

    Menu.main()

