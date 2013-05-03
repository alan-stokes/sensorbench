#!/usr/bin/python

import re, getopt, logging, sys, os, string, UtilLib, CSVLib, AvroraLib, networkLib, shutil
import SneeqlLib
import parseAcquireDeliverTimes, equivRuns #TODO: Move these to where they are needed

optLabel = ""
optOutputDir = os.getenv('HOME')+os.sep+"tmp"+os.sep+"sensebench"+os.sep
tempSneeFilesDir = optOutputDir + "tempSNEEFiles" #Move to SNEElib
avroraJobDir = optOutputDir + "avroraJobs" #Move to SNEELib

#Default list of platforms to run experiments over
#optPlatList = ["MHOSC", "INSNEE"]
optPlatList = ["INSNEE"]

#Default list of experiments to be run
#optExprList = ['0a', '0b', '0c', '0d', '0e']
#optExprList = ['alphaCalib2']
#optExprList = ["1a", "1b", "2a", "2b", "3a", "3b", "4a", "4b", "5a", "5b", "6a", "6b", "7"]
optExprList = ["1a"]

#optNumInstances = 10
optNumInstances = 2

#Flag to determine whether Avrora jobs will be executed via Condor parallel execution system
optUseCondor = True

def parseArgs(args):	
	global optOutputDir, optPlatList, optExprList, optNumInstances, optUseCondor
	try:
		optNames = ["outputdir=", "plat=", "exp=", "num-instances=", "use-condor="]
	
		#append the result of getOpNames to all the libraries 
		optNames = UtilLib.removeDuplicates(optNames)
		
		opts, args = getopt.getopt(args, "h",optNames)
	except getopt.GetoptError, err:
		print str(err)
		usage()
		sys.exit(2)
			
	for o, a in opts:
		if (o == "--plat"):
			optPlatList = a.split(',')
		if (o == "--exp"):
			optExprList = a.split(',')
		if (o == "--num-instances"):
			optNumInstances = int(a)	
		if (o == "--use-condor"):
			optExprList = bool(a)
		else:
			usage()
			sys.exit(2)


#Ouput info message to screen and logger if applicable
def report(message):
 	if (logger != None):
 		logger.info (message)
 	print message


#Ouput warning message to screen and logger if applicable
def reportWarning(message):
 	if (logger != None):
 		logger.warning(message)
 	print message


#Ouput error message to screen and logger if applicable
def reportError(message):
 	if (logger != None):
 		logger.error(message)
 	print message

def startLogger(timeStamp):
	global logger

	logger = logging.getLogger('test')

	#create the directory if required
	#if not os.path.isdir(optOutputDir):
	#		os.makedirs(optOutputDir)
			
	hdlr = logging.FileHandler('%s/%s-%s.log' % (optOutputDir, optLabel, timeStamp))
	formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
	hdlr.setFormatter(formatter)	
	logger.addHandler(hdlr) 
	logger.setLevel(logging.INFO)
	logger.info('Starting Regression Test')


#this is after condor/avrora
def logResultsToFile(runAttr, runAttrCols, resultsFileName):
	if not os.path.exists(resultsFileName):
		resultsFile = open(resultsFileName, "w")
		resultsFile.writelines(CSVLib.header(runAttrCols))
	
	resultsFile = open(resultsFileName, "a")
	resultsFile.writelines(CSVLib.line(runAttr, runAttrCols))
	resultsFile.close()

#this is after condor/avrora
def logResultsToFiles(runAttr, runAttrCols, outputDir):
	#Per-experiment/plaftform results file
	resultsFileName = outputDir+os.sep+"exp"+runAttr["Experiment"]+"-"+runAttr["Platform"]+"-results.csv"
	logResultsToFile(runAttr, runAttrCols, resultsFileName)
	#All experiments results file
	resultsFileName = outputDir+os.sep+"all-results.csv"
	logResultsToFile(runAttr, runAttrCols, resultsFileName)

def getRunDir(runAttr, task):
	return "exp"+runAttr["Experiment"]+"-"+runAttr["Platform"]+"-x"+runAttr["xvalLabel"]+"-"+task+"-i"+runAttr["Instance"]

