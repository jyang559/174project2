import csv
import pandas as pd
import queue
import collections
import time

#begin class and function definition
class adjacency_list:
    def __init__(self):
        self.vertices = {}  #Dictionary (Hashtable) that will store all the vertices and edge information as well as its weight

        #Bibfs begins
        self.level = 0  #keeps track of when each node was found. This helps to determine who is closes in the case where multiple intersection nodes are found
        self.step = 1 #for conversion of weighted graph
        self.firstToFindSource = {} #dictionary (hashtable) to keep track of who was the first to find targeted vertex within the source frontier
        self.firstToFindDest = {}   #dictionary (hashtable) to keep track of who was the first to find targeted vertex within the source frontier
        self.queue_BibfsSource = queue.Queue()  #Source queue (frontier for source)
        self.queue_BibfsDest = queue.Queue()    #Destination queue (frontier for destination)
        self.foundSource = {}   #Dictionary keeping track of the vertices founded by source Bidirectional bfs
        self.foundDest = {}     #Dictionary keeping track of the vertices founded by destination Bidirectional bfs
        self.intersectingNodes = [] #List containing the node at which the source and destination bidirectional bfs meet
        #Bibfs end

    #add_edge function also initializes the hashtable to be used in the bidirectional bfs.
    #the term "vertex" and "node" is being used interchangably
    def add_edge(self, node1, node2, weight):
        if self.vertices.get(node1) is None: #checks to see if such key(vertex) exist already within the dictionary (hashtable)
            #In the case that the key(vertex) doesn't exist within the hashtable, one is created for it.
            #Note that the key(in this case node1) is assigned another dictionary(hashtable). self.vertices is now essentially a dictionary of dictionary (hashtable of hashtable)
            self.vertices[node1] = {}
        if self.vertices.get(node2) is None:
            self.vertices[node2] = {}
        #Because self.vertices is a hashtable of hashtable, we don't need to be concern with indices of node.
        #Example: self.vertices[A][B] will give us the edge weight connecting vertex A and B together if such an edge exist.
        #Weight is in list form, index 0 will be used in step calculation, index 1 will be used in distance calculation of path
        #Because we are assuming an undirected graph, both vertex node1 and node2 are assigned the same weight.
        self.vertices[node1][node2] = [weight,weight]
        self.vertices[node2][node1] = [weight,weight]

    #exploring_Bibfs function figures out which vertex are connected to the current sourceNode and destNode.
    #Depending on the edge weight of their connections, a new node can be pushed into their respective queue.
    def exploring_Bibfs(self,sourceNode,destNode):
        weight = 0 #This variable is a place holder intended to act as an index for the list structure being used to hold the weight of an edge.
        alreadyQueuedSource = False #This is a boolean variable used in the step calculation of edges with weight greater than 1
        for adjNodeSource in self.vertices[sourceNode]: #self.vertices[1][4] means that there is an edge from vertex 1 to 4. Thus adjNodeSource are all the nodes(vertex) connected to the source node
            self.vertices[sourceNode][adjNodeSource][weight] -= self.step #Initial calculation to reduce the edge weight between sourceNode and the current adjacent node within the loop
            if(self.vertices[sourceNode][adjNodeSource][weight] <= 0): #After the initial calculation, if the edge weight is less than or equal to 0 then proceed with exploration process
                #exploration process to find new nodes continues
                if self.firstToFindSource.get(adjNodeSource) is None: #Initial check to see if the adjacent node has a founder
                    self.firstToFindSource[adjNodeSource] = sourceNode #In the case that it doesn't, it is assigned a founder who is the sourceNode
                if self.foundSource.get(adjNodeSource) is None: #Initial check to see if the adjacent node has already been found
                    self.foundSource[adjNodeSource] = self.level #The adjacent node is added as a key into the self.foundSource dictionary with a value of the current level of exploration
                    self.queue_BibfsSource.put(adjNodeSource) #The adjacent node is then pushed into the source queue.
                    #Checks for intersection begins:
                    if self.foundDest.get(adjNodeSource) is not None: #This line checks the destiantion's found hashtable to see if it's already found the current adjacent node
                        #In the case that the destination Bibfs has already found the adjacent node
                        if(len(self.intersectingNodes) > 0 and self.foundDest[adjNodeSource] < self.foundDest[self.intersectingNodes[0]]): #This ensures that the head of the intersection list will always contain the shortest path vertex
                            self.intersectingNodes[0] = adjNodeSource
                        else:
                            self.intersectingNodes.append(adjNodeSource)
                    #Checks for intersection ends:
                #exploration process to find new nodes ends
            else: #In the case that edge greater than 0
                if alreadyQueuedSource: #This checks the initially declared false boolean to determine if the current sourceNode should be added to the queue again
                    #In the case that the sourceNode has already been pushed into the queue, we simply subtract the weight of its adjacent node
                    self.vertices[adjNodeSource][sourceNode][weight] -= self.step
                else: #This is the case where the current sourceNode has not be pushed back into the source queue.
                    alreadyQueuedSource = True
                    self.queue_BibfsSource.put(sourceNode) #pushes the sourceNode back into the queue, only once.
                    self.vertices[adjNodeSource][sourceNode][weight] -= self.step

        #Begins performing the same exploration logic but for the Destination node (destNode)
        alreadyQueuedDest = False
        for adjNodeDest in self.vertices[destNode]:
            self.vertices[destNode][adjNodeDest][weight] -= self.step
            if(self.vertices[destNode][adjNodeDest][weight] <= 0):

                if self.firstToFindDest.get(adjNodeDest) is None:
                    self.firstToFindDest[adjNodeDest] = destNode
                if self.foundDest.get(adjNodeDest) is None:
                    self.foundDest[adjNodeDest] = self.level
                    self.queue_BibfsDest.put(adjNodeDest)
                    if self.foundSource.get(adjNodeDest) is not None:
                        if(len(self.intersectingNodes) > 0 and self.foundSource[adjNodeDest] < self.foundSource[self.intersectingNodes[0]]):
                            self.intersectingNodes[0] = adjNodeDest
                        else:
                            self.intersectingNodes.append(adjNodeDest)
            else:
                if alreadyQueuedDest:
                    self.vertices[adjNodeDest][destNode][weight] -= self.step
                else:
                    alreadyQueuedDest = True
                    self.queue_BibfsDest.put(destNode)
                    self.vertices[adjNodeDest][destNode][weight] -= self.step
        #Ends performing the same exploration logic but for the Destination node (destNode)

        self.level += 1 #This variable keeps a record of when each node is found. Helps determine which intersection is shorter in the case of many intersections.

    #runBibfs function sets up intitial parameters needed to perform Bidirectional bfs, which it received as arguments.
    def runBibfs(self,sourceNode,destNode):
        #Begin initial set up for Bibfs
        self.queue_BibfsSource.put(sourceNode) #Pushes the sourceNode into the source queue
        self.queue_BibfsDest.put(destNode) #Pushes the destNode into the dest queue
        self.foundSource[sourceNode] = self.level #initial setup stating that sourceNode found itself at self.level of exploration
        self.foundDest[destNode] = self.level   #initial setup stating that destNode found itself at self.level of exploration
        self.firstToFindSource[sourceNode] = sourceNode #initial setup stating that sourceNode was the first to find iteslf.
        self.firstToFindDest[destNode] = destNode #initial setup stating that destNode was the first to find iteslf.
        #End initial set up for Bibfs
        #This while loop is constrained to 3 conditions:
        #1.) source queue must not be empty
        #2.) dest queue must not be empty
        #3.) No intersecting node has been found yet
        #In the case that any of these condition are violated, the while loop exits.
        while not self.queue_BibfsSource.empty() and not self.queue_BibfsDest.empty() and len(self.intersectingNodes) == 0:
            currentNodeExSource = self.queue_BibfsSource.get() #pops the head of the source queue
            currentNodeExDest = self.queue_BibfsDest.get() #pops the head of the dest queue
            self.exploring_Bibfs(currentNodeExSource,currentNodeExDest) #These nodes from their resepctive queues are then passed into the exploration function
        if len(self.intersectingNodes) > 0: #In the case that their were an intersection found
            #print(len(self.intersectingNodes))
            print(f"vertex {sourceNode} path to vertex {destNode} intersects at {self.intersectingNodes[0]}")
        #print(self.firstToFindSource)
        #print(self.firstToFindDest)
        #print(self.intersectingNodes)

        #Constructing the Shortest Path
        vertexSource = self.intersectingNodes[0]
        vertexDest = self.intersectingNodes[0]
        sourcePath = []
        destPath = []
        sourcePath.append(vertexSource) #assumes the intersecting node was discovered by the source. Not always true however
        while vertexSource != sourceNode:
            nextVertexSource = self.firstToFindSource[vertexSource]
            sourcePath.append(nextVertexSource)
            vertexSource = nextVertexSource
        sourcePath.reverse()
        print(f"source path {sourcePath}")

        while vertexDest != destNode:
            nextVertexDest = self.firstToFindDest[vertexDest]
            destPath.append(nextVertexDest)
            vertexDest = nextVertexDest
        print(f"dest path {destPath}")

        shortestPath = sourcePath + destPath
        print(f"The shortest path from vertex {sourceNode} to vertex {destNode} is {shortestPath}")
        totalWeight = 0
        for ind in range(len(shortestPath) - 1):
            totalWeight += self.vertices[shortestPath[ind]][shortestPath[ind+1]][1]
        print(f'Weight of the shortest path from {sourceNode} to {destNode} is {totalWeight}')

#end class and function definition

adj_list = adjacency_list()
edgeArray = []
#file = 'n1024-l1.tsv'
#file = 'data.csv'
#file = 'data4.csv'
#file = 'data2.csv'
#file = 'https://raw.githubusercontent.com/DicheDiez10/TestProject/main/CSCI_174_Nodes_and_Weights.csv'
file = 'https://raw.githubusercontent.com/DicheDiez10/TestProject/main/CampusTopLeft.csv'

CSV_DATA = pd.read_csv(file,sep=",")

edgeArray = CSV_DATA.values.tolist()

for ind in edgeArray:
    node1,node2,weight = ind
    adj_list.add_edge(node1,node2,weight)

time1 = time.perf_counter()
adj_list.runBibfs(1,172)
time2 = time.perf_counter()
total_time = time2 - time1
print(f"total time = {total_time} seconds")
