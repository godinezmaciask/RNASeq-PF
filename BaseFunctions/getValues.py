## Common genes expression level values
## Karla Godinez, Jon Mohl


# DECLARATIONS
import sys
import excelFunctions as exFunction
import parseFunctions as pf


def vals(f1,f2,gene,index):

	return f1[gene][index],f2[gene][index]

def getGenes(gene_info):
	genes = []
	for gene in gene_info:
		genes.append(gene[0])
	return genes

def getValuesCD(common_genes,value_list,values_file1,values_file2):
	common_gene_values = []
	for gene in common_genes:
		temp = [gene]
		for opt in value_list:
			if opt == "value_1":
				temp += (vals(values_file1,values_file2,gene,0))
			elif opt == "value_2":
				temp += (vals(values_file1,values_file2,gene,1))
			elif opt == "log2":
				temp += (vals(values_file1,values_file2,gene,2))
			elif opt == "test_stat":
				temp += (vals(values_file1,values_file2,gene,3))
			elif opt == "p_value":
				temp += (vals(values_file1,values_file2,gene,4))
			elif opt == "q_value":
				temp += (vals(values_file1,values_file2,gene,5))
			elif opt == "significant":
				temp += (vals(values_file1,values_file2,gene,6))
			elif opt == 'fold':
				temp += (vals(values_file1,values_file2,gene,7))
			elif opt == '-1/fold':
				temp += (vals(values_file1,values_file2,gene,8))
			else:
				print('Error: Not valid option')
		common_gene_values.append(temp)
	return common_gene_values

def findValues(common_genes,val_list,val_data1,val_data2,head1,head2):
	common_gene_values = []
	for gene in common_genes:
		tmp = [gene]
		for opt in val_list:
			ind = pf.getColumnHeader(opt,head1)
			tmp_dat1 = (val_data1[gene][ind] if (ind != 'NaN') else 'N/A')

			ind = pf.getColumnHeader(opt,head2)
			tmp_dat2 = (val_data2[gene][ind] if (ind != 'NaN') else 'N/A')

			tmp += (tmp_dat1,tmp_dat2)
		common_gene_values.append(tmp)
	return common_gene_values

	

def getValues(infile1,infile2,out_file,sheet_list,value_list):
	sheet_list = [sheet_list[i:i+2] for i in range(0, len(sheet_list), 2)]
	
	for sheet in sheet_list:
		print('Processing '+sheet[0]+' vs '+sheet[1])
		name_sheet1 = exFunction.getCorrectName(infile1,sheet[0])
		name_sheet2 = exFunction.getCorrectName(infile2,sheet[1])

		try:
			# Find header of each file
			head1 = exFunction.headerExcel(infile1,name_sheet1)
			head2 = exFunction.headerExcel(infile2,name_sheet2) 

			# Find stat index
			stat1 = pf.getStats(head1)
			stat2 = pf.getStats(head2)

			# Get genes/values data
			genes_file1 = getGenes(exFunction.readExcel(infile1,name_sheet1))
			genes_file2 = getGenes(exFunction.readExcel(infile2,name_sheet2))

			values_file1 = exFunction.readValues(genes_file1,infile1,name_sheet1,stat1)
			values_file2 = exFunction.readValues(genes_file2,infile2,name_sheet2,stat2)

			# Find common genes
			common_gene = []
			for gene in genes_file1:
				if gene in genes_file2:
					common_gene.append(gene)
			for gene in genes_file2:
				if (gene in genes_file1) and not(gene in common_gene):
					common_gene.append(gene)
			
			# Get values for common genes
			common_gene_values = findValues(common_gene,value_list,values_file1,values_file2,head1[stat1:],head2[stat2:])

			#WRITE FILE
			sheet1,sheet2 = exFunction.getNameSheet(sheet[0],sheet[1])
			status = exFunction.writeExcel_values(infile1,infile2,common_gene_values,value_list,out_file+'_'+sheet1+'_vs_'+sheet2)
			if(status):
				print('Success: Process complete')
			else:
				print('Error: Excel could not be generated')
		except:
			print('Error: Couldn\'t read file(s)')
