#!/usr/bin/env python2
'''General File Operations'''
__author__ = "Michael Gruenstaeudl, PhD"
__copyright__ = "Copyright (C) 2014 Michael Gruenstaeudl"
__email__ = "gruenstaeudl.1@osu.edu"
__version__ = "2014.06.08.1700"
__status__ = "Working"

#####################
# IMPORT OPERATIONS #
#####################

import os

###########
# CLASSES #
###########


class loadFile:
    '''class for loading input files;
       needs filename <a> as input'''
    def __init__(self, a):
        self.filename = a

    def openFile(self):
        infile = open(self.filename, "r").read()
        return infile

    def readLines(self):
        infile = open(self.filename, "r").readlines()
        return infile

    def commaDelimited(self):
        infile = open(self.filename, "r").read().split(",")
        return infile


class saveF:
    '''class for saving data files;
       needs (a) filename <a>, (b) datafile <b>, and (c) appendflag <c>'''
    def __init__(self, a, b, c):
        self.filename = a
        self.data = b
        self.appendflag = c

    def go(self):
        if self.appendflag:
            outfile = open(self.filename, "a")
        if not self.appendflag:
            outfile = open(self.filename, "w")
        outfile.write(self.data)
        outfile.close()


class saveFilewithDFN:
    '''class for saving data files;
       needs (a) filename <a>, (b) datafile <b>, and (c) a datafile-name <c> as input'''
    def __init__(self, a, b, c):
        self.filename = a
        self.data = str(b)
        self.info = c

    def go(self):
        outfile = open(self.filename, "a")
        outfile.write(self.info+"\n"+self.data+"\n")
        outfile.close()


class removeFile:
    ''' class for deleting files;
        needs (a) filename <a> as input'''
    def __init__(self, a):
        self.filename = a

    def go(self):
        os.remove(self.filename)


class listallfilesindir:
    '''class for listing all files in directory;
       needs directory name <a> as input'''
    def __init__(self, a):
        self.directory = a

    def go(self):
        files_list = os.listdir(self.directory)
        return files_list


###############
# DEFINITIONS #
###############


def loadR(a):
    return loadFile(a).openFile()


def loadRL(a):
    return loadFile(a).readLines()


def loadCD(a):
    return loadFile(a).commaDelimited()


def saveFile(a, b):
    return saveF(a, b, False).go()


def append(a, b):
    return saveFile(a, b, True).go()


def saveFn(a, b, c):
    return saveFilewithDFN(a, b, c).go()


def deleteFile(a):
    removeFile(a).go()


def ListAllFilesInDir(a):
    return listallfilesindir(a).go()
