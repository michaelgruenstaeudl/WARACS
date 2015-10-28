#!/usr/bin/env python2
'''Visualizing Character State Reconstruction Results using TreeGraph2'''
__author__ = "Michael Gruenstaeudl, PhD <mi.gruenstaeudl@gmail.com>"
__copyright__ = "Copyright (C) 2015 Michael Gruenstaeudl"
__info__ = "Visualizing Character State Reconstruction Results using TreeGraph2 (http://treegraph.bioinfweb.info/)"
__version__ = "2015.10.28.1800"

#####################
# IMPORT OPERATIONS #
#####################

from collections import OrderedDict as OrdDict
from subprocess import Popen, PIPE
import argparse
import os
import re
import sys
import CustomFileOps as CFO
import CustomInstallOps as CIO
import CustomStringOps as CSO
import xml.etree.ElementTree as ET

opt_deps = []
if opt_deps:
    try:
        map(__import__, opt_deps)
    except:
        CIO.installPkgs(opt_deps)

#############
# DEBUGGING #
#############

#import pdb
#pdb.set_trace()

####################
# GLOBAL VARIABLES #
####################

labelMargin_xml_1 = '<LabelMargin Left="1.0" Top="0.0" Right="1.0" Bottom="0.0"></LabelMargin>'
labelMargin_xml_2 = '<LabelMargin Left="1.0" Top="1.0" Right="1.0" Bottom="1.0"></LabelMargin>'
#labelMargin_xml_3 = '<LabelMargin Left="1.0" Top="0.0" Right="1.0" Bottom="1.0"></LabelMargin>' # optimal for phylograms

pieChartLabel_xml = '<PieChartLabel LineColor="#000000" LineWidth="0.2" Width="8.0" Height="8.0" InternalLines="true" NullLines="false" Id="internals" Above="true" LineNo="0" LinePos="0"></PieChartLabel>'

textLabel_xml = '<TextLabel Text="" IsDecimal="false" TextColor="#000000" TextHeight="3.0" TextStyle="" FontFamily="Arial" DecimalFormat="#0.0#####" LocaleLang="en" LocaleCountry="" LocaleVariant="" Id="internals" Above="true" LineNo="" LinePos="0"></TextLabel>'

###########
# CLASSES #
###########

class CustomizeXTG_Nodes:
    ''' class for parsing XTG files: turning raw XTG code into
        publication-ready XTG code '''

    def __init__(self, a):
        self.inFn = a

    def go(self):
        tree = ET.parse(self.inFn)
        root = tree.getroot()
        for n in root.iter('Node'):
            n.attrib["LineWidth"] = "0.6"
            n.attrib["EdgeRadius"] = "0.9"
            n.attrib["TextHeight"] = "5.0"
            n.attrib["TextStyle"] = "Italics"
        for n in root.iter('Branch'):
            n.attrib["LineWidth"] = "0.6"

        tree.write(self.inFn)


class CustomizeXTG_Global:
    ''' class for parsing XTG files: turning raw XTG code into
        publication-ready XTG code '''

    def __init__(self, a, b):
        self.inStr = a
        self.flags = b

    def go(self):
        tree = ET.fromstring(str(self.inStr))
        if "NOROOT" in self.flags.upper():
            tree.attrib["ShowRooted"] = "false"
        if "BRLX2" in self.flags.upper():
            var = tree.attrib["BranchLengthScale"]
            tree.attrib["BranchLengthScale"] = str(float(var)*2)
        if "BRLX3" in self.flags.upper():
            var = tree.attrib["BranchLengthScale"]
            tree.attrib["BranchLengthScale"] = str(float(var)*3)

        return ET.tostring(tree)


class AddPieCharts:
    '''class for adding pie labels to phylogenetic trees in XTG format'''

    def __init__(self, a, b, c):
        self.inStr = a
        self.piedata = b
        self.colorDict = c

    def go(self):
        tree = ET.fromstring(self.inStr)
        piedata = self.piedata.splitlines()

