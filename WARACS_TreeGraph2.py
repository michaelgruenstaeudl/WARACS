#!/usr/bin/env python2
'''Visualizing Character State Reconstruction Results using TreeGraph2'''
__author__ = "Michael Gruenstaeudl, PhD <mi.gruenstaeudl@gmail.com>"
__copyright__ = "Copyright (C) 2015 Michael Gruenstaeudl"
__info__ = "Visualizing Character State Reconstruction Results using TreeGraph2 (http://treegraph.bioinfweb.info/)"
__version__ = "2015.10.31.2300"

#####################
# IMPORT OPERATIONS #
#####################

from collections import OrderedDict as _ordDict
from os.path import isfile as _isfile
from xml.etree import ElementTree as _ET

import argparse
import re
import sys
import CustomFileOps as CFO
import CustomPhyloOps as CPO
import CustomStringOps as CSO

#############
# DEBUGGING #
#############

import pdb
#pdb.set_trace()

####################
# GLOBAL VARIABLES #
####################

labelMargin_xml_1 = '<LabelMargin Left="1.0" Top="0.0" Right="1.0" Bottom="0.0"> </LabelMargin>'
labelMargin_xml_2 = '<LabelMargin Left="1.0" Top="1.0" Right="1.0" Bottom="1.0"> </LabelMargin>'
#labelMargin_xml_3 = '<LabelMargin Left="1.0" Top="0.0" Right="1.0" Bottom="1.0"></LabelMargin>' # optimal for phylograms
pieChartLabel_xml = '<PieChartLabel LineColor="#000000" LineWidth="0.2" Width="8.0" Height="8.0" InternalLines="true" NullLines="false" Id="internals" Above="true" LineNo="0" LinePos="0"> </PieChartLabel>'
textLabel_xml = '<TextLabel Text="" IsDecimal="false" TextColor="#000000" TextHeight="3.0" TextStyle="" FontFamily="Arial" DecimalFormat="#0.0#####" LocaleLang="en" LocaleCountry="" LocaleVariant="" Id="1" Above="true" LineNo="" LinePos="0"> </TextLabel>'

default_palette = ["#8dd3c7","#ffffb3","#bebada","#fb8072","#80b1d3","#fdb462","#b3de69","#fccde5","#d9d9d9","#bc80bd","#ccebc5","#ffed6f","#a6cee3","#1f78b4","#b2df8a","#33a02c","#fb9a99","#e31a1c","#fdbf6f","#ff7f00","#cab2d6","#6a3d9a","#ffff99","#b15928"]

###########
# CLASSES #
###########

class CustomizeXTG_Nodes:
    ''' class for parsing XTG files: turning raw XTG code into publication-ready XTG code '''
    def __init__(self, a):
        self.inFn = a
    def go(self):
# 1. Parsing of .xtg file:
        try:
            tree = _ET.parse(self.inFn)
            root = tree.getroot()
        except:
            sys.exit("  ERROR: Parsing of XML code unsuccessful: " + sys.exc_info()[0])
# 2. Customizing XTG file 
        for n in root.iter('Node'):
            n.attrib["LineWidth"] = "0.6"
            n.attrib["EdgeRadius"] = "0.9"
            n.attrib["TextHeight"] = "5.0"
            n.attrib["TextStyle"] = "Italics"
        for n in root.iter('Branch'):
            n.attrib["LineWidth"] = "0.6"
        tree.write(self.inFn)


# DEPRECATED CLASS:
#class CustomizeXTG_Global:
#    ''' class for parsing XTG files: turning raw XTG code into
#        publication-ready XTG code '''
#
#    def __init__(self, a, b):
#        self.inStr = a
#        self.flags = b
#
#    def go(self):
#        tree = _ET.fromstring(str(self.inStr))
#        if "NOROOT" in self.flags.upper():
#            tree.attrib["ShowRooted"] = "false"
#        return _ET.tostring(tree)


class AddPieCharts:
    '''class for adding pie labels to phylogenetic trees in XTG format'''

    def __init__(self, a, b, c):
        self.inStr = a
        self.piedata = b
        self.colorDict = c

    def go(self):

# 1. Parsing of XML code:
        try:
            tree = _ET.fromstring(self.inStr)
        except:
            sys.exit("  ERROR: Parsing of XML code unsuccessful: " + sys.exc_info()[0])
        piedata = self.piedata.splitlines()

# 2. Inserting pie chart XTG lines into infile by looping through inlist values
# 2.1. Parsing of piedata
        for line in piedata:
            aList = line.split(",")
            node = aList[0]
            nodeN = "Node_" + node
            nodeinfo = 'UniqueName="' + nodeN + '"'

            # FUTURE CODE:
            #if aList[1] == "0":                                        # REACTIVATE, WHEN N OF TREES WITHOUT NODE RELEVANT
            #    print "  Warning: Node " + node + " was not present in reconstruction trees."
            #if nodeinfo not in self.inStr:
            #    print "    Warning: Node " + node + " was not present in plotting tree."
            #if aList[1] != "0" and nodeinfo in self.inStr:

            aDict = _ordDict()
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

