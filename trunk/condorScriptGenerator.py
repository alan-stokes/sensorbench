#!/usr/bin/python
import os, sys, networkLib, math, getopt, UtilLib, CSVLib, shutil

optNumInstances = 10
optCondorDir = "condor"
optBinaryDir = "avrora-Bineries"
pathSeperator = os.sep

optExprList = ["1a", "1b", "2a", "2b", "3a", "3b", "4a", "4b", "5a", "5b", "6a", "6b", "7"]
optPlatList = ["INSNEE", "HC", "TinyDB", "MHOCS"]
def parseArgs(args):	
	global optScenarioDir
	try:
		optNames = ["condor-dir=", "num-instances=", "binary-dir="]
	
		#append the result of getOpNames to all the libraries 
		optNames = UtilLib.removeDuplicates(optNames)
		
		opts, args = getopt.getopt(args, "h", optNames)
	except getopt.GetoptError, err:
		print str(err)
		usage()
		sys.exit(2)
			
	for o, a in opts:
		if (o == "--condor-dir"):
			optCondorDir = a
		elif (o == "--num-instances"):
			optNumInstances = int(a)
		elif (o == "--binary-dir"):
			optBinaryDir = a
		else:
			usage()
			sys.exit(2)


def usage():
	print "generate-scenarios.py --condor-dir=<dir> --num-instances=<int> --binary-dir=<dir>"


def check_dir(d):
	if not os.path.exists(d):
		os.makedirs(d)

def generateTopBlurb():
	check_dir(optCondorDir)
	condorFile = open(optCondorDir + pathSeperator + "submit.txt", "w") 
	condorFile.write("universe = vanilla \n executable = start.sh \n when_to_transfer_output = ON_EXIT \n Should_Transfer_Files = YES \n transfer_input_files = ../SNEE.jar,../jre.tar.gz \n Requirements = (OpSys == \"LINUX\") &&(HAS_STANDARD_IMAGE =?= True) \n Request_Disk = 3000000 \n request_memory = 2048 \n #Output = output$(Process).txt \n #Error = error$(Process).txt \n log = log.txt \n Output = out.txt \n Error = err.txt \n notification = error \n\n\n")
	



def condorLine(task,xVals,xValLabels,xValAttr,exprAttr):
	condorFile = open(optCondorDir + pathSeperator + "submit.txt", "a") 
	CONVENTION ="CONVENTION"
	binaryFolderName = optBinaryDir + pathSeperator + CONVENTION
	condorFile.write("Arguments = %s \n	initialdir   = %s \n	queue \n\n"%(binaryFolderName, CONVENTION))
	check_dir(optCondorDir + pathSeperator + CONVENTION)




def generateScriptForEachJob(exprAttr, exprAttrCols):
	global optPlatList, noInstances

	tasks = exprAttr["Tasks"].split(";")
	xValAttr = exprAttr["XvalAttr"]
	xVals = exprAttr[xValAttr+"s"].split(";")
	xValLabels = exprAttr["XvalLabels"].split(";")

	for plat in optPlatList:	
		for task in tasks:
			for instance in range(1,optNumInstances):
				condorLine(task,xVals,xValLabels,xValAttr,exprAttr)

def generateScript():
	colNames = None
	first = True

	for line in open("experiments.csv", 'r'):
		if first:
			exprAttrCols = CSVLib.colNameList(line)
			exprAttrCols += ["TimeStamp"]
			first = False
			continue

		exprAttr = CSVLib.line2Dict(line, exprAttrCols)

		if not str(exprAttr['Experiment']) in optExprList:
			continue

		#Experiment,X,Y,Tasks,Xlabels,Network,RadioLossRate,AcquisitionRate
		generateTopBlurb()
		generateScriptForEachJob(exprAttr, exprAttrCols)


def moveCollections():
	shutil.copyfile(optBinaryDir+".zip", optCondorDir + pathSeperator + optBinaryDir+".zip")
	shutil.copyfile("avrora-1.7.113.jar", optCondorDir + pathSeperator + "avrora-1.7.113.jar")
	shutil.copyfile("jre.tar.gz", optCondorDir + pathSeperator + "jre.tar.gz")


def main(): 	
	global optScenarioDir

  #parse the command-line arguments
	parseArgs(sys.argv[1:]) 
	generateScript()
	moveCollections()
  


if __name__ == "__main__":
	main()
            
