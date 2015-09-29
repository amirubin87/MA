__author__ = 't-amirub'
import os.path
import os
'''''''''''''''''''''''''''''''''''''''''''''''''''

                NMI

'''''''''''''''''''''''''''''''''''''''''''''''''''

def GetMetricResultFromFile(path):
    if not os.path.isfile(path):
      return 0.0
    if os.stat(path).st_size == 0:
        return 0.0
    file = open(path, 'r')
    line = file.readline()
    file.close()
    metricS = line.split('\t')[1].replace('\n','')
    if 'e-' in metricS:
        return 0.0
    return float(metricS)

def GenerateMetricSummaryForOverlappingLouvain(metricName, outputPath):  
    output = open(outputPath, 'a')   
    output.write(metricName)
    for commsSize in ['b', 's']:
		for onp in ['10', '50']:
			for om in range(2, 9):
			    if commsSize == 'b' or onp == '10' or om < 7 :
				output.write('			N5000' + commsSize + '/ONp' + onp+ '/OM' + str(om) + '\n')
				metricSum = 0
				for i in range(1,11):				      
					#Ovelapping Louvain
					bestMetric = 0.0
					for k in range(1, 2):
						for betta in ["1.01","1.02","1.03","1.04","1.05","1.06","1.07","1.08","1.09","1.1","1.2","1.3","1.4"]:
							metric = GetMetricResultFromFile('../../benchmarks/binary_networks/N5000' + commsSize+ '/ONp' + onp+ '/OM' + str(om) + '/' + str(i) + '/metrics/' + metricName + '/O-Louvain/' + str(k) +'/betta' + betta + '.dat')
							if metric > bestMetric:
								bestMetric = metric						
						metricSum += bestMetric

				output.write('O-Louvain ' + str(metricSum/10)+'\n')
    output.close()
 


def GenerateMetricSummary(metricName, outputPath):
	
	if metricName not in ["NMI2", "OmegaIndex", "F1"]:
	  print " metric name must be one of NMI2 OmegaIndex"
	  return
	
	output = open(outputPath, 'a')
	output.write(metricName)
	for commsSize in ['b', 's']:
		for onp in ['10', '50']:
			for om in range(2, 9):
				if commsSize == 'b' or onp == '10' or om < 7 :
					output.write('			N5000' + commsSize + '/ONp' + onp+ '/OM' + str(om) + '\n')
					print "				N5000{0}/Onp{1}/OM{2}".format(commsSize,onp,str(om))
					SLPAMetricSum = 0
					OSLOMMetricSum = 0
					CFINDERMetricSum = 0
					COPRAMetricSum = 0
					GCEMetricSum = 0
					OLMetricSum = 0
					for i in range(1, 11):
						print "  	i {0}".format(i)
					

		#Ovelapping Louvain
						bestMetric = 0.0
						for k in range(1, 2):
							for betta in ["1.01","1.02","1.03","1.04","1.05","1.06","1.07","1.08","1.09","1.1","1.2","1.3","1.4"]:
								metric = GetMetricResultFromFile('../../benchmarks/binary_networks/N5000' + commsSize+ '/ONp' + onp+ '/OM' + str(om) + '/' + str(i) + '/metrics/' + metricName + '/O-Louvain/' + str(k) +'/betta' + betta + '.dat')
								if metric > bestMetric:
									bestMetric = metric
							print bestMetric
							OLMetricSum += bestMetric
	

		#SLPA
						bestMetric = 0.0
						for k in range(1, 11):
							for r in ["0.01", "0.05", "0.1", "0.15", "0.2", "0.25", "0.3", "0.35", "0.4", "0.45", "0.5"]:
								metric = GetMetricResultFromFile('../../benchmarks/binary_networks/N5000' + commsSize+ '/ONp' + onp+ '/OM' + str(om) + '/' + str(i) + '/metrics/' + metricName + '/SLPA/' + str(k) + '/r' + r + '.dat')
								if metric > bestMetric:
									bestMetric = metric
							SLPAMetricSum += bestMetric
						
		#OSLOM
						bestMetric = 0.0
						metric = GetMetricResultFromFile('../../benchmarks/binary_networks/N5000' + commsSize+ '/ONp' + onp+ '/OM' + str(om) + '/' + str(i) + '/metrics/' + metricName + '/OSLOM/tp.dat')
						if metric > bestMetric:
							bestMetric = metric
						tp=1
						while os.path.isfile('../../benchmarks/binary_networks/N5000' + commsSize+ '/ONp' + onp+ '/OM' + str(om) + '/' + str(i) + '/metrics/' + metricName + '/OSLOM/tp' + str(tp) + '.dat'):
							metric = GetMetricResultFromFile('../../benchmarks/binary_networks/N5000' + commsSize+ '/ONp' + onp+ '/OM' + str(om) + '/' + str(i) + '/metrics/' + metricName + '/OSLOM/tp' + str(tp) + '.dat')
							if metric > bestMetric:
								bestMetric = metric
							tp+=1
						OSLOMMetricSum += bestMetric
						
		#CFinder
						bestMetric = 0.0
						k = 3
						while os.path.isfile('../../benchmarks/binary_networks/N5000' + commsSize+ '/ONp' + onp+ '/OM' + str(om) + '/' + str(i) + '/metrics/' + metricName + '/CFinder/CFinder' + str(k) + '.dat'):
							metric = GetMetricResultFromFile('../../benchmarks/binary_networks/N5000' + commsSize+ '/ONp' + onp+ '/OM' + str(om) + '/' + str(i) + '/metrics/' + metricName + '/CFinder/CFinder' + str(k) + '.dat')
							if metric > bestMetric:
								bestMetric = metric
							k += 1
						CFINDERMetricSum += bestMetric
					
		#COPRA
