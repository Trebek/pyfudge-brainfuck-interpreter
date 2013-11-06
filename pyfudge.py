#===============================================================================
# PyFudge: A Python-based Brainfuck Interpreter
#-------------------------------------------------------------------------------
# Version: 0.1.1
# Updated: 05-11-2013
# Author: Alex Crawford
# License: MIT
#===============================================================================

'''***THIS IS A WIP, AND NOT FULLY FUNCTIONAL.***

PyFudge is a Python-based (2.7.5) Brainfuck interpreter.

At the moment it can interepret straightforward Brainfuck programs, but 
can't handle nested loops properly, yet. Will work on that.

'''

#===============================================================================
# IMPORTS
#===============================================================================

from __future__ import print_function

#===============================================================================
# THE BRAINFUCK INTERPRETER
#===============================================================================

class Pyfudge(object):
    ''''''

    MEMORYSIZE = 30000
    CELLSIZE = 255
    MEMORY = []

    @classmethod
    def interp(self, program):
        ''''''

        RUNNING = True

        pointer = 0
        progpos = 0

        value = 0

        looping = False
        loopstart = 0

        memleft = self.MEMORYSIZE
        while memleft > 0:
            self.MEMORY.append(0)
            memleft -= 1
        del memleft

        program = program.replace(" ", "")

        while RUNNING:
            try:
                for char in program[progpos]:
                    if char is '+':
                        self.MEMORY[pointer] += 1
                    elif char is '-':
                        self.MEMORY[pointer] -= 1
                    elif char is '>':
                        if value > 0:
                            self.MEMORY[pointer] += value
                        pointer += 1
                        value = 0
                    elif char is '<':
                        if value > 0:
                            self.MEMORY[pointer] += value
                        pointer -= 1
                        value = 0
                    elif char is '.':
                        if self.MEMORY[pointer] > 0:
                            print(chr(self.MEMORY[pointer]), end="")
                        else:
                            print(chr(self.MEMORY[pointer]), end="\n")
                    elif char is ',':
                        cmd  = int(raw_input())
                        self.MEMORY[pointer] = cmd
                    elif char is '[':
                        loopstart = progpos
                        looping = True
                    elif char is ']':
                        if looping:
                            if self.MEMORY[pointer] > 0:
                                progpos = loopstart
                            if self.MEMORY[pointer] == 0:
                                looping = False
                    elif char  is '*':
                        print(self.MEMORY[pointer], end=" ")

                    if self.MEMORY[pointer] > self.CELLSIZE:
                        self.MEMORY[pointer] = 0
                    elif self.MEMORY[pointer] <= -1:
                        self.MEMORY[pointer] = self.CELLSIZE

                    progpos += 1

            except:
                break
