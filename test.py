import os
import sys
from scipy import stats
import math
import numpy as np

ran = sys.argv[1]

def calculate_run(data):
	dataLength = len(data)
	# numberofRuns = 6648
	numberofRuns = 0
	# logic
	flag = (data[0] < data[1])
	for i in xrange(1, dataLength):
		if (data[i-1] < data[i] and not flag) or (data[i-1] > data[i] and flag):
			numberofRuns = numberofRuns + 1
			flag = not flag
	return numberofRuns

def runsUpandrunsDown(data, numberofRuns):
	dataLength = len(data)
	mu = (dataLength*2 - 1)/3.0
	sigmaSquare = (dataLength*16 - 29)/90.0
	sigma = math.sqrt(sigmaSquare)
	normalStatistic = 1.0*(numberofRuns - mu)/sigma
	# print "mu is ", mu, " sigmaSquare is ", sigmaSquare, " normalStatistic is " , normalStatistic
	return normalStatistic

def runsAboveandrunsBelow(data, numberofRuns):
	dataLength = len(data)
	dataMean = np.mean(data)
	countAboveMean = 0
	for x in data:
		if x >= dataMean:
			countAboveMean = countAboveMean + 1
	countBelowMean = dataLength - countAboveMean
	temp = countAboveMean * countBelowMean * 2
	mu = 1.0*(temp)/dataLength + 0.5	
	sigmaSquare = 1.0*(temp)*(temp - dataLength)/((dataLength**2)*(dataLength-1))
	sigma = math.sqrt(sigmaSquare)
	normalStatistic = 1.0*(numberofRuns - mu)/sigma
	# print "mu is ", mu, " sigmaSquare is ", sigmaSquare, " normalStatistic is " , normalStatistic
	return normalStatistic



def length_of_runs(data):
	# return associative array 1=>obsVal(1), 2=>...
	dataLength = len(data)
	# numberofRuns = 6648
	runsLengthArray = {1:1}
	numberofRuns = 1
	runLength = 0
	# logic
	flag = (data[0] < data[1])
	for i in xrange(1, dataLength):
		if data[i-1] < data[i]:
			if flag: 
				runLength = runLength + 1
			else:
				numberofRuns = numberofRuns + 1
				if runLength in runsLengthArray:
					runsLengthArray[runLength] += 1
				else:
					runsLengthArray[runLength] = 1
				runLength = 1
				flag = not flag

		if data[i-1] > data[i]:
			if not flag:
				runLength = runLength + 1
			if flag:
				numberofRuns = numberofRuns + 1
				if runLength in runsLengthArray:
					runsLengthArray[runLength] += 1
				else:
					runsLengthArray[runLength] = 1
				runLength = 1
				flag = not flag
	return numberofRuns, runsLengthArray

def runstestLengthofruns(data, runsLengthArray):
	dataLength = len(data)
	# RURD 
	expectedRunLengthRURD = {}
	for i, value in runsLengthArray.iteritems():
		if i <= dataLength - 2:
			temp = 2.0 *(dataLength*( i**2 + 3*i + 1 ) - (i**3 + 3*(i**2) - i - 4))/math.factorial(i+3)
		elif i == dataLength - 1:
			temp = 2.0/math.factorial(dataLength)
		expectedRunLengthRURD[i] = temp

	# RABM
	dataMean = np.mean(data)
	countAboveMean = 0
	for x in data:
		if x >= dataMean:
			countAboveMean = countAboveMean + 1
	countBelowMean = dataLength - countAboveMean
	expectedRunLengthRABM = {}
	temp2 = 1.0*countBelowMean/countAboveMean + 1.0*countAboveMean/countBelowMean
	# print "temp 2 is ", temp2
	for i, value in runsLengthArray.iteritems():
		temp = ((1.0*countAboveMean/dataLength)**i)*(1.0*countBelowMean/dataLength) + ((1.0*countBelowMean/dataLength)**i)*(1.0*countAboveMean/dataLength)
		temp3 = 1.0 * dataLength * temp/temp2
		# print "i is", i, "  and temp is ", temp
		expectedRunLengthRABM[i] = temp3

	expectedTotalRuns = dataLength/temp2

	# print expectedRunLengthRURD

	chisquareRABM = 0.0
	for i, value in runsLengthArray.iteritems():
		temp = 1.0*((value - expectedRunLengthRABM[i])**2)/expectedRunLengthRABM[i]
		chisquareRABM = chisquareRABM + temp


	lastKey = runsLengthArray.keys()[-1]
	
	chisquareRURD = 0.0
	for i, value in runsLengthArray.iteritems():
		if i == lastKey:
			break
		temp = 1.0*((value - expectedRunLengthRURD[i])**2)/expectedRunLengthRURD[i]
		# print "value is ", value, " expected run length rurd ", expectedRunLengthRURD[i], " temp  is ", temp
		chisquareRURD = chisquareRURD + temp
		# print chisquareRURD


	return chisquareRURD, chisquareRABM


