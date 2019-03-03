from parser.gparser import GraphParser
from parser.operations import Weights, Uniq, Include, Len


class Graph:

    def __init__(self):
        self.name_idx = 0
        self.name_var = 'X'
        self.normal = []
        self.not_normal = []

    def build(self, from_parser: list):
        # print(str(from_parser))

        res = [[], []]
        NAME = 2
        WEIGHT = 3
        LEN = 4
        UNIQ = 6
        N = 5

        names = set([x[NAME] for x in from_parser])
        names.remove(None)
        for e in from_parser:

            if e[NAME] is None:
                new_name = self.next_name()
                while new_name in names:
                    new_name = self.next_name()
                e[NAME] = new_name

            default = [Weights.default().build(None), Len.default().build(None), Include.default().build(None),
                       Uniq.default().build(None)]

            for i in [WEIGHT, LEN, N, UNIQ]:
                if e[i] is None:
                    e[i] = default[i - WEIGHT]
            simple_edge = (e[LEN] == Len.default().build(None))

            if simple_edge:
                res[0].append(e)
            else:
                res[1].append(e)

        return res

    def next_name(self):
        self.name_idx += 1
        return self.name_var + '_' + str(self.name_idx - 1)

    @staticmethod
    def parse(graph_str: str):
        g = []
        input = graph_str.split(';')
        for part in input:
            if part != '':
                GraphParser().parse(part).build(g)

        return Graph().build(g)

    @staticmethod
    def beautiful_parse(graph_str: str):
        res = Graph.parse(graph_str)

        ft = lambda x: 'from ' + str(x[0]) + ' to ' + str(x[1])
        for row in res:
            for e in row:
                print("Edge {")
                print("\tFrom:    " + str(e[0]))
                print("\tTo:      " + str(e[1]))
                print("\tName:    " + str(e[2]))

                print("\tWeights: " + ft(e[3]))
                print("\tLength:  " + ft(e[4]))
                print("\tInclude: " + str(e[5]))
                print("\tUniq:    " + ft(e[6]))
                print('}')
