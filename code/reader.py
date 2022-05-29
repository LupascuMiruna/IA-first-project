class Reader:
    def __init__(self, fileName):
        self.file = None
        self.fileName = fileName

    def parseNextLine(self):
        return [int(line) for line in self.file.readline().split()]

    def read(self):
        self.file = open(self.fileName)
        cabbages, goats, wolves = self.parseNextLine()
        A, B, M = self.parseNextLine()
        N1, N2, N3 = self.parseNextLine()
        minCabbages, minGoats, minWolves = self.parseNextLine()
        heuristic = self.file.readline()

        return {
            "cabbages": cabbages,
            "goats": goats,
            "wolves": wolves,
            "A": A,
            "B": B,
            "M": M,
            "N1": N1,
            "N2": N2,
            "N3": N3,
            "minCabbages": minCabbages,
            "minGoats": minGoats,
            "minWolves": minWolves,
            "heuristic": heuristic
        }