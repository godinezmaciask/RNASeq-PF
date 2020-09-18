## Barplot generator
## Karla Godinez, Jon Mohl


import sys
import GOFunctions as go
from matplotlib import pyplot as plt

# Create and save figure
def plot_fig(outfile,terms,vals,t):
	# Need to invert lists because plot index position
	pos = list(range(len(terms),0,-1))
	plt.figure()

	# Plot term description
	plt.subplot(121)
	plt.title("Gene ontology "+t)
	plt.axis([0, len(vals), 0, len(terms)+1])
	plt.axis('off')
	# Plot values
	plt.subplot(122)
	plt.barh(pos, vals, alpha=0.5)
	plt.title("Number of Genes Involved")
	plt.yticks(ticks=pos, labels=terms)

	plt.savefig(outfile+'.png')
	plt.close()

# Format barplot data
def barPlot(outfile,dat,term,n):
	ont={'bp':'biological process','cc':'cellular compound','mf':'molecular function'}
	terms_f1 = go.getTermByType(dat,term)

	# Sort terms by number genes associated
	terms_f1.sort(reverse=True, key=lambda x: x[3])
	
	terms = []
	count = []
	f = open(outfile+'.txt','w')
	for t in terms_f1:
		if (t[6] != 'yes') and (len(terms) <= n):
			terms.append(t[2])
			count.append(t[3])
		f.write(t[0] + '\t' + t[2] + '\t' + str(t[3]) + '\n')
	f.close()
	plot_fig(outfile,terms,count,ont[term])




