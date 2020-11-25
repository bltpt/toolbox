#!/usr/bin/python3

# find-duplicates: DirPath [Options] -> StdOut
# Purpose: to return a list of duplicate files residing in the
#          directory hierarchy in DirPath.

import hashlib
import os

def hashFile(filePath, algorithm):
    '''hashFile(): Str1 Str2 --> StrA
    Purpose: to hash the file at Str1 with the algorithm of Str2 and
             return its hash as StrA.
    '''
    if algorithm in hashlib.algorithms_guaranteed:
        hasher = getattr(hashlib, algorithm)()
    else:
        raise ValueError("Unsupported hash algorithm: %s" % algorithm)

    blocksize = 65536

    with open(filePath, 'rb') as f:
        buf = f.read(blocksize)
        while len(buf) > 0:
            hasher.update(buf)
            buf = f.read(blocksize)

    return(hasher.hexdigest())

def main(dirPath, algorithm):
    '''main(): Str1 Str2 -> StdOut
    Purpose: to find all duplicate files in directory path Str1 using
             hash algorithm Str2, printing their hashes and file paths
             to StdOut.
    '''

    # Need support for -max-depth optional arg.

    # Walk the path at dirPath, hash each file, check whether hash has
    # been seen, and if not, add to the "seen" list. If it's already
    # been seen, print the already "seen" one and the one in the
    # current loop.
    seen = list()

    # will need to recurse through each directory it finds. See if
    # there's a native way to do this with the os module, else,
    # put it in an function and call it recursively.
    try:
        for item in os.walk(dirPath):
            if item[0] == cwd:
                for file in item[2]:
                    # various temp file tests...
                    if '~' not in file:
                    if '#' not in file:
                        if file[0] not in '.':
                            if os.access(file, os.X_OK): # is executable?
                                executables.append(file)
   
    
    
    

