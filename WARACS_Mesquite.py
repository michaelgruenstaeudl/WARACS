#!/usr/bin/env python2
'''Reconstructing Ancestral Character States using Mesquite'''
__author__ = "Michael Gruenstaeudl, PhD <mi.gruenstaeudl@gmail.com>"
__copyright__ = "Copyright (C) 2015 Michael Gruenstaeudl"
__info__ = "Reconstructing Ancestral Character States using Mesquite (http://mesquiteproject.org)"
__version__ = "2015.10.28.1800"

#####################
# IMPORT OPERATIONS #
#####################

# LEGACYCODE:
from subprocess import Popen, PIPE
import subprocess
import commands

import argparse
import csv
import os
import sys
import time
import CustomFileOps as CFO
import CustomInstallOps as CIO
import CustomStringOps as CSO

opt_deps = ["dendropy", "numpy", "prettytable"]
if opt_deps:
    try:
        map(__import__, opt_deps)
    except:
        CIO.installPkgs(opt_deps)

import dendropy
import numpy
from prettytable import PrettyTable

#############
# DEBUGGING #
#############

#import pdb
#pdb.set_trace()


####################
# GLOBAL VARIABLES #
####################

mesquite_block1 = "Begin MESQUITE;\n\tMESQUITESCRIPTVERSION 2;\n\tTITLE AUTO;\n\ttell ProjectCoordinator;\n\tgetEmployee #mesquite.minimal.ManageTaxa.ManageTaxa;\n\ttell It;\n\t\tsetID 0 111; \n\tendTell;\n\tgetEmployee #mesquite.charMatrices.ManageCharacters.ManageCharacters;\n\ttell It;\n\t\tsetID 0 222; \n\tendTell;\n\tString.resultsFile 'RAWRESULTS_treeID_reconstID.txt';\n\tgetWindow;\n\tgetEmployee  #mesquite.trees.BasicTreeWindowCoord.BasicTreeWindowCoord; \n\ttell It;\n\t\tmakeTreeWindow #111  #mesquite.trees.BasicTreeWindowMaker.BasicTreeWindowMaker; \n\t\ttell It;\n\t\t\tsetTreeSource  #mesquite.trees.StoredTrees.StoredTrees; \n\t\t\ttell It;\n\t\t\t\tsetTreeBlock 2;\n\t\t\t\ttoggleUseWeights off;\n\t\t\tendTell;\n\t\t\tgetTreeWindow;\n\t\t\ttell It;\n\t\t\t\tsetTreeNumber 1; \n\t\t\t\tnewAssistant  #mesquite.ancstates.TraceCharOverTrees.TraceCharOverTrees;\n\t\t\t\ttell It;\n\t\t\t\t\tsuppress;\n\t\t\t\t\tsetHistorySource  #mesquite.ancstates.RecAncestralStates.RecAncestralStates;\n\t\t\t\t\ttell It;\n\t\t\t\t\t\tgetCharacterSource  #mesquite.charMatrices.CharSrcCoordObed.CharSrcCoordObed;\n\t\t\t\t\t\ttell It;\n\t\t\t\t\t\t\tsetCharacterSource #mesquite.charMatrices.StoredCharacters.StoredCharacters;\n\t\t\t\t\t\t\ttell It;\n\t\t\t\t\t\t\t\tsetDataSet #222;\n\t\t\t\t\t\t\tendTell;\n\t\t\t\t\t\tendTell;"
mesquite_block2 = "\t\t\t\t\tendTell;\n\t\t\t\t\tsetCharacter 1;\n\t\t\t\t\tsetTreeSource  #mesquite.trees.StoredTrees.StoredTrees;\n\t\t\t\t\ttell It;\n\t\t\t\t\t\tsetTreeBlock 1;\n\t\t\t\t\t\ttoggleUseWeights off;\n\t\t\t\t\tendTell;\n\t\t\t\t\tsetNumTrees 100;\n\t\t\t\t\tsetMode Count_All_Trees_with_State;\n\t\t\t\t\tdesuppress;\n\t\t\t\tendTell; \n\t\t\tendTell; \n\t\t\ttell It;\n\t\t\t\ttext;\n\t\t\tendTell;\n\t\tendTell; \n\tendTell; \n\tendTell;\n\tcloseFileAfterRead;\nend;\n"
parsimonyModel = "\t\t\t\t\t\tsetMethod  #mesquite.parsimony.ParsAncestralStates.ParsAncestralStates; \n\t\t\t\t\t\ttell It; \n\t\t\t\t\t\t\tsetModelSource  #mesquite.parsimony.CurrentParsModels.CurrentParsModels; \n\t\t\t\t\t\tendTell;"
likeModel = "\t\t\t\t\t\tsetMethod  #mesquite.stochchar.MargProbAncStates.MargProbAncStates;\n\t\t\t\t\t\ttell It;\n\t\t\t\t\t\t\tsetModelSource  #mesquite.stochchar.CurrentProbModels.CurrentProbModels;\n\t\t\t\t\t\t\tgetEmployee #mesquite.stochchar.zMargLikeCateg.zMargLikeCateg;\n\t\t\t\t\t\t\ttell It;\n\t\t\t\t\t\t\t\tsetReportMode Proportional_Likelihoods;\n\t\t\t\t\t\t\t\tsetRootMode Use_Root_State_Frequencies_as_Prior;\n\t\t\t\t\t\t\t\tsetDecision 2.0;\n\t\t\t\t\t\t\t\tsetUnderflowCheckFreq 2;\n\t\t\t\t\t\t\tendTell;\n\t\t\t\t\t\tendTell;"
bayesModel = "\t\t\t\t\t\tsetMethod  #mesquite.stochchar.StochCharMapper.StochCharMapper;\n\t\t\t\t\t\ttell It;\n\t\t\t\t\t\t\tsetModelSource  #mesquite.stochchar.CurrentProbModels.CurrentProbModels;\n\t\t\t\t\t\t\tgetEmployee #mesquite.stochchar.zMargLikeCateg.zMargLikeCateg;\n\t\t\t\t\t\t\ttell It;\n\t\t\t\t\t\t\t\tsetReportMode Proportional_Likelihoods;\n\t\t\t\t\t\t\t\tsetRootMode Use_Root_State_Frequencies_as_Prior;\n\t\t\t\t\t\t\t\tsetDecision 2.0;\n\t\t\t\t\t\t\t\tsetUnderflowCheckFreq 2;\n\t\t\t\t\t\t\tendTell;\n\t\t\t\t\t\tendTell;"

