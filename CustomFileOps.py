#!/usr/bin/env python2
''' General File Operations '''
__author__ = "Michael Gruenstaeudl, PhD"
__copyright__ = "Copyright (C) 2015 Michael Gruenstaeudl"
__email__ = "mi.gruenstaeudl@gmail.com"
__version__ = "2015.10.29.1800"

#####################
# IMPORT OPERATIONS #
#####################

from subprocess import Popen, PIPE
from pkg_resources import WorkingSet, DistributionNotFound
from sys import platform as _platform
from sys import exit as _exit
from time import sleep as _sleep

import os

###########
# CLASSES #
###########

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

class InstallPkgs:
    ''' Automatically installing packages.
    Args:
        list <a> (example: ["dendropy", "numpy"])
    Returns:
        none
    '''
    def __init__(self, a):
        self.pkgList = a
        
    def go(self):
        working_set = WorkingSet()
        for pkgName in self.pkgList:
            try:
                depends = working_set.require(pkgName)
            except DistributionNotFound:
                from setuptools.command.easy_install import main as install
                import urllib2
                print "\n  Library '" + pkgName + "' needs to be installed."
                allow = raw_input("  May I install the above library? ([y]/n): ")  # Prompt for user decision if a package requires installation
                allow = allow.upper()
                if allow == "N" or allow == "NO":
                    _exit("\n  ERROR: Please install package '" + pkgName + "' manually.\n")
                else:
                    try:
                        response = urllib2.urlopen("http://www.python.org/", timeout=10)
                    except urllib2.URLError as err:
                        _exit("\n  ERROR: No internet connection available.\n")
                try:
                    install(["--user", pkgName])                                # Make certain to use the user flag
                    # ALTERNATIVE: os.system("easy_install-2.7 --user " + pkgName + "==" + pkgVersion)
                    print "\n  Library '" + pkgName + "' installed successfully."
                    # ALTERNATIVE: print "\n  Library '" + pkgName + "v." + pkgVersion + "' installed successfully."
                except:
                    import os
                    if _platform == "linux" or _platform == "linux2":
                        if isExe("pip2.7"):
                            os.system("pip2.7 install " + pkgName + " --user")
                        else:
                            ("\n  ERROR: Python setuptools inaccessible.\n")
                    elif _platform == "darwin":
                        if isExe("pip2.7"):
                            os.system("pip2.7 install " + pkgName + " --user")
                        else:
                            ("\n  ERROR: Python setuptools inaccessible.\n")
                    elif _platform == "win32":
                        if isExe("pip2.7.exe"):
                            os.system("pip2.7.exe install " + pkgName)
                        else:
                            ("\n  ERROR: Python setuptools inaccessible.\n")
                try:
                    exec("import " + pkgName)
                except ImportError:
                    _exit("\n  Please restart this script.\n")         # After installation via easy_install, Python must be restarted for certain new modules to be properly loaded
                    #import os                                          # For later: Automatic restart
                    #os.execv(__file__, sys.argv)

class IsExe:
    ''' Checking if executable exists. '''
    def __init__(self, a):
        self.fpath = a
    def go(self):
        return os.path.isfile(self.fpath) and os.access(self.fpath, os.X_OK)

class PopenExtProg:
    ''' Class for communicating with executable via Popen.
    Args:
        inlist <a>, flag <b>
    Returns:
        string
    '''
    def __init__(self, a, b):
        self.cmdL = a
        self.flag = b
    def go(self):
        initCmd = " ".join(self.cmdL)
        p = Popen(initCmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
        if self.flag:
            _sleep(float(self.flag))
            p.stdin.write("quit\n")
        outStream, errorStream = p.communicate()
        #if errorStream:                                                # too sensistive with many programs
        #    _exit("  ERROR: ", self.err)
        return outStream

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

###############
# DEFINITIONS #
###############

def append(a, b):
    return SaveFile(a, b, True).go()
    
def deleteFile(a):
    RemoveFile(a).go()

def extprog(a, b=None):
    return PopenExtProg(a, b).go()

def installPkgs(pkgList):
    InstallPkgs(pkgList).go()

def isExe(a):
    return IsExe(a).go()

def listAllFilesInDir(a):
    return ListFilesInDir(a).go()

def loadCD(a):
    return LoadFile(a).commaDelim()

def saveFile(a, b):
    return SaveFile(a, b, False).go()

def saveFn(a, b, c):
    return SaveFilewithDFN(a, b, c).go()

def loadR(a):
    return LoadFile(a).openFile()

def loadRL(a):
    return LoadFile(a).readLines()
