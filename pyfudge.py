#===============================================================================
# PyFudge: A Python-based Brainfuck Interpreter
#-------------------------------------------------------------------------------
# Version: 0.1.6
# Updated: 11-11-2013
# Author: Alex Crawford
# License: MIT
#===============================================================================

'''PyFudge is a (slow) Python-based (2.7.5) Brainfuck interpreter, with a 
few extra (useless?) features. I believe it's fully functional, but haven't 
tested it thoroughly yet.
'''

#===============================================================================
# IMPORTS
#===============================================================================

from __future__ import print_function
import sys

#===============================================================================
# PYFUDGE CLASS
#===============================================================================

class Pyfudge(object):
    ''''''

    memsize = 'auto'
    cellsize = 255
    memory = [0]
    mempos = 0

    program = None
    proglen = 0    
    progpos = 0

    looplst = None
    looplen = 0

    def __init__(self, program, memsize='auto', cellsize=255):
        ''''''
        self.memsize = memsize
        self.cellsize = cellsize
        
        try:
            from bfcclean import BFCCstrip
            self.program = BFCCstrip(program)
        except:
            self.program = program.replace(" ", "")
        self.proglen = len(self.program)

        self.looplst = self.findloops()
        self.looplen = self.program.count('[')

    def run(self, wrap=True, binary=False, debug=False):
        '''pyfudge.run(program, wrap=True, binary=False, debug=False)

        Interprets a Brainfuck program fed into it.
        '''
        outbuff = []

        while self.progpos < self.proglen:

            char = self.program[self.progpos]
            memlen = len(self.memory)

            if char is '+':
                self.memory[self.mempos] += 1
            elif char is '-':
                self.memory[self.mempos] -= 1
            elif char is '>':
                self.mempos += 1
            elif char is '<':
                self.mempos -= 1
            elif char is '.':
                if not binary and self.memory[self.mempos] == 10:
                    outbuff.extend('\n')
                else:
                    outbuff.extend(chr(self.memory[self.mempos]))
            elif char is ',':
                cmd = raw_input()
                if len(cmd) != 0:
                    self.memory[self.mempos] = ord(cmd)
                elif len(cmd) == 0:
                    break
            elif char is '[':
                if self.memory[self.mempos] == 0:
                    self.progpos = self.doloops(char)
            elif char is ']':
                if self.memory[self.mempos] != 0:
                    self.progpos = self.doloops(char)
            elif char is '#' and debug:
                print(self.memory[self.mempos])

            if self.memsize is 'auto' and self.mempos == memlen:
                    self.memory.extend([0])
            elif self.mempos == memlen:
                    raise Error('Not enough memory.')
            if wrap:
                if self.memory[self.mempos] > self.cellsize:
                    self.memory[self.mempos] = 0
                elif self.memory[self.mempos] < 0:
                    self.memory[self.mempos] = self.cellsize

            self.progpos += 1

        return "".join(outbuff), self.memory 

    def findloops(self):
        '''findloops(program, proglen) -> list of loop jump points'''
        temp = []
        looplst = []

        if self.program.count('[') == self.program.count(']'):
            for i in range(self.proglen):
                if self.program[i] is '[':
                    temp.append(i)
                elif self.program[i] is ']':
                    index = temp.pop()
                    looplst.append([index, i])
            return looplst
        else:
            raise Error('Mismatched number of loop brackets.')

    def doloops(self, char):
        '''doloops(char) -> next loop position'''
        if char is '[':
            x, y = 0, 1
        elif char is ']':
            x, y = 1, 0

        for i in range(self.looplen):
            if self.progpos == self.looplst[i][x]:
                return self.looplst[i][y]

    @classmethod
    def setmemory(self, memsize='auto', cellsize=255):
        '''setmemory(memsize='auto', cellsize=None)

        Sets the memory, and cell size to the specified sizes.
        '''
        self.memsize = memsize
        if self.memsize is not 'auto':
            self.memory = [0] * self.memsize
            
        if cellsize is not None:
            self.cellsize = cellsize

#===============================================================================
# ERROR EXCEPTION CLASS
#===============================================================================

class Error(Exception):
    ''''''

    def __init__(self, message):
        ''''''
        Exception.__init__(self, message)

#===============================================================================
# SHORTCUT
#===============================================================================

def fudgethis(program, name=None):
    ''''''
    output = Pyfudge(program).run()
    if name is None:
        outputmsg(output, 'program')
    else:
        outputmsg(output, name)

#===============================================================================
# DONE NOTIFICATION
#===============================================================================

def outputmsg(output, filename):
    '''The main function.'''
    print('\nDone interpreting ' + filename + '\n')
    if len(output[0]) != 0:
        with open('output.txt', 'w') as outfile:
            outfile.write(output[0])
            print('See \"output.txt\" for output results.')

    with open('memory.txt', 'w') as memfile:
        memfile.write(str(output[1]))
    print('See \"memory.txt\" for memory dump.')

#===============================================================================
# IF MAIN
#===============================================================================

if __name__ == '__main__':
    if len(sys.argv) == 2:
        with open(sys.argv[1], 'r') as prog:
            program = prog.read()
        fudgethis(program, sys.argv[1])
