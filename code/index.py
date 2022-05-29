from boat import Boat
from graph import Graph
from node import CrossingNode

import heapq

from argparse import ArgumentParser
import os
import sys

from time import time

def printSolution(file, currentNode, time, maxStackNodes,maxComputedNodes ):
    print("Solution:\n")
    currentNode.printPath()
    print("Time:", str(time), "miliseconds \n")
    print("Maximum number of nodes in memory:", maxStackNodes, "\n")
    print("Maximum number of computed nodes:", maxComputedNodes, "\n")
    print("Cost: ", currentNode.f, "\n")
    print("Length: ", len(currentNode.getPath()), "\n")

def aStar(file):
    boat = Boat({
        "wolves": 0,
        "goats": 0,
        "cabbages": 0
    },
        {
            "wolves": 0,
            "goats": 0,
            "cabbages": 0
        })
    startNode = CrossingNode(
        None, Graph.initialBoatPosition, Graph.east, Graph.west, Graph.store, boat
    )
    maxStackNodes = 1
    maxComputedNodes = 1
    startTime = time()

    openList = [startNode]
    while len(openList) > 0:
        currentIndex = 0
        currentNode = openList.pop(currentIndex)

        # Reached final state
        if currentNode.isFinalState():
            endTime = time()
            printSolution(file, currentNode, round(endTime - startTime, 4), maxStackNodes, maxComputedNodes)
            return

        successors = currentNode.getSuccessors()
        maxComputedNodes += len(successors)
        for successor in successors:
            if any(successor == item for item in openList):
                continue
            index = 0
            foundPlace = False
            for index in range(len(openList)):
                if openList[index].f > successor.f:
                    foundPlace = True
                    break
            if foundPlace:
                openList.insert(index, successor)
            else:
                openList.append(successor)
        maxStackNodes = max(maxStackNodes, len(openList))

def astarOptimized(file):

    boat = Boat( {
        "wolves": 0,
        "goats": 0,
        "cabbages": 0
    },
     {
        "wolves":0,
        "goats": 0,
        "cabbages": 0
    })
    startNode = CrossingNode(
        None, Graph.initialBoatPosition, Graph.east, Graph.west, Graph.store, boat
    )

    lopen = [startNode]
    lclose = []
    maxStackNodes = 1
    maxComputedNodes = 1
    startTime = time()

    while len(lopen) > 0:
        currentNode = lopen.pop(0)
        lclose.append(currentNode)

        if currentNode.isFinalState():
            endTime = time()
            printSolution(file, currentNode, round(endTime - startTime, 4), maxStackNodes, maxComputedNodes)
            # -1
            # 00->return
            return

        successors = currentNode.getSuccessors()
        maxComputedNodes += len(successors)

        for successor in successors:
            foundOpen = False
            for node in lopen:
                if node == successor:
                    foundOpen = True
                    if successor.f < node.f:  # will eliminiate from open and then add the current node in open
                        if node in lopen:
                            lopen.remove(node)
                    else:
                        if successor in successors:
                            successors.remove(successor)
                    break
            if foundOpen == False:  # will search it in lclose
                for node in lclose:
                    if successor == node:
                        if successor.f < node.f:
                            lclose.remove(node)
                        else:
                            successors.remove(successor)
                        break
        for successor in successors:  # add them in lopen as we keep the order --> order ascendinf f && desc g
            foundPlace = False

            for place in range(len(lopen)):
                if lopen[place].f > successor.f or (
                        lopen[place].f == successor.f and lopen[place].g <= successor.g):
                    foundPlace = True
                    break
            if foundPlace == True:
                lopen.insert(place, successor)

            else:
                lopen.append(successor)
        maxStackNodes = max(maxStackNodes, len(lopen) + len(lclose))