def pokers_test(data):
	dataLength = len(data)
	# convert to first 3 digits
	# frequency in diff cases
	observedFreq = [0,0,0]
	expectedFreq = [0.72, 0.01, 0.27]
	# 1: all same
	# 2: all diff
	# 3: atleast one same
	for x in data:
		x = str(x).split('.')[1]
		x = x[0:3]
		temp = check_identicals(x)
		observedFreq[temp] += 1
	# print observedFreq

	chisquare = 0.0
	for i in xrange(0,3):
		observedFreq[i] = 1.0*observedFreq[i]/dataLength
		chisquare += ((observedFreq[i] - expectedFreq[i])**2)/expectedFreq[i]

	return chisquare
	# calculate chi-square


def check_identicals(num):

	if num[0] == num[1] == num[2]:
		return 0
	elif (num[0] is not num[1]) and (num[1] is not num[2]) and (num[0] is not num[2]):
		return 1
	else:
		return 2


def auto_correlation_test(data, interval):
	dataLength = len(data)
	# calculate 
	estimatorDistribution = 0.0
	temp = 0.0
	M = dataLength/interval - 1
	for i in xrange(0,M):
		temp += data[interval*i]*data[interval*(i+1)]
	estimatorDistribution /= (M+1)
	estimatorDistribution -= 0.25
	
	estimatorSD = 1.0*((13*interval + 7)**(0.5))/12*(interval+1)
	testStatistic = estimatorDistribution/estimatorSD
	return testStatistic



text_file = open(ran)
data = text_file.read().split('\n')
del data[-1]
data = [float(x) for x in data]
#print data
#data = [x for x in data]


# data = [0.30, 0.48, 0.36, 0.01, 0.54, 0.34, 0.96, 0.06, 0.61, 0.85, 0.48, 0.86, 0.14, 0.86, 0.89, 0.37, 0.49, 0.60, 0.04, 0.83, 0.42, 0.83, 0.37, 0.21, 0.90, 0.89, 0.91, 0.79, 0.57, 0.99, 0.95, 0.27, 0.41, 0.81, 0.96, 0.31, 0.09, 0.06, 0.23, 0.77, 0.73, 0.47, 0.13, 0.55, 0.11, 0.75, 0.36, 0.25, 0.23, 0.72, 0.60, 0.84, 0.70, 0.3, 0.26, 0.38, 0.05, 0.19, 0.73, 0.44]
# data = [0.41, 0.68, 0.89, 0.94, 0.74, 0.91, 0.55, 0.62, 0.36, 0.27, 0.19, 0.72, 0.75, 0.08, 0.54, 0.02, 0.01, 0.36, 0.16, 0.28, 0.18, 0.01, 0.95, 0.69, 0.18, 0.47, 0.23, 0.32, 0.82, 0.53, 0.31, 0.42, 0.73, 0.04, 0.83, 0.45, 0.13, 0.57, 0.63, 0.29]
print "Displaying first 10 data items:"
print data[1:10]
print "Length of Data: ", len(data)



print
print  "Chi-Square testing:", stats.chisquare(data)
print
print "KS-test:" , stats.kstest(data, 'uniform') 

# print calculate_run(data)
numberofRuns, runsLengthArray = length_of_runs(data) 
print
print "Number of Runs:", numberofRuns
print "Runs Length frequency:", runsLengthArray
print
print "Runs up and runs down test: Z value", runsUpandrunsDown(data, numberofRuns)

print 
print "Runs above and runs below test: Z value", runsAboveandrunsBelow(data, numberofRuns)

print
print "Runs test: Length of Runs" 
chisquareRURD, chisquareRABM = runstestLengthofruns(data, runsLengthArray)
print "ChiSquare RURD is", chisquareRURD
print "ChiSquare RABM is", chisquareRABM


print 
print "Poker's Test: Chi-square", pokers_test(data)

print 
print "Autocorrelation Test: ", auto_correlation_test(data, 400)