#   1. Inserting pie chart XTG lines into infile by looping through inlist values
#   1.1. Parsing of piedata
        for line in piedata:
            aList = line.split(",")
            node = aList[0]
            nodeN = "Node_" + node
            nodeinfo = 'UniqueName="' + nodeN + '"'

            #if aList[1] == "0":                                        # REACTIVATE, WHEN N OF TREES WITHOUT NODE RELEVANT
            #    print "  Warning: Node " + node + " was not present in reconstruction trees."
            #if nodeinfo not in self.inStr:
            #    print "    Warning: Node " + node + " was not present in plotting tree."
            #if aList[1] != "0" and nodeinfo in self.inStr:
            aDict = OrdDict()
            try:
                inL = aList[1].split(";")
            except:                                                     # if aList[2] cannot be split (i.e., contains only a single elem)
                inL = aList[1]
            for i in inL:
                if "E-" not in i and "0.00" not in i:                   # boolt = any("." in i for i in inL)
                    is_ast = bool("*" in inL)
                    m = i.strip("*").split(":")
                    area = m[0]
            #        enum = float(m[1])                                 # REACTIVATE, WHEN N OF TREES WITHOUT NODE RELEVANT
            #        divis = float(aList[1])
            #        prop = enum/divis
                    prop = float(m[1])
                    prop = str("{0:.3f}".format(prop))
                    if is_ast:
                        prop = prop + " *"                              # Adding back asterisk for significant reconstructions
                    aDict[area] = prop
            if len(aDict.keys()) < 1:
                print "    Warning: Pie data for node " + node + " not parsed."
            for n in tree.iter("Node"):                                 # Must be inside loop "for line in piedata"
                if n.attrib["UniqueName"] == nodeN:                     # Stop at the correct node

#   1.2. Addition of pie labels
                    for c, (k, v) in enumerate(aDict.items(), start=1):
                        textLabel = ET.fromstring(textLabel_xml)
                        textLabel.attrib["Text"] = k + " " + v
                        textLabel.attrib["LineNo"] = str(c)
                        labelMargin_1 = ET.fromstring(labelMargin_xml_1)
                        textLabel.insert(0, labelMargin_1)

                        n.find("Branch").append(textLabel)              # Insert the textLabel into xtg code

                        # Addition of dummy text label for proper alignment - do NOT delete
                        textLabel = ET.fromstring(textLabel_xml)
                        textLabel.attrib["Text"] = ""
                        textLabel.attrib["LineNo"] = "0"
                        labelMargin_1 = ET.fromstring(labelMargin_xml_1)
                        textLabel.insert(0, labelMargin_1)
                        n.find("Branch").append(textLabel)

#   1.3. Addition of pie charts
                    pieChartLabel_1 = ET.fromstring(pieChartLabel_xml)
                    labelMargin_2 = ET.fromstring(labelMargin_xml_2)
                    pieChartLabel_1.insert(0, labelMargin_2)

                    dis = ET.Element("DataIds")
                    dis.text = " "                                      # tricky! Getting an empty tag.
                    tmp = ET.Element("Temp")
                    tmp.text = " "

                    for k, v in aDict.items():                          # Loop through aDict and append PieColor definitions
                        di = ET.Element("DataId")
                        di.attrib["PieColor"] = self.colorDict[k]           # Color dictionary in action here
                        di.text = k
                        dis.append(di)

                        invd = ET.Element("InvisibleData")
                        invd.attrib["Id"] = k
                        invd.attrib["Text"] = v
                        invd.attrib["IsDecimal"] = "true"
                        tmp.append(invd)

                    pieChartLabel_1.append(dis)
                    n.find("Branch").append(pieChartLabel_1)
                    n.find("Branch").append(tmp)

# REACTIVATE, WHEN TIME
#   1.4. Switch position of bootstrap values to below branches, b/c they would conflict with pie charts
#        if "BS" in self.flags.upper():
#            new_out_list = []
#            kw = '<TextLabel Text="'
#
#            for line in out_list:
#                if (kw in line and CSO.afind(line, kw) in 
#                    [str(s) for s in [1]+range(5, 10)]):
#                    bsvalue = CSO.exstr(line, 'Text="', '"')[:-2]
#                    line = CSO.replstr(line, 'Text="', '"', bsvalue)
#                    line = line.replace('IsDecimal="true"', 'IsDecimal="false"')
#                    line = line.replace('Above="true"', 'Above="false"')
#                    new_out_list.append(line)
#
#                if (kw in line and CSO.afind(line, kw) in 
#                    [str(s) for s in [0]]):
#                    line = line.replace('Above="true"', 'Above="false"')
#                    new_out_list.append(line)
#
#                else:
#                    new_out_list.append(line)

        outStr = ET.tostring(tree)
        outStr = outStr.replace("<Temp>","")
        outStr = outStr.replace("</Temp>","")
        return outStr


class ConversionNEX2XTG:
    ''' class for performing nex2xtg conversion in TreeGraph2 via
        commandline; needs inputfile name <a> and command to start
        TreeGraph2 <b> as input '''

    def __init__(self, a, b):
        self.inFn = a
        self.pathToTG2 = b

    def go(self):
        ''' execute function '''
        # Get current working directory
        cwd = os.getcwd()

#     1 Generating in- and output specs for nex2xtg
        inPath = os.path.join(cwd, self.inFn)                              # Note: os.path.join constructs pathnames while accounting for platform-dependent special cases (backslashes in Win)
        outPath = os.path.join(cwd, CSO.rmext(self.inFn) + ".xtg")

