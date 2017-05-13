import math
import operator as op

mathematical_operators = {"+", "-", "*", "/", "rem"}
relational_operators = {">", "<", "<=", ">=", "/=", "="}

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
    if len(lisp_list) == 0:
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


def define(oprnds):
    env[oprnds[0]] = oprnds[1]
    # print("DEFINE : {}".format(env[oprnds[0]]))


def math_operators(opr_oprnds):
    if opr_oprnds[0] == "+":
        sum = 0
        for term in opr_oprnds[1:]:
            sum = sum + eval_lisp_program(term)
        return sum
    elif opr_oprnds[0] == "*":
        product = 1
        for term in opr_oprnds[1:]:
            product = product * eval_lisp_program(term)
        return float(product)
    elif opr_oprnds[0] == "rem":
        return eval_lisp_program(opr_oprnds[1]) % eval_lisp_program(opr_oprnds[2])
    elif opr_oprnds[0] == "-":
        return eval_lisp_program(opr_oprnds[1]) - eval_lisp_program(opr_oprnds[2])
    elif opr_oprnds[0] == "/":
        return eval_lisp_program(opr_oprnds[1]) // eval_lisp_program(opr_oprnds[2])


def rel_operators(opr_oprnds):
    if opr_oprnds[0] == "/=":
        return eval_lisp_program(opr_oprnds[1]) != eval_lisp_program(opr_oprnds[2])
    elif opr_oprnds[0] == "=":
        return eval_lisp_program(opr_oprnds[1]) == eval_lisp_program(opr_oprnds[2])
    else:
        return eval(str(eval_lisp_program(opr_oprnds[1])) + " " +
                    str(opr_oprnds[0]) + " " + str(eval_lisp_program(opr_oprnds[2])))


def if_clause(oprnds):
    print("IF {} {} {}".format(oprnds[0], oprnds[1], oprnds[2]))
    if eval_lisp_program(oprnds[0]) == True:
        return eval_lisp_program(oprnds[1])
    else:
        return eval_lisp_program(oprnds[2])


def car(oprnds):
    return oprnds[0][0]


def cdr(oprnds):
    return oprnds[0][1:]


def cons(oprnds):
    if oprnds[0] == ["nil"]:
        return oprnds[1]
    elif oprnds[1] == ["nil"]:
        return oprnds[0]
    else:
        return oprnds[0] + oprnds[1]


def update(oprnds):
    env[oprnds[0]] = oprnds[1]


def begin(*oprnds):
    return oprnds[-1]


def list(oprnds):
    return list(oprnds)


def is_list(oprnds):
    return isinstance(oprnds, list)


def is_null(oprnds):
    return oprnds == []


def is_number(oprnds):
    return isinstance(oprnds, Number)


def is_symbol(oprnds):
    return isinstance(oprnds, Symbol)


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
       "set!": update,
       "begin": begin,
       "list": list,
       "list?": is_list,
       "null?": is_null,
       "number?": is_number,
       "symbol?": is_symbol
       }

env.update(vars(math))


def eval_lisp_program(x):
    global env
    if isinstance(x, Symbol):
        return env[x]
    elif isinstance(x, Number):
        return x
    elif x[0] == "define":
        return define(x[1:])
    elif x[0] == "if":
        return if_clause(x[1:])
    elif x[0] in mathematical_operators:
        # print(x[0])
        return math_operators(x)
    elif x[0] in relational_operators:
        return rel_operators(x)
    elif x[0] == "#":
        pass
    else:
        args = [eval_lisp_program(arg) for arg in x[1:]]
        # print(args)
        return env[x[0]](*args)

program = input("Enter Lisp Input: ")
parsed_list = parse_lisp_program(program)
print("Parsed list: {}".format(parsed_list))
print("Evaluated result: {}".format(eval_lisp_program(parsed_list)))
