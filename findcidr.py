#!/usr/bin/env python3

# findcidr.py: StdInString --> StdOutString
# Purpose: to accept an IP address as String, and print its smallest
#          registered CIDR block as a String to StdOut

import sys
import os

def main(calltype, pInput):
    '''main: String String/FileHandle
    Purpose: determine whether the program was passed a file handle or
             piped string input
    '''
    if calltype is "file":
        processFile(pInput)
    elif calltype is "pipe":
        processPipe(pInput)
    else:
        sys.exit("findcidr: program called incorrectly. Accepts input
        only from StdIn or when passed a path to a file of IP
        addresses.")

def processFile(addrFile): 
    '''processFile: FileHandle
    '''

# Call main
if __name__ == '__main__':
    if not os.isatty(0):
        pipeInput = sys.stdin.readlines()
        for line in pipeInput:
            main("pipe", line)
    else:
         try:
             addressFile = open(sys.argv[1], 'r')
             main(addressFile)
         except IndexError as e:
             print('Correct use: findcidr /path/to/ListOfIPs')
         except:
             print("Unexpected error: ", sys.exc_info()[0])
             raise
