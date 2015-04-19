'''
Created on Apr 18, 2015

@author: t-amirub
'''
from CompareUtils import *

'''-------------------------------------------
                    MAIN
-------------------------------------------'''
#TODO - read file name from user
print("fileName(no extension):")
fileName = input()
groundTruthFile = open("C:/cygwin64/home/t-amirub/weighted_directed_nets/community" + fileName + ".dat" , "r")
groundTruth = convertFileToPartition(groundTruthFile)
louvainOutputFile = open("C:/LiClipse Workspace/MA/MA/output" + fileName + ".txt" , "r")
louvainOutput = convertFileToPartition(louvainOutputFile)

print("groundTruth:   {0}".format(groundTruth))
print("louvainOutput: {0}".format(louvainOutput))
groundTruthComms = com2Nodes(groundTruth)
louvainOutputComms = com2Nodes(louvainOutput)
print("groundTruthComms amount of comms:   {0}, {1}".format(len(groundTruthComms), groundTruthComms))
print("louvainOutputComms amountof comms : {0}, {1}".format(len(louvainOutputComms), louvainOutputComms))
