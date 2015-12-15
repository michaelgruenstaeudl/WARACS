#!/usr/bin/env python
"""General String Operations
"""
__author__ = "Michael Gruenstaeudl, PhD"
__copyright__ = "Copyright (C) 2015 Michael Gruenstaeudl"
__email__ = "mi.gruenstaeudl@gmail.com"
__version__ = "2015.12.15.1100"

#####################
# IMPORT OPERATIONS #
#####################

from sys import platform as _platform
from random import choice as _choice
from string import lowercase as _lowercase
from sys import exit as _exit

import re

###########
# CLASSES #
###########

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
            print "  ERROR: ", self.__class__.__name__
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

class findAll:
    ''' class to find all instances of a substring in string 
    Args:
        substring <a>, string <b>
    Returns:
        list
    '''
    def __init__(self, a, b):
        self.substring = a
        self.astring = b
    def go(self):
        return [elem.start() for elem in re.finditer(self.substring, self.astring)]

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

class makePrettyTable:
    ''' Generate a table from an array
    Args:
        array <a>
    Returns:
        string
    '''
    def __init__(self, a):
        self.inArray = a
    def go(self):
        longest_str = max(self.inArray[:,0], key=len)
        outStr = ""
        for row in self.inArray:
            whitespaces = len(longest_str)-len(row[0])
            outStr += row[0].ljust(whitespaces) + " " + row[1] + "\n"
        return outStr

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
        return ''.join(_choice(_lowercase) for i in range(self.inInt))

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

class removePath:
    ''' Returns inStr without the prepending file path.
    Args:
        string <a>
    Returns:
        string
    '''
    def __init__(self, a):
        self.inStr = a
    def go(self):
        if _platform == "linux" or _platform == "linux2":
            sep = "/"
        elif _platform == "darwin":
            sep = "/"
        elif _platform == "win32":
            sep = "\\"
        return self.inStr[self.inStr.rfind(sep)+len(sep):]

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

class rmBlankLns:
    ''' Removes blank lines from file object
    Args:
        file object <a>
    Returns:
        string
    '''
    def __init__(self, a):
        self.inFile = a
    def go(self):
        aList = self.inFile.splitlines()
        aList = filter(None, aList)
        return "\n".join(aList)
    def go2(self):                                                      # Faster alternative that go()
        import os
        aList = self.inFile.splitlines()
        return os.linesep.join([s for s in aList if s])

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

class splitKeepSep2:                                                    # Problem: Difficult to know, if separator should be attached to left or right of element; currently to right 
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

class sublistInList:
    ''' Checks is sublist is in list
    Args:
        list <a>, list <b>
    Returns:
        list
    '''
    def __init__(self, a, b):
        self.alist = a
        self.sublist = a
    def go(self):
        n = len(self.sublist)
        return any((self.sublist == self.alist[i:i+n]) for i in xrange(len(self.alist)-n+1))


###############
# DEFINITIONS #
###############

def afind(inStr, kw):
    return afterFind(inStr, kw).go()

def csplit(inStr, delim, rflag=False):
    return clearSplit(inStr, delim, rflag).go()

def findall(substring, astring):
    return findAll(substring, astring).go()

def exstr(inStr, kw1, kw2):
    return exciseStr(inStr, kw1, kw2).afterKw()

def exstrkeepkw(inStr, kw1, kw2):
    return exciseStr(inStr, kw1, kw2).keepKw1()

def iseven(inInt):
    return isEven(inInt).go()

def makeprettytable(inArray):
    return makePrettyTable(inArray).go()

def randomword(length):
   return randomWord(length).go()

def replstr(inStr, kw1, kw2, replc):
    return replaceStr(inStr, kw1, kw2, replc).go()

def rmblanklns(inFile):
    return rmBlankLns(inFile).go()

def rmext(inStr):
    return removeExt(inStr).go()

def rmpath(inStr):
    return removePath(inStr).go()

def splitkeepsep(inStr, sep):
    return splitKeepSep(inStr, sep).go()

def splitkeepsep2(inStr, sep):
    return splitKeepSep2(inStr, sep).go()

def sublistinlist(alist, sublist):
    return sublistInList(alist, sublist).go()
