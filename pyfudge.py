#===============================================================================
# PyFudge: A Python-based Brainfuck Interpreter
#-------------------------------------------------------------------------------
# Version: 0.1.3
# Updated: 07-11-2013
# Author: Alex Crawford
# License: MIT
# Demo: http://repl.it/MOC
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

MEMSIZE = 30000
BYTESIZE = 255

MEMORY = [0] * MEMSIZE

#===============================================================================
# PYFUDGE MAIN FUNCTION
#===============================================================================

def run(program, wrap=True):
    '''pyfudge.run(program, wrap=True)

    Interprets a Brainfuck program fed into it.

    '''

    pointer = 0
    progpos = 0

    program = program.replace(" ", "")

    outbuff = []

    while progpos < len(program):

        char = program[progpos]

        if char is '+':
            MEMORY[pointer] += 1
        elif char is '-':
            MEMORY[pointer] -= 1
        elif char is '>':
            pointer += 1
        elif char is '<':
            pointer -= 1
        elif char is '.':
            if MEMORY[pointer] == 10:
                outbuff.extend('\n')
            else:
                outbuff.extend(chr(MEMORY[pointer]))
        elif char is ',':
            MEMORY[pointer] = ord(raw_input())
        elif char is '[' and MEMORY[pointer] == 0:
            loops = 1
            while loops > 0:
                progpos += 1
                if program[progpos] is '[':
                    loops += 1
                elif program[progpos] is ']':
                    loops -= 1
        elif char is ']' and MEMORY[pointer] != 0:
            loops = 1
            while loops > 0:
                progpos -= 1
                if program[progpos] is '[':
                    loops -= 1
                elif program[progpos] is ']':
                    loops += 1
        elif char is '#':
            print(MEMORY[pointer])

        if wrap:
            if MEMORY[pointer] > BYTESIZE:
                MEMORY[pointer] = 0
            elif MEMORY[pointer] < 0:
                MEMORY[pointer] = BYTESIZE

        progpos += 1

    return "".join(outbuff)
