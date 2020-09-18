## RNA-seq command line comparison analysis 
## Karla Godinez, Jon Mohl


# DECLARATIONS
import argparse
import time
import os
import sys
from config import *

# SCRIPTS TO IMPORT
from same_genes import expLevel
from getValues import getValues
from vennDiag import venn_diagrams

# SET DEFAULTS
fpath1 = './'
fpath2 = './'
get_values = ['fold','-1/fold']
get_sheets = ['>2 Fold','>2 Fold','<-2 Fold','<-2 Fold']
get_comparisons = ['>2 Fold','>2 Fold','>2 Fold','<-2 Fold','<-2 Fold','<-2 Fold']
analysis = ['vd','vals','explev']
label = True


# REPLACE VARS BY ARGPARSE
# files and paths
parser = argparse.ArgumentParser()
parser = argparse.ArgumentParser(description='UTEP\'s Gene diff analysis')
parser.add_argument('-in1', metavar="FILENAME", dest="infile1", required=True, help='Input file is necessary to analyze the data, include path')
parser.add_argument('-in2', metavar="FILENAME", dest="infile2", required=True, help='Input file is necessary to analyze the data, include path')
parser.add_argument('-outdir', metavar="STRING", dest='outdir', help='PATH to results file')
# job details
parser.add_argument('-jobId', metavar="STRING", dest='jobId')
parser.add_argument('-p', metavar="STRING", dest='prefix', help='Predefined parsed file name')
# parameters -> sheets, options
parser.add_argument('-lvals', metavar="LIST", nargs='+', dest="listvals", help='List of values to retrieve')
parser.add_argument('-lsheets', metavar="LIST", nargs='+', dest="listsheets", help='List of sheets to get common genes from, format: [sheet file 1, sheet file 2]')
parser.add_argument('-lcompare', metavar="LIST", nargs='+', dest="listcomp", help='List of lists sheets comparison, format: [sheet file 1, sheet file 2, name out sheet]')
# analysis to perform
parser.add_argument('-all', action='store_true', dest='all', help='Perform every analysis')
parser.add_argument('-vd', action='store_true', dest='vd', help='Obtain only Venn Diagrams')
parser.add_argument('-explev', action='store_true', dest='explev', help='Obtain only Expression Levels of common genes')
parser.add_argument('-vals', action='store_true', dest='vals', help='Obtain only values for common genes')


results = parser.parse_args()
if (results.infile1):
	infile1 = results.infile1
	tmp = infile1.split('/')
	fname1 = tmp[-1].split('.')[0]
	if (len(tmp)>1):
		fpath1 = infile1.split(fname1)[0]
	
if (results.infile2):
	infile2 = results.infile2
	tmp = infile2.split('/')
	fname2 = tmp[-1].split('.')[0]
	if (len(tmp)>1):
		fpath2 = infile2.split(fname2)[0]

if (results.jobId):
	job_ID = results.jobId
else:
	job_ID = str(time.time())
if (results.prefix):
	prefix = results.prefix
else:
	prefix = job_ID
if (results.outdir):
	output_path = results.outdir
else:
	output_path = prefix

if (results.listvals):
	get_values = results.listvals

	#Check if correct code
	for val in get_values:
		if (val not in ['value_1','value_2','log2','test_stat','p_value','q_value','significant','fold','nfold']):
			print('Not valid: ',val)
			quit()
	if ('nfold' in get_values):
		get_values[get_values.index('nfold')] = '-1/fold'

if (results.listsheets):
	get_sheets = results.listsheets
	if (len(get_sheets)%2 == 1):
		print('Not valid, format: sheet_file_1 sheet_file_2')
		quit()
if (results.listcomp):
	get_comparisons = results.listcomp
	if (len(get_comparisons)%3 == 1):
                print('Not valid, format: sheet_file_1 sheet_file_2 out_sheet_name')
                quit()

# CHECK IF OUTPUT FOLDER EXISTS
if (os.path.exists(output_path)):
	print('Folder not valid\nPlease remove prior folder or rename and resubmit')
	sys.exit()
os.mkdir(output_path)

# VALIDATIONS FOR PARAMETER FORMAT
if ('.xlsx' not in fname1):
	fname1 += '.xlsx'
if ('.xlsx' not in fname2):
	fname2 += '.xlsx'

# CHECK FLAGS FOR ANALYSIS
tmp = []
if (not results.all):
	if (results.vd):
		tmp.append('vd')
	if (results.vals):
		tmp.append('vals')
	if (results.explev):
		tmp.append('explev')
if (len(tmp)!=0):
	analysis = tmp

# CALL FUNCTIONS
for i in analysis:
	if (i == 'vd'):
		print('Processing Venn Diagrams')
		venn_diagrams(fpath1+fname1,fpath2+fname2,output_path+'/'+prefix+'_vd',get_sheets)
	elif (i == 'vals'):
		print('Processing common genes values')
		getValues(fpath1+fname1,fpath2+fname2,output_path+'/'+prefix+'_values',get_sheets,get_values)
	elif (i == 'explev'):
		print('Processing same expression levels')
		expLevel(fpath1+fname1,fpath2+fname2,output_path+'/'+prefix+'_explev',get_comparisons)


# CHECK FOR END RUN
print('Complete')

