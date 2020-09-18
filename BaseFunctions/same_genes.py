## Genes with similar expression level values
## Karla Godinez, Jon Mohl


# DECLARATIONS
import sys
import excelFunctions as exFunction
import parseFunctions as pf


# Get genes based on CuffDiff excel
def getSameGenes(genes_file1,genes_file2,index_s1,index_s2,index_lf1,index_lf2):
	tmp_gene = []
	tmp_stat = []
		
	for gene in genes_file2:
		tmp_gene.append(gene[0])
		tmp_stat.append(gene)
	
	#Get same genes and sign on both
	same_gene = []
	same_sign = []
	
	for gene in genes_file1:
		if gene[0] in tmp_gene:
			ind = tmp_gene.index(gene[0])

			if((float(gene[index_lf1]) < 0 and float(tmp_stat[ind][index_lf2]) < 0) or (float(gene[index_lf1]) >= 0 and float(tmp_stat[ind][index_lf2]) >= 0) or (gene[index_lf1] == "-inf" and tmp_stat[ind][index_lf2] == "-inf") or (gene[index_lf1] == "inf" and tmp_stat[ind][index_lf2] == "inf")):
				same_sign.append([gene[0]]+gene[index_s1:]+tmp_stat[ind][index_s2:])
			
	return same_sign


# Main Function
def expLevel(infile1,infile2,out_file,comparison_list):
	comparison_list = [comparison_list[i:i+3] for i in range(0, len(comparison_list), 3)]
	genes = []
	comparison = []

	for comp in comparison_list:
		print('Processing '+comp[0]+' vs '+comp[1])
		# Name output
		sheet1,sheet2 = exFunction.getNameSheet(comp[0],comp[1])
		# Name Excel sheet
		name_sheet1 = exFunction.getCorrectName(infile1,comp[0])
		name_sheet2 = exFunction.getCorrectName(infile2,comp[1])

		genes_file1 = exFunction.readExcel(infile1,name_sheet1)
		genes_file2 = exFunction.readExcel(infile2,name_sheet2)
		
		if(genes_file1 != False and genes_file2 != False):
			# Find correct indexes for analysis
			head1 = exFunction.headerExcel(infile1,name_sheet1)
			head2 = exFunction.headerExcel(infile2,name_sheet2)
			stat1 = pf.getStats(head1)
			stat2 = pf.getStats(head2)
			lf1 = pf.getLogFold(head1)
			lf2 = pf.getLogFold(head2)
			# Correct indexes for output
			f1 = len(head1[stat1:]) - 1
			nf1 = len(head1[stat1:])
			f2 = -2
			nf2 = -1
			
			# Get same genes
			genes.append(getSameGenes(genes_file1,genes_file2,stat1,stat2,lf1,lf2))
			comparison.append(exFunction.getCorrectName(infile1,comp[2]))
		else:
			print('Error: Incorrect file(s)')

	#WRITE FILE
	status = exFunction.writeExcel_expLevel(genes,comparison,infile1,infile2,out_file,['gene']+head1[stat1:],head2[stat2:],f1,f2,nf1,nf2)
	if(status):
		print('Success: Process complete')
	else:
		print('Error: Excel could not be generated')
		