# 2.2. Addition of pie labels
                    for c, (k, v) in enumerate(aDict.items(), start=1):
                        textLabel = _ET.fromstring(textLabel_xml)
                        textLabel.attrib["Text"] = k + " " + v
                        textLabel.attrib["LineNo"] = str(c)
                        textLabel.attrib["Id"] = k + " " + v            # Very important that this is a label not used by any other on this particular branch
                        
                        labelMargin_1 = _ET.fromstring(labelMargin_xml_1)
                        textLabel.insert(0, labelMargin_1)

                        n.find("Branch").append(textLabel)              # Insert the textLabel into xtg code

                        # Addition of dummy text label for proper alignment - do NOT delete
                        textLabel = _ET.fromstring(textLabel_xml)
                        textLabel.attrib["Text"] = ""
                        textLabel.attrib["LineNo"] = "0"
                        labelMargin_1 = _ET.fromstring(labelMargin_xml_1)
                        textLabel.insert(0, labelMargin_1)
                        n.find("Branch").append(textLabel)

# 2.3. Addition of pie charts
                    pieChartLabel_1 = _ET.fromstring(pieChartLabel_xml)
                    labelMargin_2 = _ET.fromstring(labelMargin_xml_2)
                    pieChartLabel_1.insert(0, labelMargin_2)

                    dis = _ET.Element("DataIds")
                    dis.text = " "                                      # trick! Getting an empty tag.
                    tmp = _ET.Element("Temp")
                    tmp.text = " "

                    for k, v in aDict.items():                          # Loop through aDict and append PieColor definitions
                        di = _ET.Element("DataId")
                        di.attrib["PieColor"] = self.colorDict[k]       # Color dictionary in action here
                        di.text = k
                        dis.append(di)

                        invd = _ET.Element("InvisibleData")
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

        outStr = _ET.tostring(tree)
        outStr = outStr.replace("<Temp>","")
        outStr = outStr.replace("</Temp>","")
        return outStr


class ConversionNEX2XTG:
    ''' class for performing nex2xtg conversion in TreeGraph2 via commandline;
    needs inputfile name <a> and command to start TreeGraph2 <b> as input '''

    def __init__(self, a, b, c):
        self.inFn = a
        self.outFn = b
        self.pathToTG2 = c
    def go(self):
# 1. Check if nex-file present
        if not _isfile(self.inFn):
            sys.exit("  ERROR: .nex file not found.")
# 2. Performing nex2xtg via Treegraph2
        cmdL = ["java -jar", self.pathToTG2, "-convert", self.inFn, "-xtg", self.outFn]
        CFO.extprog(cmdL)
# 3. Check if nex-file present
        if not _isfile(self.inFn):
            sys.exit("  ERROR: Conversion .nex to .xtg unsuccessful.")

class ConversionXTG2IMG:
    ''' class for performing XTG2IMG conversion in TreeGraph2 via commandline '''

    def __init__(self, a, b, c):
        self.inFn = a
        self.pathToTG2 = b
        self.flags = c
    def go(self):
        #cwd = os.getcwd()
# 1. Check if xtg-file present
        if not _isfile(self.inFn):
            sys.exit("  ERROR: .xtg file not found.")
# 2. Set if plotting as phylo- or cladogram
        resolut = "-width 600mm -res 120ppi"
        if self.flags.upper() in ["C", "CLADO"]:
            pass                
        if self.flags.upper() in ["P", "PHYLO"]:
            resolut = "-phyl " + resolut
# 3. Save as .svg and as .png
        for fEnd in [".png", ".svg"]:
            outPath = self.inFn + fEnd
            cmdL = ["java -jar", self.pathToTG2, "-image", self.inFn, outPath, resolut]
            CFO.extprog(cmdL)

class LabelingNodesXTG:
    '''class for labeling nodes of phylogenetic tree in XTG format'''

    def __init__(self, a):
        self.inFn = a
    def go(self):
# 1. Check if .xtg file present
        if not _isfile(self.inFn):
            sys.exit("  ERROR: .xtg file not found.")
# 2. Parsing of .xtg file:
        try:
            tree = _ET.parse(self.inFn)
            root = tree.getroot()
        except:
            sys.exit("  ERROR: Parsing of XML code unsuccessful: " + sys.exc_info()[0])
# 3. Adding node labels:
        for c,n in enumerate(root.iter('Node')):
            n.attrib["UniqueName"] = "Node_"+str(c+1)
        tree.write(self.inFn)


