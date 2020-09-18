## Command line parser
## Karla Godinez, Jon Mohl


# DECLARATIONS
import os
import argparse
import time
import sys

from config import *
import gene_diff_parsing as geneParse


# SET DEFAULTS
filetype = 'cd'
species = 'hs'
sigthreshold = 0.05
threshold = [2]
sheets = ['ok','sig','gl','gogl','ll','goll','gf','gogf','lf','golf','cml','cmf']
analysis = ['bpl','bpf']
termtype = ['bp','cc','mf']
numterms = 25


# REPLACE VARS BY ARGPARSE
parser = argparse.ArgumentParser()
parser = argparse.ArgumentParser(description='UTEP\'s Gene diff parser')
parser.add_argument('-in', metavar="FILENAME", dest="infile", required=True, help='Input file is necessary to parse the gene diff file')
parser.add_argument('-outdir', metavar="STRING", dest='outdir', help='PATH to results file',default='./')
parser.add_argument('-jobId', metavar="STRING", dest='jobId')
parser.add_argument('-p', metavar="STRING", dest='prefix', help='Predefined parsed file name')
parser.add_argument('-sp', metavar="STRING", dest='species', help='Predefined species')
parser.add_argument('-ft',metavar="STRING", dest='filetype', help='Input format type: cd or r')
parser.add_argument('-st', metavar="INT",type=float, dest='sigthreshold')
#parameters -> sheets
parser.add_argument('-s', metavar="LIST", nargs='+', dest="sheets", help='List of sheets to be parsed')
parser.add_argument('-t', metavar="INT",type=float, dest="threshold", help='Threshold for fold and log fold change value')
parser.add_argument('-lgt', metavar="INT",type=float, dest="lgt", help='Threshold for log fold change value greater than')
parser.add_argument('-llt', metavar="INT",type=float, dest="llt", help='Threshold for log fold change value lower than')
parser.add_argument('-fgt', metavar="INT",type=float, dest="fgt", help='Threshold for fold change value greater than')
parser.add_argument('-flt', metavar="INT",type=float, dest="flt", help='Threshold for fold change value lower than')
# analysis to perform / figures to obtain
parser.add_argument('-all', action='store_true', dest='all', help='Perform every analysis')
parser.add_argument('-bpl', action='store_true', dest='bpl', help='Obtain only GO Terms Log fold change barplot')
parser.add_argument('-bpf', action='store_true', dest='bpf', help='Obtain only GO Terms Fold change barplot')
parser.add_argument('-nt', metavar="INT", dest="numterms", help='Number terms to get GO Terms for each barplot')
parser.add_argument('-tt', metavar="LIST", nargs='+', dest="termtype", help='Type GO Term to get barplot from')


results = parser.parse_args()

if results.infile:
	infile = results.infile
if results.filetype:
	filetype = results.filetype
if results.sigthreshold:
	sigthreshold = results.sigthreshold

# Assign single threshold or individual. If not given, use default
if results.threshold:
	threshold = [results.threshold]
elif results.lgt or results.llt or results.fgt or results.flt:
	lgt = (results.lgt if results.lgt else '2')
	llt = (results.llt if results.llt else  '-2')
	fgt = (results.fgt if results.fgt else '2')
	flt = (results.flt if results.flt else '-2')
	threshold = [lgt,llt,fgt,flt]

if results.species:
	species = results.species

if results.jobId:
	job_ID = results.jobId
else:
	job_ID = str(time.time())
if results.prefix and results.prefix != '':
	prefix = results.prefix
else:
	prefix = job_ID
output_path = results.outdir+prefix
if results.sheets:
	sheets = results.sheets

# CHECK FLAGS FOR ANALYSIS
tmp = []
if (not results.all):
	if results.bpl:
		tmp.append('bpl')
	if results.bpf:
		tmp.append('bpf')
if (len(tmp)!=0):
	analysis = tmp

if results.numterms:
	numterms = results.numterms
if results.termtype:
	termtype = results.termtype


# CHECK IF OUTPUT FOLDER EXISTS
if (os.path.exists(output_path)):
	print('Folder not valid\nPlease remove prior folder or rename and resubmit')
	sys.exit()
os.mkdir(output_path)

# VALIDATIONS FOR PARAMETER FORMAT
if (filetype == 'cd' and '.diff' not in infile):
	infile += '.diff'
elif (filetype == 'r' and '.csv' not in infile):
	infile += '.csv'

# CALL FUNCTION
status,msg = geneParse.parse_file(prefix+'_gd',infile,output_path+'/',threshold,sheets,species,filetype,sigthreshold,analysis,termtype,numterms)
print(msg)

# CHECK FOR END RUN
print('Complete')



