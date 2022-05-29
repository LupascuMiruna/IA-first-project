from reader import Reader


class Graph:
    """
    The problem will be modeled using a graph
    As the graph doesn't change, all the fields will be STATIC to be accessible from CROSSING NODE
    The graph class will contain:


    """

    def __init__(self, fileName):
        Graph.fileReader = Reader(fileName)
        inputData = Graph.fileReader.read()

        Graph.initialShore = "Est"
        Graph.finalShore = "West"
        Graph.cabbages = inputData.get("cabbages")
        Graph.goats = inputData.get("goats")
        Graph.wolves = inputData.get("wolves")
        Graph.A = inputData.get("A")
        Graph.B = inputData.get("B")
        Graph.storeHouse = inputData.get("M")
        Graph.wolvesEatGoats = inputData.get("N1")
        Graph.wolvesEatWolves = inputData.get("N2")
        Graph.goatsEatCabbages = inputData.get("N3")
        Graph.finalCabbages = inputData.get("minCabbages")
        Graph.finalGoats = inputData.get("minGoats")
        Graph.finalWolves = inputData.get("minWolves")
        Graph.heuristic = inputData.get("heuristic")
        Graph.west = {
            "cabbages": 0,
            "goats": 0,
            "wolves": 0
        }
        Graph.store = {
            "cabbages": 0,
            "goats": 0,
            "wolves": 0
        }
        Graph.east = {
            "cabbages": Graph.cabbages,
            "goats": Graph.goats,
            "wolves": Graph.wolves
        }
        Graph.initialBoatPosition = "east"

        Graph.validInput = Graph.veifyInput()

    def veifyInput():
        """
        check if we have enough products
        """
        return Graph.cabbages >= Graph.finalCabbages and Graph.goats >= Graph.finalGoats and \
               Graph.wolves >= Graph.finalWolves

    def isValidState(self, east, west, store):
        return east["wolves"] + west["wolves"] + store["wolves"] >= Graph.finalWolves and \
               east["cabbages"] + west["cabbages"] + store["cabbages"] >= Graph.finalCabbages and \
               east["goats"] + west["goats"] + store["goats"] >= Graph.finalGoats