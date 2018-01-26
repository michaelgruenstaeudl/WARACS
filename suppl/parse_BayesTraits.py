#!/usr/bin/env python
"""Parsing the Results of BayesTraits
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
__copyright__ = "Copyright (C) 2015-2016 Michael Gruenstaeudl"
__info__ = "Parsing the Results of BayesTraits"
__version__ = "2016.01.08.1600"

#############
# DEBUGGING #
#############

#import pdb
#pdb.set_trace()

####################
# GLOBAL VARIABLES #
####################


###########
# CLASSES #
###########


###########
# MODULES #
###########

def main(bayestraitsFn, plottreeFn, rcnmdl):

# 1. Read input
# 1.1. Decision on model
    kw = rcnmdl.lower()
    if kw == "likelihood" or kw == "like" or kw == "l":
        parseKw = "Tree No\tLh"
    if kw == "bayesian" or kw == "bayes" or kw == "b":
        parseKw = "Iteration\tLh"
# 1.2. Setting outfilenames
    fileprfx = CSO.rmpath(CSO.rmext(bayestraitsFn))
    outFn_tree = fileprfx + "_out" + ".tre"
    outFn_table = fileprfx + "_out" + ".csv"
    
# 2. Generate list of nodes of plotting tree
    out_handle = CPO.GetNodeListFromTree(plottreeFn)
    node_specs, nodeL = out_handle[0], out_handle[1]

# 3. Extract reconstruction data
# 3.1. Get section
    data_handle = CFO.loadR(bayestraitsFn)
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

# 4. Saving results to files
# 4.1. Converting tree from nexus to newick
    plottree = CFO.loadR(plottreeFn)
    plottree_newick = CPO.ConvertNexusToNewick(plottree)                # Converting tree from nexus into newick format, because nexus format may contain translation table, which TreeGraph2 cannot parse
    CFO.saveFile(outFn_tree, plottree_newick)
# 4.2. Save main results
    CFO.saveFile(outFn_table, outD)


############
# ARGPARSE #
############

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="  --  ".join([__author__, __copyright__, __info__, __version__]))
    parser.add_argument('-t', '--bayestraits',
                        help='/path_to_input/bayestraits_results.tre',
                        required=True)
    parser.add_argument('-p', '--plottree',
                        help='/path_to_input/plotting_tree.tre',
                        required=True)
    parser.add_argument('-o', '--optcrit',
                        help='models of character evolution; available: likelihood, bayesian',
                        default='likelihood',
                        required=True)
    parser.add_argument('-V', '--version', 
                        help='Print version information and exit',
                        action='version',
                        version='%(prog)s ' + __version__)
    args = parser.parse_args()


########
# MAIN #
########

main(args.bayestraits, args.plottree, args.optcrit)
