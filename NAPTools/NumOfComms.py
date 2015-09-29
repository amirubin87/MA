__author__ = 't-amirub'
import os.path
import os
'''''''''''''''''''''''''''''''''''''''''''''''''''

                num of comms

'''''''''''''''''''''''''''''''''''''''''''''''''''

def CalcAccuracyI(GTPath, resultPath):
    Gc =0
    if not os.path.isfile(GTPath) or not os.path.isfile(resultPath):
      return 0.0
    GTfile = open(GTPath, 'r')
    Glines = GTfile.readlines()
    for line in Glines:
 count more than 3?
    GTfile.close()
    if Cs == 0:
        return 0.0
    Rfile = open(resultPath, 'r')
    Cr = len(Rfile.readlines())
    Rfile.close()
    res = 1 - float(abs(Cs-Cr)/float(Cs))
    return res

def CalcAccuracy(GTPath, resultPath,outputPath):
    ans = CalcAccuracyI(GTPath, resultPath)
    output = open(outputPath, 'a')
    output.write( 'NumOfCommsAccuracy:\t' + str(ans) + '\n')
    output.close()

