'''
Created on Apr 18, 2015

@author: t-amirub
'''


def _sortBySmallestNode(com2Nodes):
    ans = dict()
    for key in com2Nodes.keys():        
        nodesA = list(com2Nodes[key])
        nodesA = sorted(nodesA)
        ans[key] = nodesA
    ans = sorted(ans.items(), key = lambda comm : comm[1][0])    
    return ans
        
    
    
def _convertFileToPartition(file):
    ans= dict()
    content = file.readlines()
    for line in content:
        node = int(line.split('\t')[0])
        comms = line.split('\t')[1].split(' ')
        comms.pop()
        ans[node] = comms
    return ans

def _com2Nodes(partition):
    ans= dict()    
    for node in partition.keys():
        comms = partition[node]
        for comm in comms :
            if ans.get(comm) == None :
                ans[comm] = set()
            ans[comm].add(int(node))
            ans[comm]
    return _sortBySmallestNode(ans)

groundTruthFile = open("C:/cygwin64/home/t-amirub/weighted_directed_nets/community.dat" , "r")
groundTruth = _convertFileToPartition(groundTruthFile)
louvainOutputFile = open("C:/LiClipse Workspace/MA/MA/output.txt" , "r")
louvainOutput = _convertFileToPartition(louvainOutputFile)

print("groundTruth:   {0}".format(groundTruth))
print("louvainOutput: {0}".format(louvainOutput))
groundTruthComms = _com2Nodes(groundTruth)
louvainOutputComms = _com2Nodes(louvainOutput)
print("groundTruthComms:   {0}".format(groundTruthComms))
print("louvainOutputComms: {0}".format(louvainOutputComms))