def obtainNetworkTopologyAttributes(runAttr):
	physicalSchemaName = runAttr['PhysicalSchema']

        #get the network attributes from topology file name
	m = re.search("n(\d+)_(linear|grid|random)_d(\d+)_s(\d+)", physicalSchemaName)
	if (m != None):
		runAttr['NetworkSize'] = int(m.group(1))
		runAttr['Layout'] = m.group(2)
		runAttr['NetworkDensity'] = int(m.group(3))
		runAttr['NetworkPercentSources'] = int(m.group(4))
		runAttr['PhysicalSchemaFilename'] = networkLib.getPhysicalSchemaFilename("",runAttr['NetworkSize'],runAttr['Layout'],runAttr['NetworkDensity'],runAttr['NetworkPercentSources'],runAttr['Instance'])
		(runAttr['SNEETopologyFilename'],runAttr['AvroraTopologyFilename']) = networkLib.getTopologyFilenames("", runAttr['NetworkSize'],runAttr['Layout'],runAttr['NetworkDensity'],runAttr['Instance'])
	else:
		print "ERROR: physical schema filename %s does not conform to standard format" % (physicalSchemaName)
		sys.exit(2)


def initRunAttr(exprAttr, x, xValLabel, xValAttr, instance, plat, task):
	runAttr = exprAttr.copy()
	runAttr["Platform"] = plat
	#set fixed parameters for the experiments
	runAttr["PhysicalSchema"] = runAttr["PhysicalSchemas"] 
	runAttr["RadioLossRate"] = runAttr["RadioLossRates"]
	runAttr["AcquisitionRate"] = runAttr["AcquisitionRates"]
	#overwrite variable param
	runAttr[xValAttr] = x
	runAttr["xvalLabel"] = xValLabel
	runAttr["Instance"] = instance
	obtainNetworkTopologyAttributes(runAttr)
	runAttr["Task"] = task
	return runAttr


def generateAvroraLogfileName(runAttr):
	 return "%s-exp%s-x%s-i%s-avrora-log.txt" % (runAttr["Platform"], runAttr["Experiment"], runAttr["xvalLabel"], runAttr["Instance"])

#TODO: Move this to after Condor/Avrora script
def parseEnergyMonitorOutput(avroraLogFile, runAttr):

	simulationDuration = runAttr["SimulationDuration"]
	(sumEnergy, maxEnergy, averageEnergy, radioEnergy, cpu_cycleEnergy, sensorEnergy, otherEnergy, networkLifetime) = AvroraLib.computeEnergyValues(".", simulationDuration, avroraLogFile, ignoreLedEnergy = True, defaultSiteEnergyStock = 31320, siteLifetimeRankFile = None, sink = 0, ignoreList = [])
	#All node energy in Joules for simulation duration
	runAttr["Sum Energy"] = sumEnergy
        #All node energy in Joules scaled to 6 month period
	runAttr["Sum Energy 6M"] = sumEnergy*((60.0*60.0*24.0*30.0*6.0)/float(simulationDuration))
	runAttr["Max Energy"] = maxEnergy
	runAttr["Average Energy"] = averageEnergy
	runAttr["CPU Energy"] = cpu_cycleEnergy
	runAttr["Sensor Energy"] = sensorEnergy
	runAttr["Other Energy"] = otherEnergy
	runAttr["Network Lifetime secs"] = networkLifetime
	runAttr["Network Lifetime days"] = float(networkLifetime)/60.0/60.0/24.0



