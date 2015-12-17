# WARACS
WARACS: Wrappers to Automate the Reconstruction of Ancestral Character States

![](https://github.com/michaelgruenstaeudl/WARACS/blob/master/examples/example_TreeGraph2/02_output/tree_distribution__BayesTraits_likelihood_char1.xtg.png)

### - Compatibility
* Python v.2.7 (https://www.python.org/download/releases/2.7/)
* Python v.3.5 (https://www.python.org/downloads/release/python-350/)

### - Prerequisites
* Python package *DendroPy* (https://pypi.python.org/pypi/DendroPy)
* Python package *numpy* (https://pypi.python.org/pypi/numpy)
* Python package *six* (https://pypi.python.org/pypi/six)

### - Wrapped Applications
* Mesquite (http://mesquiteproject.org)
* BayesTraits (http://www.evolution.reading.ac.uk/BayesTraits.html)
* TreeGraph2 (http://treegraph.bioinfweb.info/)

### - Usage under Linux and Mac OS
###### 1. Test the wrapper
```
python /path_to_WARACS/WARACS_Mesquite.py -h
```
###### 2. Perform an ancestral character state reconstruction via [Mesquite](http://mesquiteproject.org)
```
python /path_to_WARACS/WARACS_Mesquite.py
  -c /path_to_input/character_state_distribution.csv
  -t /path_to_input/tree_distribution.tre
  -p /path_to_input/plotting_tree.tre
  -o likelihood
  -n 2
  -s /path_to_Mesquite/mesquite.sh
  -v True
```
###### 3. Perform an ancestral character state reconstruction via [BayesTraits](http://www.evolution.reading.ac.uk/BayesTraits.html)
```
python /path_to_WARACS/WARACS_BayesTraits.py
  -c /path_to_input/character_state_distribution.csv
  -t /path_to_input/tree_distribution.tre
  -p /path_to_input/plotting_tree.tre
  -n 1
  -o likelihood
  -s /path_to_BayesTraits/BayesTraitsV2
  -v True
```
###### 4. Visualize the character state reconstruction results via [TreeGraph2](http://treegraph.bioinfweb.info/)
```
python /path_to_WARACS/WARACS_TreeGraph2.py
  -r /path_to_input/tree_distribution__Mesquite_likelihood_char2.csv
  -p /path_to_input/tree_distribution__Mesquite_likelihood_char2.tre
  -d /path_to_input/color_dictionary.csv
  -c /path_to_input/character_state_distribution.csv
  -n 2
  -s /path_to_TreeGraph2/TreeGraph.jar
  -v True
```
### - Usage under Windows

###### Testing the wrapper; the other commands work correspondingly
```
C:\Python\python.exe \path_to_WARACS\WARACS_Mesquite.py -h
```
