## Parser tool
## Karla Godinez, Jon Mohl


# DECLARATIONS
import sys
import math
import time

from config import *
import barPlot as bp
import GOFunctions as go
import excelFunctions as output
import parseFunctions as pf



# Function to be parsed
'''
g2Log  -> (> 2 Log) or infinite
l2Log  -> (< -2 Log) or -infinite
g2Fold -> (> 2)
l2Fold -> (> -2)
cmap   -> (up/down regulated genes sorted by most/less regulated level)
'''


def getFold(val):
	if 'inf' in val:
		return ''
	try:
		return math.pow(2,float(val))
	except:
		return 999

def calculateFold(val_list,index):
	# Calculate fold, -1/fold and append to list
	for item in val_list:
		# Get value 1 and value 2 from read
		fold = getFold(item[index])
		if fold != '':
			item.append(fold)
			if fold != 0:
				item.append(-1/fold)
			else:
				item.append('undefined')
		else:
			item.append('undefined')
			item.append('undefined')

	return val_list

def g2Log(reads,t,index):
	seq = []
	for read in reads:
		if float(read[index]) >= t or read[index] == 'inf':
			seq.append(read)
	return seq

def l2Log(reads,t,index):
	seq = []
	for read in reads:
		if float(read[index]) <= t or read[index] == '-inf':
			seq.append(read)
	return seq

def g2Fold(reads,t,index):
	seq = []

	for read in reads:
		if(read[-2] == 'undefined' and read[index] == 'inf'):
			seq.append(read)
		elif read[-2] != 'undefined' and float(read[-2]) >= t:
			seq.append(read)
	return seq

def l2Fold(reads,t,index):
	seq = []
	for read in reads:
		if(read[-1] == 'undefined' and read[index] == '-inf'):
			seq.append(read)
		elif read[-1] != 'undefined' and float(read[-1]) <= t:
			seq.append(read)
	return seq

def cmap(species,up,down,index):
	#Read file to get valid genes
	f = open(REF_DIR+'validGenes-'+species+'.txt')
	valid_genes = f.read()
	f.close()
	valid_genes = valid_genes.split('\n')

	seq = []
	# Sort up/down regulated genes by level of expression
	up = sorted(up, key = lambda x: x[index])[::-1]
	down = sorted(down, key = lambda x: x[index])[::-1]
	
	# Check for valid genes
	valid_up = []
	valid_down = []
	for gene in up:
		if (gene[0] in valid_genes):
			valid_up.append(gene)
	for gene in down:
		if (gene[0] in valid_genes):
			valid_down.append(gene)
	
	# Get list of top 150 genes
	if len(valid_up)>len(valid_down):
		for i in range(len(valid_down)):
			seq.append([valid_up[i][0],valid_down[i][0]])
		for i in range(len(valid_down),len(valid_up)):
			seq.append([valid_up[i][0],''])
	else:
		for i in range(len(valid_up)):
			seq.append([valid_up[i][0],valid_down[i][0]])
		for i in range(len(valid_up),len(valid_down)):
			seq.append(['',valid_down[i][0]])
	
	if (len(seq)>150):
		return (seq[:150])
	else:
		return (seq)

# Main function
'''
prefix      -> name excel file
path_file   -> path where file to be read is
path_output -> path where to save file, default same as in file
options     -> list of sheets to be obtained
GO_file     -> GO terms reference file
'''

