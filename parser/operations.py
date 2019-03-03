class Operation:
    ID = -1

    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right

    def build(self, graph):
        pass


class Unary(Operation):
    _ID = 1

    def __init__(self, value):
        super().__init__(value, None)


class Const(Unary):
    ID = 2

    def build(self, graph):
        return "const " + str(self.left)

    def __str__(self):
        return str(int(self.left))


class Name(Unary):
    ID = 3

    def build(self, graph):
        return "'" + str(self.left) + "'"


class ParametrizedEdge(Operation):
    ID = 4

    def __init__(self, left, right, params: list):
        super().__init__(left, right)
        self.__params = params

    def prepare(self, operand: Operation, graph) -> str:
        if operand is None:
            return None
        if operand.ID == SimpleEdge.ID or operand.ID == ParametrizedEdge.ID:
            operand.build(graph)
            return operand.right.build(graph)
        return operand.build(graph)

    def build(self, graph):

        edge_from = self.prepare(self.left, graph)
        edge_to = self.prepare(self.right, graph)

        self.__params.sort(key=lambda p: p.ID)

        result = [edge_from, edge_to]

        # edge ( from, to, name, weights,len, n, uniq)

        result = [edge_from, edge_to, None, None, None, None, None]

        for param in self.__params:
            result[2 + param.ID - GenomeName.ID] = param.build(graph)
        graph.append(result)

        # print("add edge " + str(result) + ' params_ids ' + str([i.ID for i in self.__params]))

        return edge_to


class SimpleEdge(ParametrizedEdge):
    ID = 0

    def __init__(self, left, right):
        super().__init__(left, right, list())


class Param(Unary):

    def __init__(self, args: list):
        super().__init__(None)
        self.args = args

    def build(self, graph):
        return self.args[0], self.args[1]


class Uniq(Param):
    ID = 14

    @staticmethod
    def default():
        return Uniq([0, -1])


class Len(Param):
    ID = 12

    @staticmethod
    def default():
        return Len([1, 1])


class Include(Param):
    ID = 13

    def build(self, graph):
        return self.args

    @staticmethod
    def default():
        return Include([])


class GenomeName(Param):
    ID = 10

    def build(self, graph):
        return str(self.args[0])

    @staticmethod
    def default(graph):
        return GenomeName([graph.next_name()])


class Weights(Param):
    ID = 11

    @staticmethod
    def default():
        return Weights([1, -1])

# print(Graph.parse("'-1' > '0' {w(0,100):g(X_0)} '1' {u(20, 100):l(0, 100)} '2' {u(20, 100):n(1, 2, 3, 4, 5, 6, 7)}"))
