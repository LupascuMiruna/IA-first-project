import math

from boat import Boat
from graph import Graph


class CrossingNode:
    """
    Class that represents a node in the search tree built when we solve the problem
    Each node contains following information:
        parent - reference to the parent node (None for the startNode)
        boatPosition - "east" or "west" depending where there is the man with the boat
        east - a dictionary with 3 keys
                { "wolves": nrWolves, "goats": nrGoats, "cabbages": nrCabbages}
                containg the number of elemets from the east shore
        west - dictionary same as east but memorates the info about east shore
        store - dictionary same as east, but memoreates the info from the storeHouse
                (just one of them will be non-zero bcs we can not store diffenet products)
        boat - the configuration of the boat at this point
         {"A": {"wolves": nrWolvesA, "goats": nrGoatsA,"cabbages": nrCabbagesA},
          "B": {"wolves": nrWolvesB, "goats": nrGoatsB,"cabbages": nrCabbagesB},
        }

        g - the cost from parent to itself
        h - heuristic factor
        f - value used by A* algorithm f = g + h
        listSuccesors = list of nodes -- its children
    """

    def __init__(self, parent, boatPosition, east, west, store, boat):
        self.east = east
        self.west = west
        self.store = store
        self.boatPosition = boatPosition
        self.parent = parent
        self.boat = boat

        self.g = boat.getCost() if self.parent is None else self.parent.g + boat.getCost()
        self.h = self.getHeuristic(Graph.heuristic)
        self.f = self.g + self.h  # h is estimation until final node

        self.listSuccessors = []

    def getEastState(self):
        """
        :return: a string that it's the configuration of EAST shore
                --containing the number of each product
                --displays the man if he is here
        """
        prefix = ""
        if self.boatPosition == "east":
            prefix = "Taranul "

        return f'{prefix}' \
               f'{self.east["cabbages"]} verze ' \
               f'{self.east["goats"]} capre ' \
               f'{self.east["wolves"]} lupi\n'

    def getStoreState(self):
        """
        :return: the configuration of the storeHouse
        """

        if self.store["goats"]:
            return f'{self.store["goats"]} capre'
        if self.store["wolves"]:
            return f'{self.store["wolves"]} lupi'
        if self.store["cabbages"]:
            return f'{self.store["cabbages"]} verze'
        return 0

    def getWestState(self):
        """
        :return: same as at getEastState but for WEST
        """

        prefix = ""
        if self.boatPosition == "west":
            prefix = "Taranul "

        return f'{prefix}' \
               f'{self.west["cabbages"]} verze ' \
               f'{self.west["goats"]} capre ' \
               f'{self.west["wolves"]} lupi ' \
               f'magazie: {self.getStoreState()}\n'

    def __str__(self):
        eastState = self.getEastState()
        westState = self.getWestState()

        return f'Pe malul de est se gasesc:\n' + \
               eastState + \
               f'Pe malul de vest se gasesc:\n' + \
               westState + \
               f'F :' + str(self.f) + f' G :' + str(self.g) + "\n"

    def __repr__(self):
        eastState = self.getEastState()
        westState = self.getWestState()

        return f'Pe malul de est se gasesc:\n' + \
               eastState + \
               f'Pe malul de vest se gasesc:\n' + \
               westState  + \
               f'F :' + str(self.f) + f' G :' + str(self.g) + "\n"

    def __eq__(self, other):
        return self.east == other.east and self.west == other.west and self.store == other.store

    def isFinalState(self):
        """
        Verifies if there are at least the desired number of each product on west shore
        """
        return self.west["cabbages"] + self.store["cabbages"] >= Graph.finalCabbages and \
               self.west["goats"] + self.store["goats"] >= Graph.finalGoats and \
               self.west["wolves"] + self.store["wolves"] >= Graph.finalWolves

    def getPath(self):
        """
        Goes up on the search tree and returns the path(a list of nodes) that ends with the currentNode
        :return: list of nodes
        """
        path = [self]
        currentNode = self
        while currentNode.parent is not None:
            path.insert(0, currentNode.parent)
            currentNode = currentNode.parent
        return path

    def printPath(self):
        """
        Used with getPath to print all info about the path of currentNode
        """
        path = self.getPath()
        index = 1
        for node in path:
            print(
                f'{index})\n{str(node)}\n' + \
                "------------------\n"
            )
            index += 1

    def getHeuristic(self, heuristic = "basic"):
        """
        Computes the euristic factor, using different criteria
        """
        if heuristic == "basic":    #the minimum number of transports
            boatSubtract = 0
            if self.boatPosition == "east":
                boatSubtract = 1

            return 2 * math.ceil(
                (
                        (Graph.finalCabbages - self.west["cabbages"] - self.store["cabbages"]) +
                        (Graph.finalGoats - self.west["goats"] - self.store["goats"]) +
                        (Graph.finalWolves - self.west["wolves"] - self.store["wolves"])
                ) / (Graph.A + Graph.B)
            ) + (1 - boatSubtract) - 1
        elif heuristic =="heuristic1":  #how much we still have to transfer
            return max(0, Graph.finalCabbages - self.west["cabbages"] - self.store["cabbages"]) + \
                   max(0, Graph.finalGoats - self.west["goats"] - self.store["goats"]) + \
                   max(0, Graph.finalWolves - self.west["wolves"] - self.store["wolves"])
        # elif heuristic == "heuristic2": #less products ate
        #     prod = ["cabbages", "goats", "wolves"]
        #     total = 0
        #     if self.parent == None or self == None:
        #         return 0
        #     for elem in prod:
        #         total += self.parent.west[elem] + self.self.parent.east[elem] + self.parent.store[elem] - \
        #                  self.west[elem] - self.east[elem] - self.store[elem]
        #     return total
        # elif heuristic == "badHeuristic":
        #     boatSubtract = 0
        #     if self.boatPosition == "east":
        #         boatSubtract = 1
        #     return 2 * math.ceil(
        #         (
        #                 (Graph.finalCabbages - self.west["cabbages"] - self.store["cabbages"]) * 100+
        #                 (Graph.finalGoats - self.west["goats"] - self.store["goats"]) * 200+
        #                 (Graph.finalWolves - self.west["wolves"] - self.store["wolves"]) * 300
        #         ) / (Graph.A + Graph.B)
        #     ) + (1 - boatSubtract) - 1
        #

    def inPath(self, newNode):
        """
        verifies if this node has already been visited in the past -- there is in the searc tree
        """
        path = self.getPath()
        if self.parent is not None and newNode == self.parent :
            return True
        for node in path:
            if node.west == newNode.west and node.east == newNode.east and node.store == newNode.store  and node.boatPosition == newNode.boatPosition :
                return True
        return False

    def getOppositeShore(self):
        """
        :return: dictionaryy with the configuration of the shore wehere THERE IS NOT THE BOAT
        """
        if self.boatPosition == "west":
            return self.east.copy()
        else:
            return self.west.copy()

    def getCurrentShoreAmount(self, product):
        """
        The method gets the cantity of the product:
            -east --> just from shore
            -west --> shore + store house
        """
        return getattr(self, self.boatPosition)[product] + (self.store[product] if self.boatPosition == "west" else 0)

    def eat(self, shore):
        """
        The method will perform the eating from the shore given as param
            1) goats will eat as many cabbages they want, or all the cabbages if there are not enogh
            2) wolves will eat as many goats they want, or all the goats if there are not enogh
            2') if there are not any cabbages --> they will eat each other
        :param shore: the shore "east" or "west" from were the products will be ate
        :return: the new dictionary with the configuration of the current shore
        """
        newCabbages = max(0, shore["cabbages"] - Graph.goatsEatCabbages * shore["goats"])
        newGoats = max(0, shore["goats"] - Graph.wolvesEatGoats * shore["wolves"])
        return {
            "cabbages": newCabbages,
            "goats": newGoats,
            "wolves": shore["wolves"]
        }

    def areEnoughProducts(self, east, west, store):
        """
        The method compares the total number(east, west, store) of each product and see if there are at least as many as in the final configuration
        If at least one of them is less, we can not reach final configuration
        """
        totalCabbages = east["cabbages"] + west["cabbages"] + store["cabbages"]
        totalGoats = east["goats"] + west["goats"] + store["goats"]
        totalWolves = east["wolves"] + west["wolves"] + store["wolves"]

        return totalCabbages >= Graph.finalCabbages and totalGoats >= Graph.finalGoats and totalWolves >= Graph.finalWolves

    def generateCombinationsStore(self, cabbagesA, cabbagesB, goatsA, goatsB, wolvesA, wolvesB):
        """
        Params: the configuration of the boat and heuristic used
        We have a configuration of boat with the products that we have just transfered
        Depending on the shore that we are:
            East - the boat has just left east and arrives on west
                 - makes all the possibilites to put in the store the new number of elements
            West - leave west shore
                 - take as many elemets from the shore and if not enough, take from storeHouse as we can pu the desired amount on the boat
                 - idea: take first of all the shore because the products from the storeHouse are safe

        """
        if self.boatPosition == "east":  # left the east shore
            newCabbagesEst = self.east["cabbages"] - (cabbagesA + cabbagesB)
            newGoatsEst = self.east["goats"] - (goatsA + goatsB)
            newWolvesEst = self.east["wolves"] - (wolvesA + wolvesB)

            #get outside everything that we have in store that we can make new combinaition
            newCabbagesWest = cabbagesA + cabbagesB + self.west["cabbages"] + self.store["cabbages"]
            newGoatsWest = goatsA + goatsB + self.west["goats"] + self.store["goats"]
            newWolvesWest = wolvesA + wolvesB + self.west["wolves"] + self.store["wolves"]

            maxCabbageStore = min(Graph.storeHouse,newCabbagesWest)  # the new number on the west shore
            maxGoatStore = min(Graph.storeHouse,newGoatsWest)  # the new number on the west shore
            maxWolveStore = min(Graph.storeHouse,newWolvesWest)  # the new number on the west shore

            newEast = {
                "wolves": newWolvesEst,
                "goats": newGoatsEst,
                "cabbages": newCabbagesEst
            }
            newWest = {
                "wolves": newWolvesWest,
                "goats": newGoatsWest,
                "cabbages": newCabbagesWest
            }
            store = {
                "wolves": 0,
                "goats": 0,
                "cabbages": 0
            }
            eastAfterEating = self.eat(newEast)
            if not self.areEnoughProducts(eastAfterEating, newWest, store):
                return

            boat = Boat({
                "wolves": wolvesA,
                "goats": goatsA,
                "cabbages": cabbagesA
            },
                {
                    "wolves": wolvesB,
                    "goats": goatsB,
                    "cabbages": cabbagesB
                }
            )

            if maxCabbageStore:
                newWest = {
                    "wolves": newWolvesWest,
                    "goats": newGoatsWest,
                    "cabbages": newCabbagesWest - maxCabbageStore
                }
                store = {
                    "wolves": 0,
                    "goats": 0,
                    "cabbages": maxCabbageStore
                }
                node = CrossingNode(self, "west", eastAfterEating, newWest, store, boat)
                if not self.inPath(node):
                    self.listSuccessors.append(node)

            if maxGoatStore:
                    newWest = {
                        "wolves": newWolvesWest,
                        "goats": newGoatsWest - maxGoatStore ,
                        "cabbages": newCabbagesWest
                    }
                    store = {
                        "wolves": 0,
                        "goats": maxGoatStore,
                        "cabbages": 0
                    }
                    node = CrossingNode(self, "west", eastAfterEating, newWest, store, boat)
                    if not self.inPath(node):
                        self.listSuccessors.append(node)

            if maxWolveStore:
                    newWest = {
                        "wolves": newWolvesWest - maxWolveStore,
                        "goats": newGoatsWest,
                        "cabbages": newCabbagesWest
                    }
                    store = {
                        "wolves": maxWolveStore,
                        "goats": 0,
                        "cabbages": 0
                    }
                    node = CrossingNode(self, "west", eastAfterEating, newWest, store, boat)
                    if not self.inPath(node):
                        self.listSuccessors.append(node)


        else:
            # to do
            newCabbagesEst = self.east["cabbages"] + (cabbagesA + cabbagesB)
            newGoatsEst = self.east["goats"] + (goatsA + goatsB)
            newWolvesEst = self.east["wolves"] + (wolvesA + wolvesB)

            minCabbagesFromStore = max(0, (cabbagesA + cabbagesB) - self.west["cabbages"])
            minGoatsFromStore = max(0,(goatsA + goatsB) - self.west["goats"])
            minWolvesFromStore = max(0,(wolvesA + wolvesB) - self.west["wolves"])


            newEast = {
                "wolves": newWolvesEst,
                "goats": newGoatsEst,
                "cabbages": newCabbagesEst
            }

            newWest = {
                "wolves": self.west["wolves"] - (wolvesA + wolvesB - minWolvesFromStore),
                "goats":  self.west["goats"] - (goatsA + goatsB - minGoatsFromStore),
                "cabbages": self.west["cabbages"] - (cabbagesA + cabbagesB - minCabbagesFromStore)
            }
            store = {
                "cabbages": self.store["cabbages"] - minCabbagesFromStore,
                "goats": self.store["goats"] - minGoatsFromStore,
                "wolves": self.store["wolves"] - minWolvesFromStore
            }
            boat = Boat({
                "wolves": wolvesA,
                "goats": goatsA,
                "cabbages": cabbagesA
            },
                {
                    "wolves": wolvesB,
                    "goats": goatsB,
                    "cabbages": cabbagesB
                }
            )
            westAfterEating = self.eat(newWest)

            node = CrossingNode(self, "east", newEast, westAfterEating, store, boat)
            if (not self.areEnoughProducts(newEast, westAfterEating, store)) or self.inPath(node):
                return

            self.listSuccessors.append(node)


    def getSuccessors(self):
        """
        The method extend the currentNode and returns a list of possible next steps
        :param heuristic: the heuristic used
        :return: list of CrossingNode
        """
        cabbagesCurrentShore = self.getCurrentShoreAmount("cabbages")
        goatsCurrentShore = self.getCurrentShoreAmount("goats")
        wolvesCurrentShore = self.getCurrentShoreAmount("wolves")
        newWest = self.eat(self.west)
        if self.boatPosition == "west" and newWest == self.west:
            self.generateCombinationsStore(0, 0, 0, 0, 0, 0)
        else:
            cabbageCombinations = {0, min(cabbagesCurrentShore, Graph.A), min(cabbagesCurrentShore, Graph.B),
                                   min(cabbagesCurrentShore, Graph.A + Graph.B)}
            for nrCabbagesBoat in cabbageCombinations:
                if nrCabbagesBoat == 0:
                    maxGoatsBoat = min(goatsCurrentShore, Graph.A + Graph.B)
                elif nrCabbagesBoat >= Graph.B and nrCabbagesBoat >= Graph.A:  # we have in both A and B cabbages
                    maxGoatsBoat = 0
                else:
                    '''
                    even if we start with some bad combinations( cheap and less products in A and more in B)
                    in the end we will test and the optimised ones (cabbages(cheap) in B(expensive) and goats(expensive) in A(cheap)
                    '''
                    if nrCabbagesBoat <= Graph.B:
                        maxGoatsBoat = min(goatsCurrentShore, Graph.A)
                    else:
                        maxGoatsBoat = min(goatsCurrentShore, Graph.B)

                goatsCombinations = {0, min(maxGoatsBoat, Graph.A), min(maxGoatsBoat, Graph.B),
                                     min(maxGoatsBoat, Graph.A + Graph.B)}
                for nrGoatsBoat in goatsCombinations:
                    if nrCabbagesBoat == 0 and nrGoatsBoat == 0:
                        maxWolvesBoat = min(wolvesCurrentShore, Graph.A + Graph.B)
                    elif (nrGoatsBoat > 0 and nrCabbagesBoat > 0) or (
                            nrGoatsBoat > Graph.A and nrGoatsBoat > Graph.B) or (
                            nrCabbagesBoat > Graph.A and nrCabbagesBoat > Graph.B):  # both compartments have obj
                        maxWolvesBoat = 0
                    elif nrCabbagesBoat == 0 and nrGoatsBoat > 0:
                        if nrGoatsBoat <= Graph.B:
                            maxWolvesBoat = min(wolvesCurrentShore, Graph.A)
                        else:
                            maxWolvesBoat = min(wolvesCurrentShore, Graph.B)
                    elif nrCabbagesBoat > 0 and nrGoatsBoat == 0:
                        if nrCabbagesBoat <= Graph.B:
                            maxWolvesBoat = min(wolvesCurrentShore, Graph.A)
                        else:
                            maxWolvesBoat = min(wolvesCurrentShore, Graph.B)

                    wolvesCombinations = {0, min(maxWolvesBoat, Graph.A), min(maxWolvesBoat, Graph.B),
                                          min(maxWolvesBoat, Graph.A + Graph.B)}
                    for nrWolvesBoat in wolvesCombinations:
                        if nrWolvesBoat == 0 and nrGoatsBoat == 0 and nrCabbagesBoat == 0:
                            self.generateCombinationsStore(0, 0, 0, 0, 0, 0)
                        # we know that always nrCabbagesBoat + nrGoatsBoat + nrWolvesBoat <= A + B
                        # it's impossible that all three to be > 0
                        # when we have just 1 elem first of all fill A

                        if nrCabbagesBoat > 0 and nrGoatsBoat > 0:
                            if nrCabbagesBoat <= Graph.B and nrCabbagesBoat <= Graph.A and nrGoatsBoat <= Graph.B and nrGoatsBoat <= Graph.A:
                                # not the best idea to put cabbages in B and goats in A --> if we have a looot c
                                costBoat1 = Boat({
                                    "wolves": 0,
                                    "goats": nrGoatsBoat,
                                    "cabbages": 0
                                },
                                    {
                                        "wolves": 0,
                                        "goats": 0,
                                        "cabbages": nrCabbagesBoat
                                    }
                                ).getCost()

                                costBoat2 = Boat({
                                    "wolves": 0,
                                    "goats": 0,
                                    "cabbages": nrCabbagesBoat
                                },
                                    {
                                        "wolves": 0,
                                        "goats": nrGoatsBoat,
                                        "cabbages": 0
                                    }
                                ).getCost()
                                if costBoat1 < costBoat2:
                                    self.generateCombinationsStore(0, nrCabbagesBoat, nrGoatsBoat, 0, 0, 0)
                                else:
                                    self.generateCombinationsStore(nrCabbagesBoat, 0, 0, nrGoatsBoat, 0, 0)


                            elif nrCabbagesBoat <= Graph.B and nrGoatsBoat <= Graph.A:
                                self.generateCombinationsStore(0, nrCabbagesBoat, nrGoatsBoat, 0, 0, 0)
                            else:
                                self.generateCombinationsStore(nrCabbagesBoat, 0, 0, nrGoatsBoat, 0, 0)




                        elif nrCabbagesBoat > 0 and nrWolvesBoat > 0:
                            if nrCabbagesBoat <= Graph.B and nrCabbagesBoat <= Graph.A and nrWolvesBoat <= Graph.B and nrWolvesBoat <= Graph.A:
                                costBoat1 = Boat({
                                    "wolves": 0,
                                    "goats": 0,
                                    "cabbages": nrCabbagesBoat
                                },
                                    {
                                        "wolves": nrWolvesBoat,
                                        "goats": 0,
                                        "cabbages": 0
                                    }
                                ).getCost()

                                costBoat2 = Boat({
                                    "wolves": nrWolvesBoat,
                                    "goats": 0,
                                    "cabbages": 0
                                },
                                    {
                                        "cabbages": nrCabbagesBoat,
                                        "wolves": 0,
                                        "goats": 0
                                    }
                                ).getCost()
                                if costBoat1 < costBoat2:
                                    self.generateCombinationsStore(nrCabbagesBoat, 0, 0, 0, 0, nrWolvesBoat)
                                else:
                                    self.generateCombinationsStore(0, nrCabbagesBoat, 0, 0, nrWolvesBoat, 0)


                            elif nrCabbagesBoat <= Graph.B and nrWolvesBoat <= Graph.A:
                                self.generateCombinationsStore(0, nrCabbagesBoat, 0, 0, nrWolvesBoat, 0)
                            else:
                                self.generateCombinationsStore(nrCabbagesBoat, 0, 0, 0, 0, nrWolvesBoat)




                        elif nrGoatsBoat > 0 and nrWolvesBoat > 0:
                            if nrGoatsBoat <= Graph.B and nrGoatsBoat <= Graph.A and nrWolvesBoat <= Graph.B and nrWolvesBoat <= Graph.A:
                                costBoat1 = Boat({
                                    "wolves": 0,
                                    "goats": nrGoatsBoat,
                                    "cabbages": 0
                                },
                                    {
                                        "wolves": nrWolvesBoat,
                                        "goats": 0,
                                        "cabbages": 0
                                    }
                                ).getCost()

                                costBoat2 = Boat({
                                    "wolves": nrWolvesBoat,
                                    "goats": 0,
                                    "cabbages": 0
                                },
                                    {
                                        "wolves": 0,
                                        "goats": nrGoatsBoat,
                                        "cabbages": 0
                                    }
                                ).getCost()
                                if costBoat1 < costBoat2:
                                    self.generateCombinationsStore(0, 0, nrGoatsBoat, 0, 0, nrWolvesBoat)
                                else:
                                    self.generateCombinationsStore(0, 0, 0, nrGoatsBoat, nrWolvesBoat, 0)

                            elif nrGoatsBoat <= Graph.A and nrWolvesBoat <= Graph.B:
                                self.generateCombinationsStore(0, 0, nrGoatsBoat, 0, 0, nrWolvesBoat)
                            else:
                                self.generateCombinationsStore(0, 0, 0, nrGoatsBoat, nrWolvesBoat, 0)

                        elif nrCabbagesBoat > Graph.A:  # JUST 1 ELEM ---> first of all fill A
                            self.generateCombinationsStore(Graph.A, nrCabbagesBoat - Graph.A, 0, 0, 0, 0)
                        elif nrCabbagesBoat > 0:
                            self.generateCombinationsStore(nrCabbagesBoat, 0, 0, 0, 0, 0)


                        elif nrGoatsBoat > Graph.A:  # JUST 1 ELEM ---> first of all fill A
                            self.generateCombinationsStore(0, 0, Graph.A, nrGoatsBoat - Graph.A, 0, 0)
                        elif nrGoatsBoat > 0:
                            self.generateCombinationsStore(0, 0, nrGoatsBoat, 0, 0, 0)


                        elif nrWolvesBoat > Graph.A:  # JUST 1 ELEM ---> first of all fill A
                            self.generateCombinationsStore(0, 0, 0, 0, Graph.A, nrWolvesBoat - Graph.A)
                        elif nrWolvesBoat > 0:
                            self.generateCombinationsStore(0, 0, 0, 0, nrWolvesBoat, 0)
        return self.listSuccessors
