import sys	#for accessing the command-line arguments
import csv	#for handling comma-separated-value file (especially in order to handle escaped comma)

#name : readInputFileAndCreateMap
#parameter : 
#            name : path
#            type : string
#open the input file with the given path
#read line by line and update a map each time
#return the complete map
def readInputFileAndCreateMap(path):
	inputFile = open(path, 'r')
	
	try:
		reader = csv.reader(inputFile, delimiter = ',')
		
		#name : mp
		#type : dictionary (map)
		#       key   : drug_name
		#       value : list
		#               index 0 : drug_name
		#               index 1 : set of tuples
		#                         index 0 : prescriber_last_name
		#                         index 1 : prescriber_first_name
		#               index 2 : total_cost (cumulative)
		mp = dict()
		
		reader.next()	#hard-coded in order to discard header row of the data
		
		#read a line and process immediately (update map) in order to be able to handle a huge dataset
		for line in reader:
			key = line[3]					#hard-coded column index (4th column is drug_name)
			if key in mp:
				#update map
				#add new item to the set (and automatically update the set)
				mp[key][1].add((line[1], line[2]))	#hard-coded column index (2nd and 3rd columns are last_name and first_name)
				#increment total_cost. I used "eval()" to convert into corresponding type of int or float
				mp[key][2] += eval(line[4])		#hard-coded column index (5th column is drug_cost)
			else:
				#create a new entry and insert into map
				mp[key] = [key, set([(line[1], line[2])]), eval(line[4])]
		
		inputFile.close()
	
	except Exception:	#makes sure to close the input file even if error has occurred
		inputFile.close()
		raise
	return mp

#name : processMap
#parameter : 
#            name : mp
#            type : dictionary (map)
#given a map, process it to obtain desired data, which is the number of unique prescribers
#return the processed data as a list of lists
def processMap(mp):
	
	#name : stats
	#type : list of lists
	#inner list :
	#             index 0 : drug_name
	#             index 1 : # of unique prescribers
	#             index 2 : total_cost
	stats = []
	
	#iterate each entry in map, process, and append into the list
	for key in mp:
		value = mp[key]
		stats.append([value[0], len(value[1]), value[2]])
	
	return stats

#name : writeOutputFile
#parameter : 
#            name : path
#            type : string
#            name : contents
#            type : list of lists
#open an output file with the given path
#write the contents line by line into the file
def writeOutputFile(path, contents):
	outputFile = open(outputFilePath, 'w')
	
	try:
		writer = csv.writer(outputFile, delimiter = ',')
		
		#write line by line into the file
		for line in contents:
			writer.writerow(map(str, line))	#convert each element in the list into string to avoid any unexpected writing problem
		
		outputFile.close()
	
	except Exception:	#makes sure to close the output file even if error has occurred
		outputFile.close()
		raise

#Main function
#get file paths for input and output files
inputFilePath = sys.argv[1]
outputFilePath = sys.argv[2]

#hard-coded headers to be used for output file
outputHeaders = ["drug_name", "num_prescriber", "total_cost"]

#read the input file, process, and return the processed data as a map
mp = readInputFileAndCreateMap(inputFilePath)

#refine the data even more to get the desired data as a list of lists
stats = processMap(mp)

#sort the list into the order of writing
#this sorting is stable, which means that it will keep the original order if there is a tie
#the original order is by drug_name. So it will be sorted by total_cost then by drug_name if there is a tie
outputData = sorted(stats, key = lambda entry: entry[2], reverse = True)

#write the data in comma-separated-value format
writeOutputFile(outputFilePath, [outputHeaders] + outputData)
