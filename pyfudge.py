#===============================================================================
# PyFudge: A Python-based Brainfuck Interpreter
#-------------------------------------------------------------------------------
# Version: 0.1.4
# Updated: 08-11-2013
# Author: Alex Crawford
# License: MIT
# Demo: http://repl.it/MQz/1
#===============================================================================

'''PyFudge is a Python-based (2.7.5) Brainfuck interpreter.

I believe it's fully functional, but haven't tested it thoroughly yet.

'''

#===============================================================================
# IMPORTS
#===============================================================================

from __future__ import print_function

#===============================================================================
# MEMORY VARIABLES
#===============================================================================

MEMSIZE = 'Auto'
CELLSIZE = 255
MEMORY = [0]

#===============================================================================
# PYFUDGE FUNCTIONS
#===============================================================================

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

    if 'ERROR' in looplst[0]:
        return looplst

    while progpos < proglen:

        char = program[progpos]

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
            if cmd is not '':
                MEMORY[mempos] = ord(cmd)
            else:
                MEMORY[mempos] = 0
        elif char is '[':
            if MEMORY[mempos] == 0:
                for i in range(looplen):
                    if progpos == looplst[i][0]:
                        progpos = looplst[i][1]
        elif char is ']':
            if MEMORY[mempos] != 0:
                for i in range(looplen):
                    if progpos == looplst[i][1]:
                        progpos = looplst[i][0]
        elif char is '#' and debug:
            print(MEMORY[mempos])

        if MEMSIZE is 'Auto':
            try:
                test = MEMORY[mempos]
            except:
                MEMORY.extend([0])
        else:
            try:
                test = MEMORY[mempos]
            except:
                return ['ERROR: Not enough memory.']

        if wrap:
            if MEMORY[mempos] > CELLSIZE:
                MEMORY[mempos] = 0
            elif MEMORY[mempos] < 0:
                MEMORY[mempos] = CELLSIZE

        progpos += 1

    return "".join(outbuff), MEMORY 

def findloops(program, proglen):
    '''findloops(program, proglen) -> list of loop jump points'''

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
        return ['ERROR: Mismatched number of loop brackets.']

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

