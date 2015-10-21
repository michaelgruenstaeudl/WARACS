# MANUAL
WARACS: Wrappers to Automate the Reconstruction of Ancestral Character States

### - Commandline Usage via Linux and MacOSX
###### 1. Specify input directory
```
INDIR=/home/michael/git/WARACS/examples/WARACS_BayesTraits_Example/01_input/
```
###### 2. Change into desired output directory
```
mkdir -p ~/Desktop/
cd ~/Desktop/
```
###### 3. Perform an ancestral character state reconstruction via Mesquite
```
python2.7 ~/git/github.com_WARACS/WARACS_Mesquite.py
  -t $INDIR/treedistr.tre
  -p $INDIR/plottree.tre
  -c $INDIR/chars.csv
  -n 1
  -m likelihood
  -s /home/michael/binaries/Mesquite3.03/mesquite.sh
```
###### 4. Perform an ancestral character state reconstruction via BayesTraits
```
python2.7 ~/git/github.com_WARACS/WARACS_BayesTraits.py
  -t $INDIR/treedistr.tre
  -p $INDIR/plottree.tre
  -c $INDIR/chars.csv
  -n 2
  -m likelihood
  -s /home/michael/binaries/BayesTraits_V2/BayesTraitsV2
```
###### 5. Visualize Character State Reconstruction Results generated via BayesTraits
```
python2.7 ~/git/github.com_WARACS/WARACS_TreeGraph2.py
-r treedistr__BayesTraits_likelihood.csv
-p treedistr__BayesTraits_likelihood.tre
-c $INDIR/colordict.csv
-s /home/michael/binaries/Treegraph2/TreeGraph.jar
```
### - Commandline Usage via Windows
(in prep.)
