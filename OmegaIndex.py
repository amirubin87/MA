__author__ = 't-amirub'

'''''''''''''''''''''''''''''''''''''''''''''''''''

                OMEGA INDEX

'''''''''''''''''''''''''''''''''''''''''''''''''''
def IntesectionSize(collection1,collection2):
    '''
    counts the amount of elements in the intersection of two collections
    :param collection1: first collection
    :param collection2: second collection
    :return: the amount of elements in the intersection of thetwo collections
    '''
    if len(collection1) > len(collection2):
        small = collection2
        big = collection1
    else :
        small = collection1
        big = collection2
    ans = 0
    for comm in small:
        if comm in big :
            ans += 1
    return ans


def UnadjustedOmegaIndex(M,amountsOfNodesWithSameAmountOfComms):
    '''
    Calcs Unadjusted Omega Index
    :param M: num of couples of nodes
    :param amountsOfNodesWithSameAmountOfComms: A dictionary. keys are amounts of couples of nodes.
            Values are an array of three: amount in C1, amount in C2, amount of shared couples.
    :return:Unadjusted Omega Index
    '''
    sum = 0
    for val in amountsOfNodesWithSameAmountOfComms.values():
       sum = sum + val[2]
    return sum/M

def ExpectedOmegaIndex(M, amountsOfNodesWithSameAmountOfComms):
    '''
    Calcs ExpectedOmegaIndex
    :param M: num of couples of nodes
    :param amountsOfNodesWithSameAmountOfComms: A dictionary. keys are amounts of couples of nodes.
            Values are an array of three: amount in C1, amount in C2, amount of shared couples.
    :return:ExpectedOmegaIndex
    '''
    sum = 0
    for val in amountsOfNodesWithSameAmountOfComms.values():
       sum = sum + val[0]*val[1]
    return sum/(pow(M,2.0))

def AmountOfSharedCommsToAmountOfPairsOfNodes(Node2Comm1, Node2Comm2):
    '''
    Goes over all pairs of nodes.
    Counts shared comms in c1, and in c2.
    Increments by 1 the count for these values.
    :param Node2Comm1: mapping of nodes to comms.
    :param Node2Comm2: mapping of nodes to comms.
    :return: A dictionary - keys are amounts of couples of nodes.
            Values are an array of three: amount in C1, amount in C2, amount of shared couples.
            So if C1 has only 1 couple of nodes and they share 2 comms, and another 2 couples with 0 shared comms,
            and C2 has 2 couples of nodes with 2 shared comms and another single couple with 0 shared comms,
            but only one couple got in both 0 shared comms, we will have:
            0:[2,2,1], 1:[0,0,0], 2:[1,2,0]
    '''
    ans = dict()
    nodes = Node2Comm1.keys()
    for v in range(1, len(nodes)) :
        #get comms of v in both C1 and C2
        vComms1 = Node2Comm1[v]
        vComms2 = Node2Comm2[v]
        for u in range(v, len(nodes)):
            #get comms of u in both C1 and C2
            uComms1 = Node2Comm1[u]
            uComms2 = Node2Comm2[u]

            # check how many shared comms v and u have in C1, increment by 1 the count of it
            amountOfSharedComms1 = IntesectionSize(vComms1,uComms1)
            if ans.get(amountOfSharedComms1) == None :
                ans[amountOfSharedComms1] = [0,0,0]
            ans[amountOfSharedComms1][0] += 1

            # check how many shared comms v and u have in C2, increment by 1 the count of it
            amountOfSharedComms2 = IntesectionSize(vComms2,uComms2)
            if ans.get(amountOfSharedComms2) == None :
                ans[amountOfSharedComms2] = [0,0,0]
            ans[amountOfSharedComms2][1] += 1

            # if they share the same amount of nodes in C1 and C2, increment by 1 the count of it.
            if amountOfSharedComms1 == amountOfSharedComms2:
                ans[amountOfSharedComms2][2] += 1
    return ans

def OmegaIndex(Node2Comm1, Node2Comm2):
    '''
    Calcs Omega index as in "Overlapping Community Detection in Networks: The State-of-the-Art and Comparative Study"
    '''
    n = len(Node2Comm1.keys())
    #amount of nodes pairs
    M = n*(n-1)/2
    amountsOfNodesWithSameAmountOfComms =  AmountOfSharedCommsToAmountOfPairsOfNodes(Node2Comm1,Node2Comm2)
    Wu = UnadjustedOmegaIndex(M,amountsOfNodesWithSameAmountOfComms)
    We = ExpectedOmegaIndex(M,amountsOfNodesWithSameAmountOfComms)
    return (Wu-We)/(1-We)