#						bestMetric = 0.0
#						for k in range(1, 11):
#							metric = GetMetricResultFromFile('../../benchmarks/binary_networks/N5000' + commsSize+ '/ONp' + onp+ '/OM' + str(om) + '/' + str(i) + '/metrics/' + metricName + '/COPRA/COPRA-best-V-' + str(k) + '.dat')
#							if metric > bestMetric:
#								bestMetric = metric
#						COPRAMetricSum += bestMetric 
					
		#GCE
						bestMetric = 0.0
						for k in range(3, 9):
							metric = GetMetricResultFromFile('../../benchmarks/binary_networks/N5000' + commsSize+ '/ONp' + onp+ '/OM' + str(om) + '/' + str(i) + '/metrics/' + metricName + '/GCE/minimumCliqueSize' + str(k) + '.dat')
							if metric > bestMetric:
								bestMetric = metric
						GCEMetricSum += bestMetric 
					
					output.write('O-Louvain ' + str(OLMetricSum/10)+'\n')
					output.write('GCE ' + str(GCEMetricSum/10)+'\n')						
					output.write('COPRA ' + str(COPRAMetricSum/10)+'\n')					
					output.write('CFinder ' + str(CFINDERMetricSum/10)+'\n')					
					output.write('OSLOM ' + str(OSLOMMetricSum/10)+'\n')					
					output.write('SLPA ' + str(SLPAMetricSum/100)+'\n\n')
	output.close()


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
    return sum/float(M)

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
    for v in range(1, len(nodes)+1) :
        #get comms of v in both C1 and C2
        if  Node2Comm1.get(v) == None :
             Node2Comm1[v] = []
        if  Node2Comm2.get(v) == None :
             Node2Comm2[v] = []
        vComms1 = Node2Comm1[v]
        vComms2 = Node2Comm2[v]
        for u in range(v, len(nodes)+1):
            #get comms of u in both C1 and C2
            if  Node2Comm1.get(u) == None :
                 Node2Comm1[u] = []
            if  Node2Comm2.get(u) == None :
                 Node2Comm2[u] = []

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

def AmountOfSharedCommsToAmountOfPairsOfNodesV2(Node2Comm1, Node2Comm2, comm2Nodes1, comm2Nodes2, M):
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
    amountOfNodes= len(nodes)
    totalCouplesCovered=0
    for v in range(1, amountOfNodes) :
        #get comms of v in both C1 and C2
        vComms1 = Node2Comm1[v]
        vComms2 = Node2Comm2.get(v) or set()

        # deal only with nodes which are relevant to v
        nodesReleventToVin1 = set()

        for comm in vComms1:
            nodesReleventToVin1= nodesReleventToVin1.union(set(comm2Nodes1[comm]))

        nodesReleventToVin2 = set()

        for comm in vComms2:
            nodesReleventToVin2 = nodesReleventToVin2.union(set(comm2Nodes2[comm]))

        nodesReleventToV = nodesReleventToVin1.union(nodesReleventToVin2)
        
        nodesReleventToV=set(filter(lambda x:x>v,nodesReleventToV))
        totalCouplesCovered += len(nodesReleventToV)
        for u in nodesReleventToV:
            #get comms of u in both C1 and C2
            uComms1 = Node2Comm1[u]
            uComms2 = Node2Comm2.get(u) or set()

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



    # deal with the nodes which doesnt have any shared comms with v
    if ans.get(0) == None :
            ans[0] = [0,0,0]
    couplesNotCovered = M - totalCouplesCovered
    ans[0][0] += couplesNotCovered
    ans[0][1] += couplesNotCovered
    ans[0][2] += couplesNotCovered

    return ans

