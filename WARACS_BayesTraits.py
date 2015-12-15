#!/usr/bin/env python
"""Reconstructing Ancestral Character States using BayesTraits
"""

#####################
# IMPORT OPERATIONS #
#####################

from __future__ import absolute_import
from __future__ import print_function
from six.moves import zip

import argparse
import csv
import sys
import CustomFileOps as CFO
import CustomPhyloOps as CPO
import CustomStringOps as CSO

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO                                             # In Python 3, the 'io' module replaces the 'StringIO' module

numpy = CFO.loadModule("numpy")

###############
# AUTHOR INFO #
###############

__author__ = "Michael Gruenstaeudl, PhD <mi.gruenstaeudl@gmail.com>"
__copyright__ = "Copyright (C) 2015 Michael Gruenstaeudl"
__info__ = "Reconstructing Ancestral Character States using BayesTraits (http://www.evolution.reading.ac.uk/BayesTraits.html)"
__version__ = "2015.12.15.1100"

#############
# DEBUGGING #
#############

#import pdb
#pdb.set_trace()

####################
# GLOBAL VARIABLES #
####################

bayesModel = "1\n2\n"
bayesKw = "Iteration\tLh"
likeModel = "1\n1\n"
likeKw = "Tree No\tLh"

###########
# CLASSES #
###########


###########
# MODULES #
###########

def main(treedistrFn, plottreeFn, charsFn, charnum, rcnmdl, pathToSoftware, keepTmpFile, verbose):

    # 1.1. Decision on model
    kw = rcnmdl.lower()
    if kw == "likelihood" or kw == "like" or kw == "l":
        mdl = likeModel
        parseKw = likeKw
    if kw == "bayesian" or kw == "bayes" or kw == "b":
        mdl = bayesModel
        parseKw = bayesKw

    # 1.2. Setting outfilenames
    fileprfx = CSO.rmpath(CSO.rmext(treedistrFn))
    fileinfo = "__BayesTraits_" + kw + "_char" + str(charnum)
    outFn_raw = fileprfx + fileinfo + ".txt"
    outFn_tree = fileprfx + fileinfo + ".tre"
    outFn_table = fileprfx + fileinfo + ".csv"
    charsFnTmp = charsFn + ".tmp"
    compiledInFn = "compiledInfileForBayesTraits.tmp"

    # 1.3. Generate tip list
    out_handle = CPO.GetNodeListFromTree(plottreeFn)
    node_specs, nodeL = out_handle[0], out_handle[1]

    # 1.4. Modify chars-file
    reader = csv.reader(open(charsFn, "r"), delimiter=",")
    arr = numpy.array(list(reader))
    arr = arr[:,[0,charnum]]                                            # Extracting a particular column
    out_handle = CSO.makeprettytable(arr)
    CFO.saveFile(charsFnTmp, out_handle)

    # 1.5. Generate command string as save to file
    cmdStr = mdl + node_specs + "\nrun\n"
    CFO.saveFile(compiledInFn, cmdStr)


# 2. Reconstruction in BayesTraits
    if verbose.upper() in ["T", "TRUE"]:
        print("  Character Reconstruction in BayesTraits")
        print("  Selected Reconstruction Method:", rcnmdl)
    cmdL = [pathToSoftware, treedistrFn, charsFnTmp, "<", compiledInFn]
    data_handle = CFO.extprog(cmdL)
    if not data_handle or parseKw not in data_handle:
        sys.exit("  ERROR: No reconstruction data from BayesTraits received.")
    CFO.saveFile(outFn_raw, data_handle)

# 3. Parse reconstruction data
# 3.1. Get section
    tmp = CSO.exstrkeepkw(data_handle, parseKw, "Sec:")
    reader = csv.reader(StringIO(tmp), delimiter="\t")                  # csv.reader can only read file object
    arr = numpy.array(list(reader))                                     # reader holds the data only for one execution; hence immediately transfer it to variable "arr"

