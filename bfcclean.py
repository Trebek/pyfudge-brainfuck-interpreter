#===============================================================================
# BFCC: Brainfuck Code Cleaner
#-------------------------------------------------------------------------------
# Version: 0.1.0
# Updated: 11-11-2013
# Author: Alex Crawford
# License: MIT
#===============================================================================

'''Removes useless (at least in terms of interpreting) characters, and 
whitespace from Brainfuck programs, leaving the bare code. Also has an 
extra function for breaking up BF programs into 80 (or any other number) 
character lines, and then returning the reformatted code.
'''

#===============================================================================
# IMPORTS
#===============================================================================

from __future__ import print_function

#===============================================================================
# BFCC CLASS
#===============================================================================

class BFCC(object):
    ''''''

    def __init__(self, program):
        ''''''
        self.funcchar = '+-><.,[]'

        self.program = program
        self.proglen = len(self.program)

    def strip(self):
        ''''''
        progpos = 0

        while progpos < self.proglen:
            char = self.program[progpos]
            if char not in self.funcchar or char is '\n':
                self.program = self.program.replace(char, '')
                self.proglen = len(self.program)
                progpos = -1
            progpos += 1

        return self.program

    def stripspace(self):
        ''''''
        self.program = self.program.replace(' ', '')
        return self.program

    def breaklines(self, width=80):
        ''''''
        progpos = 0
        count = 0
        start = 0
        broken = []

        while progpos < self.proglen:
            if count == width:
                broken.append(self.program[start:progpos])
                broken.append('\n')
                start = progpos
                count = 0
            count += 1
            progpos += 1
        else:
            broken.append(self.program[start:progpos])

        self.program = ''.join(broken)

        return self.program

#===============================================================================
# SHORTCUT FUNCTIONS
#===============================================================================

def BFCCstrip(program):
    ''''''
    output = BFCC(program).strip()
    return output

def BFCCstripspace(program):
    ''''''
    output = BFCC(program).stripspace()
    return output

def BFCCbreak(program, width=80):
    ''''''
    output = BFCC(program).breaklines(width=width)
    return output

def BFCCmain(program, width=80):
    ''''''
    stage1 = BFCC(program).strip()
    output = BFCC(stage1).breaklines(width=width)
    return output
    
