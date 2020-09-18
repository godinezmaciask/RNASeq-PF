## Update reference file if newer version of raw files
## Karla Godinez, Jon Mohl


# DECLARATIONS
import os
import argparse
from config import *
import sys

import GOFunctions as go
import parseFunctions as pf


# SET DEFAULTS
ftype = 'geneDict'


# REPLACE VARS BY ARGPARSE
parser = argparse.ArgumentParser()
parser = argparse.ArgumentParser(description='Reference update files generator')
parser.add_argument('-in', metavar='FILENAME', dest='infile', required=True, help='Input file containig the reference') 
parser.add_argument('-out', metavar='STRING', dest='outfile', required=True, help='output file')
parser.add_argument('-type', metavar='STRING', dest='ftype', help='Type of file to update: geneDict, geneInfo')

results = parser.parse_args()

infile = results.infile
outfile = results.outfile

if (results.ftype):
	ftype = results.ftype


# VALIDATIONS FOR PARAMETER FORMAT
if (ftype == 'geneDict'):
	try :
		msg = go.createGeneGODict(infile,outfile)
		print(msg)
	except:
		print('Error: Please check the reference file is a valid .goa file and the output location is valid')
if (ftype == 'geneInfo'):
        try :
                msg = pf.createGeneInfoDict(infile,outfile)
                print(msg)
        except:
                print('Error: Please check the reference file is a valid .gtf file and the output location is valid')



