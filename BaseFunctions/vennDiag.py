## Gene relationship between samples (Venn Diagram)
## Karla Godinez, Jon Mohl


# DECLARATIONS
import sys

import excelFunctions as exFunction
import matplotlib_venn as vplt
from matplotlib import pyplot as plt

# Function to obtain genes from files

def getGenes(gene_info):
	genes = []
	for gene in gene_info:
		genes.append(gene[0])
	return genes

# Function for plotting
def get_fig(a,b,ab,infile1,infile2,outfile):
	f1_name = exFunction.getName(infile1)
	f2_name = exFunction.getName(infile2)
	sizes = [len(a),len(b),len(ab)]
	
	# Circle sizes
	if sizes[2] == 0:
		v = vplt.venn2(subsets = (sizes[0], sizes[1], 0),set_labels =(f1_name,f2_name))
		
	elif sizes[2] > 0 and sizes[2]/max(sizes[0],sizes[1]) < .4:
		v = vplt.venn2(subsets = (sizes[0], sizes[1], sizes[2]+max(sizes[0],sizes[1])/(max(sizes[0],sizes[1])-min(sizes[0],sizes[1]))),set_labels =(f1_name,f2_name))

	else:
		v = vplt.venn2(subsets = (sizes[0], sizes[1], sizes[2]),set_labels =(f1_name,f2_name))

	
	
	# Circle colors
	v.get_patch_by_id('10').set_color('c')
	v.get_patch_by_id('01').set_color('#FF99CC')
	if sizes[2] != 0:
		v.get_patch_by_id('11').set_color('blue')

	# Circle text
	v.get_label_by_id('10').set_text(sizes[0])
	v.get_label_by_id('01').set_text(sizes[1])
	if sizes[2] != 0:
		v.get_label_by_id('11').set_text(sizes[2])

	
	plt.title('Gene Differentiation Expression\n'+f1_name+' vs '+f2_name)
	plt.savefig(outfile+'.png')
	plt.close()


# Main function
def venn_diagrams(infile1,infile2,out_file,sheet_list):	
	sheet_list = [sheet_list[i:i+2] for i in range(0, len(sheet_list), 2)]

	for sheet in sheet_list:
		print('Processing '+sheet[0]+' vs '+sheet[1])
		# Name output
		sheet1,sheet2 = exFunction.getNameSheet(sheet[0],sheet[1])
		# Name Excel sheet
		name_sheet1 = exFunction.getCorrectName(infile1,sheet[0])
		name_sheet2 = exFunction.getCorrectName(infile2,sheet[1])

		genes_file1 = exFunction.readExcel(infile1,name_sheet1)
		genes_file2 = exFunction.readExcel(infile2,name_sheet2)
		
		if(genes_file1 != False and genes_file2 != False):
			genes_file1 = getGenes(genes_file1)
			genes_file2 = getGenes(genes_file2)
			# Variables for Venn Diagram Representation
			''' a  -> genes only in file 1
			    b  -> genes only in file 2
			    ab -> genes in both file 1 and 2
			'''
			a = []
			b = []
			ab = []

			for gene in genes_file1:
				if gene in genes_file2:
					ab.append(gene)
				else:
					a.append(gene)

			for gene in genes_file2:
				if (gene in genes_file1):
					if not gene in ab:
						ab.append(gene)
				else:
			    		b.append(gene)

			#WRITE OUTPUT FILE
			status = exFunction.writeExcel_vd(a,b,ab,infile1,infile2,out_file+'_'+sheet1+'_vs_'+sheet2)
		## Image VD
			if(status):
				get_fig(a,b,ab,infile1,infile2,out_file+'_'+sheet1+'_vs_'+sheet2)
				print('Success: Process complete')
			else:
				print('Error: Image could not be generated')
		else:
			print('Error: Incorrect file(s)')
		

