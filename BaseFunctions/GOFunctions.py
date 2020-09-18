## GO terms functions
## Karla Godinez, Jon Mohl


# DECLARATIONS
import re

# Creates dictionary with GO terms as keys and GO term description as value
def getGOnames(gofile):
        godict = {}
        f = open(gofile, 'r')
        goFile = f.readlines()
        f.close()
        ont = {'biological_process':'bp','molecular_function':'mf','cellular_component':'cc'}
        godict = {}
        for line in goFile:
                sl = line.strip().split('\t')
                godict[sl[0]] = [sl[1],sl[2],int(sl[3])]
        return godict

# Creates dictionary with genes as keys and a list of lists for values.
def geneToGo(genefile):
	f = open(genefile, 'r')
	geneFile = f.readlines()
	f.close()
	genedict = {}
	for line in geneFile:
		if line[0] != '!':
			temp = line.split('\t')
			if temp[2] in genedict.keys():
				if temp[4] not in genedict[temp[2]]:
					genedict[temp[2]].append(temp[4])
			else:
				genedict[temp[2]] = [temp[4]]
	return genedict

# Check GO term significance
def getSignificance(A,B,C,D):
	from scipy.stats import fisher_exact
	from statsmodels.stats import multitest as multitest
	pval = fisher_exact([[A,B],[C,D]])[1]
	fdr = 'N/A'
	if pval < 0.05:
		significance = 'Yes'
	else:
		significance = 'No'
	return [pval,fdr,significance]


# Returns list of GO terms based on gene list
def getTerm(genes,gonames,genetogo):
	from scipy.stats import fisher_exact
	from statsmodels.stats import multitest as multitest
	dict_terms = {}
	for gene in genes:
		if gene[0] != 'N/A':
			if any(gene[0] == gk for gk in genetogo.keys()):
				terms = genetogo[gene[0]]
				for term in terms:
					if term in dict_terms.keys():
						if gene[0] not in dict_terms[term]:
							dict_terms[term].append(gene[0])
					else:
						dict_terms[term] = [gonames[term][1],gonames[term][0],gene[0]]
	list_terms = []
	try:
		for key, value in dict_terms.iteritems():
			list_terms.append([key,value[0],value[1],len(value)-2] + getSignificance(len(value)-2,gonames[key][2]-len(value)-2,len(genes)-len(value)-2,len(genetogo.keys())-len(genes)-gonames[key][2]+len(value)-2) + value[2:])
	except:
		for key, value in list(dict_terms.items()):
			list_terms.append([key,value[0],value[1],len(value)-2] + getSignificance(len(value)-2,int(gonames[key][2])-len(value)+2,len(genes)-len(value)+2,len(genetogo.keys())-len(genes)-int(gonames[key][2])+len(value)-2) + value[2:])
	pva = []
	for lt in list_terms:
		pva.append(lt[4])
	mt = multitest.multipletests(pva,alpha=0.05,method='fdr_bh',is_sorted=False,returnsorted=False)
	for x in range(0,len(list_terms)):
		list_terms[x][5] = mt[1][x]
		if mt[0][x]:
			list_terms[x][6] = 'Yes'
		else:
			list_terms[x][6] = 'No'

	return list_terms


# Returns list of GO terms based on a term (bp,mf,cc)
def getTermByType(dat,term):
	try:
		terms = []
		for d in dat:
			if d[1] == term:
				terms.append(d)
		return terms
	except:
		return 'NaN'


# Creates a consolidated txt file for use in getDict function
def createGeneGODict(infile,outfile):
	geneDict = geneToGo(infile)
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

#Create a summarized GO term list for use in getGOnames functions
#Created by JEM, 20190819
def createGOinfoDict(genedict,obo,outfile):
	import re
	godict = {}
	f = open(genedict,'r')
	goFile = f.readlines()
	f.close()
	got = {}
	for g in goFile:
		sl = g.strip().split('\t')
		for s in sl[1:]:
			if s in got.keys():
				got[s].append(sl[0])
			else:
				got[s] = [sl[0]]
	f = open(obo,'r')
	goFile = f.read()
	f.close()
	ont = {'biological_process':'bp','molecular_function':'mf','cellular_component':'cc'}
	p = re.compile("id: GO:\d+")
	fo = open(outfile,'w')
	for m in p.finditer(goFile):
		start = goFile.find('\nname: ',m.start())
		ns = goFile.find('\nnamespace: ',start)
		end = goFile.find('\n',ns+1)
		if m.group()[4:] in got.keys():
			fo.write('\t'.join([m.group()[4:],goFile[start+7:ns],ont[goFile[ns+12:end]],str(len(got[m.group()[4:]]))]) + '\n')
		else:
			fo.write('\t'.join([m.group()[4:],goFile[start+7:ns],ont[goFile[ns+12:end]],'0']) + '\n')
	fo.close()
	return 'Complete'

# Returns a dictionary based on list
def getGeneGODict(infile):
	d = {}
	read = open(infile,'r').readlines()
	for r in read:
		tmp = r.strip().split('\t')
		d[tmp[0]] = tmp[1:]
	return d
