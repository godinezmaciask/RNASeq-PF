# RNA-seq Data Analysis

RNA sequencing (RNA-seq) uses next generation sequencing to reveal the presence and quantity of RNA in different biological samples. Here, different Python scripts were created to get insights in the difference of gene expression from different treatments, or samples, by analyzing the raw RNA-seq data obtained from Illumina NGS sequencing method. In addition, plots/outputs to facilitate the interpretation of results are generated.


## Getting Started

Scripts can be executed using Linux-based command line. Please note that reference folders must be present for correct execution.

### Prerequisites

Python			3.0
xlrd 			1.2
XlsxWriter		1.2
matplotlib		2.0
matplotlib_venn	0.11
statsmodels		4.7
scipy			1.5

## Conda environment
This project can be executed with preinstall packages, or using a conda environment. To install the Anaconda enviornment type the following:
```
conda env create --file rnaseq_analysis-env.txt --name rnaseq_analysis python=3
```
To activate directory
```
conda activate rnaseq_analysis
```
### Execute
1. Move into directory containing base scripts. Note that if using anaconda environment, it must be activated first
2. Execute command line script

### For parser:
```
python gdparsingCL.py -in filename.diff
```

Optional output name:
```
python gdparsingCL.py -in filename.diff -p 'outputname'
```

Description of available options:
```
python gdparsingCL.py -h
```

### For complete transcriptome analysis:
```
python gdanalysisCL.py -in1 filename.xlsx -in2 filename.xlsx -all
```

Optional output name:
```
python gdanalysisCL.py -in1 filename.xlsx -in2 filename.xlsx -all -p 'outputname'
```


Description of available options:
```
python gdanalysisCL.py -h
```


## Example
Tested using gastric corpus biopsies, Gastritis vs Atrophy with normal tissues as control (NCBI SRA’s BioProject: PRJEB9749)


### Parsing a condition file
Obtain a complete parsed Excel file for both conditions

```
python gdparsingCL.py -in gene_exp_AtrvCon.diff -p 'gene_exp_AtrvCon'
```

```
python gdparsingCL.py -in gene_exp_GastvCon.diff -p 'gene_exp_GastvCon'
```

By default the tool will parse for genes with expression with fold values of <-2 and >2. A different threshold can be utilized as follows:
```
python gdparsingCL.py -in gene_exp_GastvCon.diff -p 'gene_exp_GastvCon' -t 3
```

One could also get a reduced parsed version. Note that a reduced parsed Excel file will possibly not allow every comparison from the analysis list.
```
python gdparsingCL.py -in gene_exp_GastvCon.diff -p 'gene_exp_GastvCon' 
```

### Comparing different conditions

Compare both conditions obtaining full analysis
```
python gdanalysisCL.py -in1 gene_exp_AtrvCon_gd.xlsx -in2 gene_exp_GastvCon_gd.xlsx -all -p 'AtrvCon_vs_GastvCon'
```

Alternatively, one could only obtain differentially expressed genes in both samples (intersection) and genes that are present in only one sample (disjunction) in both graphical and file format.

```
python gdanalysisCL.py -in1 gene_exp_AtrvCon_gd.xlsx -in2 gene_exp_GastvCon_gd.xlsx -all -p 'AtrvCon_vs_GastvCon' -vd
```

By default, the tool will compare fold values >2 and <-2 (assuming the initial parsed file had that threshold) from both conditions. It is possible to determine what comparisons to perform, for example obtain genes with fold values <-2
```
python gdanalysisCL.py -in1 gene_exp_AtrvCon_gd.xlsx -in2 gene_exp_GastvCon_gd.xlsx -all -p 'AtrvCon_vs_GastvCon' -vd -lsheets '<-2 Fold' '<-2 Fold'
```



## Authors

* **Karla P. Godinez-Macias** (https://github.com/godinezmaciask)

* **Jonathon E. Mohl** (https://github.com/jonmohl)

* **Ming-Ying Leung** (http://www.math.utep.edu/Faculty/mleung/home.php)

## Acknowledgments

* This project is supported in part by NIH Grants #5G12RR007592 from the National Center for Research Resources (NCRR)/NIH to BBRC. 
* Dr. Renato Aguilera from The University of Texas at El Paso for his end user feedback during creation of pipeline.



