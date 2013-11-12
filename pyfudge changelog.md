PyFudge Changelog
=============================

#### v0.1.6

- Created a Pyfudge class, and collected all of the main functions, memory variables, etc. in there.
- PyFudge now uses the BFCC (Brainfuck Code Cleaner) script if it's available. Runs slightly faster overall when using BFCC over the default str.replace call, which only removes spaces at the moment.

#### v0.1.5

- Can now run PyFudge from the command line.
- Added a general error handling exception that tells you what the error was.
- PyFudge now dumps the program output and memory to two separate text files after running a program (output.txt, and memory.txt).
- Fixed the auto memory feature, so it doesn't use 'try' anymore. Don't know why I did it that way in the first place.
- Added a function for handing loops. Cuts down some minor code repetition.

#### v0.1.4

- PyFudge now generates and uses a list of loop jump points, instead of counting brackets.
- Added a function for setting the memory. Used by MakeFudge.
- Changed a few of the variable names.
