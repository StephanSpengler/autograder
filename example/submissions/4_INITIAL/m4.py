from tokenize import TokenError
import math
import io
import tokenize


class TokenizeWrapper:
    def __init__(self, line):
        self.line = line
        self.tokens = tokenize.generate_tokens(io.StringIO(line).readline)
        self.current = next(self.tokens)
        self.previous = 'START'

    def __str__(self):
        return self.current[0] + self.current[1]

    def get_current(self):
        if self.current[0] > 0:
            return self.current[1]
        else:
            return 'NO MORE TOKENS'

    def get_previous(self):
        return self.previous

    def next(self):
        # The return value is mainly intended for debugging purposes
        if self.has_next():
            self.previous = self.current[1]
            self.current = next(self.tokens)
            #print('next', self.current[0], self.current[1])
            return self.current
        else:
            return (0, 'EOS')

    def is_number(self):
        return self.current[0] == 2

    def is_name(self):
        return self.current[0] == 1

    def is_string(self):
        return self.current[0] == 3

    def is_newline(self):
        return self.current[0] == 4

    def is_comment(self):
        return self.current[0] == 55

    def is_at_end(self):
        return self.current[0] == 0 or self.current[0] == 4 or \
            self.current[1][0] == '#'  # self.current[0] == 55

    def has_next(self):
        return self.current[0] != 0 and self.current[0] != 4


def log(x):
    if x <= 0:
        raise EvaluationError(f'Illegal argument to log: {x}')
    return math.log(x)


def fib(n, memory):
    if n<0 or n//1!=n:
        raise EvaluationError(f'Illegal argument to fib: {n}')
    if n not in memory:
        memory[n] = fib(n - 1, memory) + fib(n - 2, memory)
    return memory[n]


FUNCTIONS_1 = {  # Functions with a single argument
    'sin': math.sin,
    'cos': math.cos,
    'exp': math.exp,
    'log': log,
    'fib': fib
}

FUNCTIONS_N = {  # Functions with several arguments
    'sum': sum,
    'max': max
}

def arglist(wtok, variables):
    """ See syntax diagram for arglist"""
    if wtok.get_current() != '(':
        raise SyntaxError("Expected '(' after function name")
    wtok.next()
    args = []
    while True:
        a = assignment(wtok, variables)
        args.append(a)
        if wtok.get_current() == ')':
            wtok.next()
            break
        if wtok.get_current() != ',':
            raise SyntaxError('Incorrect argument list. Expected ","')
        wtok.next()
    return args

class EvaluationError(Exception):
    def __init__(self, arg):
        self.arg = arg
        super().__init__(self.arg)


class SyntaxError(Exception):
    def __init__(self, arg):
        self.arg = arg
        super().__init__(self.arg)


def statement(wtok, variables):
    result = assignment(wtok, variables)
    while wtok.get_current() == ',':
        wtok.next()
        result = assignment(wtok, variables)
    if wtok.is_at_end() == False:
        raise SyntaxError('Expected comma or end of line')
    return result


def assignment(wtok, variables):
    result = expression(wtok, variables)
    while wtok.get_current() == '=':
        wtok.next()
        if wtok.is_name():
            variables[wtok.get_current()] = result
        else:
            raise SyntaxError("Expected name after assignment operator")
        wtok.next()
    return result


def expression(wtok, variables):
    try:
        result = term(wtok, variables)
        while wtok.get_current() in ('+', '-'):
            if wtok.get_current() == '+':
                wtok.next()
                result = result + term(wtok, variables)
            else:
                wtok.next()
                result = result - term(wtok, variables)
        return result
    except (TypeError, ValueError) as te:
        raise EvaluationError(te)


def term(wtok, variables):
    result = factor(wtok, variables)
    while wtok.get_current() in ('*', '/'):
        op = wtok.get_current()
        wtok.next()
        if op == '*':
            result = result * factor(wtok, variables)
        else:
            try:
                result = result / factor(wtok, variables)
            except ZeroDivisionError:
                raise EvaluationError("Division by zero")
    return result


def parse(wtok, c, aux=''):  # Just for convenience
    if wtok.get_current() != c:
        raise SyntaxError(f"Expected '{c}'" + aux)
    wtok.next()


def factor(wtok, variables):
    if wtok.get_current() == '(':
        wtok.next()
        result = assignment(wtok, variables)
        parse(wtok, ')', '')

    elif wtok.get_current() in FUNCTIONS_1:
        func = FUNCTIONS_1[wtok.get_current()]
        wtok.next()
        if wtok.get_current() == '(':
            result = func(factor(wtok, variables))
        else:
            raise SyntaxError("Missing '(' after function name")
    elif wtok.get_current() in FUNCTIONS_N:
        func = wtok.get_current()
        wtok.next()
        args = arglist(wtok, variables)
        result = FUNCTIONS_N[func](args)

    elif wtok.is_name():
        if wtok.get_current() in variables:
            result = variables[wtok.get_current()]
            wtok.next()
        else:
            raise EvaluationError(
                f"Undefined variable: '{wtok.get_current()}'")

    elif wtok.is_number():
        result = float(wtok.get_current())
        wtok.next()

    elif wtok.get_current() == '-':
        wtok.next()
        result = -factor(wtok, variables)

    else:
        raise SyntaxError(
            "Expected number, word or '('")
    return result


def vars_print(variables):
    for name, value in sorted(variables.items()):
        print(f"   {name:<5} : {value}")

def memory_print(memory):
    for name, value in sorted(memory.items()):
        print(f"   {name:<5} : {value}")


def main():

    print("Numerical calculator")
    variables = {"ans": 0.0}
    memory = {0: 0, 1 :1}

    while True:
        line = input('\nInput: ')
        if line == '' or line[0] == '#':
            continue
        wtok = TokenizeWrapper(line)
        if wtok.get_current() == 'vars':
            vars_print(variables)
        if wtok.get_current() == 'mem':
            memory_print(memory)
        elif wtok.get_current() == 'quit':
            print('Bye')
            exit()
        else:
            try:
                result = statement(wtok, variables)
                variables['ans'] = result
                print(result)

            except EvaluationError as ee:
                print("*** Evaluation error: ", ee)

            except SyntaxError as se:
                print("*** Syntax error: ", se)
                print(
                    f"*** Error occurred at '{wtok.get_current()}' just after '{wtok.get_previous()}'")

            except TokenError as te:
                print('*** Syntax error: Unbalanced parentheses')


if __name__ == "__main__":
    main()