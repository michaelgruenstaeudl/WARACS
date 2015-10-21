#!/usr/bin/env python2
'''General Install Operations'''
__author__ = "Michael Gruenstaeudl, PhD"
__copyright__ = "Copyright (C) 2015 Michael Gruenstaeudl"
__email__ = "mi.gruenstaeudl@gmail.com"
__version__ = "2015.10.21.1300"

###########
# IMPORTS #
###########

from pkg_resources import WorkingSet, DistributionNotFound
import sys

###########
# CLASSES #
###########

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
                print "\n  Library " + pkgName + " needs to be installed."
                allow = raw_input("  May I install the above library? ([y]/n): ")  # Prompt for user decision if a package requires installation
                allow = allow.upper()
                if allow == "N" or allow == "NO":
                    sys.exit("\n  Please install package " + pkgName + " manually. Aborting.\n")
                else:
                    try:
                        response = urllib2.urlopen("http://www.google.com", timeout=10)
                    except urllib2.URLError as err:
                        sys.exit("\n  Please connect to the internet. Aborting.\n")
                install(["--user", pkgName])                                # Make certain to use the user flag
                # ALTERNATIVE 1: os.system("easy_install-2.7 --user " + pkgName)

                #import os
                #os.execv(__file__, sys.argv)                            # After installation via easy_install, I must restart the script for certain new modules (i.e. those installed via egg, like dendropy) to be properly loaded


class InstallPkgsByVersion:
    ''' Automatically installing packages using version information.
    Args:
        dictionary <a> (example: {"dendropy": "3.12.0", "numpy": "1.9.0"})
    Returns:
        none
    '''
    def __init__(self, a):
        self.pkgDict = a
        
    def go(self):
        working_set = WorkingSet()
        for pkgName, pkgVersion in self.pkgDict.iteritems():
            try:
                depends = working_set.require(pkgName)
            except DistributionNotFound:
                from urllib2 import URLError
                from setuptools.command.easy_install import main as install
                import os
                print "\n  Library " + pkgName + " needs to be installed.\n"
                allow = raw_input("  May I install the above library? ([y]/n): ")  # Prompt for user decision if a package requires installation
                allow = allow.upper()
                if allow == "N" or allow == "NO":
                    sys.exit("\n  Please install package " + pkgName + " manually. Aborting.\n")
                else:
                    try:
                        response = urllib2.urlopen("http://www.google.com", timeout=10)
                    except URLError as err:
                        sys.exit("\n  Please connect to the internet. Aborting.\n")
                install(["-U", pkgName, "==", pkgVersion])              # Make certain to use the user flag
                # ALTERNATIVE 2: os.system("easy_install-2.7 --user " + pkgName + "==" + pkgVersion)

                #import os
                #os.execv(__file__, sys.argv)                            # After installation via easy_install, I must restart the script for certain new modules (i.e. those installed via egg, like dendropy) to be properly loaded


###############
# DEFINITIONS #
###############

def installPkgs(pkgList):
    InstallPkgs(pkgList).go()

def installPkgsByVersion(pkgDict):
    InstallPkgsByVersion(pkgDict).go()