###########
# MODULES #
###########

def main(treedistrFn, plottreeFn, charsFn, charnum, optcrit, pathToSoftware, keepTmpFile, verbose):

# 1. Generating indata

    # 1.1. Decision on model
    kw = optcrit.lower()
    if kw == "parsimony":
        mdl = mesquite_block1 + "\n" + parsimonyModel + "\n" + mesquite_block2
    if kw == "likelihood":
        mdl = mesquite_block1 + "\n" + likeModel + "\n" + mesquite_block2
    if kw == "bayesian":
        mdl = mesquite_block1 + "\n" + bayesModel + "\n" + mesquite_block2

    # 1.2. Setting outfilenames
    fileprfx = CSO.rmpath(CSO.rmext(treedistrFn))
    fileinfo = "__Mesquite_" + kw + "_char" + str(charnum)
# FUTURE CODE
#    if charmodel:
#        fileinfo = fileinfo + "__optcrit_" + optcrit.replace(";",".").replace(",",".")
    outFn_raw = fileprfx + fileinfo + ".full"
    outFn_tree = fileprfx + fileinfo + ".tre"
    outFn_table = fileprfx + fileinfo + ".csv"

    # 1.3. Load infiles
    treedistr = CFO.loadR(treedistrFn)
    treedistrL = treedistr.splitlines()
    treedistr_tmpL = []
    for l in treedistrL:
        if ";" in l:
            treedistr_tmpL.append(l.upper())
        else:
            treedistr_tmpL.append(l)
    treedistr = "\n".join(treedistr_tmpL)

    plottree = CFO.loadR(plottreeFn)
    plottreeL = plottree.splitlines()
    plottree_tmpL = []
    for l in plottreeL:
        if ";" in l:
            plottree_tmpL.append(l.upper())
        else:
            plottree_tmpL.append(l)
    plottree = "\n".join(plottree_tmpL)

    # 1.4. Parse treedistr
    try:
        pos = treedistr.find("BEGIN TREES;") + len("BEGIN TREES;")
        treedistrH = treedistr[:pos] + "\nTitle 'block1'" + treedistr[pos:]
    except: 
        print "  Warning: Problem with tree distribution."
        
    # 1.5. Parse plottree
    plottreeH = plottree.replace("#NEXUS","")
    if "BEGIN TAXA;" in plottreeH:
        try:
            pos = plottreeH.find("END;", plottreeH.find("BEGIN TAXA;")) + len("END;")
        except: 
            print "  Warning: Problem with plotting tree."
            pos = 0
    else:
        pos = 0
    plottreeH = plottreeH[pos:]
    try:
        pos = plottreeH.find("BEGIN TREES;") + len("BEGIN TREES;")
        plottreeH = plottreeH[:pos] + "\nTitle 'block2'" + plottreeH[pos:]
    except: 
        sys.exit("  ERROR: Error with plotting tree.")

    # 1.6. Parse characters
    #mdl = mdl.replace("setCharacter 1;", "".join(["setCharacter ", charnum, ";"]))  # Adjusting character in question in mdl
    block1 = "\nBEGIN CHARACTERS;\nTITLE  'MYCHARS';\nDIMENSIONS  NCHAR=1;\nFORMAT DATATYPE = STANDARD GAP = - MISSING = ? SYMBOLS = '"
    block2 = "';\nMATRIX\n"
    block3 = "\n;\nEND;\n"
    try:
        reader = csv.reader(open(charsFn, "r"), delimiter=",")
        matrx = numpy.array(list(reader))
        #nchars = matrx.shape[1]-1
        n = int(charnum)
        charstates = set(matrx[:, n])
        charstates = [x for x in charstates if x != "?"]                # Question mark is not a character state, but indicates missing data
        #pdb.set_trace()
        if kw == "parsimony":
            if "I" in charstates:
                sys.exit("  ERROR: Character state 'I' is a reserved state and cannot be used.")
        if kw == "likelihood" or kw == "bayesian":
            try:
                [int(c) for c in charstates]
            except ValueError:
                sys.exit("  ERROR: Likelihood reconstruction in Mesquite requires character states to be coded as integers, starting at 0.")
        p = PrettyTable()
        matrx_used = matrx[:, [0,n]]
        for row in matrx_used:
            p.add_row(row)
        matrxStr = p.get_string(header=False, border=False)
        chars = block1 + " ".join(charstates) + block2 + matrxStr + block3
    except: 
        sys.exit("  ERROR: Error when parsing the character states.")

