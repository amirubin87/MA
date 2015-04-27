# source: https://bitbucket.org/taynaud/python-louvain
#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
This module implements community detection.
"""
#from __future__ import print_function
#__all__ = ["partition_at_level", "modularity", "best_partition", "generate_dendrogram", "generate_dendogram", "induced_graph"]
#__author__ = """Thomas Aynaud (thomas.aynaud@lip6.fr)"""
#    Copyright (C) 2009 by
#    Thomas Aynaud <thomas.aynaud@lip6.fr>
#    All rights reserved.
#    BSD license.

__PASS_MAX = -1
__MIN = 0.0000001

import networkx as nx


def partition_at_level(dendrogram, level) :
    """Return the partition of the nodes at the given level

    A dendrogram is a tree and each level is a partition of the graph nodes.
    Level 0 is the first partition, which contains the smallest communities, and the best is len(dendrogram) - 1.
    The higher the level is, the bigger are the communities

    ! If nodes can be in more than one comm -
        when a nodes fits to more than 1 comm, we add the comm to the list of comms he is suitable for.

    Parameters
    ----------
    dendrogram : list of dict
       a list of partitions, ie dictionnaries where keys of the i+1 are the values of the i.
    level : int
       the level which belongs to [0..len(dendrogram)-1]

    Returns
    -------
    partition : dictionnary
       A dictionary where keys are the nodes and the values are lists of the communities(!) it belongs to

    Raises
    ------
    KeyError
       If the dendrogram is not well formed or the level is too high

    See Also
    --------
    best_partition which directly combines partition_at_level and generate_dendrogram to obtain the partition of highest modularity

    Examples
    --------
    >>> G=nx.erdos_renyi_graph(100, 0.01)
    >>> dendo = generate_dendrogram(G)
    >>> for level in range(len(dendo) - 1) :
    >>>     print "partition at level", level, "is", partition_at_level(dendo, level)
    """
    partition = dendrogram[0].copy()
    for index in range(1, level + 1) :
        for node, communities in partition.items():
            partition[node] = []
            for community in communities :
                #The community of the node in level i in the dendro is the name of the node to look for in level i+1 in the dendro.
                partition[node].extend(dendrogram[index][community])
    return partition


def modularity(partition, graph) :
    """Compute the modularity of a partition of a graph
    
    ! If nodes can be in more than one comm - 
        for each node will iterate throw all, in each comm, for each neighbor, 
        if he is also in the given comm, the value is increased.

    Parameters
    ----------
    partition : dict
       the partition of the nodes, i.e a dictionary where keys are their nodes and values the communities
    graph : networkx.Graph
       the networkx graph which is decomposed

    Returns
    -------
    modularity : float
       The modularity

    Raises
    ------
    KeyError
       If the partition is not a partition of all graph nodes
    ValueError
        If the graph has no link
    TypeError
        If graph is not a networkx.Graph

    References
    ----------
    .. 1. Newman, M.E.J. & Girvan, M. Finding and evaluating community structure in networks. Physical Review E 69, 26113(2004).

    Examples
    --------
    >>> G=nx.erdos_renyi_graph(100, 0.01)
    >>> part = best_partition(G)
    >>> modularity(part, G)
    """
    if type(graph) != nx.Graph :
        raise TypeError("Bad graph type, use only non directed graph")

    inc = dict([])
    deg = dict([])
    links = graph.size(weight='weight')
    if links == 0 :
        raise ValueError("A graph without link has an undefined modularity")

    for node in graph :
        coms = partition[node]
        for com in coms :
            deg[com] = deg.get(com, 0.) + graph.degree(node, weight = 'weight')
            for neighbor, datas in graph[node].items() :
                weight = datas.get("weight", 1)
                if com in partition[neighbor] :
                    if neighbor == node :
                        inc[com] = inc.get(com, 0.) + float(weight)
                    else :
                        inc[com] = inc.get(com, 0.) + float(weight) / 2.

    res = 0.
    
    for com in __getCommsFromPartition(partition):
        res += (inc.get(com, 0.) / links) - (deg.get(com, 0.) / (2.*links))**2
    return res


def best_partition(graph, partition = None) :
    """Compute the partition of the graph nodes which maximises the modularity
    (or try..) using the Louvain heuristices

    This is the partition of highest modularity, i.e. the highest partition of the dendrogram
    generated by the Louvain algorithm.

    Parameters
    ----------
    graph : networkx.Graph
       the networkx graph which is decomposed
    partition : dict, optionnal
       the algorithm will start using this partition of the nodes. It's a dictionary where keys are their nodes and values the communities

    Returns
    -------
    partition : dictionnary
       The partition, with communities numbered from 0 to number of communities

    Raises
    ------
    NetworkXError
       If the graph is not Eulerian.

    See Also
    --------
    generate_dendrogram to obtain all the decompositions levels

    Notes
    -----
    Uses Louvain algorithm, with the ability of overlapping comms

    References
    ----------
    .. 1. Blondel, V.D. et al. Fast unfolding of communities in large networks. J. Stat. Mech 10008, 1-12(2008).
    .. 2. TBD
    """
    dendo = generate_dendrogram(graph, partition)
    return partition_at_level(dendo, len(dendo) - 1 )

def generate_dendrogram(graph, part_init = None, splitNodesInL1 = False) :
    """Find communities in the graph and return the associated dendrogram

    A dendrogram is a tree and each level is a partition of the graph nodes.  Level 0 is the first partition, which contains the smallest communities, and the best is len(dendrogram) - 1. The higher the level is, the bigger are the communities

    ! If nodes can be in more than one comm -
        only in the first step we give the nodes that option.
        
    Parameters
    ----------
    graph : networkx.Graph
        the networkx graph which will be decomposed
    part_init : dict, optionnal
        the algorithm will start using this partition of the nodes. It's a dictionary where keys are their nodes and values the communities
    splitNodesInL1: bool
        when true, nodes will be duplicated in the first level.
    Returns
    -------
    dendrogram : list of dictionaries
        a list of partitions, ie dictionnaries where keys of the i+1 are the values of the i. and where keys of the first are the nodes of graph

    Raises
    ------
    TypeError
        If the graph is not a networkx.Graph

    See Also
    --------
    best_partition

    Notes
    -----
    Uses Louvain algorithm

    References
    ----------
    .. 1. Blondel, V.D. et al. Fast unfolding of communities in large networks. J. Stat. Mech 10008, 1-12(2008).

    Examples
    --------
    >>> G=nx.erdos_renyi_graph(100, 0.01)
    >>> dendo = generate_dendrogram(G)
    >>> for level in range(len(dendo) - 1) :
    >>>     print "partition at level", level, "is", partition_at_level(dendo, level)
    """
    if type(graph) != nx.Graph :
        raise TypeError("Bad graph type, use only non directed graph")

    #special case, when there is no link
    #the best partition is everyone in its community
    if graph.number_of_edges() == 0 :
        part = dict([])
        for node in graph.nodes() :
            part[node] = [node]
        return part

    current_graph = graph.copy()
    status = Status()
    status.init(current_graph, part_init)  
    status_list = list()
    __one_level(current_graph, status, splitNodesInL1)
    new_mod = __modularity(status)
    partition = __renumberComms(status.node2com)
    status_list.append(partition)
    mod = new_mod
    current_graph = induced_graph(partition, current_graph)

    status.init(current_graph)
    
    while True :
        print("")
        print("")
        print("MY         ENTERED WHILE")

        __one_level(current_graph, status)
        print("My  Louvain  status.node2com after one level:   {0}".format(status.node2com))
        new_mod = __modularity(status)
        print("my Louvain  new_mod in while: {0}".format(new_mod))
        if new_mod - mod < __MIN :
            break
        partition = __renumberComms(status.node2com)
        status_list.append(partition)
        mod = new_mod
        current_graph = induced_graph(partition, current_graph)
        status.init(current_graph)
    return status_list[:]


def induced_graph(partition, graph) :
    
    """Produce the graph where nodes are the communities

    there is a link of weight w between communities if the sum of the weights of the links between their elements is w
    
    ! If nodes can be in more than one comm -
        the weight between two nodes in the induced graph will  be the sum of weights
        between nodes in the comms the nodes represents.
        
        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        
        NOTICE: if nodes u and v are both in comms c1 and c2,
                and the weight is w, we will count it TWICE:
                once when we check the copy of u in c1 and v in c2
                and once for the copy of u in c2 and v in c1!
        TODO: This should be reconsidered!
         
        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    
    Parameters
    ----------
    partition : dict
       a dictionary where keys are graph nodes and  values the part the node belongs to
    graph : networkx.Graph
        the initial graph

    Returns
    -------
    g : networkx.Graph
       a networkx graph where nodes are the parts

    Examples
    --------
    >>> n = 5
    >>> g = nx.complete_graph(2*n)
    >>> part = dict([])
    >>> for node in g.nodes() :
    >>>     part[node] = node % 2
    >>> ind = induced_graph(part, g)
    >>> goal = nx.Graph()
    >>> goal.add_weighted_edges_from([(0,1,n*n),(0,0,n*(n-1)/2), (1, 1, n*(n-1)/2)])
    >>> nx.is_isomorphic(int, goal)
    True
    """
    ret = nx.Graph()
    
    #get all comms, and set them as nodes in the induced graph
    ret.add_nodes_from(__getCommsFromPartition(partition))
    
    for node1, node2, datas in graph.edges_iter(data = True) :
        weight = datas.get("weight", 1)
        coms1 = partition[node1]
        coms2 = partition[node2]
        for com1 in coms1 :
            for com2 in coms2 :
                #get the old edge weight
                w_prec = ret.get_edge_data(com1, com2, {"weight":0}).get("weight", 1)
                #set the new edge weight
                ret.add_edge(com1, com2, weight = w_prec + weight)

    return ret


def __renumberComms(dictionary) :
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

#! splitNodesInL1 - when true nodes will be splitted!
def __one_level(graph, status, splitNodesInL1 = False) :
    
    """Compute one level of communities
    ! If nodes can be in more than one comm -
        FIRST IMPLEMETATION NOT SUPPORTING MULTIPLE COMMS PER NODE.
        TODO
    """
    modif = True
    nb_pass_done = 0
    cur_mod = __modularity(status)
    print("My     cur_mod when enter oneLevel: {0}".format(cur_mod))
    print("My     status.total_weight when enter oneLevel: {0}".format(status.total_weight))
    new_mod = cur_mod

    while modif  and nb_pass_done != __PASS_MAX :
        cur_mod = new_mod
        modif = False
        nb_pass_done += 1

        for node in graph.nodes() :
            coms_node = status.node2com[node]
            degc_totw = status.gdegrees.get(node, 0.) / (status.total_weight*2.)
            neigh_communities = __neighcom(node, graph, status)
            best_coms = coms_node.copy()
            # remove node from all coms he is in
            while coms_node :
                com_node = coms_node.pop()
                __remove(node, com_node,
                    neigh_communities.get(com_node, 0.), status)
            best_increase = 0

            for com, dnc in neigh_communities.items() :
                incr =  dnc  - status.degrees.get(com, 0.) * degc_totw
                #print("My  com:{0} status.degrees:   {1}".format(com,status.degrees))

                if incr > best_increase :
                    best_increase = incr
                    #for now, one com only(TODO!)
                    best_coms = [com]

            for best_com in best_coms :
                __insert(node, best_com,
                        neigh_communities.get(best_com, 0.), status)
            
            if best_coms != coms_node :
                modif = True
        new_mod = __modularity(status)
        if new_mod - cur_mod < __MIN :
            break


class Status :
    """
    To handle several data in one struct.

    Could be replaced by named tuple, but don't want to depend on python 2.6
    """
    node2com = {}
    total_weight = 0
    internals = {}
    degrees = {}
    gdegrees = {}

    def __init__(self) :
        self.node2com = dict([])
        self.total_weight = 0
        self.degrees = dict([])
        self.gdegrees = dict([])
        self.internals = dict([])
        self.loops = dict([])

    def __str__(self) :
        return ("node2com : " + str(self.node2com) + " degrees : "
            + str(self.degrees) + " internals : " + str(self.internals)
            + " total_weight : " + str(self.total_weight))

    def copy(self) :
        """Perform a deep copy of status"""
        new_status = Status()
        new_status.node2com = self.node2com.copy()
        new_status.internals = self.internals.copy()
        new_status.degrees = self.degrees.copy()
        new_status.gdegrees = self.gdegrees.copy()
        new_status.total_weight = self.total_weight

    def init(self, graph, part = None) :
        """Initialize the status of a graph with every node in one community"""
        count = 0
        self.node2com = dict([])
        self.total_weight = 0
        self.degrees = dict([])
        self.gdegrees = dict([])
        self.internals = dict([])
        self.total_weight = graph.size(weight = 'weight')
        if part == None :
            for node in graph.nodes() :
                self.node2com[node] = set([count])
                deg = float(graph.degree(node, weight = 'weight'))
                if deg < 0 :
                    raise ValueError("Bad graph type, use positive weights")
                self.degrees[count] = deg
                self.gdegrees[node] = deg
                self.loops[node] = float(graph.get_edge_data(node, node,
                                                 {"weight":0}).get("weight", 1))
                self.internals[count] = self.loops[node]
                count = count + 1
        else :
            for node in graph.nodes() :
                com = part[node]
                self.node2com[node] = com
                deg = float(graph.degree(node, weight = 'weight'))
                self.degrees[com] = self.degrees.get(com, 0) + deg
                self.gdegrees[node] = deg
                inc = 0.
                for neighbor, datas in graph[node].items() :
                    weight = datas.get("weight", 1)
                    if weight <= 0 :
                        raise ValueError("Bad graph type, use positive weights")
                    if part[neighbor] == com :
                        if neighbor == node :
                            inc += float(weight)
                        else :
                            inc += float(weight) / 2.
                self.internals[com] = self.internals.get(com, 0) + inc



def __neighcom(node, graph, status) :
    """
    Compute the communities in the neighborood of node in the graph given
    with the decomposition node2com
    
    ! If nodes can be in more than one comm - 
        for each neighbor we will check in each comm he is in, and will update its weight.

        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        
        NOTICE: if nodes u and v are both in comms c1 and c2,
                and we now work on u - 
                when we look at his neighborhood comms, both c1 and c2
                are calculated when v is treated.
                The fact the u is in both DOESNT EFFECT ANYTHING.
                 
        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 
    """
    weights = {}
    for neighbor, datas in graph[node].items() :
        if neighbor != node :
            weight = datas.get("weight", 1)
            neighborcoms = status.node2com[neighbor]            
            for neighborcom in neighborcoms :
                weights[neighborcom] = weights.get(neighborcom, 0) + weight
            
    return weights


def __remove(node, com, weight, status, splitNodesInL1 = False) :
    """ For a node WHICH WAS REMVOD from a community com, we modify status"""
    status.degrees[com] = ( status.degrees.get(com, 0.)
                                    - status.gdegrees.get(node, 0.) )
    status.internals[com] = float( status.internals.get(com, 0.) -
                weight - status.loops.get(node, 0.) )
    #This is not needed - already poped the com from the list!
    #status.node2com[node].remove(com)

def __insert(node, com, weight, status, splitNodesInL1 = False) :
    """ Insert node into community and modify status"""
    status.node2com[node].add(com)
    status.degrees[com] = (status.degrees.get(com, 0.) +
                                status.gdegrees.get(node, 0.))

    status.internals[com] = float(status.internals.get(com, 0.) +
                            weight +
                            status.loops.get(node, 0.))

def __getCommsFromPartition(partition) :
    """
    Return a set of all comms
    """
    ans = set()
    for comsSet in partition.values():
        for com in comsSet:
            ans.add(com)
    return ans

def __modularity(status) :
    """
    Compute the modularity of the partition of the graph fast using status precomputed
    """
    links = float(status.total_weight)
    result = 0.
    #get sets of comms from the dict
    commsSet = __getCommsFromPartition(status.node2com)
    for community in commsSet :        
        in_degree = status.internals.get(community, 0.)
        degree = status.degrees.get(community, 0.)
        if links > 0 :
            result = result + in_degree / links - ((degree / (2.*links))**2)
    return result


