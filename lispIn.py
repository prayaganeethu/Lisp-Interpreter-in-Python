def tokenizeLispProg(lispProgram):
    return lispProgram.replace("(", " ( ").replace(")", " ) ").split()


def numberOrSymbol(token):
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return str(token)


def readAsList(lispList):
    if len(lispList) == 0:
        raise SyntaxError("Unexpected EOF while reading")
    token = lispList.pop(0)
    if token == "(":
        newList = []
        while lispList[0] != ")":
            newList.append(readAsList(lispList))
        lispList.pop(0)
        return newList
    elif token == ")":
        raise SyntaxError('Unexpected )')
    else:
        return numberOrSymbol(token)


def parseLispProgram(lispProgram):
    return readAsList(tokenizeLispProg(lispProgram))

program = input("Enter Lisp Input")
print(parseLispProgram(program))
# print(tokenizeLispProg(program))
