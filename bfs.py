import csv
import pandas as pd
import queue
import collections
import time


class adjacency_list:
    def __init__(self):
        self.vertices = {}

        # #Regular bfs begin
        # self.firstToFind = {}
        # self.queue_bfs = queue.Queue()
        # self.visited = {} #Not really needed, just there to demonstrate where a found node came from
        # self.found = {}
        # #Regular bfs end

        #Bibfs begins
        self.level = 0  #keeps track of when each node was found. This helps to determine who is closes in the case where multiple intersection nodes are found
        self.step = 1 #for conversion of weighted graph
        self.firstToFindSource = {}
        self.firstToFindDest = {}
        self.queue_BibfsSource = queue.Queue()
        self.queue_BibfsDest = queue.Queue()
        #self.visitedSource = {}
        #self.visitedDest = {}
        self.foundSource = {}
        self.foundDest = {}
        self.intersectingNodes = []
        #Bibfs end

    def add_node(self, node):
        self.vertices[node] = {}

        #Regular bfs begin
    #    self.firstToFind[node] = None
    #    self.found[node] = False
    #    self.visited[node] = False #Not really needed, just there to demonstrate where a found node came from
        #Regular bfs end


    def add_edge(self, node1, node2, weight):
        #self.vertices[node1].append([node2,weight])
        if self.vertices.get(node1) is None:
            self.vertices[node1] = {}
        if self.vertices.get(node2) is None:
            self.vertices[node2] = {}
        self.vertices[node1][node2] = weight
        self.vertices[node2][node1] = weight

    # def exlporing_bfs(self, node):
    #     for adjNode in self.vertices[node]:
    #         if self.firstToFind.get(adjNode[0]) is None:
    #             self.firstToFind[adjNode[0]] = node
    #         #if adjNode[0] not in self.found:
    #         if self.found.get(adjNode[0]) is None:
    #             #self.found.append(adjNode[0])
    #             self.found[adjNode[0]] = True
    #             self.queue_bfs.put(adjNode[0])
    #     #print(self.queue_bfs.queue)
    #     print(f"visited {self.visited}") #Not really needed, just there to demonstrate where a found node came from
    #     print(f"found {self.found}")

    # def runBFS(self,node):
    #     self.queue_bfs.put(node)
    #     self.found[node] = True
    #     self.firstToFind[node] = node
    #     #print(self.queue_bfs.queue)
    #     while not self.queue_bfs.empty():
    #         currentNodeEx = self.queue_bfs.get()
    #         self.visited[currentNodeEx] = True #Not really needed, just there to demonstrate where a found node came from
    #         self.exlporing_bfs(currentNodeEx)
    #     print(self.firstToFind)


    def exploring_Bibfs(self,sourceNode,destNode):
        #print(self.vertices[sourceNode])
        # self.vertices[sourceNode][0][1] -= self.step
        # if(self.vertices[sourceNode][0][1] <= 0):
        #     print("gucci gang")
        #quit()


        alreadyQueuedSource = False
        for adjNodeSource in self.vertices[sourceNode]: #self.vertices[1][4] means that there is an edge from vertex 1 to 4. Thus adjNodeSource is all the edge from sourceNode to other nodes
            #print(self.vertices[sourceNode][adjNodeSource]) #this gets the weight
            #quit()
            #print(self.vertices[sourceNode][adjNodeSource])
            self.vertices[sourceNode][adjNodeSource] -= self.step
            #print(f"from Source vertex {sourceNode} to vertex {adjNodeSource} distance is {self.vertices[sourceNode][adjNodeSource]}")

            #print(self.queue_BibfsSource.queue)
            #print(self.vertices[adjNodeSource][sourceNode])
            if(self.vertices[sourceNode][adjNodeSource] <= 0):
                #print("yessir")
            #print("quit it!")
            #quit()

                if self.firstToFindSource.get(adjNodeSource) is None:
                    self.firstToFindSource[adjNodeSource] = sourceNode
                if self.foundSource.get(adjNodeSource) is None:
                    self.foundSource[adjNodeSource] = self.level
                    self.queue_BibfsSource.put(adjNodeSource)
                    if self.foundDest.get(adjNodeSource) is not None:
                        if(len(self.intersectingNodes) > 0 and self.foundDest[adjNodeSource] < self.foundDest[self.intersectingNodes[0]]):
                            self.intersectingNodes[0] = adjNodeSource
                        else:
                            self.intersectingNodes.append(adjNodeSource)
            else:
                if alreadyQueuedSource:
                    self.vertices[adjNodeSource][sourceNode] -= self.step
                    #print(self.vertices[adjNodeSource][sourceNode])
                else:
                    alreadyQueuedSource = True
                    self.queue_BibfsSource.put(sourceNode)
                    self.vertices[adjNodeSource][sourceNode] -= self.step
                    #print(self.vertices[adjNodeSource][sourceNode])

        # if alreadyQueuedSource:
        #     self.queue_BibfsSource.put(sourceNode)
        # print(f"source queue {self.queue_BibfsSource.queue}")
            #quit()

        alreadyQueuedDest = False
        for adjNodeDest in self.vertices[destNode]:
            self.vertices[destNode][adjNodeDest] -= self.step
            #print(f"from Destination vertex {destNode} to vertex {adjNodeDest} distance is {self.vertices[destNode][adjNodeDest]}")
            if(self.vertices[destNode][adjNodeDest] <= 0):

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
                    self.vertices[adjNodeDest][destNode] -= self.step
                    #print(self.vertices[adjNodeDest][destNode])
                else:
                    alreadyQueuedDest = True
                    self.queue_BibfsDest.put(destNode)
                    self.vertices[adjNodeDest][destNode] -= self.step
                    #print(self.vertices[adjNodeDest][destNode])

        # if alreadyQueuedDest:
        #     self.queue_BibfsDest.put(destNode)
        # print(f"destination queue {self.queue_BibfsDest.queue}")

        self.level += 1
        pass

    def runBibfs(self,sourceNode,destNode):
        self.queue_BibfsSource.put(sourceNode)
        self.queue_BibfsDest.put(destNode)
        self.foundSource[sourceNode] = True
        self.foundDest[destNode] = True
        self.firstToFindSource[sourceNode] = sourceNode
        self.firstToFindDest[destNode] = destNode
        while not self.queue_BibfsSource.empty() and not self.queue_BibfsDest.empty() and len(self.intersectingNodes) == 0:
            currentNodeExSource = self.queue_BibfsSource.get()
            currentNodeExDest = self.queue_BibfsDest.get()
            self.exploring_Bibfs(currentNodeExSource,currentNodeExDest)
        if len(self.intersectingNodes) > 0:
            print(len(self.intersectingNodes))
            print(f"vertex {sourceNode} path to vertex {destNode} intersects at {self.intersectingNodes[0]}")
        print(self.firstToFindSource)
        print(self.firstToFindDest)
        print(self.intersectingNodes)

        #Constructing the Shortest Path
        vertexSource = self.intersectingNodes[0]
        vertexDest = self.intersectingNodes[0]
        sourcePath = []
        destPath = []
        #print(vertex == sourceNode)
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
        #sourcePath.reverse()
        print(f"dest path {destPath}")

        shortestPath = sourcePath + destPath
        print(f"The shortest path from vertex {sourceNode} to vertex {destNode} is {shortestPath}")


        pass



#time1 = time.perf_counter()
adj_list = adjacency_list()


edgeArray = []
#file = 'n1024-l1.tsv'
#file = 'data.csv'
#file = 'data4.csv'
#file = 'data2.csv'
file = 'https://raw.githubusercontent.com/DicheDiez10/TestProject/main/CSCI_174_Nodes_and_Weights.csv'


CSV_DATA = pd.read_csv(file,sep=",")
edgeArray = CSV_DATA.values.tolist()
#print(edgeArray)
# for ind in edgeArray:
#     adj_list.add_node(ind[0])


for ind in edgeArray:
    node1,node2,weight = ind
    adj_list.add_edge(node1,node2,weight)

#print(adj_list.vertices)
time1 = time.perf_counter()
adj_list.runBibfs(5,3)
time2 = time.perf_counter()
total_time = time2 - time1
print(f"total time = {total_time} seconds")
#adj_list.runBibfs('1','200')
