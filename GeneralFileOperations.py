#!/usr/bin/env python2
''' General File Operations '''
__author__ = "Michael Gruenstaeudl, PhD"
__copyright__ = "Copyright (C) 2015 Michael Gruenstaeudl"
__email__ = "mi.gruenstaeudl@gmail.com"
__version__ = "2015.10.09.1800"

#####################
# IMPORT OPERATIONS #
#####################

import os

###########
# CLASSES #
###########

class LoadFile:
    ''' Loading input files.
    Args:
        string <a>, string <b>, string <c>
    Returns:
        string
    '''
    def __init__(self, a):
        self.Fn = a
    def openFile(self):
        infile = open(self.Fn, "r").read()
        return infile
    def readLines(self):
        infile = open(self.Fn, "r").readlines()
        return infile
    def commaDelim(self):
        infile = open(self.Fn, "r").read().split(",")
        return infile

class SaveFile:
    ''' Saving data files.
    Args:
        string <a>, filehandle <b>, flag <c>
    Returns:
        none
    '''
    def __init__(self, a, b, c):
        self.Fn = a
        self.data = b
        self.appendflag = c
    def go(self):
        if self.appendflag:
            outfile = open(self.Fn, "a")
        if not self.appendflag:
            outfile = open(self.Fn, "w")
        outfile.write(self.data)
        outfile.close()

class SaveFilewithDFN:
    ''' Saving data files with filenames.
    Args:
        string <a>, filehandle <b>, string <c>
    Returns:
        none
    '''
    def __init__(self, a, b, c):
        self.Fn = a
        self.data = str(b)
        self.info = c
    def go(self):
        outfile = open(self.Fn, "a")
        outfile.write(self.info+"\n"+self.data+"\n")
        outfile.close()

class RemoveFile:
    ''' Deleting files.
    Args:
        string <a>
    Returns:
        none
    '''
    def __init__(self, a):
        self.Fn = a
    def go(self):
        os.remove(self.Fn)

class ListFilesInDir:
    ''' Listing all files in directory.
    Args:
        string <a>
    Returns:
        list
    '''
    def __init__(self, a):
        self.dr = a
    def go(self):
        return os.listdir(self.dr)


###############
# DEFINITIONS #
###############

def loadR(a):
    return LoadFile(a).openFile()

def loadRL(a):
    return LoadFile(a).readLines()

def loadCD(a):
    return LoadFile(a).commaDelim()

def saveFile(a, b):
    return SaveFile(a, b, False).go()

def append(a, b):
    return SaveFile(a, b, True).go()

def saveFn(a, b, c):
    return SaveFilewithDFN(a, b, c).go()

def deleteFile(a):
    RemoveFile(a).go()

def listAllFilesInDir(a):
    return ListFilesInDir(a).go()
