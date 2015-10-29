#!/usr/bin/env python2
'''General Install Operations'''
__author__ = "Michael Gruenstaeudl, PhD"
__copyright__ = "Copyright (C) 2015 Michael Gruenstaeudl"
__email__ = "mi.gruenstaeudl@gmail.com"
__version__ = "2015.10.28.2200"

###########
# IMPORTS #
###########

from pkg_resources import WorkingSet, DistributionNotFound
from sys import platform as _platform
import sys
import CustomFileOps as GFO

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
                print "\n  Library '" + pkgName + "' needs to be installed."
                allow = raw_input("  May I install the above library? ([y]/n): ")  # Prompt for user decision if a package requires installation
                allow = allow.upper()
                if allow == "N" or allow == "NO":
                    sys.exit("\n  ERROR: Please install package '" + pkgName + "' manually.\n")
                else:
                    try:
                        response = urllib2.urlopen("http://www.python.org/", timeout=10)
                    except urllib2.URLError as err:
                        sys.exit("\n  ERROR: No internet connection available.\n")
                try:
                    install(["--user", pkgName])                                # Make certain to use the user flag
                    # ALTERNATIVE: os.system("easy_install-2.7 --user " + pkgName + "==" + pkgVersion)
                    print "\n  Library '" + pkgName + "' installed successfully."
                    # ALTERNATIVE: print "\n  Library '" + pkgName + "v." + pkgVersion + "' installed successfully."
                except:
                    import os
                    if _platform == "linux" or _platform == "linux2":
                        if GFO.isExe("pip2.7"):
                            os.system("pip2.7 install " + pkgName + " --user")
                        else:
                            ("\n  ERROR: Python setuptools inaccessible.\n")
                    elif _platform == "darwin":
                        if GFO.isExe("pip2.7"):
                            os.system("pip2.7 install " + pkgName + " --user")
                        else:
                            ("\n  ERROR: Python setuptools inaccessible.\n")
                    elif _platform == "win32":
                        if GFO.isExe("pip2.7.exe"):
                            os.system("pip2.7.exe install " + pkgName)
                        else:
                            ("\n  ERROR: Python setuptools inaccessible.\n")
                try:
                    exec("import " + pkgName)
                except ImportError:
                    sys.exit("\n  Please restart this script.\n")         # After installation via easy_install, Python must be restarted for certain new modules to be properly loaded
                    #import os                                          # For later: Automatic restart
                    #os.execv(__file__, sys.argv)


###############
# DEFINITIONS #
###############

def installPkgs(pkgList):
    InstallPkgs(pkgList).go()
