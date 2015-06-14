__author__ = 't-amirub'
import networkx as nx

class MetaData :

    m = 0
    K_v = {}
    K_v_c = {}
    Sigma_c ={}
    C_v= {}
    node2com = {}

    def __init__(self) :
        self.m = 0.0
        self.K_v = dict([])
        self.K_v_c = dict([])
        self.Sigma_c = dict([])
        self.node2com = dict([])

    def __str__(self) :
        return ( " total_weight : " + str(self.m)
            + " K_v : " + str(self.K_v)
            + " K_v_c : " + str(self.K_v_c)
            + " Sigma_c : " + str(self.Sigma_c)
            + "node2com : " + str(self.node2com))

    def copy(self) :
        new_MetaData = MetaData()
        new_MetaData.m = self.m
        new_MetaData.K_v = self.K_v.copy()
        new_MetaData.K_v_c = self.K_v_c.copy()
        new_MetaData.Sigma_c = self.Sigma_c.copy()
        new_MetaData.node2com = self.node2com.copy()

    def VerifyNodesNumbers(self,graph):
        numOfNodes= graph.number_of_nodes()
        nodes = graph.nodes()
        for i in range(0,numOfNodes -1):
            if i not in nodes:
                raise ValueError("Bad graph - node ids must be all numbers between 0 and |v| -1")

    def init(self, graph):
        """Initialize the MetaData of a graph with every node in one community"""
        self.VerifyNodesNumbers(graph)
        count = 0
        self.m = 0.0
        self.K_v = dict([])
        self.K_v_c = dict()
        self.Sigma_c = dict([])
        self.node2com = dict([])
        self.m = graph.size(weight = 'weight')
        for node in graph.nodes() :
            self.node2com[node] = [count]
            nodeWeight = float(graph.degree(node, weight = 'weight'))
            if nodeWeight < 0 :
                raise ValueError("Bad graph type, use positive weights")
            self.K_v[count] = nodeWeight
            self.Sigma_c[count] = nodeWeight
            count = count + 1

        for node in graph.nodes() :
            if self.K_v_c.get(node) == None :
                self.K_v_c[node] = dict([])
            for neighbour in graph.neighbors(node):
                comm = self.node2com[neighbour][0]
                weight = float(graph.get_edge_data(node, neighbour,{"weight":0}).get("weight", 1))
                self.K_v_c[node][comm] = weight

    def ClearComms(self, node):
        self.node2com[node] = []

    def SetCommsForNode(self, node, comms):
        self.node2com[node] = comms

