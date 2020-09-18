## Parser functions
## Karla Godinez, Jon Mohl


import datetime

# Creates dictionary with genes as keys and a list of lists for values.
def geneToInfo(genefile):
        f = open(genefile, 'r')
        geneFile = f.readlines()
        f.close()
        genedict = {}
        for line in geneFile:
                pos = line.find('gene')
                if (line[0] != '#') and (pos != -1) and (pos < 10):
                        chr = line[0:line.find('\t')]
                        loc = line[pos:line.find('.',pos)].split('\t')
                        pos = line.find('gene_name',pos)
                        gene = line[pos:line.find(';',pos)].split('"')[1]
                        genedict[gene] = ['chr'+chr,loc[1]+':'+loc[2]]
        return genedict

# Creates a consolidated txt file for use in getDict function
def createGeneInfoDict(infile,outfile):
        geneDict = geneToInfo(infile)
        f = open(outfile,'w')
        try:
                for key, value in geneDict.iteritems():
                        temp = key + '\t' + '\t'.join(value) + '\n'
                        f.write(temp)
        except:
                for key, value in geneDict.items():
                        temp = key + '\t' + '\t'.join(value) + '\n'
                        f.write(temp)
        f.close()
        return 'Complete'

# Returns a dictionary based on list
def getGeneInfoDict(infile):
        d = {}
        read = open(infile,'r').readlines()
        for r in read:
                tmp = r.strip().split('\t')
                d[tmp[0]] = tmp[1:]
        return d

# Find index for corrected significance
def getCorrectedIndex(header):
	for i in header:
		if (i == 'PValue') or (i == 'FDR') or (i == 'q_value') or (i == 'corrected') or (i == 'padj'):
			return header.index(i)
	return 'NaN'

# Find index for Log Fold change
def getLogFold(header):
	for i in header:
		if (i == 'log2(fold_change)') or (i == 'log2') or (i == 'logFC') or (i == 'log2FoldChange'):
			return header.index(i)
	return 'NaN'

# Find index for name in header
def getColumnHeader(name,header):
	for i in header:
		if (i == 'fold') or (i == 'Fold'):
			return header.index(i)
		if (i == '-1/fold') or (i == '-1/Fold'):
			return header.index(i)
	if name in header:
		return header.index(name)
	return 'NaN'

# Find index for Numerical values in header
def getStats(header):
	for i in header:
		if (i != 'gene') and (i != 'chromosome') and (i != 'position') and (i != 'sample_1') and (i != 'sample_2') and (i != 'status'):
			return header.index(i)
	return 'NaN'


# Return ok/significant data for Cuffdiff
def getDataCD(header,reads,sigthreshold):
	# Output new list: gene chromosome position sample_1 sample_2 status value_1 value_2 log2,test_stat,p_value,q_value,significant
	header = header.split()
	header = header[2:]
	header[1] = 'chromosome'
	header.insert(2,'position')

	# Get significant and OK elements
	sig_list = []
	ok_list = []

	# Find index for significance
	index = getCorrectedIndex(header)
	if index == 'NaN':
		return False,header,ok_list,sig_list

	# Get data
	for read in reads:
		temp = read.split('\t')
		if(temp[2] != '-' and temp[6] == 'OK'):
			# Get significance status
			if (float(temp[-2]) < sigthreshold):
				significance = 'yes'
			else:
				significance = 'no'

			# Get chromosome/position
			locus = temp[3].split(':')
			locus[1] = locus[1].replace('-',':')
			ok_list.append([temp[2]]+locus+temp[4:-1]+[significance])
			# Get SIGNIFICANT reads
			if (significance == 'yes'):
				sig_list.append([temp[2]]+locus+temp[4:-1]+[significance])
	return True,header,ok_list,sig_list

# Return ok/significant data for R
def getDataR(header,reads,sigthreshold):
	# Minimum output header: gene, chr, position, log2, corrected, significant
	header = header.strip().replace('"','').split(',') + ['significant']

	# Get significant and OK elements
	sig_list = []
	ok_list = []

	# Find index for significance
	index = getCorrectedIndex(header)
	if index == 'NaN':
		return False,header,ok_list,sig_list

	# Get data
	for read in reads:
		temp = read.replace('"','').strip().split(',')
		if (temp[0] != '-') or (temp[0] != ''):
			if temp[index] == 'NA':
				significance = 'no'
			elif (float(temp[index]) < sigthreshold):
				significance = 'yes'
			else:
				significance = 'no'

			ok_list.append(temp + [significance])
			if(significance == 'yes'):
				sig_list.append(temp + [significance])
	return True,header,ok_list,sig_list

# Append chromosome and position data into every read
def addGeneInfo(header,reads,geneInfo):
	header = 'gene,chromosome,position'+header
	tmp_reads = []
	for read in reads:
		tmp_read = read.split(',')
		tmp_gene = tmp_read[0].replace('"','').split('_')[0]
		tmp_data = ','.join(geneInfo.get(tmp_gene,['N/A','N/A']))
		tmp_reads.append(tmp_gene+','+tmp_data+','+','.join(tmp_read[1:]))

	return header,tmp_reads

# Get summary data
def getSummary(summary_sheets,threshold,species,filetype,sigthreshold,fileVersions):
	summary = []
	# Date
	summary.append(['Date',datetime.datetime.now().strftime("%Y-%m-%d")])
	# File Versions
	for f in fileVersions:
		summary.append(f.split('\t'))
	# Species
	if species == 'hs':
		summary.append(['Species','Human'])
	elif species == 'mm':
		summary.append(['Species','Mouse'])
	elif species == 'dr':
		summary.append(['Species','Zebrafish'])
	else:
		summary.append(['Species','Other'])
	# Input file type
	if filetype == 'cd':
		summary.append(['Input file type','CuffDiff'])
	else:
		summary.append(['Input file type','R'])
	# Thresholds
	summary.append(['Significance threshold value',+sigthreshold])
	summary.append(['Log > threshold ',threshold[0]])
	summary.append(['Log < threshold ',threshold[1]])
	summary.append(['Fold > threshold ',threshold[2]])
	summary.append(['Fold < threshold ',threshold[3]])
	# Sheets
	for s in summary_sheets:
		summary.append(s.split(':'))

	return summary





