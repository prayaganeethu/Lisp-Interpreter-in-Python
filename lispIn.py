env = {}

mathematical_operators = {"+", "-", "*", "/"}
relational_operators = {">", "<", "<=", ">=", "/=", "="}


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


def quote(a):
    return tuple(a)


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
        return product
    elif opr_oprnds[0] == "-":
        return eval_lisp_program(opr_oprnds[1]) - eval_lisp_program(opr_oprnds[2])
    elif opr_oprnds[0] == "/":
        return eval_lisp_program(opr_oprnds[1]) // eval_lisp_program(opr_oprnds[2])


def rel_operators(x):
    if x[0] == "/=":
        return eval_lisp_program(x[1]) != eval_lisp_program(x[2])
    elif x[0] == "=":
        return eval_lisp_program(x[1]) == eval_lisp_program(x[2])
    else:
        return eval(str(eval_lisp_program(x[1])) + " " + str(x[0]) + " " + str(eval_lisp_program(x[2])))


def if_clause(x):
    if eval_lisp_program(x[0]) == True:
        return eval_lisp_program(x[1])
    else:
        return eval_lisp_program(x[2])


def cons(a, b):
    if a == ["nil"]:
        return b
    elif b == ["nil"]:
        return a
    else:
        return a + b


def max(a):
    big = eval_lisp_program(a[0])
    b = a[1:]
    for term in b:
        if eval_lisp_program(term) > big:
            big = eval_lisp_program(term)
    return big


def min(a):
    small = eval_lisp_program(a[0])
    b = a[1:]
    for term in b:
        if eval_lisp_program(term) < small:
            small = eval_lisp_program(term)
    return small


def update(a, b):
    env[a] = b


def eval_lisp_program(x):
    if isinstance(x, list):
        if x[0] == "eq?":
            return eq(eval_lisp_program(x[1]), eval_lisp_program(x[2]))
        if x[0] == "quote":
            return quote(eval_lisp_program(x[1:]))
        if x[0] == "define":
            env[x[1]] = eval_lisp_program(x[2])
            print(env)
        if x[0] == "if":
            return if_clause(x[1:])
        if x[0] in mathematical_operators:
            return math_operators(x)
        if x[0] in relational_operators:
            return rel_operators(x)
        if x[0] == "car":
            return x[1][0]
        if x[0] == "cdr":
            return x[1][1:]
        if x[0] == "cons":
            return cons([x[1]], [x[2]])
        if x[0] == "max":
            return max(x[1:])
        if x[0] == "min":
            return min(x[1:])
        if x[0] == "update":
            return update(x[1], eval_lisp_program(x[2]))
        if x[0] == "#":
            pass
    elif isinstance(x, str):
        return env[x]
    elif isinstance(x, int):
        return x

program = input("Enter Lisp Input: ")
parsed_list = parse_lisp_program(program)
print("Parsed list: {}".format(parsed_list))
print("Evaluated result: {}".format(eval_lisp_program(parsed_list)))
