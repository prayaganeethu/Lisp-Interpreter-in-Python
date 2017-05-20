import math
import operator as op
from fractions import Fraction

mathematical_operators = ["+", "-", "*", "/", "rem"]
relational_operators = [">", "<", "<=", ">=", "/=", "="]

Symbol = str
List = list
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
    if (lisp_list == [None]) or (not lisp_list):
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


def eq(oprnds):
    return oprnds[0] == oprnds[1]


def quote(oprnds):
    return tuple(oprnds)


def math_operators(opr_oprnds):
    oprnd_li = list(map(str_to_fraction, opr_oprnds[1:]))
    # print("MATH OP I: {}".format(oprnd_li))
    oprnd_li = list(map(eval_lisp_program, oprnd_li))
    # print("MATH OP II: {}".format(oprnd_li))
    oprnd_li = list(map(str_to_fraction, oprnd_li))
    # print("MATH OP III: {}".format(oprnd_li))
    if opr_oprnds[0] == "+":
        sum = 0
        for term in oprnd_li:
            sum = sum + term
        return sum
    elif opr_oprnds[0] == "*":
        product = 1
        for term in oprnd_li:
            product = product * term
        return int(product)
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


def rel_operators(opr_oprnds):
    oprnd_li = list(map(str_to_fraction, opr_oprnds[1:]))
    oprnd_li = list(map(eval_lisp_program, oprnd_li))
    if opr_oprnds[0] == "/=":
        return oprnd_li[0] != oprnd_li[1]
    elif opr_oprnds[0] == "=":
        return oprnd_li[0] == oprnd_li[1]
    else:
        return eval(str(oprnd_li[0]) + " " +
                    str(opr_oprnds[0]) + " " + str(oprnd_li[1]))


def if_clause(oprnds):
    oprnd_li = list(map(eval_lisp_program, oprnds))
    print("IF {} {} {}".format(oprnd_li[0], oprnd_li[1], oprnd_li[2]))
    if oprnd_li[0]:
        return oprnd_li[1]
    else:
        return oprnd_li[2]


def car(oprnds):
    return oprnds[0][0]


def cdr(oprnds):
    return oprnds[0][1:]


def cons(*oprnds):
    if oprnds[0] == "nil":
        return oprnds[1]
    elif oprnds[1] == "nil":
        return oprnds[0]
    else:
        return [oprnds[0]] + [oprnds[1]]


def update(oprnds):
    env[oprnds[0]] = oprnds[1]


def begin(*oprnds):
    return oprnds[-1]


def to_list(oprnds):
    return list(oprnds)


def is_list(oprnds):
    return isinstance(oprnds, list)


def is_null(oprnds):
    return oprnds == []


def is_number(oprnds):
    return isinstance(oprnds, Number)


def is_symbol(oprnds):
    return isinstance(oprnds, Symbol)


def set(oprnds):
    if oprnds[1] in env.keys():
        env[oprnds[1]] = eval_lisp_program(oprnds[2])
        print(env[oprnds[1]])


# def lambda(oprnds):
#     return eval_lisp_program(oprnds[2])


env = {"eq?": op.is_,
       "equal?": op.eq,
       "quote": quote,
       "car": car,
       "cdr": cdr,
       "cons": cons,
       "max": max,
       "min": min,
       "update": update,
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
       }

env.update(vars(math))


def eval_lisp_program(x):
    global env
    if isinstance(x, Symbol):
        return env[x]
    elif isinstance(x, Number):
        return x
    elif x[0] == "define":
        env[x[1]] = eval_lisp_program(x[2])
    elif x[0] == "if":
        return if_clause(x[1:])
    elif x[0] in mathematical_operators:
        # print(x[0])
        return math_operators(x)
    elif x[0] in relational_operators:
        return rel_operators(x)
    elif x[0] == "set!":
        return set(x)
    elif x[0] == "#":
        pass
    else:
        args = [eval_lisp_program(arg) for arg in x[1:]]
        # print(args)
        return env[x[0]](*args)

while True:
    program = input(">>> ")
    parsed_list = parse_lisp_program(program)
    print("Parsed list: {}".format(parsed_list))
    print("Evaluated result: {}".format(eval_lisp_program(parsed_list)))
