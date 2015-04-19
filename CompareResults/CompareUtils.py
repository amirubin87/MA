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
    Takes a file with a dict in it and tranlate to a dict of node 2 comm.
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