# FUTURE CODE
#    # 1.7. Character models
#    if optcrit:
#    # 1.7.1. Parsimony stepmatrix
#        if kw == "parsimony":
#            block4 = "\n\nBEGIN ASSUMPTIONS;\n\tUSERTYPE STEPMATRIX (STEPMATRIX) ="
#            block5 = ";\n\tTYPESET * UNTITLED (CHARACTERS = 'MYCHARS') = unord: 1;\nEND;\n"
#            try:
#                stpmtrx_L = optcrit.split(";")
#                charstate_L = stpmtrx_L[0].split(",")
#                ncharstates = len(charstate_L)
#                if ncharstates != len(charstates):
#                    sys.exit("  ERROR: Error when parsing the character model.")
#                stpmtrx = '\n'.join([i.replace(","," ") for i in stpmtrx_L])
#                charmdl = block4 + str(ncharstates) + "\n" + stpmtrx + "\n" + block5
#            except: 
#                sys.exit("  ERROR: Error when parsing the character model.")
#            # Once optcrit has been formatted
#            kw_find = "\n\t\t\t\t\t\t\tsetModelSource  #mesquite.parsimony.CurrentParsModels.CurrentParsModels;"
#            kw_replace = "\n\t\t\t\t\t\t\tsetModelSource  #mesquite.parsimony.StoredParsModel.StoredParsModel;\n\t\t\t\t\t\t\ttell It;\n\t\t\t\t\t\t\t\tsetModel 2  STEPMATRIX;\n\t\t\t\t\t\t\tendTell;"
#            mdl = mdl.replace(kw_find, kw_replace)
#    # 1.7.2. 2P-MarkovK Model
#        if kw == "likelihood" and optcrit or kw == "bayesian" and optcrit :
#            block6 = "\nBEGIN MESQUITECHARMODELS;\n\tCharModel 'CUSTOM_MARKOVK_MODEL' (AsymmMk) ="
#            block7 = " equilibAsPrior;\n\tProbModelSet * UNTITLED (CHARACTERS = 'MYCHARS') = 'Mk1 (est.)': 1;\nEND;\n"
#            try:
#                tpmarkovmdl_L = optcrit.split(",")
#                if len(tpmarkovmdl_L) != len(charstates):
#                    sys.exit("  ERROR: Unequal number of character states between input data and character model.")
#                tmp = " forward " + tpmarkovmdl_L[0] + " backward " + tpmarkovmdl_L[1]
#                charmdl = block6 + tmp + block7
#            except: 
#                sys.exit("  ERROR: Error when parsing the character model.")
#            # Once optcrit has been formatted
#            kw_find = "\n\t\t\t\t\t\t\tsetModelSource  #mesquite.stochchar.CurrentProbModels.CurrentProbModels;"
#            kw_replace = "\n\t\t\t\t\t\t\tsetModelSource  #mesquite.stochchar.StoredProbModel.StoredProbModel;\n\t\t\t\t\t\t\ttell It;\n\t\t\t\t\t\t\t\tsetModel 2   'CUSTOM_MARKOVK_MODEL';\n\t\t\t\t\t\t\tendTell;"
#            mdl = mdl.replace(kw_find, kw_replace)
#    else:
#        charmdl = ""

    charmdl = ""

    # 1.8. Combine to indata
    inD = "\n".join([treedistrH, plottreeH, chars, charmdl])
    #inD = inD.replace("#nexus", "#NEXUS")


