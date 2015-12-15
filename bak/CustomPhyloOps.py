#!/usr/bin/env python
"""Custom Phylo Operations
"""
__author__ = "Michael Gruenstaeudl, PhD"
__copyright__ = "Copyright (C) 2015 Michael Gruenstaeudl"
__email__ = "mi.gruenstaeudl@gmail.com"
__version__ = "2015.12.15.1100"

#####################
# IMPORT OPERATIONS #
#####################

import CustomFileOps as GFO
import sys

opt_deps = ["dendropy"]
if opt_deps:
    try:
        map(__import__, opt_deps)
#    except ImportError:                                                # Not all systems raise the exception "ImportError"; others raise different exception.
    except:
        print sys.exc_info()[0]
        sys.exit("  ERROR: Please install the following Python packages: " + ", ".join(opt_deps))
        # FUTURE CODE:
        # CFO.installPkgs(opt_deps)
import dendropy

###########
# CLASSES #
###########

class convertNexusToNewick:
    ''' Convert a phylogenetic tree in NEXUS format to a phylogenetic tree in NEWICK format
    Args:
        string <a>
    Returns:
        string
    '''
    def __init__(self, a):
        self.inStr = a
    def go(self):
        treeH = dendropy.Tree.get_from_string(self.inStr, schema="nexus")
        return treeH.as_string(schema='newick')

class getNodeListFromTree:
    ''' class for generating a list of nodes from a phylogenetic tree
    Args:
        string <a>
    Returns:
        str, list
    '''
    def __init__(self, a):
        self.inFn = a
    def go(self):
        nodespecL, nodeL = [], []
        treeH = dendropy.Tree.get_from_path(self.inFn, schema="nexus")
        for c, node in enumerate(treeH.nodes(), start=1):
            tips = [tip.taxon.label.replace(" ", "_") for tip in node.leaf_nodes()]
            if len(tips) > 1:
                nodespecL.append("AddNode Node" + str(c) + " " + " ".join(tips))
                nodeL.append(c)                                         # generate list of relevant node numbers
        node_specs = "\n".join(nodespecL)
        return [node_specs, nodeL]

###############
# DEFINITIONS #
###############

def ConvertNexusToNewick(a):
    return convertNexusToNewick(a).go()


def GetNodeListFromTree(a):
    return getNodeListFromTree(a).go()