#     2. Performing nex2xtg via Treegraph2 and reporting output/error
        cmd = "java -jar " + self.pathToTG2 + " -convert " + inPath + " -xtg " + outPath
        p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
        output, error = p.communicate()
        CSO.errep(output, error)

#     3. Loading xtg-file into memory
        return CFO.loadR(outPath)


class ConversionXTG2IMG:
    ''' class for performing XTG2IMG conversion in TreeGraph2
        via commandline '''

    def __init__(self, a, b, c):
        self.inFn = a
        self.pathToTG2 = b
        self.flags = c

    def go(self):
        cwd = os.getcwd()

#     1.a. Check if xtg-file present
        try:
            inD = os.path.join(cwd, self.inFn)
        except: 
            sys.exit("  ERROR: .xtg file not found.")

#     1.b. Set if plotting as phylo- or cladogram
        resolut = "-width 600mm -res 120ppi"
        if "CLADO" in self.flags.upper():
            pass                
        if "PHYLO" in self.flags.upper():
            resolut = "-phyl " + resolut

#     2. Save as .svg and as .png
        for fend in [".png", ".svg"]:
            cmd = "java -jar " + self.pathToTG2 + " -image " + inD + " " + inD + fend + " " + resolut
            p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
            output, error = p.communicate()
            CSO.errep(output, error)


class LabelingNodesXTG:
    '''class for labeling nodes of phylogenetic tree in XTG format'''

    def __init__(self, a):
        self.inFn = a

    def go(self):
        tree = ET.parse(self.inFn)
        root = tree.getroot()
        for c,n in enumerate(root.iter('Node')):
            n.attrib["UniqueName"] = "Node_"+str(c+1)
        tree.write(self.inFn)


class PrettyPrintXTG:
    '''class for adding tabs to make XTG code human-readable'''

    def __init__(self, a):
        self.inStr = a

    def go(self):
        outStr = self.inStr

        outStr = re.sub(r'<([A-Z])', r'\n<\1', outStr, flags=re.M)      # Newline before every xml starttag
        outStr = re.sub('^<Branch ', '\t<Branch ', outStr, flags=re.M)  # don't alter spaces in keywords; they are important
        outStr = re.sub('^<LeafMargin ', '\t<LeafMargin ', outStr, flags=re.M)
        outStr = re.sub('^<LabelMargin ', '\t\t<LabelMargin ', outStr, flags=re.M)
        outStr = re.sub('^<TextLabel ', '\t\t<TextLabel ', outStr, flags=re.M)
        outStr = re.sub('^<PieChartLabel ', '\t\t<PieChartLabel ', outStr, flags=re.M)
        outStr = re.sub('^<DataId ', '\t\t\t<DataId ', outStr, flags=re.M)
        outStr = re.sub('^<DataIds>', '\t\t\t<DataIds>', outStr, flags=re.M)
        outStr = re.sub('^<InvisibleData ', '\t\t\t<InvisibleData ', outStr, flags=re.M)
        outStr = outStr.replace("\t\n", "\n")
        outStr = os.linesep.join([s for s in outStr.splitlines() if s]) # Remove empty lines from string

        return outStr

###########
# MODULES #
###########

def main(reconstrFn, treeFn, colordictFn, pathToTG2, flags, keepTmpFile, verbose):

# 1. Setting file names and load infiles
    fileprfx = CSO.rmpath(CSO.rmext(reconstrFn))
    tmpFn1 = fileprfx + ".TMP.xtg"
    tmpFn2 = fileprfx + ".xtg"
    reconstrD = CFO.loadR(reconstrFn)

# 1.2. Loading color dictionary and running rudimentary checks
    colorTmp = CFO.loadR(colordictFn).split("\n")
    colorTmp = filter(None, colorTmp)                                   # removing all empty elements of tmp
    colorDict = {}
    for line in colorTmp:
        tmp = line.split(",")
        if len(tmp[0]) != 1:
            sys.exit("  ERROR: Problem with area codes in color dictionary.")
        if tmp[1][0] != "#" or len(tmp[1]) != 7:
            sys.exit("  ERROR: Problem with color codes in color dictionary.")
        colorDict[tmp[0]] = tmp[1]

#   2.1. Conversion from .nex to .xtg format
    if verbose.upper() in ["T", "TRUE"]:
        print "  Step 1: Conversion .nex -> .xtg"
    out_step1 = ConversionNEX2XTG(treeFn, pathToTG2).go()
    CFO.deleteFile(CSO.rmext(treeFn) + ".xtg")

