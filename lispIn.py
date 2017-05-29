import math
import operator as op
from fractions import Fraction

mathematical_operators = ["+", "-", "*", "/", "rem"]
relational_operators = [">", "<", "<=", ">=", "/=", "="]

Symbol = str
List = list
Number = (int, float)

dictry = dict


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


# def eq(oprnds, gl_env, loc_env):
#     return oprnds[0] == oprnds[1]


def math_operators(opr_oprnds, gl_env, loc_env):
    # print("MATH")
    # print("{} \n {} \n {}".format(opr_oprnds, gl_env, loc_env))
    oprnd_li = [eval_lisp_program(p, gl_env, loc_env) for p in opr_oprnds[1:]]
    oprnd_li = list(map(str_to_fraction, oprnd_li))
    # print("OPRNDS {}".format(oprnd_li))
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


def rel_operators(opr_oprnds, gl_env, loc_env):
    oprnd_li = [eval_lisp_program(p, gl_env, loc_env) for p in opr_oprnds[1:]]
    oprnd_li = list(map(str_to_fraction, oprnd_li))
    if opr_oprnds[0] == "/=":
        return oprnd_li[0] != oprnd_li[1]
    elif opr_oprnds[0] == "=":
        return oprnd_li[0] == oprnd_li[1]
    else:
        return eval(str(oprnd_li[0]) + " " +
                    str(opr_oprnds[0]) + " " + str(oprnd_li[1]))


def if_clause(oprnds, gl_env, loc_env):
    oprnd_li = [eval_lisp_program(p, gl_env, loc_env) for p in oprnds]
    # print("IF {} {} {}".format(oprnd_li[0], oprnd_li[1], oprnd_li[2]))
    if oprnd_li[0]:
        return oprnd_li[1]
    else:
        return oprnd_li[2]


def car(*oprnds, gl_env, loc_env):
    return oprnds[0]


def cdr(*oprnds, gl_env, loc_env):
    return oprnds[1:]


def cons(*oprnds, gl_env, loc_env):
    if oprnds[0] == "nil":
        return oprnds[1]
    elif oprnds[1] == "nil":
        return oprnds[0]
    else:
        return [oprnds[0]] + [oprnds[1]]


def update(oprnds, gl_env, loc_env):
    env[oprnds[0]] = oprnds[1]


def begin(*oprnds, gl_env, loc_env):
    return oprnds[-1]


def to_list(oprnds, gl_env, loc_env):
    return list(oprnds)


def is_list(oprnds, gl_env, loc_env):
    return isinstance(oprnds, list)


def is_null(oprnds, gl_env, loc_env):
    return oprnds == []


def is_number(oprnds, gl_env, loc_env):
    return isinstance(oprnds, Number)


def is_symbol(oprnds, gl_env, loc_env):
    return isinstance(oprnds, str)


def set(oprnds, gl_env, loc_env):
    if oprnds[1] in env.keys():
        env[oprnds[1]] = eval_lisp_program(oprnds[2], env)
        # print(env[oprnds[1]])


def lambdafn(param, body, args, gl_env):
    locl_var = dictry()
    locl_var.update(zip(param, args))
    return eval_lisp_program(body, gl_env, locl_var)


def environment(variable, global_env, local_env):
    if local_env:
        if variable in local_env.keys():
            return local_env[variable]
        else:
            return global_env[variable]
    elif global_env:
        if variable in global_env.keys():
            return global_env[variable]
    else:
        return variable

env = dictry()

env = {"eq?": op.is_,
       "equal?": op.eq,
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


def eval_lisp_program(x, gl_env, loc_env=None):
    # print("EVAL {} \n {} \n {}".format(x, gl_env, loc_env))
    if isinstance(x, str):
        reslt = environment(x, gl_env, loc_env)
        # print("SYMBOL {}".format(reslt))
        return reslt
    elif isinstance(x, Number):
        return x
    elif x[0] == "quote":
        return x[1:]
    elif x[0] == "define":
        env[x[1]] = eval_lisp_program(x[2], gl_env, loc_env)
    elif x[0] == "if":
        return if_clause(x[1:], gl_env, loc_env)
    elif x[0] in mathematical_operators:
        reslt = math_operators(x, gl_env, loc_env)
        # print("EVAL MATH")
        # print("{} \n {} \n {}".format(x, gl_env, loc_env))
        return reslt
    elif x[0] in relational_operators:
        return rel_operators(x, gl_env, loc_env)
    elif x[0] == "set!":
        set(x, gl_env, loc_env)
    elif isinstance(x[0], list) and x[0][0] == "lambda":
        return lambdafn(x[0][1], x[0][2], x[1:], gl_env)
    elif x[0] in ["car", "cdr", "cons", "begin", "update", "list", "list?", "symbol?", "null?", "number?"]:
        args = [eval_lisp_program(arg, gl_env, loc_env) for arg in x[1:]]
        return env[x[0]](*args, gl_env, loc_env)
    else:
        args = [eval_lisp_program(arg, gl_env, loc_env) for arg in x[1:]]
        return env[x[0]](*args)


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
