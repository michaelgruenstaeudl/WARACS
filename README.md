# WARACS
WARACS: Wrappers to Automate the Reconstruction of Ancestral Character States

### - Prerequisites
* Python v.2.7 (https://www.python.org/download/releases/2.7/)
* Python package *setuptools* (https://pypi.python.org/pypi/setuptools)

### - Wrapped Applications
* Mesquite (https://mesquiteproject.wikispaces.com/)
* BayesTraits (http://www.evolution.reading.ac.uk/BayesTraits.html)
* TreeGraph2 (http://treegraph.bioinfweb.info/)

### - Commandline Usage via Linux and MacOSX
###### 1. Specify input directory
```
INDIR=/home/waracs_user/git/WARACS/examples/WARACS_BayesTraits_Example/01_input/
```
###### 2. Change into desired output directory
```
mkdir -p ~/Desktop/
cd ~/Desktop/
```
###### 3. Perform an ancestral character state reconstruction via [Mesquite](https://mesquiteproject.wikispaces.com/)
```
python2.7 ~/git/github.com_WARACS/WARACS_Mesquite.py
  -t $INDIR/treedistr.tre
  -p $INDIR/plottree.tre
  -c $INDIR/chars.csv
  -n 1
  -m likelihood
  -s /home/waracs_user/binaries/Mesquite3.03/mesquite.sh
```
###### 4. Perform an ancestral character state reconstruction via [BayesTraits](http://www.evolution.reading.ac.uk/BayesTraits.html)
```
python2.7 ~/git/github.com_WARACS/WARACS_BayesTraits.py
  -t $INDIR/treedistr.tre
  -p $INDIR/plottree.tre
  -c $INDIR/chars.csv
  -n 2
  -m likelihood
  -s /home/waracs_user/binaries/BayesTraits_V2/BayesTraitsV2
```
###### 5. Visualize character state reconstruction results via [TreeGraph2](http://treegraph.bioinfweb.info/)
```
python2.7 ~/git/github.com_WARACS/WARACS_TreeGraph2.py
  -r treedistr__BayesTraits_likelihood.csv
  -p treedistr__BayesTraits_likelihood.tre
  -c $INDIR/colordict.csv
  -s /home/waracs_user/binaries/Treegraph2/TreeGraph.jar
```
### - Commandline Usage via Windows
(in prep.)