def parse_file(prefix,infile,path_output,threshold,sheets,species,filetype,sigthreshold,analysis,termtype,numterms):
	try:
		f=open(infile,'r')
		header = f.readline()
		reads = f.readlines()
		f.close()
	except:
		return(False,'Error: Reading file')

	try:
		# Define threshold values
		# lgt -> log>#, llt -> log<#, fgt -> fold>#, flt -> fold<#
		if len(threshold)==1:
			lgt = fgt = threshold[0]
			llt = flt = threshold[0]*-1
		elif len(threshold)==2:
			if ('lgt' in sheets):
				lgt = threshold[0]
				llt = threshold[1]
			else:
				fgt = threshold[0]
				flt = threshold[1]
		else:
			lgt = threshold[0]
			llt = threshold[1]
			fgt = threshold[2]
			flt = threshold[3]
		
		# Handle header and data with filetype
		if filetype == 'cd':
			status,header,ok_list,sig_list = pf.getDataCD(header,reads,sigthreshold)
		elif filetype == 'r':
			geneDict = pf.getGeneInfoDict(REF_DIR+'geneInfo-'+species+'.txt')
			header,reads = pf.addGeneInfo(header,reads,geneDict)
			status,header,ok_list,sig_list = pf.getDataR(header,reads,sigthreshold)
		
		if not status: # Status: True -> valid corrected column False -> invalid corrected column
			return (False,'Error: Invalid corrected column')

		# Add header and values: [fold, -1/fold]
		header += ['Fold','-1/Fold']
		index = pf.getLogFold(header)

		if index == 'NaN':
			return (False,'Error: Invalid log fold column')
		
		ok_list = calculateFold(ok_list,index)
		sig_list = calculateFold(sig_list,index)

		# Options to be written in Excel file
		data = []
		sheet = []
		headers = []
		
		if any(s in ['gl','gogl','cml'] for s in sheets):
			gl = g2Log(sig_list,lgt,index)
			ll = l2Log(sig_list,llt,index)

		if any(s in ['gf','golf','cmf'] for s in sheets):
			gf = g2Fold(sig_list,fgt,index)
			lf = l2Fold(sig_list,flt,index)
		
		if any(s in ['gogl','goll','gogf','golf'] for s in sheets):
			goNames = go.getGOnames(REF_DIR+'goInfo-'+species+'.txt')
			geneDict = go.getGeneGODict(REF_DIR+'geneDict-'+species+'.txt')
		
		# Append summary sheet
		summary_sheets = []
		# Append data sheets to be written in Excel file
		for opt in sheets:
			if opt == 'ok':
				summary_sheets.append('Total OK genes: '+str(len(ok_list)))
				data.append(ok_list)
				sheet.append('OK')
				headers.append(header)
			elif opt == 'sig':
				summary_sheets.append('Total Significant genes: '+str(len(sig_list)))
				data.append(sig_list)
				sheet.append('Significant')
				headers.append(header)
			elif opt == 'gl':
				summary_sheets.append('Total >'+str(lgt)+' Log genes: '+str(len(gl)))
				data.append(gl)
				sheet.append('>'+str(lgt)+' Log')
				headers.append(header)
			elif opt == 'gogl':
				tmp = go.getTerm(gl,goNames,geneDict)
				summary_sheets.append('Total >'+str(lgt)+' Log GO Terms: '+str(len(tmp)))
				data.append(tmp)
				sheet.append('GO >'+str(lgt)+' Log')
				headers.append(['GO term','ontology','description','count','p-value','FDR','significant','genes'])
			elif opt == 'll':
				summary_sheets.append('Total <'+str(llt)+' Log genes: '+str(len(ll)))
				data.append(ll)
				sheet.append('<'+str(llt)+' Log')
				headers.append(header)
			elif opt == 'goll':
				tmp = go.getTerm(ll,goNames,geneDict)
				summary_sheets.append('Total <'+str(llt)+' Log GO Terms: '+str(len(tmp)))
				data.append(tmp)
				sheet.append('GO <'+str(llt)+' Log')
				headers.append(['GO term','ontology','description','count','p-value','FDR','significant','genes'])
			elif opt == 'gf':
				summary_sheets.append('Total >'+str(fgt)+' Fold genes: '+str(len(gf)))
				data.append(gf)
				sheet.append('>'+str(fgt)+' Fold')
				headers.append(header)
			elif opt == 'gogf':
				tmp = go.getTerm(gf,goNames,geneDict)
				summary_sheets.append('Total >'+str(fgt)+' Fold GO Terms: '+str(len(tmp)))
				data.append(tmp)
				sheet.append('GO >'+str(fgt)+' Fold')
				headers.append(['GO term','ontology','description','count','p-value','FDR','significant','genes'])
			elif opt == 'lf':
				summary_sheets.append('Total <'+str(flt)+' Fold genes: '+str(len(lf)))
				data.append(lf)
				sheet.append('<'+str(flt)+' Fold')
				headers.append(header)
			elif opt == 'golf':
				tmp = go.getTerm(lf,goNames,geneDict)
				summary_sheets.append('Total <'+str(flt)+' Fold GO Terms: '+str(len(tmp)))
				data.append(tmp)
				sheet.append('GO <'+str(flt)+' Fold')
				headers.append(['GO term','ontology','description','count','p-value','FDR','significant','genes'])
			elif opt == 'cml':
				data.append(cmap(species,gl,ll,index))
				sheet.append('CMap Log')
				headers.append(['upregulated','downregulated'])
			elif opt == 'cmf':
				data.append(cmap(species,gf,lf,index))
				sheet.append('CMap Fold')
				headers.append(['upregulated','downregulated'])
			
		fv = open(REF_DIR+'fileVersion.txt','r').readlines()
		data.insert(0,pf.getSummary(summary_sheets,[lgt,llt,fgt,flt],species,filetype,sigthreshold,fv))
		sheet.insert(0,'Summary')
		headers.insert(0,['Parsed file summary'])

		# Change directory to where save file
		try:
			output.parsedExcel(path_output,prefix,headers,sheet,data)
			#return (True, 'Success: Writing the file')
		except:
			return (False,'Error: Writing Excel file')

		# Analysis to perform
		try:
			infile = path_output+prefix+'.xlsx'
			outfile = path_output+prefix.split('_gd')[0]
			objectfile = output.openExcel(infile)

			for opt in analysis:
				if (opt == 'bpl'):
					for tt in termtype:
						bp.barPlot(outfile+'_'+opt+'_'+tt,output.extractData(objectfile,output.getCorrectName(infile,'GO < Log')),tt,numterms)

					for tt in termtype:
						bp.barPlot(outfile+'_'+opt+'_'+tt,output.extractData(objectfile,output.getCorrectName(infile,'GO < Fold')),tt,numterms)
						bp.barPlot(outfile+'_'+opt+'_'+tt,output.extractData(objectfile,output.getCorrectName(infile,'GO > Fold')),tt,numterms)

			return (True, 'Success: Generating the figures')
		except:
			return (False,'Error: Generating the figures')
	except:
		return (False,'Error: Parsing file')