# 2. Character Reconstruction

#   2.1. Saving of tempfile
    tmpFn = CSO.randomword(6) + ".tmp"
    CFO.saveFile(tmpFn, "\n".join([inD, mdl]))                           # a temporary infile without underscores is generated, but deleted immediately after execution.

#   2.2. Execute and then delete tempfile
    if verbose.upper() in ["T", "TRUE"]:
        print "  Character Reconstruction in Mesquite"
        print "  Selected Reconstruction Method:", optcrit

    calctime = len(treedistrL)*0.05
    cmd = pathToSoftware + " " + tmpFn
    p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
    time.sleep(calctime)
    # Change this line dependning on operating system?
    p.stdin.write("quit\n")
    output, error = p.communicate()
    data_handle = output
    CFO.saveFile(outFn_raw, data_handle)

# ALTERNATIVE:
#    calctime = len(treedistrL)*0.05
#    cmdL = ["timeout", str(calctime), pathToSoftware, tmpFn]
#    cmdStr = " ".join(cmdL)
#    p = Popen(cmdStr, stdin=PIPE, stdout=PIPE, shell=True)              # Other shell invocations (os.system, subprocess.call) don't work; I have tried many of them.
#    data_handle = p.communicate()

# LEGACYCODE:
#    startMesquite = "sh " + pathToSoftware
#    p = Popen(startMesquite, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
#    time.sleep(5)                                                       # WIthout such waiting times, scripting Mesquite does not work.
#    p.stdin.write("cd " + os.getcwd() + "/\n")                          # Can contain underscores
#    time.sleep(2)
#    p.stdin.write("openFile " + tmpFn + "\n")                           # Must not contain underscores, because Mesquite cannot load filenames containing underscores! Hence, I chose "tmp".
#    time.sleep(45)
#    p.stdin.write("quit\n")
#    output, error = p.communicate()
#    data_handle = [output, error]

    if not data_handle:
        sys.exit("  ERROR: No reconstruction data from Mesquite received.")

