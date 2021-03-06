"""
@Names: Cj Buresch and Nathan Fischer
@Date: 9/15/2014
@ Homework #2 -- Data Visualization
@Description: 
	
@Version: Python v2.7
"""

import csv
import matplotlib
matplotlib.use('pdf')
import matplotlib.pyplot as pyplot
import numpy
import math

def create_freq_diagram(attributes,table,exelist):
	"""Create a Frequency diagram for each catagorical attribute in the prepared dataset"""
	for att in exelist:
		xs, ys = get_frequencies(get_all_col_values(table,att))
		graph_freq_diagram(attributes[att],xs,ys,1)

def graph_freq_diagram(title,values,counts,step):
	"""Creates a Frequency diagram, saves the pdf using the entered step number"""
	pyplot.figure()
	pyplot.title(title + " Frequency Diagram")
	xrng = numpy.arange(len(values))
	yrng = numpy.arange(0,max(counts)+ 50,20)
	pyplot.bar(xrng,counts,.45,align ='center')
	pyplot.xticks(xrng,values)
	pyplot.yticks(yrng)
	pyplot.xlabel(title)
	pyplot.ylabel("Count")
	pyplot.grid(True)
	pyplot.savefig("step-"+str(step)+"-"+ title + '.pdf')
	pyplot.clf()

def create_cont_to_cat_graphs(table):
	"""Runs the two different approaches for the step, and creates the related graphs"""
	run_approach_one(table)
	run_approach_two(table)

def run_approach_one(table):
	"""Creates a frequencey diagram of calculated mpg ratings in the dataset."""
	mpg_values = get_all_col_values(table,1)
	ratinglist = get_list_of_mpg_ratings(mpg_values)
	xs, ys = get_frequencies(ratinglist)
	graph_freq_diagram("Car MPG Rating",xs,ys,4)

def run_approach_two(table):
	"""Creates a frequencey diagram of five equal bins of MPG from the dataset"""
	mpg_values = get_all_col_values(table,1)
	#List of cutoff values for the bins
	cuttoffs = equal_width_cutoffs(mpg_values,4)
	#List of values for each bin
	bin_freq = frequencies_for_cutoffs(mpg_values,cuttoffs)
	#seperate into the bins
	xs, bin_freq = get_frequencies(bin_freq)
	#create labels
	xs = populate_range_label_list(cuttoffs)
	graph_freq_diagram("Car MPG by Range",xs,bin_freq,4)

def get_list_of_mpg_ratings(xs):
	"""From a list of MPG values, return a list of ratings"""
	result = []
	for x in xs:
		if x >= 45:
			result.append(10)
		elif x >= 37:
			result.append(9)
		elif x >= 31:
			result.append(8)
		elif x >= 27:
			result.append(7)
		elif x >= 24:
			result.append(6)
		elif x >= 20:
			result.append(5)
		elif x >= 17:
			result.append(4)
		elif x >= 15:
			result.append(3)
		elif x == 14:
			result.append(2)
		elif x <= 13:
			result.append(1)
	return result

def populate_range_label_list(xs):
	"""Generates labels from a list of labels for the bins of a frequency diagram"""
	result = []
	#First label
	result.append("<" + str(xs[0]))
	for i in range(0,len(xs)-1):
		#append the range of each bin that isnt first or last
		result.append(str(xs[i] + 1) + "--" + str(xs[i+1]))
		#append last label
	result.append(">" + str(xs[len(xs)-1]))
	return result
# Create and save graphs for each attribute in attlist
def create_pie_charts(filein, attlist = ['Model Year', 'Cylinders', 'Origin']):
	for attribute in attlist:
		graph_pie_chart(filein, attribute, 'step-2-pie-'+ attribute +'.pdf', title = attribute + ' Pie Chart')

