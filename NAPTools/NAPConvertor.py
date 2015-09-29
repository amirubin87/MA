__author__ = 't-amirub'

def FRLGroundTruthToListOfNodes(inputPath, outputPath):
    comm2Nodes= dict()
    groundTruth = open(inputPath, 'r')
    content = groundTruth.readlines()
    groundTruth.close()
    for line in content:
        parts = line.split('\t')
        node = parts[0]
        comms = parts[1].replace(' \n', '').split(' ')
        for comm in comms:
            if comm2Nodes.get(comm) == None :
                comm2Nodes[comm] = []
            comm2Nodes[comm].append(node)


    output = open(outputPath, 'w')
    for nodes in comm2Nodes.values():
        for node in nodes:
            output.write("%s " % node)
        output.write('\n')
    output.close()


FRLGroundTruthToListOfNodes('./community.dat', './readycommunity.dat')
def ClearComments(filePath):
    graphFile = open(filePath, 'r')
    content = graphFile.readlines()
    graphFile.close()
    graphFile = open(filePath, 'w')
    for line in content:
        if not line == '\n' and not '#' in line:
            graphFile.write(line)
    graphFile.close()

def CFinderToListOfNodesInComms(filePath):
    ClearComments(filePath)
    graphFile = open(filePath, 'r')
    content = graphFile.readlines()
    graphFile.close()
    graphFile = open(filePath, 'w')
    for line in content:
        graphFile.write(line.split(": ")[1])
    graphFile.close()

'''
def OSLOMToNMI(oslomPath, outputPath):
    file = open(outputPath,'w')
    oslomFile = open(oslomPath, 'r')
    content = oslomFile.readlines()
    i = 1
    for line in content:
        if i%2 == 0:
            nodes = line.replace(' \n', '').split(' ')
            for node in nodes:
                file.write("%s " % node)
            file.write("\n")
        i = i + 1
    file.close()
'''

def FRLGroundTruthToNMI(FRLGroundTruthpath, outputPath):
    file = open(outputPath,'w')
    FRLGroundTruthFile = open(FRLGroundTruthpath, 'r')
    content = FRLGroundTruthFile.readlines()
    FRLGroundTruthFile.close()
    com2Nodes = dict()
    for line in content:
        parts = line.split('\t')
        node = parts[0]
        comms = parts[1].replace(' \n', '').split(' ')
        for comm in comms:
            if com2Nodes.get(comm) == None:
                com2Nodes[comm] = []
            com2Nodes[comm].append(node)

    for nodes in com2Nodes.values():
        print(nodes)
        for node in nodes:
            file.write("%s " % node)
        file.write("\n")
    file.close()