class PrettyPrintXTG:
    '''class for adding tabs to make XTG code human-readable'''

    def __init__(self, a):
        self.inStr = a
    def go(self):
        outStr = self.inStr
        outStr = CSO.rmblanklns(outStr)                                 # Remove empty lines from string
        outStr = outStr.replace("\n\n", "\n")                           # Remove any double newlines
        outStr = re.sub(r'<([A-Z])', r'\n<\1', outStr, flags=re.M)      # Newline before every xml starttag
        outStr = re.sub('^<Branch ', '\t<Branch ', outStr, flags=re.M)  # don't alter spaces in keywords; they are important
        outStr = re.sub('^<LeafMargin ', '\t<LeafMargin ', outStr, flags=re.M)
        outStr = outStr.replace('\n<LabelMargin ', ' <LabelMargin ')    # Do NOT do via re.sub, which acts line by line
        outStr = re.sub('^<TextLabel ', '\t\t<TextLabel ', outStr, flags=re.M)
        outStr = re.sub('^<PieChartLabel ', '\t\t<PieChartLabel ', outStr, flags=re.M)
        outStr = re.sub('^<DataId ', '\t\t\t<DataId ', outStr, flags=re.M)
        outStr = re.sub('^<DataIds>', '\t\t\t<DataIds>', outStr, flags=re.M)
        outStr = re.sub('^<InvisibleData ', '\t\t\t<InvisibleData ', outStr, flags=re.M)
        outStr = outStr.replace("\t\n", "\n")
        outStr = CSO.rmblanklns(outStr)                                 # Remove empty lines from string
        return outStr

###########
# MODULES #
###########

def main(reconstrFn, treeFn, pathToTG2, colordictFn, flags, keepTmpFile, verbose):

#######################
# 0. Setting file names 
#######################
    fileprfx = CSO.rmpath(CSO.rmext(reconstrFn))
    tmpFn = fileprfx + ".tmp"
    compiledInFn = fileprfx + ".xtg"
    try:
############################################
#1. loading infiles, customizing color dict.
############################################
# 1.1. Loading infiles
        reconstrD = CFO.loadR(reconstrFn)
# 1.2. Loading color dictionary and running rudimentary checks
# 1.2.1. Loading areas
        handle = [a.split(",")[1] for a in reconstrD.splitlines() if ":" in a]
        areaL = []
        for line in handle:
            indxL = [x-1 for x in CSO.findall(":", line)]
            resL = [list(line)[i] for i in indxL]
            areaL.extend(resL)
        areaL = sorted(set(areaL))                                      # command 'set' keeps only unqiue items
# 1.2.2. If color dictionary supplied by user
        if colordictFn:
# 1.2.2.1. Loading color dictionary
            color_specs = CFO.loadRL(colordictFn)
            color_specs = filter(None, color_specs)                     # removing all empty elements of tmp
            colorDict = {}
# 1.2.2.2. Checking individual colors
            for line in color_specs:
                tmp = line.split(",")
                area = tmp[0]
                color = tmp[1]
                if len(area) != 1:
                    sys.exit("  ERROR: Please use only single letters or digits as area codes in your color dictionary.")
                if color[0] != "#" or len(color) != 7:
                    sys.exit("  ERROR: The colors in your color dictionary do not constitutes hex codes.")
                colorDict[area] = color
# 1.2.2.3. Checking if as many colors as reconstructions
            if not CSO.sublistinlist(colorDict.keys(), areaL):
                sys.exit("  ERROR: Number of areas in reconstruction results unequal to number of areas in color dictionary.")
# 1.2.3. If color dictionary not supplied by user
        if not colordictFn:
# 1.2.3.1. Generate default color dictionary
            colorDict = {}
            for c,area in enumerate(areaL, start=0):
                colorDict[area] = default_palette[c]

#######################################################
# 2. Converting NEX to XTG, extracting relevant section
#######################################################
# 2.1. Conversion from .nex to .xtg format
        if verbose.upper() in ["T", "TRUE"]:
            print "  Step 1: Conversion .nex -> .xtg"
        ConversionNEX2XTG(treeFn, tmpFn, pathToTG2).go()
        out_step1 = CFO.loadR(tmpFn)
# 2.2. Extraction of relevant XML part
        try:
            split1 = out_step1.split("<GlobalFormats")
            split1[1] = "<GlobalFormats" + split1[1]
            split2 = split1[1].split("</GlobalFormats>")           # Extract element "<Tree></Tree>", because parser cannot read flanking code
            split2[0] = split2[0] + "</GlobalFormats>"                  # Reattaching delimiter keyword
            split3 = split2[1].split("</Tree>")
            split3[0] = split3[0] + "</Tree>"                           # Reattaching delimiter keyword

            out_step1 = split3[0]
            start_cap_1 = split1[0]                                     # Needed for later
            start_cap_2 = split2[0]                                     # Needed for later
            end_cap = "</TreegraphDocument>"                            # Needed for later
        except IndexError:
            sys.exit("  ERROR: Malformed .xtg file.")