# Graph data for attribute from file_in
def graph_pie_chart(file_in, attribute, file_out, title = None):
	labels = []
	data = []
	with open(file_in, 'r') as f:
		reader = csv.DictReader(f)
		for inst in reader:
			if str(inst[attribute]) in labels:
				data[labels.index(str(inst[attribute]))] += 1
			else:
				labels.append(str(inst[attribute]))
				data.append(1)
	# if title is not defined, use attribute name as title
	if title == None:
		title = attribute
	pyplot.title(title)
	pyplot.pie(data, labels = labels, autopct='%1.1f%%', colors=('b', 'g', 'r', 'c', 'm', 'y', 'w'))
	pyplot.savefig(file_out)
	pyplot.clf()

def create_scatter_plot(attributes,table,exelist):
	"""Creates a scatterplot for each attribute in the execution list"""
	for x in exelist:
		graph_scatter_plot(attributes[x],table,x)

def graph_scatter_plot(attribute,table,index):
	"""Creates a scatterplotusing MPG information against a chosen attribute"""
	pyplot.figure()
	pyplot.title(attribute + " vs MPG Scatter Plot")
	xs , ys = get_points_from_table(table,index,1)
	pyplot.plot(xs, ys, 'b.')
	pyplot.xlim(0, int(max(xs) * 1.10))
	pyplot.ylim(0, int(max(ys) * 1.10))
	pyplot.xlabel(attribute)
	pyplot.ylabel("MPG")
	pyplot.grid(True)
	pyplot.savefig('step-6-' +attribute + '.pdf')
	pyplot.clf()

def get_points_from_table(table,xindex,yindex):
	"""Grabs points of data from the table and returns them as two lists"""
	xresult = []
	yresult = []
	for row in table:
		if (row[xindex] != 'NA') and (row[yindex] != 'NA'):
			xresult.append(float(row[xindex]))
			yresult.append(float(row[yindex]))
	return xresult,yresult

# Create and save graphs for each attribute in attlist
def create_dot_plots(file_in, attlist = ['MPG', 'Displacement', 'Horsepower', 'Weight', 'Acceleration', 'MSRP']):
	for attribute in attlist:
		graph_dot_plot(file_in, attribute,  title = attribute + ' Dot Plot')
		save_fig('step-3-dot-'+ attribute +'.pdf')

# Graph data for attribute from file_in
def graph_dot_plot(file_in, attribute, title = None):
	pyplot.clf()
	pyplot.gca().get_yaxis().set_visible(False)
	with open(file_in, 'r') as f:
		reader = csv.DictReader(f)
		for inst in reader:
			pyplot.plot(float(inst[attribute]), 1, 'k.', alpha=.05, markersize=15)
	# if title is not defined, use attribute name as title
	if title == None:
		title = attribute
	pyplot.title(title)
	pyplot.xlabel(attribute)
	
# Create and save graphs for each attribute in attlist
def create_histograms(file_in, attlist = ['MPG', 'Displacement', 'Horsepower', 'Weight', 'Acceleration', 'MSRP']):
	for attribute in attlist:
		graph_histogram(file_in, attribute,  title = attribute + ' Histogram')
		save_fig('step-5-histo-'+ attribute +'.pdf')

# Graph data for attribute from file_in
def graph_histogram(file_in, attribute, title = None):
	pyplot.clf()
	# if title is not defined, use attribute name as title
	if title == None:
		title = attribute
	xs = []
	with open(file_in, 'r') as f:
		reader = csv.DictReader(f)
		for inst in reader:
			xs.append(float(inst[attribute]))
	pyplot.title(title)
	pyplot.xlabel(attribute)
	pyplot.ylabel('Instances')
	pyplot.hist(xs)

# Save the current pyplot figure and clear the figure so a new one can be created
def save_fig(file_out):
	pyplot.savefig(file_out)
	pyplot.clf()

def calculate_best_fit_line(xs, ys):
	if len(xs) != len(ys):
		return None
	_x = numpy.mean(xs)
	_y = numpy.mean(ys)
	num = 0
	denom = 0
	for x_point, y_point in zip(xs, ys):
		num += (x_point-_x)*(y_point-_y)
		denom += math.pow(x_point-_x, 2)
	m = num/denom
	return (_x, _y, m)

# Returns the correlation coefficient for dataset (xs[i], ys[i]) and slope m
def calculate_correlation_coefficient(xs, ys, m):
	return m * numpy.std(xs) / numpy.std(ys)

