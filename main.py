import lib, sys, pathlib

def isnum(n):
    try:
        float(n)
    except:
        return False
    return True

def preprocess(filename):
    def expand(file, path):
        working_directory = pathlib.Path(path).parent.resolve()
        tmp = file.replace("\\\n", "").split("\n")
        defs = {}
        for idx, i in enumerate(tmp):
            parts = i.split(":")
            if len(i) < 1:
                continue
            elif i[:8] == "INCLUDE:":
                fpath = str(working_directory)+"/"+i[8:]
                tdefs, tmp[idx] = expand(open(fpath).read(), fpath)
                defs.update(tdefs)
            elif i[:7] == "DEFINE:":
                parts = parts[1:]
                defs[parts[0]] = (parts[2:], parts[1].replace("\t", " "))
                tmp.pop(idx)
            elif i[0] == ":":
                tmp.pop(idx)
            elif i.split(":")[0] in defs.keys():
                parts = i.split(":")
                args, exp = defs[parts[0]]

                for arg_idx, arg in enumerate(parts[1:]):
                    if len(args) < 1: break
                    exp = exp.replace(
                        args[arg_idx], arg
                    )
                #print(exp, "exp")
                tmp[idx] = exp
            #print(i, "\nsep")
        return (defs, "\n".join(tmp))

    f = open(filename).read()
    f = expand(f, sys.argv[1])[1]

    f = f.replace(" ", " RDANEELOLIVAW ") # spacer
    for r in ["(", ")", "\"", ","]: f = f.replace(r, " "+r+" ")
    return f.split()

def tokenize(f):
    toks = []
    collector = ""
    instr = False
    i = 0
    while i < len(f):
        c = f[i]
        if c == "\"":
            nex = f.index("\"", i+1)
            toks.append("".join(f[i:nex+1]).replace("RDANEELOLIVAW", " "))
            i = nex+1
            continue
        elif c == "(" or c == ")":
            pass
        elif c == ",":
            pass
        elif isnum(c):
            toks.append(float(c))
            i += 1
            continue
        elif c == "RDANEELOLIVAW":
            i += 1
            continue
        toks.append(c)
        i += 1
    return toks

def lex(toks):
    lexed = []
    parendepth = 0
    for t in toks:
        if type(t) == type(0.0):
            lexed.append(("number", t))
        elif t[0] == "\"":
            lexed.append(("string", t[1:-1]))
        elif t == "(":
            lexed.append(("open", parendepth))
            parendepth += 1
        elif t == ")":
            parendepth -= 1
            lexed.append(("close", parendepth))
        elif t == ",":
            pass#lexed.append(("sep", None))
        else:
            lexed.append(("identifier", t))
    return lexed

def structurize(program):
    def _amidone(prog):
        good = True
        for i in prog:
            if i[0] == "open":
                good = False
                break
        return good
    def _gethighestparen(prog):
        highest = -9001
        for i in prog:
            if i[0] == "open" and i[1] > highest:
                highest = i[1]
        return highest

    parenq = _gethighestparen(program)
    res = program
    while not _amidone(res):
        for i, tok in enumerate(program):
            if tok[0] == "open" and tok[1] == parenq:
                end = res.index(("close", parenq), i)
                res[i:end+1] = [res[i+1:end]]
        parenq -= 1
    return res




#print(tokenize(f))
#print(lex(tokenize(f)), "\n")
program = structurize(lex(tokenize(preprocess(sys.argv[1]))))
#lib.execute(structurize(lex(tokenize(f))))

#print(program)

lib.execute(program)
