"""
dictionary that keeps the cost of transport of each product in each compartment
"""
costs = {
    "A": {
        "wolves": 3,
        "goats": 2,
        "cabbages": 1
    },
    "B": {
        "wolves": 3 + 0.5 * 3,
        "goats": 2 + 0.5 * 2,
        "cabbages": 1 + 0.5
    }
}


class Boat:
    """
    configuration of the boat
    what products are in each compartment
    """
    def __init__(self, A, B):
        self.A = A
        self.B = B

    def getCost(self):
        """
        based on the configuration returns the cost of the transport
        from parent to child
        """
        goatsA = self.A["goats"]
        wolvesA =  self.A["wolves"]
        cabbagesA =  self.A["cabbages"]
        goatsB =  self.B["goats"]
        wolvesB =  self.B["wolves"]
        cabbagesB =  self.B["cabbages"]

        return goatsA * costs["A"]["goats"] + \
               wolvesA * costs["A"]["wolves"] + \
               cabbagesA * costs["A"]["cabbages"] + \
               goatsB * costs["B"]["goats"] + \
               wolvesB * costs["B"]["wolves"] + \
               cabbagesB * costs["B"]["cabbages"]