def runINSNEE(task,xVal,xValLabel,xValAttr,instance,exprAttr,runAttrCols,rootOutputDir):
	global sneeRoot
	
	print "\n**********Experiment="+exprAttr['Experiment']+" Platform=INSNEE task="+task+" x="+xVal + " xLabel="+xValLabel+" instance="+str(instance)
	
	runAttr = initRunAttr(exprAttr, xVal, xValLabel, xValAttr, instance, 'INSNEE', task)
	runAttr["Query"] = SneeqlLib.tasks2queries[task]

	#check if equiv experiment run exists
	#if (runAttr['Experiment'],'INSNEE') in equivRuns.dict:
	#equivRuns.copyExperimentRunResults(runAttr, rootOutputDir)
	#else:

	#1 Compile SNEEql query and compile the nesC to generate the Avrora binaries
	#SneeqlLib.compileQuery(runAttr)

	#2 Extract the Avrora binaries from SNEETemporaryFiles folder,
	#put them in AvroraJobs folder
	#with avrora CommandString.txt
	#avrora topology file
	#### SneeqlLib.extractAvroraFiles(runAttr)
		
	#TODO: if Condor flag is not set?
	#2 Run the query in Avrora
	#if (runAttr['SNEEExitCode']==0):
	#	runSNEEInAvrora(runAttr, runAttrCols)

	#copy SNEE/nesC/avrora files over
	#runOutputDir = getRunOutputDir(runAttr, rootOutputDir, task) 
	#os.makedirs(runOutputDir)
	#sneeOutputDir = sneeRoot + os.sep + "output" + os.sep + "query1" + os.sep
	#shutil.copytree(sneeOutputDir + "query-plan", runOutputDir+ os.sep + "query-plan")
	#if (os.path.exists(sneeOutputDir + "avrora_micaz_t2")):
	#	shutil.copytree(sneeOutputDir + "avrora_micaz_t2", runOutputDir+ os.sep + "avrora_micaz_t2")
	#shutil.copyfile(sneeRoot + os.sep + "logs/snee.log", runOutputDir + os.sep + "snee.log")

        #3 Log the results
	#logResultsToFiles(runAttr, runAttrCols, rootOutputDir)
	

def runExperiment(exprAttr, exprAttrCols, outputDir):
	global optPlatList, optNumInstances

	print "runExperiments"
	runAttrCols = exprAttrCols + ["BufferingFactor", "Platform", "Task", "xvalLabel", "Instance", "SNEEExitCode", "NetworkSize", "Layout", "NetworkDensity","NetworkPercentSources", "SimulationDuration", "Tuple Acq Count", "Tuple Del Count", "Tuple Delta Sum", "Data Freshness", "Output Rate", "Delivery Rate", "Sum Energy", "Sum Energy 6M", "Max Energy", "Average Energy", "CPU Energy", "Sensor Energy", "Other Energy", "Network Lifetime secs", "Network Lifetime days", "Comments"]

	tasks = exprAttr["Tasks"].split(";")
	xValAttr = exprAttr["XvalAttr"]
	xVals = exprAttr[xValAttr+"s"].split(";")
	xValLabels = exprAttr["XvalLabels"].split(";")

	for plat in optPlatList:	
		for task in tasks:
			for (xVal,xValLabel) in zip(xVals,xValLabels):
				for i in range(1,optNumInstances+1):
					#if (plat == "MHOSC"):
					#	runMHOSCExperiment(task,xVals,xValLabels,xValAttr,exprAttr,runAttrCols,outputDir)
					if (plat == "INSNEE"):
						runINSNEE(task,xVal,xValLabel,xValAttr,i,exprAttr,runAttrCols,outputDir)
				
def runExperiments(timeStamp, outputDir):
	colNames = None
	first = True

	print "creating dir: "+outputDir
	os.makedirs(outputDir)

	for line in open("experiments.csv", 'r'):
		print "runExperiments"
		if first:
			exprAttrCols = CSVLib.colNameList(line)
			exprAttrCols += ["TimeStamp"]
			first = False
			continue

		exprAttr = CSVLib.line2Dict(line, exprAttrCols)

		if not str(exprAttr['Experiment']) in optExprList:
			continue

		exprAttr['TimeStamp']=timeStamp
		#Experiment,X,Y,Tasks,Xlabels,Network,RadioLossRate,AcquisitionRate
		runExperiment(exprAttr, exprAttrCols, outputDir)
						

def main(): 	
	global optScenarioDir, optOutputDir, optUseCondor

	#parse the command-line arguments
	parseArgs(sys.argv[1:]) 

	timeStamp = UtilLib.getTimeStamp()
	#if (not optTimeStampOutput):
	#	timeStamp = ""
	startLogger(timeStamp)
	
	#RandomSeeder.setRandom()
	
	runExperiments(timeStamp, optOutputDir+os.sep+timeStamp)

if __name__ == "__main__":
	main()