# 3.2. Extract all those cols that contain keyw
    colHeaders = list(arr[0])
    outL = []
    for node in nodeL:
        kw = "Node" + str(node) + " "                                   # Keyword: "Node" + str(node) + " "
        matchHeaders = [h for h in colHeaders if kw in h]
        matchCols = [colHeaders.index(h) for h in matchHeaders]
        valueArr = [e[matchCols] for e in arr[1:]]                      # values for a particular node still as columns
        valueArr_t = numpy.transpose(valueArr)                          # after transposition, values for a particular node now as rows

# 3.2.1. Calculate column sum divided by column length
        matchVals = []
        for line in valueArr_t:
            l = list(line)
            if "--" in l:
                l = [i for i in l if i != "--"]                         # remove elements that indicate absence of node in tree
            try:
                l = [float(i) for i in l]                               # convert all list items to floats
                r = sum(l)/len(l)
                r = float("{0:.3f}".format(r))                          # round float to 3 decimal places; preferrable than string indexing (e.g. string[:3])
            except ZeroDivisionError or TypeError:                      # if list l were empty, b/c all items "--"
                r = 0
            matchVals.append(r)
        if len(matchHeaders) != len(matchVals):
            sys.exit("  ERROR: Error when parsing the reconstruction results.")

# 3.2.2. Important step
        if sum(matchVals) > 0:                                          # IMPORTANT STEP: only write line if reconstruction present
            tmpL = []
            for h, v in zip(matchHeaders, matchVals):
                if v > 0:                                               # IMPORTANT STEP: only write area if present
                    tmpL.append(CSO.exstr(h,"(",")") + ":" + str(v))
            node_recon = ";".join(tmpL)
            tmpStr = str(node) + "," + node_recon
            outL.append(tmpStr)
    outD = "\n".join(outL)


# 4. Saving files to disk  
#   4.1. Converting tree from nexus to newick
    plottree = CFO.loadR(plottreeFn)
    plottree_newick = CPO.ConvertNexusToNewick(plottree)                # Converting tree from nexus into newick format, because nexus format may contain translation table, which TreeGraph2 cannot parse
    CFO.saveFile(outFn_tree, plottree_newick)

#   4.2. Save main results
    CFO.saveFile(outFn_table, outD)
    
# 5. Decision on deleting temporary files
    CFO.deleteFile(charsFnTmp + ".log.txt")
    if keepTmpFile.upper() in ["F", "FALSE"]:
        CFO.deleteFile(charsFnTmp)
        CFO.deleteFile(compiledInFn)
        CFO.deleteFile(outFn_raw)

############
# ARGPARSE #
############

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="  --  ".join([__author__, __copyright__, __info__, __version__]))
    parser.add_argument('-t', '--treedistr',
                        help='/path_to_input/tree_distribution.tre',
                        required=True)
    parser.add_argument('-p', '--plottree',
                        help='/path_to_input/plotting_tree.tre',
                        required=True)
    parser.add_argument('-c', '--chars',
                        help='/path_to_input/character_state_distribution.csv',
                        required=True)
    parser.add_argument('-n', '--charnumber',
                        help='which character to use (e.g. 1)',
                        default='1',
                        required=True)
    parser.add_argument('-o', '--optcrit',
                        help='models of character evolution; available: likelihood, bayesian',
                        default='likelihood',
                        required=True)
    parser.add_argument('-s', '--software',
                        help='/path_to_software/mesquite.sh',
                        required=True)
    parser.add_argument('-k', '--keep',
                        help='Keeping the temporary input file; a boolean operator',
                        required=False,
                        default='False')
    parser.add_argument('-v', '--verbose',
                        help='Displaying full; a boolean operator',
                        required=False,
                        default='False')
    parser.add_argument('-V', '--version', 
                        help='Print version information and exit',
                        action='version',
                        version='%(prog)s ' + __version__)
    args = parser.parse_args()


########
# MAIN #
########

main(args.treedistr, args.plottree, args.chars, args.charnumber, args.optcrit, args.software, args.keep, args.verbose)
