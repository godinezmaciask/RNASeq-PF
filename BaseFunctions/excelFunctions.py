## Excel write/read functions
## Karla Godinez, Jon Mohl


# Excel writer and reader Python package
import xlsxwriter
import xlrd

# Formating excel sheet
merge_form = {'bold': 1,'align': 'center','valign': 'vcenter'}
text_form = {'num_format': '@'}

# Function to get only name of file
def getName(f):
	return f.split('/')[-1].split('.')[0]

def getFiletype(infile):
	ft = 'N/A'
	f = xlrd.open_workbook(infile)
	s = f.sheet_by_name('Summary')

	return ft

def getNameSheet(s1,s2):
	if '<' in s1:
		sheet1 = ('f' if ('Fold' in s1 or 'fold' in s1) else 'l' ) + 'lt'
	else:
		sheet1 = ('f' if ('Fold' in s1 or 'fold' in s1) else 'l' ) + 'gt'

	if '<' in s2:
		sheet2 = ('f' if ('Fold' in s2 or 'fold' in s2) else 'l' ) + 'lt'
	else:
		sheet2 = ('f' if ('Fold' in s2 or 'fold' in s2) else 'l' ) + 'gt'
	

	return sheet1,sheet2

# Find correct sheet name in excel for type of comparison
def getCorrectName(infile,comp):
	# Find correct sign and fold change
	sign = ('<' if '<' in comp else '>' )
	val = ('Fold' if 'Fold' in comp else 'Log')
	special = ('GO' if 'GO' in comp else '')

	f = xlrd.open_workbook(infile)
	sheets = f.sheet_names()

	for sheet in sheets:
		if sign in sheet and val in sheet and special in sheet:
			return sheet

	return 'Error: Sheet ' + comp + ' not found in ' + getName(infile)



# Write sheet header for output Excel file
def writeHeader(header,sheet):
	# Create a format to use in the merged range.
	for i in range(len(header)):
		sheet.write(0,i,header[i])

# Write each cell data for output Excel file
def writeData(sheet,data,text_format):
	for i in range(len(data)):
		for j in range(len(data[i])):
			sheet.write(i+1,j,data[i][j])
		sheet.set_column('A:A',20,text_format)

# Create Excel file depending on type of input
'''
file_name -> output file name
header -> list with header ['head 1','head 2',...]
sheets -> list with sheet names ['ok','significant',...]
data   -> list of lists with data [[list_ok],[list_significant],...]
'''

def parsedExcel(path,file_name,header,sheets,data):
	try: 
		# Check if sheets and data matches in length
		if (len(sheets)!=len(data)):	
			return ('Error: Creating Excel file')
	
		workbook = xlsxwriter.Workbook(path+file_name+".xlsx")
		# Set 'text' format for each cell in Excel file
		text_format = workbook.add_format(text_form)

		# Creation and data writing for each seet
		for i in range(len(sheets)):
			sheet = workbook.add_worksheet(sheets[i])
			writeHeader(header[i],sheet)
			writeData(sheet,data[i],text_format)
	    
		workbook.close()
		return ('Success Excel file: '+file_name)
	except:
		return ('Error: Creating parsed file')

def writeExcel_vd(a,b,ab,file1,file2,outfile):
	try:
		f1_name = getName(file1)
		f2_name = getName(file2)

		workbook = xlsxwriter.Workbook(outfile+".xlsx")
		sheet = workbook.add_worksheet("Genes")
		genes = [a,b,ab]

		for i in range(0,3):
			#GENES ONLY IN FILE 1
			if (i == 0):
				sheet.write(0,i,f1_name)
			#GENES ONLY IN FILE 2
			elif (i == 1):
				sheet.write(0,i,f2_name)
			#GENES IN BOTH FILES
			else:
				sheet.write(0,i,"both "+f1_name+" and "+f2_name)
			for j in range(0,len(genes[i])):
				sheet.write(j+1,i,genes[i][j])
		workbook.close()
		return(True)
	except:
                return(False)

def writeExcel_bp(terms,tt,outfile):
	try:
		workbook = xlsxwriter.Workbook(outfile+"_bp.xlsx")
		sheet = workbook.add_worksheet('BarPlot '+tt)
		
		sheet.write(0,0,'GO term description')
		sheet.write(0,1,'count')
		for i in range(0,len(terms)):
			sheet.write(i+1,0,terms[i][0])
			sheet.write(i+1,1,terms[i][1])
		workbook.close()
		return (True)
	except:
		return (False)
		

