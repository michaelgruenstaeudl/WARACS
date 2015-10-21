#!/usr/bin/env python2
''' General String Operations '''
__author__ = "Michael Gruenstaeudl, PhD"
__copyright__ = "Copyright (C) 2015 Michael Gruenstaeudl"
__email__ = "mi.gruenstaeudl@gmail.com"
__version__ = "2015.10.09.1800"

#####################
# IMPORT OPERATIONS #
#####################

import random
import re
import string
import sys
import GeneralInstallOperations as GIO

opt_deps = ["termcolor"]
try:
    map(__import__, opt_deps)
except:
    GIO.installPkgs(opt_deps)

from termcolor import colored

###########
# CLASSES #
###########

class exciseStr:
    ''' Excises string via kw delimitation.
    Args:
        inStr <a>, kw1 <b>, kw2 <c>
    Returns:
        outstring
    '''
    def __init__(self, a, b, c):
        self.inStr = a
        self.kw1 = b
        self.kw2 = c
    def afterKw(self):
        pos1 = afterFind(self.inStr, self.kw1).go()
        pos2 = self.inStr.find(self.kw2, pos1)
        return self.inStr[pos1:pos2]
    def keepKw1(self):
        pos1 = self.inStr.find(self.kw1)
        pos2 = self.inStr.find(self.kw2, pos1)
        return self.inStr[pos1:pos2]

class errorReport:
    ''' Reports errors during software execution.
    Args:
        inStr <a>, inStr <b>
    Returns:
        none
    '''
    def __init__(self, a, b):
        self.out = a
        self.err = b
    def go(self):
        if "ERROR" in self.out.upper():
            sys.exit(colored("  ERROR: ", "white", "on_red") + self.out)
        if self.err:
            sys.exit(colored("  ERROR: ", "white", "on_red") + self.err)

class replaceStr:
    ''' Replaces a string via kw delimitation.
    Args:
        inStr <a>, kw1 <b>, kw2 <c>, replc <d>
    Returns:
        original string containing replc(s)
    Note:
        currently requires that kws are only found once;
        otherwise use TFL:
        return self.inStr.replace(self.inStr[pos1:pos2],self.replc)
    '''
    def __init__(self, a, b, c, d):
        self.inStr = a
        self.kw1 = b
        self.kw2 = c
        self.replc = d
    def go(self):
        pos1 = afterFind(self.inStr, self.kw1).go()
        pos2 = self.inStr.find(self.kw2, pos1)
        return self.inStr[:pos1] + self.replc + self.inStr[pos2:]

class clearSplit:
    ''' Splits string without removing delim.
    Args:
        inStr <a>, delim <b>, rflag <c>
    Returns:
        outlist
    '''
    def __init__(self, a, b, c):
        self.inStr = a
        self.delim = b
        self.rflag = c
    def go(self):
        splitL = self.inStr.split(self.delim)
        if len(splitL) < 2:
            print colored("  ERROR: ", "white", "on_red") + self.__class__.__name__
            print "  Less than two elements after split."
        outlist = []
        if len(splitL) == 2:
            if not self.rflag:
                outlist = [splitL[0]+self.delim, splitL[1]]
            if self.rflag:
                outlist = [splitL[0], self.delim+splitL[1]]
        else:                                                           # Do NOT comment out the else statement, which is important for ASR_Mesquite.py
            delim_list = list(numpy.repeat(numpy.array("<"), len(splitL)))
            for a, b in zip(delim_list, splitL):
                outlist.append(a+b)
        return outlist

class afterFind:
    '''
    Args:
        string <a>, string <b>
    Returns:
        integer
    '''
    def __init__(self, a, b):
        self.inStr = a
        self.kw = b
    def go(self):
        pos1 = self.inStr.find(self.kw) + len(self.kw)
        return pos1

class removeExt:
    ''' Returns inStr without extension (i.e. ".txt" or ".trees").
    Args:
        string <a>
    Returns:
        string
    '''
    def __init__(self, a):
        self.inStr = a
    def go(self):
        sep = "."
        return self.inStr[:self.inStr.rfind(sep)]

class isEven:
    ''' Checking if number is even.
    Args:
        integer <a>
    Returns:
        boolean
    '''
    def __init__(self, a):
        self.inInt = a
    def go(self):
        return self.inInt % 2 == 0

class makePairwise:
    ''' Converts a list into pairs of two.
    Args:
        list <a>
    Returns:
        list: list of pairs
    '''
    def __init__(self, a):
        self.inL = a
    def go(self):
        from itertools import tee, izip
        a, b = tee(self.inL)
        next(b, None)
        return izip(a, b)

class rmBlankLns:
    ''' Removes blank lines from file object
    Args:
        file object <a>
    Returns:
        file object
    '''
    def __init__(self, a):
        self.inFile = a
    def go(self):
        aList = self.inFile.splitlines()
        aList = filter(None, aList)
        return "\n".join(aList)

class splitKeepSep:
    ''' Split a string by separator, but keeps separator
    Args:
        string <a>
    Returns:
        list
    '''
    def __init__(self, a, b):
        self.inStr = a
        self.sep = b
    def go(self):
        outL = reduce(lambda acc, elem: acc +
                  [elem] if elem == self.sep else acc[:-1] +
                  [acc[-1] + elem],
                  re.split("(%s)" % re.escape(self.sep), self.inStr)[1:], [])
        return outL

class splitKeepSep2:
    ''' Split a string by separator, but keeps separator
    Args:
        string <a>
    Returns:
        list
    '''
    def __init__(self, a, b):
        self.inStr = a
        self.sep = b
    def go(self):
        return [e + self.sep for e in self.inStr.split(self.sep) if e != ""]

class randomWord:
    ''' Generate a random word of defined length
    Args:
        integer <a>
    Returns:
        string
    '''
    def __init__(self, a):
        self.inInt = a
    def go(self):
        return ''.join(random.choice(string.lowercase) for i in range(self.inInt))


###############
# DEFINITIONS #
###############

def afind(inStr, kw):
    return afterFind(inStr, kw).go()

def csplit(inStr, delim, rflag=False):
    return clearSplit(inStr, delim, rflag).go()

def exstr(inStr, kw1, kw2):
    return exciseStr(inStr, kw1, kw2).afterKw()

def exstrkeepkw(inStr, kw1, kw2):
    return exciseStr(inStr, kw1, kw2).keepKw1()

def errep(inStr1, inStr2):
    return errorReport(inStr1, inStr2).go()

def iseven(inInt):
    return isEven(inInt).go()

def randomword(length):
   return randomWord(length).go()

def replstr(inStr, kw1, kw2, replc):
    return replaceStr(inStr, kw1, kw2, replc).go()

def rmblanklns(inFile):
    return rmBlankLns(inFile).go()

def rmext(inStr):
    return removeExt(inStr).go()

def splitkeepsep(inStr, sep):
    return splitKeepSep(inStr, sep).go()

def splitkeepsep2(inStr, sep):
    return splitKeepSep2(inStr, sep).go()
