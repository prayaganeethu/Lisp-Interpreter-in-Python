import math
import operator as op
from fractions import Fraction


class lambdac(object):

    def __init__(self, param, body, env):
        self.param = param
        self.body = body
        self.env = env

    def __call__(self, *args):
        return eval_lisp_program(self.body, environment(self.param, args, self.env))


class environment(dict):

    def __init__(self, param=(), args=(), outer=None):
        self.outer = outer
        self.update(zip(param, args))

    def find(self, var):
        return self if (var in self) else self.outer.find(var)

env = environment()

env.update(vars(math))

mathematical_operators = ["+", "-", "*", "/", "rem"]
relational_operators = [">", "<", "<=", ">=", "/=", "="]

Number = (int, float)


def tokenize_lisp_prog(lisp_program):
    return lisp_program.replace("(", " ( ").replace(")", " ) ").split()


def number_symbol(token):
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return str(token)


def read_as_list(lisp_list):
    if not lisp_list:
        raise SyntaxError("Unexpected EOF while reading")
    token = lisp_list.pop(0)
    if token == "(":
        new_list = []
        while lisp_list[0] != ")":
            new_list.append(read_as_list(lisp_list))
        lisp_list.pop(0)
        return new_list
    elif token == ")":
        raise SyntaxError('Unexpected )')
    else:
        return number_symbol(token)


def parse_lisp_program(lisp_program):
    return read_as_list(tokenize_lisp_prog(lisp_program))


def math_operators(opr_oprnds, env):
    oprnd_li = [eval_lisp_program(p, env) for p in opr_oprnds[1:]]
    oprnd_li = list(map(str_to_fraction, oprnd_li))
    if opr_oprnds[0] == "+":
        sum = 0
        for term in oprnd_li:
            sum = sum + term
        return sum
    elif opr_oprnds[0] == "*":
        product = 1
        for term in oprnd_li:
            product = product * term
        return product
    elif opr_oprnds[0] == "rem":
        return oprnd_li[0] % oprnd_li[1]
    elif opr_oprnds[0] == "-":
        return oprnd_li[0] - oprnd_li[1]
    elif opr_oprnds[0] == "/":
        if oprnd_li[0] % oprnd_li[1] == 0:
            return oprnd_li[0] // oprnd_li[1]
        else:
            return str(oprnd_li[0]) + '/' + str(oprnd_li[1])


def str_to_fraction(a):
    if type(a) == str:
        return Fraction(a)
    else:
        return a


def rel_operators(opr_oprnds, env):
    oprnd_li = [eval_lisp_program(p, env) for p in opr_oprnds[1:]]
    oprnd_li = list(map(str_to_fraction, oprnd_li))
    if opr_oprnds[0] == "/=":
        return oprnd_li[0] != oprnd_li[1]
    elif opr_oprnds[0] == "=":
        return oprnd_li[0] == oprnd_li[1]
    else:
        return eval(str(oprnd_li[0]) + " " +
                    str(opr_oprnds[0]) + " " + str(oprnd_li[1]))


def if_clause(oprnds, env):
    oprnd_li = [eval_lisp_program(p, env) for p in oprnds]
    if oprnd_li[0]:
        return oprnd_li[1]
    else:
        return oprnd_li[2]


def car(*oprnds, env):
    return oprnds[0]


def cdr(*oprnds, env):
    return oprnds[1:]


def cons(*oprnds, env):
    if oprnds[0] == "nil":
        return oprnds[1]
    elif oprnds[1] == "nil":
        return oprnds[0]
    else:
        return [oprnds[0]] + [oprnds[1]]


def begin(*oprnds, env):
    return oprnds[-1]


def to_list(*oprnds, env):
    return list(oprnds)


def is_list(*oprnds, env):
    return isinstance(oprnds, list)


def is_null(*oprnds, env):
    return oprnds == []


def is_number(*oprnds, env):
    return isinstance(oprnds, Number)


def is_symbol(*oprnds, env):
    return isinstance(oprnds, str)


def set_fn(oprnds, env):
    env.find(oprnds[1])[oprnds[1]] = eval_lisp_program(oprnds[2], env)

env.update({"eq?": op.is_,
            "equal?": op.eq,
            "car": car,
            "cdr": cdr,
            "cons": cons,
            "max": max,
            "min": min,
            "abs": abs,
            "length": len,
            "map": map,
            "round": round,
            "not": op.not_,
            "procedure?": callable,
            "begin": begin,
            "list": to_list,
            "list?": is_list,
            "null?": is_null,
            "number?": is_number,
            "symbol?": is_symbol,
            "nil": 'nil'
            })


def eval_lisp_program(x, env):
    if isinstance(x, str):
        reslt = env.find(x)[x]
        return reslt
    elif isinstance(x, Number):
        return x
    elif x[0] == "quote":
        return x[1:]
    elif x[0] == "define":
        env[x[1]] = eval_lisp_program(x[2], env)
    elif x[0] == "if":
        return if_clause(x[1:], env)
    elif x[0] in mathematical_operators:
        reslt = math_operators(x, env)
        return reslt
    elif x[0] in relational_operators:
        return rel_operators(x, env)
    elif x[0] == "set!":
        set_fn(x, env=env)
    elif x[0] == "lambda":
        return lambdac(x[1], x[2], env)
    elif x[0] in ["car", "cdr", "cons", "begin", "update", "list", "list?", "symbol?", "null?", "number?"]:
        func = eval_lisp_program(x[0], env)
        args = [eval_lisp_program(arg, env) for arg in x[1:]]
        return func(*args, env=env)
    else:
        func = eval_lisp_program(x[0], env)
        args = [eval_lisp_program(arg, env) for arg in x[1:]]
        return func(*args)


def lisp_form(expr):
    if isinstance(expr, list):
        return '(' + ' '.join(map(lisp_form, expr)) + ')'
    else:
        return str(expr)

# REPL(READ-EVAL-PRINT-LOOP)
# The Common LISP environment follows the algorithm below when interacting with users:
# loop
#     read in an expression from the console;
#     evaluate the expression;
#     print the result of evaluation to the console;
# end loop.


while True:
    program = input(">>> ")
    parsed_list = parse_lisp_program(program)
    res = eval_lisp_program(parsed_list, env)
    if res is not None:
        print(lisp_form(res))
