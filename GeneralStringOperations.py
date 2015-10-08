#!/usr/bin/env python2
'''General String Operations'''
__author__ = "Michael Gruenstaeudl, PhD"
__email__ = "gruenstaeudl.1@osu.edu"
__version__ = "2014.08.25.1300"
__status__ = "Working"

#####################
# IMPORT OPERATIONS #
#####################

from termcolor import colored
import numpy
import random
import re
import string
import sys


###########
# CLASSES #
###########


class ExciseString:
    ''' Excises string via keyWrd delimitation.
    Args:
        inStr <a>, keyWrd1 <b>, keyWrd2 <c>
    Returns:
        outstring
    '''

    def __init__(self, a, b, c):
        self.inStr = a           # string
        self.keyWrd1 = b           # string
        self.keyWrd2 = c           # string

    def go(self):
        pos1 = AfterFind(self.inStr, self.keyWrd1).go()
        pos2 = self.inStr.find(self.keyWrd2, pos1)
        return self.inStr[pos1:pos2]


class ErrorReport:
    ''' class for reporting errors during TreeGraph2 execution '''

    def __init__(self, a, b):
        self.out = a
        self.err = b

    def go(self):
# Legacycode:
#        if not self.err and not self.out:
#            if "java.lang.NullPointerException" in self.out:
#                print self.out
#                print "Possible problem: Path to cwd must NOT have spaces!"
#            else:
#                print colored("  Error: ", 'magenta') + "Unknown TreeGraph2 error."
        if "ERROR" in self.out.upper():
            sys.exit(colored("  Error: ", 'magenta') + self.out)
        if self.err:
            sys.exit(colored("  Error: ", 'magenta') + self.err)


class ReplaceString:
    ''' Replaces a string via keyWrd delimitation.
    Args:
        inStr <a>, keyWrd1 <b>, keyWrd2 <c>, replacement <d>
    Returns:
        original string containing replacement(s)
    Note:
        currently requires that keyWrds are only found once;
        otherwise use TFL:
        return self.inStr.replace(self.inStr[pos1:pos2],self.replacement)
    '''

    def __init__(self, a, b, c, d):
        self.inStr = a           # string
        self.keyWrd1 = b         # string
        self.keyWrd2 = c         # string
        self.replacement = d     # string

    def go(self):
        pos1 = AfterFind(self.inStr, self.keyWrd1).go()
        pos2 = self.inStr.find(self.keyWrd2, pos1)
        return self.inStr[:pos1] + self.replacement + self.inStr[pos2:]
# Legacycode:
#        if self.inStr[pos1:pos2]:
#            output = self.inStr.replace(self.inStr[pos1:pos2],self.replacement)
#        # If string to be replaced were empty:
#        if not self.inStr[pos1:pos2]:
#            output = self.inStr[:pos1]+self.replacement+self.inStr[pos2:]
#        return output


class ClearSplit:
    ''' Splits string without removing delimiter.
    Args:
        inStr <a>, delimiter <b>, rightflag <c>
    Returns:
        outlist
    '''

    def __init__(self, a, b, c):
        self.inStr = a
        self.delimiter = b
        self.rightflag = c

    def go(self):
        splitList = self.inStr.split(self.delimiter)
        if len(splitList) < 2:
            print "*** Error in " + self.__class__.__name__
            print "*** Less than two elements after split."
        outlist = []
        if len(splitList) == 2:
            if not self.rightflag:
                outlist = [splitList[0]+self.delimiter, splitList[1]]
            if self.rightflag:
                outlist = [splitList[0], self.delimiter+splitList[1]]
        # Do NOT comment out the else statement, which is important
        # for AAR.py
        else:
            delim_list = list(numpy.repeat(numpy.array("<"), len(splitList)))
            for a, b in zip(delim_list, splitList):
                #if not self.rightflag:
                #print a+b
                outlist.append(a+b)
        return outlist


class AfterFind:
    '''
    Args:
        inStr <a>, keyWrd <b>
    Returns:
        index number of end of keyWrd in inStr
    '''
    def __init__(self, a, b):
        self.inStr = a
        self.keyWrd = b

    def go(self):
        pos1 = self.inStr.find(self.keyWrd) + len(self.keyWrd)
        return pos1


class RemoveExtension:
    '''class for returning inStr without extension (i.e. ".txt" or ".trees";
       needs inStr <a> and delimiter <b> as input '''
    def __init__(self, a, b):
        self.inStr = a
        self.delimiter = b

    def go(self):
        return self.inStr[:self.inStr.rfind(self.delimiter)]


class is_even:
    '''class for checking if number is even;
       needs number <a> as input '''
    def __init__(self, a):
        self.innumber = a

    def go(self):
        return self.innumber % 2 == 0


class MakePairwise:
    ''' Converts a list into pairs of two.
    Args:
        inlist <a>
    Returns:
        outlist: list of pairs
    '''
    def __init__(self, a):
        self.inL = a

    def go(self):
        from itertools import tee, izip
        a, b = tee(self.inL)
        next(b, None)
        return izip(a, b)


###############
# DEFINITIONS #
###############

def afind(inStr, keyWrd):
    return AfterFind(inStr, keyWrd).go()


def csplit(inStr, delimiter, rightflag=False):
    return ClearSplit(inStr, delimiter, rightflag).go()


def exstr(inStr, keyWrd1, keyWrd2):
    return ExciseString(inStr, keyWrd1, keyWrd2).go()

def errep(inStr1, inStr2):
    return ErrorReport(inStr1, inStr2).go()

def replstr(inStr, keyWrd1, keyWrd2, replacement):
    return ReplaceString(inStr, keyWrd1, keyWrd2, replacement).go()


def rmext(a):
    return RemoveExtension(a, ".").go()


def iseven(a):
    return is_even(a).go()

def rmblanklns(a):
    ''' remove blank lines from string '''
    a = a.split('\n')
    a = filter(None, a)
    return '\n'.join(a)

def splitkeepsep(aStr, sep):
    ''' splits a string by separator, but keeps separator
    inspired by http://programmaticallyspeaking.com '''
    return reduce(lambda acc, elem: acc +
                  [elem] if elem == sep else acc[:-1] +
                  [acc[-1] + elem],
                  re.split("(%s)" % re.escape(sep), aStr)[1:], [])

def splitkeepsep2(aStr, sep):
        return [e+sep for e in aStr.split(sep) if e != ""]

def randomword(length):
   return ''.join(random.choice(string.lowercase) for i in range(length))
