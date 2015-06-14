'''
Created on Apr 19, 2015

@author: t-amirub
'''
def convertStanfordCommFileToPartition(stanfordCommFile):
    '''
    Takes a file with a list of list of nodes- each line is a comm.
     Translate to a dict of node 2 comm.
    Parameters
    ----------
    file : File
       A file containing the data

    Returns
    -------
    A dict of node 2 comm.
    '''
    ans= dict()
    content = stanfordCommFile.readlines()
    i = 0
    for line in content:
        nodes = line.replace('\n', '').split('\t')
        for node in nodes:
            if ans.get(node) == None:
                ans[node] = set()
            ans[node].add(i)
        i = i + 1
    return ans

def sortBySmallestNode(com2Nodes):
    '''
    2 level sorting the dictionary of com 2 nodes.
    1. Each list of nodes is sorted.
    2. Comms are sorted by the smallest node in them. 
    3. Comms are renamed according to the order.
    Parameters
    ----------
    com2Nodes : dict
       per com you have a set of nodes
    
    Returns
    -------
    An ordered array of tupples.
    '''
    ans = dict()
    for key in com2Nodes.keys():        
        nodesA = list(com2Nodes[key])
        nodesA = sorted(nodesA)
        ans[key] = nodesA
         
    #sort all
    ans = sorted(ans.items(), key = lambda comm : comm[1][0]) 
      
    #rename comms - for easy comparison
    return [(i, tup[1]) for i,tup in zip(range(len(ans)), ans)]        
    
    
def convertFileToPartition(file):
    '''
    Takes a file with a dict in it and translate to a dict of node 2 comm.
    Parameters
    ----------
    file : File
       A file containing the data
    
    Returns
    -------
    A dict of node 2 comm.
    '''
    ans= dict()
    content = file.readlines()
    for line in content:
        node = int(line.split('\t')[0])
        comms = line.split('\t')[1].split(' ')
        # last elementis '\n'- we remove it.
        comms.pop()
        ans[node] = comms
    return ans #renumberComms(ans)

def convertFileForNMI(file):
    ans= dict()
    content = file.readlines()
    for line in content:
        node = int(line.split('\t')[0])
        comms = line.split('\t')[1].split(' ')
        # last elementis '\n'- we remove it.
        comms.pop()
        for comm in comms :
            if ans.get(comm) == None:
                ans[comm] = set()
            ans[comm].add(node)
    return ans.values()

def renumberComms(dictionary) :
    """Renumber the values of the dictionary from 0 to n
    """
    count = 0
    ret = dictionary.copy()
    new_values = dict([])
    for key in dictionary.keys() :
        newSet = set()
        for value in dictionary[key]:
            new_value = new_values.get(value, -1)
            if new_value == -1 :
                new_values[value] = count
                new_value = count
                count = count + 1
            newSet.add(new_value)
        ret[key] = newSet

    return ret

def writeOutputToFile(part, louvainOutputFileName):
    output = open("MyLouvainOutput" + louvainOutputFileName + ".txt",'w')
    for keys,values in part.items():
        output.write(keys)
        output.write('\t')
        for val in values :
            output.write(str(val))
            output.write(" ")
        output.write('\n')
    output.close()

def ConvertPartitionToSetsOfNodes(partition):
    ans = dict()
    for v in partition.keys():
        for comm in partition[v]:
             if ans.get(comm) == None:
                ans[comm] = set()
             ans[comm].add(v)
    return ans.values()

def OutputSetOfNodes(setsOfNodes, path):
    file = open(path,'w')
    for comm in setsOfNodes:
        for node in comm:
            file.write("%s " % node)
        file.write("\n")
    file.close()

def convertPartitionToIntDictionary(part):
    ans = dict()
    for sub in part:
        for key in sub:
            ans[int(key)] = sub[key]
    return ans



def readSLPAFile(path, t_h):
    f= open(path + str(t_h) +"_v3_T100.icpm"  , "r")#
    output = dict()
    lines = f.readlines()

    comm = 0

    for line in lines:
        nodes =map(int, line.split())
        for node in nodes:
            if output.get(node) == None:
                output[node] = set()
            output[node].add(comm)
        comm = comm+1
    f.close()
    return output

def com2Nodes(partition):
    '''
    Converts node 2 comms to com 2 nodes.
    ----------
    partition : dict
       A node 2 comms dic
    
    Returns
    -------
    A list of tuppels of comm to nodes, sorted by smallest node in comm. 
    '''
    ans= dict()    
    for node in partition.keys():
        comms = partition[node]
        for comm in comms :
            if ans.get(comm) == None :
                ans[comm] = set()
            ans[comm].add(int(node))
            ans[comm]
    return sortBySmallestNode(ans)

def WriteOSLOMForNMI(oslomFile, path):
    file = open(path,'w')
    content = oslomFile.readlines()
    print(content)
    i = 1
    for line in content:
        if i%2 == 0:
            nodes = line.replace('\n', '').split(' ')
            print (nodes)
            for node in nodes:
                file.write("%s " % node)
            file.write("\n")
        i = i + 1
    file.close()