def BF(file, nrSearchedSolutions):
    boat = Boat({
        "wolves": 0,
        "goats": 0,
        "cabbages": 0
    },
        {
            "wolves": 0,
            "goats": 0,
            "cabbages": 0
        })
    startNode = CrossingNode(
        None, Graph.initialBoatPosition, Graph.east, Graph.west, Graph.store, boat
    )
    maxStackNodes = 1
    maxComputedNodes = 1 #all successors generated
    queueNodes = [startNode]
    startTime = time()
    while len(queueNodes) != 0:
        # print("Actual queue: " + str(queueNodes))
        currentNode = queueNodes.pop()
        if (currentNode.isFinalState()):
            endTime = time()
            printSolution(file, currentNode, round(endTime - startTime, 4),maxStackNodes,maxComputedNodes)
            nrSearchedSolutions -= 1
            if nrSearchedSolutions == 0:
                return 0
            else:
                print("========================================\n")
        succesors = currentNode.getSuccessors()

        queueNodes.extend(succesors)
        maxComputedNodes += len(succesors)
        maxStackNodes = max(maxStackNodes, len(queueNodes))

def depthFirst(file, nrSearchedSolutions):
    startTime = time()
    boat = Boat({
        "wolves": 0,
        "goats": 0,
        "cabbages": 0
    },
        {
            "wolves": 0,
            "goats": 0,
            "cabbages": 0
        })
    startNode = CrossingNode(
        None, Graph.initialBoatPosition, Graph.east, Graph.west, Graph.store, boat
    )
    maxComputedNodes = 1
    maxStackNodes = 1
    DF(file, nrSearchedSolutions, startTime, startNode, maxStackNodes, maxComputedNodes)

def DF(file, nrSearchedSolutions, startTime, currentNode, maxStackNodes, maxComputedNodes):
    if currentNode.isFinalState():
        endTime = time()
        printSolution(file, currentNode, round(endTime - startTime, 4), maxStackNodes, maxComputedNodes)
        nrSearchedSolutions -= 1
        if nrSearchedSolutions == 0:
            return nrSearchedSolutions
        else:
            print("========================================\n")

    successors = currentNode.getSuccessors()
    maxComputedNodes += len(successors)
    maxStackNodes = max(maxStackNodes, len(successors)) #df memorates just one path

    for successor in successors:
        if nrSearchedSolutions != 0:
            nrSearchedSolutions = DF(file, nrSearchedSolutions, startTime, successor, maxStackNodes, maxComputedNodes)
    return nrSearchedSolutions

def depth_first_iterative(file, nrSearchedSolutions, currentNode, depth,  maxStackNodes, maxComputedNodes):
    if depth == 1 and currentNode.isFinalState():  #at the last step for the current searched depth
        endTime = time()
        printSolution(file, currentNode, round(endTime - startTime, 4), maxStackNodes, maxComputedNodes)
        nrSearchedSolutions -= 1
        if nrSearchedSolutions == 0:
            return nrSearchedSolutions
        else:
            print("========================================\n")
    if depth > 1:
        succesors = currentNode.getSuccessors()
        maxComputedNodes += len(succesors)
        maxStackNodes = max(maxStackNodes, len(succesors))
        for succesor in succesors:
            if nrSearchedSolutions != 0:
                nrSearchedSolutions = depth_first_iterative(file,nrSearchedSolutions, succesor, depth - 1,  maxStackNodes, maxComputedNodes)
    return nrSearchedSolutions

# dfs but with a maximum depth --> combination with bfs
# it will remake all the previous trees but at least we will not have problems with the memory
def DFI(file, nrSearchedSolutions):
    startTime = time()
    maxComputedNodes = 1
    maxStackNodes =1
    for depth in range(1, 100): #the maximum length
        if nrSearchedSolutions == 0: #at the previous call we have finished all the the searches
            return
        boat = Boat({
            "wolves": 0,
            "goats": 0,
            "cabbages": 0
        },
            {
                "wolves": 0,
                "goats": 0,
                "cabbages": 0
            })
        startNode = CrossingNode(None, Graph.initialBoatPosition, Graph.east, Graph.west, Graph.store, boat)
        nrSearchedSolutions = depth_first_iterative(file, nrSearchedSolutions, startNode, depth,  maxStackNodes, maxComputedNodes)

