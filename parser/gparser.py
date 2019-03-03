from enum import Enum
from parser.operations import Const, SimpleEdge, Operation, Name, Uniq, ParametrizedEdge, Len, Include, GenomeName, \
    Weights


class Token(Enum):
    FAIL = 0
    START = 1
    END = 2
    NAME = 3
    CONST = 4
    OPEN_EDGE = '{'
    CLOSE_EDGE = '}'
    EDGE = '>'
    OPEN_BRACKET = '('
    CLOSE_BRACKET = ')'
    APOSTROPHE = '\''
    SEPARATOR_EDGE_PARAMS = ':'
    LENGTH = 'l'
    LOCATION = 'n'
    WEIGHTS = 'w'
    GENOM_NAME = 'g'
    UNIQ = 'u'
    P_EDGE = 5

    @staticmethod
    def find(symbol: str):
        for name, member in Token.__members__.items():
            if member.value == symbol:
                return member
        return Token.FAIL

    @classmethod
    def val(cls):
        return cls.value



class ParseException(Exception):
    pass


class GraphParser:
    __expression = ''
    __index = 0
    __size = 0
    __name = ''
    __value = ''
    __token = Token.FAIL

    __last_params = None
    __FUNCTIONS = []  # array of function pointers. Order sets the priority of operations

    def __init__(self):
        super().__init__()

        self.__FUNCTIONS = [self.__simple_edge, self.__primary]

    def parse_from_list(self, base: list):
        self.__graph = {}
        for line in base:
            self.parse(line)

    def next_token(self) -> Token:
        self.__skip_ws()
        if self.__size <= self.__index:
            return Token.END
        symbol = self.__expression[self.__index]
        self.__next_char()

        self.__token = Token.find(symbol)

        if self.__token != Token.FAIL:
            return self.__token

        start = self.__index - 1
        if symbol.isalpha():
            while self.__is_correct_bound() and self.current().isalpha():
                self.__next_char()

            string = self.__expression[start: self.__index]
            token = Token.find(string)
            if token == Token.FAIL:
                self.__name = string
                return Token.NAME
            return token

        if symbol.isdigit():
            while self.__is_correct_bound() and self.current().isdigit():
                self.__next_char()

            self.__value = int(self.__expression[start: self.__index])
            return Token.CONST
        return self.__token

    def __skip_ws(self):
        while self.__is_correct_bound() and self.__expression[self.__index] == ' ':  # ws
            self.__index += 1

    def __is_correct_bound(self) -> bool:
        return self.__index < self.__size

    def __next_char(self):
        self.__index += 1

    def current(self) -> str:
        return self.__expression[self.__index]

    def __parameter(self, new_token: bool):
        left = self.__next_priority(self.__parameter, new_token)
        params = []
        while True:
            if self.__token == Token.SEPARATOR_EDGE_PARAMS:
                params.append(left)
                self.__next_priority(self.__next_priority(self.__parameter, True))
                # left = SimpleEdge(left, self.__next_priority(self.__simple_edge, True))
            else:
                if len(params) == 0:
                    return left
                return params

    def __simple_edge(self, new_token: bool):

        left = self.__primary(new_token)

        while True:
            if self.__token == Token.OPEN_EDGE:
                self.__primary(False)  # parse params
            if self.__token == Token.EDGE:
                left = SimpleEdge(left, self.__next_priority(self.__simple_edge, True))
            elif self.__token == Token.P_EDGE:
                left = ParametrizedEdge(left, self.__next_priority(self.__simple_edge, True), self.__last_params)
            else:
                return left

    def __primary(self, new_token: bool):
        if new_token:
            self.__token = self.next_token()

        if self.__token == Token.CONST:
            v = self.__value
            self.__token = self.next_token()
            return Const(v)

        if self.__token == Token.APOSTROPHE:
            self.__skip_ws()
            start = self.__index
            while self.current() != Token.APOSTROPHE.value:
                self.__next_char()

            if not self.__is_correct_bound():
                raise ParseException("Wrong token at " + str(self.__index))

            new_name = self.__expression[start: self.__index]
            self.__next_char()
            self.__token = self.next_token()
            return Name(new_name)

        if self.__token == Token.OPEN_EDGE:
            start = self.__index
            while self.__is_correct_bound() and self.current() != Token.CLOSE_EDGE.value:
                self.__next_char()

            if not self.__is_correct_bound():
                raise ParseException("Wrong token at " + str(self.__index))
            self.__last_params = self.__parse_edge_param(self.__expression[start: self.__index])
            self.__token = Token.P_EDGE
            self.__next_char()
            return

        if self.__token == Token.UNIQ:
            args = []

            if self.current() != '(':
                self.__raise_wrong_token(self.__index)

            self.__next_char()
            start = self.__index
            while self.__is_correct_bound() and self.current() != ')':
                self.__next_char()
            args = [int(x) for x in self.__expression[start:self.__index].split(',')]
            self.__next_char()
            self.__token = self.next_token()
            return Uniq(args)
            # self.__raise_wrong_token(self.__index)

    def __next_priority(self, sender=None, new_token=False):
        if sender is not None:
            for i in range(0, len(self.__FUNCTIONS)):
                if self.__FUNCTIONS[i] == sender:
                    return self.__FUNCTIONS[i + 1](new_token)
        return self.__FUNCTIONS[0](new_token)

    def __low_priority(self, new_token):
        return self.__next_priority(new_token=new_token)

    def __parse_edge_param(self, params_string: str):

        splited = params_string.split(Token.SEPARATOR_EDGE_PARAMS.value)
        return [self.__to_param(arg) for arg in splited]

    def parse(self, base: str):
        self.__expression = base
        self.__size = base.__len__()

        self.__token = self.next_token()

        while self.__index < self.__size and self.__token == Token.FAIL:
            self.__token = self.next_token()

        return Operation() if self.__token == Token.END else self.__next_priority(None, False)

    def __raise_wrong_token(self, index: int):
        message = 'Wrong token at ' + str(index) + '\n' + self.__expression + '\n' + (
                ' ' * index + '^' + ' ' * (self.__size - index))
        raise ParseException(message)

    def __to_param(self, arg):

        arg = arg.replace(' ', '')
        token = Token.find(arg[0])
        idx = 0
        while idx < len(arg) and arg[idx] != Token.OPEN_BRACKET.value:
            idx += 1
        start = idx + 1

        while idx < len(arg) and arg[idx] != Token.CLOSE_BRACKET.value:
            idx += 1

        params_str = arg[start:idx]

        if token == Token.GENOM_NAME:
            return GenomeName([params_str])

        params = [int(x) for x in params_str.split(',')]

        if token == Token.UNIQ:
            return Uniq(params)
        if token == Token.LENGTH:
            return Len(params)

        if token == Token.LOCATION:
            return Include(params)
        if token == Token.WEIGHTS:
            return Weights(params)