# Return the covariance for points in xs and slope m
# Passing stdev_x (the standard deviation of xs) will make this function return faster
def calculate_covariance(m, xs, stdev_x = None):
	#return m * math.pow(numpy.std(xs), 2)
	return m * math.pow(stdev_x if stdev_x!=None else numpy.std(xs), 2) * 1.0

def graph_line(x, y, m, min_x, max_x):
	min_x = int(min_x)
	max_x = int(max_x)
	xs = [x1 for x1 in range(min_x, max_x)]
	ys = [-1*m*(x-x1)+y for x1 in range(min_x, max_x)]
	pyplot.plot(xs, ys)

# Create and save graphs for x_attribs[i] vs y_attribs[i]
def create_linear_regressions_with_scatters(file_in, x_attribs = ['Displacement', 'Horsepower', 'Weight', 'MSRP', 'Displacement'], y_attribs = ['MPG']*4+['Weight']):
	for x_attrib, y_attrib in zip(x_attribs, y_attribs):
		graph_scatter_plot_with_regression(file_in, x_attrib, y_attrib)
		save_fig('step-7-'+ x_attrib +'-vs-'+ y_attrib +'.pdf')

# Graph data for x_attrib vs y_attrib from file_in
def graph_scatter_plot_with_regression(file_in, x_attrib, y_attrib, title = None):
	pyplot.clf()
	xs = []
	ys = []
	with open(file_in, 'r') as f:
		reader = csv.DictReader(f)
		for inst in reader:
			xs.append(float(inst[x_attrib]))
			ys.append(float(inst[y_attrib]))
	pyplot.plot(xs, ys, '.')
	ys = sorted(ys)
	xs = sorted(xs)
	x, y, m = calculate_best_fit_line(xs, ys)
	graph_line(x, y, m, xs[0], xs[-1])
	b = dict(facecolor='none', color='r')
	s = 'r=' + str(calculate_correlation_coefficient(xs, ys, m))[0:8] + ' cov=' + str(calculate_covariance(m, xs))[0:8]
	pyplot.text(xs[0], ys[0], s, bbox=b, fontsize=10, color='r')
	pyplot.title(title if title!=None else str(x_attrib) + ' vs ' + str(y_attrib))
	pyplot.xlabel(x_attrib)
	pyplot.ylabel(y_attrib)
	

def run_step_8(attributes,table):
	"""Create two graphs, a boxplot and a multi-frequency diagram for step8"""
	create_box_plot(table)
	create_multi_freq_diagram(table)

def create_multi_freq_diagram(table):
	"""Creates a multiple frequency diagram for the origin of a car, for every year"""
	pyplot.figure()
	fig, ax = pyplot.subplots()
	years_list = get_all_model_years(table)
	grouped_by_year_list = group_By(table,2,8)
	list_of_freqs_by_year = []

	for xs in grouped_by_year_list:
		values , counts = get_frequencies(xs)
		list_of_freqs_by_year.append((values,counts))

	count_max = 0
	bar_width = 0.3
	locations = range(1,11)

	plot_counts = get_counts_for_origin_by_year(list_of_freqs_by_year,0)
	count_max = check_max(plot_counts,count_max)
	r1 = ax.bar(locations, plot_counts, bar_width, color='b')
	
	locations = increment_values_list(locations,bar_width)
	plot_counts = get_counts_for_origin_by_year(list_of_freqs_by_year,1)
	count_max = check_max(plot_counts,count_max)
	r2 = ax.bar(locations, plot_counts, bar_width, color='r')
	
	locations = increment_values_list(locations,bar_width)
	plot_counts = get_counts_for_origin_by_year(list_of_freqs_by_year,2)
	count_max = check_max(plot_counts,count_max)
	r3 = ax.bar(locations, plot_counts, bar_width, color='y')
	
	xrng = numpy.arange(1.5,len(list_of_freqs_by_year)+1)
	yrng = numpy.arange(0,count_max+ 25,5)
	ax.legend((r1[0], r2[0],r3[0]), ('USA', 'Europe','Japan'), loc=2)

	pyplot.xticks(xrng,years_list)
	pyplot.yticks(yrng)
	pyplot.xlabel("Model Year")
	pyplot.ylabel("Count")
	pyplot.title("Total Number of Cars by Year and Country of Origin")
	pyplot.grid(True)
	pyplot.savefig('step-8-Multiple-Freq.pdf')
	pyplot.clf()