#   2.2. Extraction of relevant XML part
    split1 = out_step1.split("<GlobalFormats")
    split1[1] = "<GlobalFormats" + split1[1]
    split2 = CSO.splitkeepsep2(split1[1], "</GlobalFormats>")           # Extract element "<Tree></Tree>", because parser cannot read flanking code
    split3 = CSO.splitkeepsep2(split2[1], "</Tree>")

    start_cap_1, start_cap_2 = split1[0], split2[0]
    end_cap = "</TreegraphDocument>"
    
    try:
        out_step1 = CSO.splitkeepsep2(split3[0], "<Tree>")[1]
        out_step1 = "<Tree>\n" + out_step1
    except:
        out_step1 = split3[0]

#   3. Pretty-print the .xtg file
    if verbose.upper() in ["T", "TRUE"]:
        print "  Step 2: Pretty-print of xtg code"
    out_step2 = PrettyPrintXTG(out_step1).go()
    CFO.saveFile(tmpFn1, out_step2)

#   4. Label internal nodes
    if verbose.upper() in ["T", "TRUE"]:
        print "  Step 3: Labeling nodes of tree"
    LabelingNodesXTG(tmpFn1).go()

#   5. Customize XTG file
    if verbose.upper() in ["T", "TRUE"]:
        print "  Step 4: Customize XTG file"
    CustomizeXTG_Nodes(tmpFn1).go()
    start_cap_2 = CustomizeXTG_Global(start_cap_2, flags).go()

#   6. Add Pie labels and charts
    out_step5 = CFO.loadR(tmpFn1)
    if reconstrD:
        if verbose.upper() in ["T", "TRUE"]:
            print "  Step 5: Adding pie labels and charts"
        out_step5 = AddPieCharts(out_step5, reconstrD, colorDict).go()      # Indentation important, because pie data if statement above
    else:
        print "  Warning: Skipping step: No pie data available."
    CFO.saveFile(tmpFn1, out_step5)

#   7. Pretty-print the .xtg file
    if verbose.upper() in ["T", "TRUE"]:
        print "  Step 6: Pretty-print of xtg code"
    out_step6 = PrettyPrintXTG(out_step5).go()
    CFO.saveFile(tmpFn1, out_step6)

#   8. Improving visualization
    if verbose.upper() in ["T", "TRUE"]:
        print "  Step 7: Improving visualization"
    tree = ET.parse(tmpFn1)
    root = tree.getroot()
    for n in root.iter('Text'):
        n.attrib["TextColor"] = "#808080"                               # Make pielabels grey
        if "BS" in flags.upper():
            bsvalue = int(n.attrib["Text"])                             # strip commans and digits from bootstrap values
            n.attrib["Text"] = bsvalue
            n.attrib["IsDecimal"] = "false"
    FinalTreeXML = ET.tostring(root)
    CFO.saveFile(tmpFn1, FinalTreeXML)

#   9. Combining all parts
    if verbose.upper() in ["T", "TRUE"]:
        print "  Step 8: Combining all xml sections"
    finalL = [start_cap_1, start_cap_2, FinalTreeXML, end_cap]
    CFO.saveFile(tmpFn2, "\n".join(finalL))
    CFO.deleteFile(tmpFn1)

#   10. Conversion from .xtg to .png format
    if verbose.upper() in ["T", "TRUE"]:
        print "  Step 9: Conversion .xtg  -> .png"
    ConversionXTG2IMG(tmpFn2, pathToTG2, flags).go()

#   11. Decision on deleting temporary input file
    if keepTmpFile.upper() in ["F", "FALSE"]:
        CFO.deleteFile(tmpFn2)

############
# ARGPARSE #
############

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="  --  ".join([__author__, __copyright__, __info__, __version__]))
    parser.add_argument('-r', '--reconstrdata',
                        help='/path_to_working_dir/reconstrdata.csv',
                        required=True)
    parser.add_argument('-p', '--plottree',
                        help='/path_to_working_dir/plotting_tree.tre',
                        required=True)
    parser.add_argument('-c', '--colordict',
                        help='/path_to_working_dir/color_dictionary.csv',
                        required=True)
    parser.add_argument('-s', '--software',
                        help='/path_to_program/TreeGraph.jar',
                        required=True,
                        default='/home/michael_science/binaries/treegraph2/TreeGraph.jar')
    parser.add_argument('-f', '--flags',
                        help='BS(bootstrap),\
                        CLADO(cladogram), PHYLO(phylogram),\
                        NOROOT(dont display root),\
                        BRLX2(multiply branch length scale by 2),\
                        BRLX3(multiply branch length scale by 3)',
                        required=False,
                        default="CLADO,BRLX2")
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

main(args.reconstrdata, args.plottree, args.colordict, args.software, args.flags, args.keep, args.verbose)