def ListOfNodesToMappings(inputPath):
    node2comms= dict()
    comm2nodes= dict()
    listOfNodesFile = open(inputPath, 'r')
    listsOfNodes = listOfNodesFile.readlines()
    listOfNodesFile.close()
    commId = 0
    for comm in listsOfNodes:
	commId += 1
        nodes = comm.replace(' \n', '').split(' ')
        comm2nodes[commId] = map(int, nodes)
        for node in nodes:
            if node2comms.get(int(node)) == None :
                node2comms[int(node)] = []
            node2comms[int(node)].append(commId)
    return (node2comms, comm2nodes)

def OmegaIndex(listOfNodes1Path, listOfNodes2Path, outputPath):
    '''
    Calcs Omega index as in "Overlapping Community Detection in Networks: The State-of-the-Art and Comparative Study"
    '''
    
    Node2Comm1, Comm2Nodes1 = ListOfNodesToMappings(listOfNodes1Path)
    Node2Comm2, Comm2Nodes2 = ListOfNodesToMappings(listOfNodes2Path)
    n = len(Node2Comm1.keys())
    #amount of nodes pairs
    M = n*(n-1)/2
    amountsOfNodesWithSameAmountOfComms =  AmountOfSharedCommsToAmountOfPairsOfNodesV2(Node2Comm1,Node2Comm2, Comm2Nodes1, Comm2Nodes2, M)
    Wu = UnadjustedOmegaIndex(M,amountsOfNodesWithSameAmountOfComms)
    We = ExpectedOmegaIndex(M,amountsOfNodesWithSameAmountOfComms)  
    output = open(outputPath, 'a')
    output.write( 'OmegaIndex:\t' + str((Wu-We)/(1-We)))
    output.close()


'''''''''''''''''''''''''''''''''''''''''''''''''''

                AVERAGE F1 SCORE

'''''''''''''''''''''''''''''''''''''''''''''''''''
def precision(guess,truth):
    return len(guess.intersection(truth))/float(len(truth))

def recall(guess,truth):
    return len(guess.intersection(truth))/float(len(guess))

def H(a,b):
    if a+b==0:
        return 0
    return 2*a*b/float((a+b))

def F1(guess,truth):
    return H(precision(guess,truth),recall(guess,truth))

def FindBestMatchingInGroundTruth(c1, GroundTruth):
    best = 0
    for truth in GroundTruth:
        f1 = F1(c1,truth)
        if f1>best:
            best = f1
    return best

def FindBestMatchingInComms1(trueComm, Comms1):
    best = 0
    for c1 in Comms1:
        f1 = F1(c1,trueComm)
        if f1>best:
            best = f1
    return best

def CalcPartialAverageF1Part1(Comms1,GroundTruth):
    ans = 0
    for c1 in Comms1:
        ans = ans + FindBestMatchingInGroundTruth(c1, GroundTruth)
    return ans / float(2*len(Comms1))

def CalcPartialAverageF1Part2(Comms1, GroundTruth):
    ans = 0
    for trueComm in GroundTruth:
        ans = ans + FindBestMatchingInComms1(trueComm, Comms1)
    return ans / float(2*len(GroundTruth))

def AverageF1(Comms1Path,GroundTruthPath, outputPath):    
    Comms1File = open(Comms1Path, 'r')
    ListOfComms1 = Comms1File.readlines()
    Comms1File.close()    
    
    Comms1 = []
    for nodes in ListOfComms1:
      Comms1.append(set(nodes.replace(' \n', '').split(' ')))
        
    GroundTruthFile = open(GroundTruthPath, 'r')
    ListOfGroundTruthComms = GroundTruthFile.readlines()
    GroundTruthFile.close()
    
    GroundTruth = []
    for nodes in ListOfGroundTruthComms:
      GroundTruth.append(set(nodes.replace(' \n', '').split(' ')))
    
    part1 = CalcPartialAverageF1Part1(Comms1, GroundTruth)
    part2 = CalcPartialAverageF1Part2(Comms1, GroundTruth)     
    ans = part1 + part2
    output = open(outputPath, 'a')
    output.write( 'AverageF1Score:\t' + str(ans))
    output.close()
 
