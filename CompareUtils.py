'''
Created on Apr 19, 2015

@author: t-amirub
'''

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
        comms.pop()
        ans[node] = comms
    return renumberComms(ans)

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


def convertPartitionToIntDictionary(part):
    ans = dict()
    for sub in part:
        for key in sub:
            ans[int(key)] = sub[key]
    return ans

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

