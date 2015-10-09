#!/usr/bin/env python2
''' Conducting Ancestral State Reconstructions (ASRs) with BayesTraits'''
__author__ = "Michael Gruenstaeudl, PhD"
__copyright__ = "Copyright (C) 2015 Michael Gruenstaeudl"
__email__ = "mi.gruenstaeudl@gmail.com"
__version__ = "2015.10.08.1700"

# IMPORT OPERATIONS
from cStringIO import StringIO
from prettytable import PrettyTable
from termcolor import colored
import argparse
import dendropy
import csv
import numpy
import os
import string
import sys
import GeneralFileOperations as GFO
import GeneralStringOperations as GSO

# DEBUG HELPER
import pdb
#pdb.set_trace()

# GLOBAL VARIABLES
bayesModel = "1\n2\n"
likeModel = "1\n1\n"

# MODULES
def main(treedistrFn, plottreeFn, charsFn, charnum, rcnmdl, pathToSoftware):


# 1. Preparatory Actions
# 1.1. Set up out- and tmp-filenames
    fileprfx = GSO.rmext(treedistrFn)
    outFn_raw = fileprfx + ".ASRviaBAYESTRAITS.full"
    outFn_tree = fileprfx + ".ASRviaBAYESTRAITS.tre"
    outFn_table = fileprfx + ".ASRviaBAYESTRAITS.csv"

    charsFnTmp = charsFn + ".tmp"
    cmdFnTmp = GSO.randomword(6) + ".tmp"

# 1.2. Generate tip list
    nodespecL, nodeL = [], []
    treeH = dendropy.Tree.get_from_path(plottreeFn, schema="nexus")
    for c, node in enumerate(treeH.nodes(), start=1):
        tips = [tip.taxon.label.replace(" ", "_") for tip in node.leaf_nodes()]
        if len(tips) > 1:
            nodespecL.append("AddNode Node" + str(c) + " " + " ".join(tips))
            nodeL.append(c)                                             # generate list of relevant node numbers
    node_specs = "\n".join(nodespecL)

# 1.3. Modify chars-file
    reader = csv.reader(open(charsFn, "rb"), delimiter=",")
    arr = numpy.array(list(reader))
    arr = arr[:,[0,charnum]]
    p = PrettyTable()
    for row in arr:
        p.add_row(row)
    tmp = p.get_string(header=False, border=False)
    out = "\n".join([i.strip() for i in tmp.splitlines()])              # left-justify the string
    GFO.saveFile(charsFnTmp, out)

# 1.4. Decision on model
    if rcnmdl.lower() == "likelihood":
        mdl = likeModel
    if rcnmdl.lower() == "bayesian":
        mdl = bayesModel

# 1.5. Generate command string as save to file
    cmdStr = mdl + node_specs + "\nrun\n"
    GFO.saveFile(cmdFnTmp, cmdStr)


# 2. Reconstruction
# 2.1. Conduct reconstruction
    print "  Character Reconstruction in BayesTraits"
    print "  Selected Reconstruction Method:", rcnmdl
    cmd = pathToSoftware + " " + treedistrFn + " " + charsFnTmp + " < " + cmdFnTmp
    dataH = os.popen(cmd).read()
    if "Tree No\tLh" not in dataH:
        sys.exit(colored("  ERROR: ", 'red') + "No reconstruction data from BayesTraits received.")

# 2.2. Save outfile and delete temp files
    GFO.saveFile(outFn_raw, dataH)
    GFO.deleteFile(charsFnTmp + ".log.txt")
    GFO.deleteFile(charsFnTmp)
    GFO.deleteFile(cmdFnTmp)


# 3. Parse reconstruction data
# 3.1. Get section
    tmp = GSO.exstrkeepkw(dataH, "Tree No\tLh", "Sec:")
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
            sys.exit(colored("  ERROR: ", "magenta") + "Something wrong with parsing the reconstruction results!")
# 3.2.2. Important step
        if sum(matchVals) > 0:                                          # IMPORTANT STEP: only write line if reconstruction present
            tmpL = []
            for h, v in zip(matchHeaders, matchVals):
                if v > 0:                                               # IMPORTANT STEP: only write area if present
                    tmpL.append(GSO.exstr(h,"(",")") + ":" + str(v))
            node_recon = ";".join(tmpL)
            tmpStr = str(node) + "," + node_recon
            outL.append(tmpStr)
    outD = "\n".join(outL)


# 4. Saving files to disk
#   4.1. Converting tree from nexus into newick
    treeH = dendropy.Tree.get_from_path(plottreeFn, schema="nexus")     # Converting tree from nexus into newick format, because nexus format may contain translation table, which TreeGraph2 cannot parse
    plottree_newick = treeH.as_string(schema='newick')
    GFO.saveFile(outFn_tree, plottree_newick)

#   4.2. Save table
    GFO.saveFile(outFn_table, outD)



# EXECUTE

print ""
print colored("  Script name: "+sys.argv[0], 'cyan')
print colored("  Author: "+__author__, 'cyan')
print colored("  Version: "+__version__, 'cyan')
#print colored("  Notes:", 'yellow')
#print colored("  1. ", 'yellow')
#print colored("  2. ", 'yellow')
print ""

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Performing ASR with BayesTraits; 2015 Michael Gruenstaeudl')
    parser.add_argument('-t', '--treedistr',
                        help='/path_to_working_dir/treedistr.nex',
                        required=True)
    parser.add_argument('-p', '--plottree',
                        help='/path_to_working_dir/plottree.nex',
                        required=True)
    parser.add_argument('-c', '--chars',
                        help='/path_to_working_dir/characters.csv',
                        required=True)
    parser.add_argument('-n', '--charnumber',
                        help='which character to use (e.g. 1)',
                        default='1',
                        required=True)
    parser.add_argument('-m', '--reconmodel',
                        help='likelihood, bayesian',
                        default='likelihood',
                        required=True)
    parser.add_argument('-s', '--software',
                        help='/path_to_program/mesquite.sh',
                        required=True,
                        default='/home/michael_science/binaries/mesquite3.03/mesquite.sh')
    args = parser.parse_args()

main(args.treedistr, args.plottree, args.chars, args.charnumber, args.reconmodel, args.software)

print ""
print colored("  Done.", 'cyan')
print ""
