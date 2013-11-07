#===============================================================================
# PyFudge: A Python-based Brainfuck Interpreter
#-------------------------------------------------------------------------------
# Version: 0.1.2
# Updated: 06-11-2013
# Author: Alex Crawford
# License: MIT
# Demo: http://repl.it/MOC
#===============================================================================

'''PyFudge is a Python-based (2.7.5) Brainfuck interpreter.

I believe it's fully functional (nested loops and all), but haven't
tested it thoroughly yet.

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

def read(program, wrap=True):
    '''pyfudge.read(program, wrap=True)

    Interprets a Brainfuck program fed into it.

    '''

    pointer = 0
    progpos = 0

    loopstack = []

    program = program.replace(" ", "")

    while True:

        try:

            for char in program[progpos]:

                if char is '+':
                    MEMORY[pointer] += 1
                elif char is '-':
                    MEMORY[pointer] -= 1
                elif char is '>':
                    pointer += 1
                elif char is '<':
                    pointer -= 1
                elif char is '.':
                    if MEMORY[pointer] != 0:
                        print(chr(MEMORY[pointer]), end="")
                elif char is ',':
                    MEMORY[pointer] = ord(raw_input())
                elif char is '[':
                    if MEMORY[pointer] == 0:
                        while True:
                            if program[progpos] is not ']':
                                progpos += 1
                            else:
                                break
                    loopstack.append(progpos - 1)
                elif char is ']':
                    if MEMORY[pointer] != 0:
                        progpos = loopstack[-1]
                    loopstack.pop(-1)
                elif char  is '#':
                    print(MEMORY[pointer])

                if wrap:
                    if MEMORY[pointer] > BYTESIZE:
                        MEMORY[pointer] = 0
                    elif MEMORY[pointer] < 0:
                        MEMORY[pointer] = BYTESIZE

                progpos += 1

        except:

            break
