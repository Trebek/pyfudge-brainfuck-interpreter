#===============================================================================
# PyFudge: A Python-based Brainfuck Interpreter
#-------------------------------------------------------------------------------
# Version: 0.1.5
# Updated: 10-11-2013
# Author: Alex Crawford
# License: MIT
#===============================================================================

'''PyFudge is a Python-based (2.7.5) Brainfuck interpreter.

I believe it's fully functional, but haven't tested it thoroughly yet.

'''

#===============================================================================
# IMPORTS
#===============================================================================

from __future__ import print_function
import sys

#===============================================================================
# MEMORY VARIABLES
#===============================================================================

MEMSIZE = 'Auto'
CELLSIZE = 255
MEMORY = [0]

#===============================================================================
# PYFUDGE FUNCTIONS
#===============================================================================

def main():
    '''The main function.'''

    if len(sys.argv) == 2:

        with open(sys.argv[1], 'r') as prog:
            program = prog.read()
        output = run(program)

        print()
        print('Done interpreting ' + sys.argv[1])
        print()
        # print('See \"output.txt\" and \"memory.txt\" for results.')

        if len(output[0]) != 0:
            with open('output.txt', 'w') as outfile:
                outfile.write(output[0])
                print('See \"output.txt\" for output results.')

        with open('memory.txt', 'w') as memfile:
            memfile.write(str(MEMORY))
        print('See \"memory.txt\" for memory dump.')


def run(program, wrap=True, binary=False, debug=False):
    '''pyfudge.run(program, wrap=True, binary=False, debug=False)

    Interprets a Brainfuck program fed into it.

    '''

    mempos = 0
    progpos = 0

    outbuff = []

    program = program.replace(" ", "")
    proglen = len(program)

    looplst = findloops(program, proglen)
    looplen = program.count('[')

    while progpos < proglen:

        char = program[progpos]
        memlen = len(MEMORY)

        if char is '+':
            MEMORY[mempos] += 1
        elif char is '-':
            MEMORY[mempos] -= 1
        elif char is '>':
            mempos += 1
        elif char is '<':
            mempos -= 1
        elif char is '.':
            if not binary and MEMORY[mempos] == 10:
                outbuff.extend('\n')
            else:
                outbuff.extend(chr(MEMORY[mempos]))
        elif char is ',':
            cmd = raw_input()
            if len(cmd) != 0:
                MEMORY[mempos] = ord(cmd)
            elif len(cmd) == 0:
                break
        elif char is '[':
            if MEMORY[mempos] == 0:
                progpos = doloops(progpos, char, looplst, looplen)
        elif char is ']':
            if MEMORY[mempos] != 0:
                progpos = doloops(progpos, char, looplst, looplen)
        elif char is '#' and debug:
            print(MEMORY[mempos])

        if MEMSIZE is 'Auto' and mempos == memlen:
                MEMORY.extend([0])
        elif mempos == memlen:
                raise Error('Not enough memory.')
        if wrap:
            if MEMORY[mempos] > CELLSIZE:
                MEMORY[mempos] = 0
            elif MEMORY[mempos] < 0:
                MEMORY[mempos] = CELLSIZE

        progpos += 1

    return "".join(outbuff), MEMORY 

def findloops(program, proglen):
    '''findloops(program, proglen) -> list of loop jump points

    '''

    temp = []
    looplst = []

    if program.count('[') == program.count(']'):
        for i in range(proglen):
            if program[i] is '[':
                temp.append(i)
            elif program[i] is ']':
                index = temp.pop()
                looplst.append([index, i])
        return looplst
    else:
        raise Error('Mismatched number of loop brackets.')

def doloops(progpos, char, looplst, looplen):
    '''doloops(progpos, char, looplst, looplen) -> next loop position'''

    if char is '[':
        x, y = 0, 1
    elif char is ']':
        x, y = 1, 0

    for i in range(looplen):
        if progpos == looplst[i][x]:
            return looplst[i][y]

def setmemory(memsize='Auto', cellsize=None):
    '''setmemory(memsize='Auto', cellsize=None)

    Sets the memory, and cell size to the specified sizes.

    '''

    global MEMSIZE
    global CELLSIZE
    global MEMORY

    if memsize is 'Auto':
        MEMSIZE = 'Auto'
    else:
        MEMSIZE = memsize
        MEMORY = [0] * MEMSIZE
        
    if cellsize is not None:
        CELLSIZE = cellsize

class Error(Exception):
    ''''''

    def __init__(self, message):

        Exception.__init__(self, message)

#===============================================================================
# IF MAIN
#===============================================================================

if __name__ == '__main__':

    main()