# 2.3. Make certain that out_step1 only the element "<Tree></Tree>"
        tmp = CSO.exstr(out_step1, "<Tree>", "</Tree>")
        out_step1 = "<Tree>" + tmp + "</Tree>"

#############################
# 3. Labelling internal nodes
#############################
# 3.1. Pretty-print the .xtg file
        if verbose.upper() in ["T", "TRUE"]:
            print "  Step 2: Pretty-print of xtg code"
        out_step2 = PrettyPrintXTG(out_step1).go()
        CFO.saveFile(tmpFn, out_step2)

# 3.2. Label internal nodes
        if verbose.upper() in ["T", "TRUE"]:
            print "  Step 3: Labeling nodes of tree"
        LabelingNodesXTG(tmpFn).go()

###########################################
# 4. Customize graphical param. in XTG file
###########################################
        if verbose.upper() in ["T", "TRUE"]:
            print "  Step 4: Customize XTG file"
        CustomizeXTG_Nodes(tmpFn).go()
        #start_cap_2 = CustomizeXTG_Global(start_cap_2, flags).go()

##############################
# 5. Add Pie labels and charts
##############################
        out_step5 = CFO.loadR(tmpFn)
        if reconstrD:
            if verbose.upper() in ["T", "TRUE"]:
                print "  Step 5: Adding pie labels and charts"
            out_step5 = AddPieCharts(out_step5, reconstrD, colorDict).go()  # Indentation important, because pie data if statement above
        else:
            print "  Warning: No pie data available."
        CFO.saveFile(tmpFn, out_step5)

###############################
# 6. Pretty-print the .xtg file
###############################
        if verbose.upper() in ["T", "TRUE"]:
            print "  Step 6: Pretty-print of xtg code"
        out_step6 = PrettyPrintXTG(out_step5).go()
        CFO.saveFile(tmpFn, out_step6)

############################
# 7. Improving visualization
############################
        if verbose.upper() in ["T", "TRUE"]:
            print "  Step 7: Improving visualization"
        try:
            tree = _ET.parse(tmpFn)
            root = tree.getroot()
        except:
            print sys.exc_info()[0]
            sys.exit("  ERROR: Parsing of XML code unsuccessful.")
        for n in root.iter('Text'):
            n.attrib["TextColor"] = "#808080"                           # Make pielabels grey
            if "BS" in flags.upper():
                bsvalue = int(n.attrib["Text"])                         # strip commas and digits from bootstrap values
                n.attrib["Text"] = bsvalue
                n.attrib["IsDecimal"] = "false"
        FinalTreeXML = _ET.tostring(root)
        CFO.saveFile(tmpFn, FinalTreeXML)

########################
# 8. Combining all parts
########################
        if verbose.upper() in ["T", "TRUE"]:
            print "  Step 8: Combining all xml sections"
        finalL = [start_cap_1, start_cap_2, FinalTreeXML, end_cap]
        CFO.saveFile(compiledInFn, "\n".join(finalL))

########################################
# 9. Conversion from .xtg to .png format
########################################
        if verbose.upper() in ["T", "TRUE"]:
            print "  Step 9: Conversion .xtg  -> .png"
        ConversionXTG2IMG(compiledInFn, pathToTG2, flags).go()

####################
# 10. Deleting files
####################
# 10.1. Decision on deleting temporary input file
        if keepTmpFile.upper() in ["F", "FALSE"]:
            CFO.deleteFile(compiledInFn)
# 10.2. Always delete unnecessary files
    finally:
        try:
            CFO.deleteFile(tmpFn)
        except:
            pass


############
# ARGPARSE #
############

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="  --  ".join([__author__, __copyright__, __info__, __version__]))
    parser.add_argument('-r', '--reconstrdata',
                        help='/path_to_input/reconstrdata.csv',
                        required=True)
    parser.add_argument('-p', '--plottree',
                        help='/path_to_input/plotting_tree.tre',
                        required=True)
    parser.add_argument('-s', '--software',
                        help='/path_to_software/TreeGraph.jar',
                        required=True)
    parser.add_argument('-c', '--colordict',
                        help='/path_to_input/color_dictionary.csv',
                        required=False)
    parser.add_argument('-f', '--flags',
                        help="Select type of tree representation: 'CLADO' (for cladogram) or 'PHYLO' (for phylogram)",
                        required=False,
                        default="CLADO")
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

main(args.reconstrdata, args.plottree, args.software, args.colordict, args.flags, args.keep, args.verbose)