#   2.3. Parsing out the relevant section of the reconstruction output and saving it to file
    mainD = CSO.exstr(data_handle, "Reading block: MESQUITE", "File reading complete")
    keywds = ["Trace Character Over Trees", "Trace Character History"]
    for k in keywds:
        if k in mainD:
            mainD = mainD[mainD.find(k):]
    if "File reading complete" in mainD:
        mainD = mainD[mainD.find(k):]
    mainD = mainD[mainD.find("\nnode"):].splitlines()                   # This steps split the string into a list!
    mainD = filter(None, mainD)                                         # removing all empty elements of mainD
    if not mainD:
        sys.exit("  ERROR: Parsing of reconstr. data unsuccessful. Possible issue: Malformed NEXUS file.")


# 3. Parsing the reconstruction output
    if verbose.upper() in ["T", "TRUE"]:
        print "  Parsing of Reconstruction Data"
    alist = [elem.split("  ") for elem in mainD if elem]                # generating parsed_data; field delimiter: two whitespaces
    outD = []
    for i in alist:
        try:
            nodeN = CSO.exstr(i[0], 'node ', ':')
            nodeN = int(nodeN)-1                                        # IMPORTANT to substract 1, because Mesquite assumes a rootes set of trees (hence, has an extraneous node)
            nodeN = str(nodeN)
        except: 
            print "  Warning: No node number information recovered."
            pass
        #try:                                                           # REACTIVATE, WHEN N OF TREES WITHOUT NODE RELEVANT
        #    Ntrees = CSO.exstr(i[1], 'Node in ', ' trees.')
        #except: 
        #    print "  Warning: No N_of_Trees information recovered!"
        #    pass
        try:
            tmp = i[2].split("each: ")[1]
            tmp = tmp.replace(" ","")
            arr = numpy.array([i.split(":") for i in tmp.split(";")])
            l = arr[:,1]
            sm = sum([float(i) for i in l])
            tmpL = []
            for line in arr:
                l = list(line)
                v = float(l[1])/sm
                v = float("{0:.3f}".format(v))                          # round to three decimal places
                outStr = l[0] + ":" + str(v)
                tmpL.append(outStr)
            recon = ";".join(tmpL)
        except: 
            print "  Warning: No reconstruction information for node", nodeN
            pass
        try:
            #outD.append(",".join([nodeN] + [Ntrees] + [recon]))        # REACTIVATE, WHEN N OF TREES WITHOUT NODE RELEVANT
            outD.append(",".join([nodeN] + [recon]))                    # Must be inside a try-command to avoid breakage when no reconstr. info for node
        except: 
            print "  Warning: Element missing for node", nodeN
            pass
    outD = "\n".join(outD)                                              # must be outside of loop
    if not outD:
        sys.exit("  ERROR: Parsing of reconstruction data unsuccessful.")


# 4. Saving files to disk
#   4.1. Converting tree from nexus into newick
    treeH = dendropy.Tree.get_from_string(plottree, schema="nexus")     # Converting tree from nexus into newick format, because nexus format may contain translation table, which TreeGraph2 cannot parse
    plottree_newick = treeH.as_string(schema='newick')
    CFO.saveFile(outFn_tree, plottree_newick)

#   4.2. Save table
    CFO.saveFile(outFn_table, outD)

#   4.3. Decision on deleting temporary input file
    if keepTmpFile.upper() in ["F", "FALSE"]:
        CFO.deleteFile(tmpFn)

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
                        help='which character state distribution to be used (e.g. 1); an integer',
                        default='1',
                        required=True)
    parser.add_argument('-o', '--optcrit',
                        help='models of character evolution; available: parsimony, likelihood, bayesian',
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
# FUTURE CODE
#    parser.add_argument('-a', '--charmodel',
#                        help='values of a character state transition model (parsimony example: "A,B,C;0,1,1;1,0,1;1,1,0"; likelihood example: "1,0")',
#                        required=False)
    args = parser.parse_args()

########
# MAIN #
########

main(args.treedistr, args.plottree, args.chars, args.charnumber, args.optcrit, args.software, args.keep, args.verbose)
