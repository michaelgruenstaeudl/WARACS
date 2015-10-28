#!/usr/bin/env python2
'''Reconstructing Ancestral Character States using BayesTraits'''
__author__ = "Michael Gruenstaeudl, PhD <mi.gruenstaeudl@gmail.com>"
__copyright__ = "Copyright (C) 2015 Michael Gruenstaeudl"
__info__ = "Reconstructing Ancestral Character States using BayesTraits (http://www.evolution.reading.ac.uk/BayesTraits.html)"
__version__ = "2015.10.28.1800"

#####################
# IMPORT OPERATIONS #
#####################

from cStringIO import StringIO
import argparse
import csv
import os
import string
import sys
import CustomFileOps as CFO
import CustomInstallOps as CIO
import CustomStringOps as CSO

opt_deps = ["dendropy", "numpy", "prettytable"]
if opt_deps:
    try:
        map(__import__, opt_deps)
    except:
        CIO.installPkgs(opt_deps)

from prettytable import PrettyTable
import dendropy
import numpy

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
    outFn_raw = fileprfx + "__BayesTraits_" + kw + ".full"
    outFn_tree = fileprfx + "__BayesTraits_" + kw + ".tre"
    outFn_table = fileprfx + "__BayesTraits_" + kw + ".csv"

    # 1.2. Setting outfilenames
    fileprfx = CSO.rmext(treedistrFn)
    fileinfo = "__BayesTraits_" + kw + "_char" + str(charnum)
    #if charmodel:                                                      # Not yet implemented
    #    fileinfo = fileinfo + "__charmodel_" + charmodel.replace(";",".").replace(",",".")
    outFn_raw = fileprfx + fileinfo + ".full"
    outFn_tree = fileprfx + fileinfo + ".tre"
    outFn_table = fileprfx + fileinfo + ".csv"

    charsFnTmp = charsFn + ".tmp"
    cmdFnTmp = CSO.randomword(6) + ".tmp"

    # 1.3. Generate tip list
    nodespecL, nodeL = [], []
    treeH = dendropy.Tree.get_from_path(plottreeFn, schema="nexus")
    for c, node in enumerate(treeH.nodes(), start=1):
        tips = [tip.taxon.label.replace(" ", "_") for tip in node.leaf_nodes()]
        if len(tips) > 1:
            nodespecL.append("AddNode Node" + str(c) + " " + " ".join(tips))
            nodeL.append(c)                                             # generate list of relevant node numbers
    node_specs = "\n".join(nodespecL)

    # 1.4. Modify chars-file
    reader = csv.reader(open(charsFn, "rb"), delimiter=",")
    arr = numpy.array(list(reader))
    arr = arr[:,[0,charnum]]
    p = PrettyTable()
    for row in arr:
        p.add_row(row)
    tmp = p.get_string(header=False, border=False)
    out = "\n".join([i.strip() for i in tmp.splitlines()])              # left-justify the string
    CFO.saveFile(charsFnTmp, out)

    # 1.5. Generate command string as save to file
    cmdStr = mdl + node_specs + "\nrun\n"
    CFO.saveFile(cmdFnTmp, cmdStr)


# 2. Reconstruction
# 2.1. Conduct reconstruction
    if verbose.upper() in ["T", "TRUE"]:
        print "  Character Reconstruction in BayesTraits"
        print "  Selected Reconstruction Method:", rcnmdl
    cmd = pathToSoftware + " " + treedistrFn + " " + charsFnTmp + " < " + cmdFnTmp
    dataH = os.popen(cmd).read()
    if parseKw not in dataH:
        sys.exit("  ERROR: No reconstruction data from BayesTraits received.")

# 2.2. Save outfile and delete temp files
    CFO.saveFile(outFn_raw, dataH)
    CFO.deleteFile(charsFnTmp + ".log.txt")
    CFO.deleteFile(charsFnTmp)


# 3. Parse reconstruction data
# 3.1. Get section
    tmp = CSO.exstrkeepkw(dataH, parseKw, "Sec:")
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
#   4.1. Converting tree from nexus into newick
    treeH = dendropy.Tree.get_from_path(plottreeFn, schema="nexus")     # Converting tree from nexus into newick format, because nexus format may contain translation table, which TreeGraph2 cannot parse
    plottree_newick = treeH.as_string(schema='newick')
    CFO.saveFile(outFn_tree, plottree_newick)

#   4.2. Save table
    CFO.saveFile(outFn_table, outD)
    
#   4.3. Decision on deleting temporary input file
    if keepTmpFile.upper() in ["F", "FALSE"]:
        CFO.deleteFile(cmdFnTmp)

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