def get_counts_for_origin_by_year(xs,index):
	"""gets the frequency count from a given list by year"""
	result = []
	for x in xs:
		values = x[0]
		counts = x[1]
		result.append(counts[index])
	return result

def increment_values_list(xs,inc):
	"""increment all values in a list by a specified increment value"""
	result = []
	for x in xs:
		result.append(x + inc)
	return result

def check_max(xs,cmax):
	"""compares the current max to the max in a list to find the new max"""
	if max(xs) > cmax:
		return max(xs)
	else:
		return cmax                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    

def create_box_plot(table):
	pyplot.figure()
	pyplot.title("MPG by Model Year")
	xs = group_By(table,2,1)
	pyplot.boxplot(xs)
	labels = get_all_model_years(table)
	pyplot.xticks(range(1,len(labels) + 1),labels)
	pyplot.xlabel("Model Year")
	pyplot.ylabel("MPG")
	pyplot.savefig('step-8-BoxPlot.pdf')
	pyplot.clf()

def get_all_col_values(table,index):
	""" Gets all attribute values from a table"""
	result = []
	for row in table:
		if row[index] != "NA":
			result.append(int(float(row[index])))
	return result

def get_all_model_years(table):
	"""Returns a list of all the model years of instances in a Dataset"""
	result = []
	for row in table:
		if row[2] != "NA":
				if int(float(row[2])) not in result:
					result.append(int(float(row[2])))
	result.sort()
	return result

def get_frequencies(xs):
	"""Returns a list of values and counts for those values in a list"""
	ys = sorted(xs)
	values, counts = [], []
	for y in ys:
		if y not in values:
			values.append(y)
			counts.append(1)
		else:
			counts[-1] += 1
	return values, counts

def group_By(table,index,infoindex):
	"""Returns a list of lists of values that have been grouped by a specific attribute value"""
	group_vals = []
	for row in table:
		value = int(float(row[index]))
		if value not in group_vals:
			group_vals.append(value)
	group_vals.sort()

	result = [[] for _ in range(len(group_vals))]
	for row in table:
		result[group_vals.index(int(float(row[index])))].append(int(float(row[infoindex])))
	return result

def frequencies_for_cutoffs(values, cutoff_points):
	""" Finds the count of values that fall in the cutoffs and returns a list"""
	new_values = []
	for v in values:
		found = False
		for i in range(len(cutoff_points)):
			if not found and v <= cutoff_points[i]:
				new_values.append(i + 1)
				found = True
		if not found:
			new_values.append(len(cutoff_points) + 1)
	return new_values

def equal_width_cutoffs(values, num_of_bins):
	"""Returns a list of cutoff values to create a number of equal bins"""
	width = int(max(values) - min(values)) / num_of_bins
	return list(range(min(values) + width, max(values), width))

def get_table_from_CSV(filename):
	"""Returns a table of strings from a CSV file"""
	table =[]
	atts = []
	with open(filename, 'rb') as _in:
		f1 = csv.reader(_in)
		atts = f1.next()
		for row in f1:
			if len(row) > 0:
				table.append(row)
	return atts, table

def main():
	#Relevant attributes to graph
	catagorical_att_list = [2,3,8]
	inputdata = "auto-data-cleaned.txt"
	#Get list of attributes, and the table from the input data
	attributes,datatable = get_table_from_CSV(inputdata)
	#step 1 - 8 (in order)
	create_freq_diagram(attributes,datatable,catagorical_att_list)
	create_pie_charts(inputdata)
	create_dot_plots(inputdata)
	create_cont_to_cat_graphs(datatable)
	create_histograms(inputdata)
	create_scatter_plot(attributes,datatable,[0,4,5,7,9])
	create_linear_regressions_with_scatters(inputdata)
	run_step_8(attributes,datatable)

main()