def writeExcel_values(file1,file2,gene_values,options,outfile):
	try:
		f1_name = getName(file1)
		f2_name = getName(file2)
		name_out = getName(outfile)

		workbook = xlsxwriter.Workbook(outfile+".xlsx")

		# Create a format to use in the merged range.
		merge_format = workbook.add_format(merge_form)

		sheet = workbook.add_worksheet("common genes")
		sheet.write(1,0,"gene")
		i = 1
		for opt in options:
			#File 1
			sheet.write(0,i,f1_name)
			sheet.write(1,i,opt)
			#File 2
			sheet.write(0,i+1,f2_name)
			sheet.write(1,i+1,opt)
			i += 2

		i = 2
		for data in gene_values:
			for j in range(len(data)):
				sheet.write(i,j,data[j])
			i += 1
		workbook.close()
		return(True)
	except:
		return(False)

def writeExcel_expLevel(genes,comparison,infile1,infile2,file_out,head1,head2,f1,f2,nf1,nf2):
	try:
		f1_name = getName(infile1)
		f2_name = getName(infile2)
		workbook = xlsxwriter.Workbook(file_out+'.xlsx')
		
		# Create a format to use in the merged range.
		merge_format = workbook.add_format(merge_form)
		
		for s in range(len(genes)):
			sheet = workbook.add_worksheet(comparison[s])
			sheet.merge_range('B1:J1', f1_name, merge_format)
			sheet.merge_range('L1:T1', f2_name, merge_format)

			# Write headers
			for i in range(len(head1)):
				sheet.write(1,i,head1[i])
			start = len(head1)+1
			for i in range(len(head2)):
				sheet.write(1,start,head2[i])
				start += 1

			# Write data
			i = 2
			for data in genes[s]:
				#Data first file
				for j in range(0,10):
					sheet.write(i,j,data[j])
				#Data second file
				for j in range(10,len(data)):
					sheet.write(i,j+1,data[j])
				i += 1

			sheet = workbook.add_worksheet(comparison[s]+'_comparison')
                        

			sheet.merge_range('B1:C1', f1_name, merge_format)      
			sheet.merge_range('D1:E1', f2_name, merge_format)

			sheet.write(1,0,"gene")
			sheet.write(1,1,"fold")
			sheet.write(1,2,"-1/fold")

			sheet.write(1,3,"fold")
			sheet.write(1,4,"-1/fold")
			
			i = 2
			for data in genes[s]:
				sheet.write(i,0,data[0])
				sheet.write(i,1,data[f1])
				sheet.write(i,2,data[nf1])
				sheet.write(i,3,data[f2])
				sheet.write(i,4,data[nf2])
				i += 1
                
		workbook.close()
		return(True)
	except:
		return(False)

# Get header Excel file (per sheet name)
def headerExcel(infile,sheet):
	try:
		f = xlrd.open_workbook(infile)
		s4 = f.sheet_by_name(sheet)
		head = s4.row_values(0)	
		return (head)
	except:
		#return(False)
		return('Error: Reading Excel file '+getName(infile))

# Read Excel file (per sheet name) to return list of genes
def readExcel(infile,sheet):
	try:
		f = xlrd.open_workbook(infile)
		s4 = f.sheet_by_name(sheet)

		genes = []
		for i in range(1,s4.nrows):
			genes.append(s4.row_values(i))
		return (genes)
	except:
		return('Error: Reading Excel file '+getName(infile))

def openExcel(infile):
	try:
		f = xlrd.open_workbook(infile)
		return (f)
	except:
		return('Error: Reading Excel file '+getName(infile))

def extractData(infile,sheet):
	try:
		s4 = infile.sheet_by_name(sheet)
		data = []
		for i in range(1,s4.nrows):
			data.append(s4.row_values(i))
		return (data)
	except:
		return('Error: Reading extracting data from file '+getName(infile))

def readValues(genes,infile,sheet,stat):
	try:
		f = xlrd.open_workbook(infile)
		s4 = f.sheet_by_name(sheet)

		values = {}
		for i in range(1,s4.nrows):
			temp = s4.row_values(i)
			if temp[0] in genes:
				values[temp[0]] = temp[stat:]
		return (values)
	except:
		return(False)