def ida_star(nrSearchedSolutions = 1):
    boat = Boat({
        "wolves": 0,
        "goats": 0,
        "cabbages": 0
    },
        {
            "wolves": 0,
            "goats": 0,
            "cabbages": 0
        })
    startNode = CrossingNode(
        None, Graph.initialBoatPosition, Graph.east, Graph.west, Graph.store, boat
    )
    limit = startNode.f
    while True: #while we are in the limit and still haven't find the nr of solutions
        nrSearchedSolutions, result = buildPath(startNode, limit, nrSearchedSolutions)
        if result == "finished":
            break
        if result == float('inf'):
            print("No more solutions")
            break
        limit = result

def buildPath(currentNode, limit, nrSearchedSolutions):
    print(currentNode)
    if currentNode.f > limit: #we can not extend this node
        return nrSearchedSolutions, currentNode.f #the new limit --> will choose the highest from all
    if currentNode.isFinalState() and currentNode.f == limit:
        print("Solution:")
        currentNode.printPath()
        nrSearchedSolutions -= 1
        if nrSearchedSolutions == 0:
            return 0, "finished"
    successors = currentNode.getSuccessors()
    minim = float('inf')
    for successor in successors: #try to extend every child
        nrSearchedSolutions, result = buildPath(successor, limit, nrSearchedSolutions)
        if result == "finished":
            return 0, "finished" #to go back at the initial call
        if result < minim:
            minim = result #calculate the minim of all limits
    return nrSearchedSolutions, minim

def allAlgo(file, nrsol):
    if not Graph.veifyInput():
        file.write("There is no solution")
        return
    # file.write("-------------------- BFS --------------------\n")
    # feedback = BF(file, nrsol)
    # file.write(str(feedback) + '\n')
    # file.write("-------------------- END BFS --------------------\n\n")

    file.write("-------------------- DFS --------------------\n")
    depthFirst(file, nrsol)
    file.write("-------------------- END DFS --------------------\n\n")

    # file.write("-------------------- ITERATIVE DFS --------------------\n")
    # DFI(file, nrsol)
    # file.write("-------------------- END ITERATIVE DFS --------------------\n\n")

    # file.write("-------------------- A* --------------------\n")
    # aStar(file)
    # file.write("-------------------- END A* --------------------\n\n")

    # file.write("-------------------- A* OPTIMIZED --------------------\n")
    # astarOptimized(file)
    # file.write("-------------------- END A* OPTIMIZED --------------------\n\n")



if __name__ == "__main__":
    graph = None

    parser = ArgumentParser()
    parser.add_argument("-in_file", "--input_folder", dest = "inputFolder", help = "Path to input")
    parser.add_argument("-out_file", "--output_folder", dest = "outputFolder", help = "Path to output")
    parser.add_argument("-nsol", dest = "nsol", help = "The desired number of solutions")
    parser.add_argument("-heur", dest = "heuristic", help = "The heuristic used")
    #parser.add_argument("-t", dest = "timeout", help = "The timeout")
    args = vars(parser.parse_args())

    inputFolder = args["inputFolder"]
    outputFolder = args["outputFolder"]
    nsol = int(args["nsol"])

    #get all input files
    inputFiles = os.listdir(inputFolder)

    #create if it doesn't exist
    if not os.path.exists(outputFolder):
        os.mkdir(outputFolder)

    #concatenate / at the end
    if inputFolder[-1] != '/':
        inputFolder += '/'
    if outputFolder[-1] != '/':
        outputFolder += '/'

    startTime = time()
    for(index, currentFile) in enumerate (inputFiles):
        outPath = outputFolder + "output" + str(index + 1)
        inPath = inputFolder + currentFile
        f = open(outPath, "w+")
        try:
            graph = Graph(inPath)
            allAlgo(f, nsol)
        except Exception as e:
            print(str(e))


