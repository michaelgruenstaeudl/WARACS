# WARACS
WARACS: Wrappers to Automate the Reconstruction of Ancestral Character States

### - Prerequisites
* Python v.2.7 (https://www.python.org/download/releases/2.7/)
* Python package *DendroPy* (https://pypi.python.org/pypi/DendroPy)
* Python package *numpy* (https://pypi.python.org/pypi/numpy)

### - Wrapped Applications
* Mesquite (http://mesquiteproject.org)
* BayesTraits (http://www.evolution.reading.ac.uk/BayesTraits.html)
* TreeGraph2 (http://treegraph.bioinfweb.info/)

### - Usage in Linux and Mac OS
###### 1. Test the wrapper
```
python2.7 /path_to_git/WARACS/WARACS_Mesquite.py -h
```
###### 2. Perform an ancestral character state reconstruction via [Mesquite](http://mesquiteproject.org)
```
python2.7 /path_to_git/WARACS/WARACS_Mesquite.py
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
python2.7 /path_to_git/WARACS/WARACS_BayesTraits.py
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
python2.7 /path_to_git/WARACS/WARACS_TreeGraph2.py
  -r /path_to_input/tree_distribution__Mesquite_likelihood_char2.csv
  -p /path_to_input/tree_distribution__Mesquite_likelihood_char2.tre
  -c /path_to_input/color_dictionary.csv
  -s /path_to_TreeGraph2/TreeGraph.jar
  -v True
```
### - Usage in Windows

###### Testing the wrapper; other commands work correspondingly
```
C:\Python27\python.exe \path_to_git\WARACS\WARACS_Mesquite.py -h
```
