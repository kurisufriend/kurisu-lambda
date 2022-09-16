import lib, sys

def isnum(n):
    try:
        float(n)
    except:
        return False
    return True
reps = ["(", ")", "\"", ","]
f = open(sys.argv[1]).read()

def expand(file):
    tmp = file.split("\n")
    for idx, i in enumerate(tmp):
        if len(i) < 1:
            continue
        elif i[:8] == "INCLUDE:":
            tmp[idx] = expand(open(i[8:]).read())
        elif i[0] == ":":
            tmp.pop(idx)
    return "\n".join(tmp)

f = expand(f)


f = f.replace(" ", " RDANEELOLIVAW ") # spacer
for r in reps: f = f.replace(r, " "+r+" ")
f = f.split()

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

def shit_structurize(chunk):
    def splitlist(l, delim):
        res = []
        tmp = []
        for i in l:
            if i == delim:
                res.append(tmp)
                tmp = []
            else:
                tmp.append(i)
        res.append(tmp)
        res = list(filter(lambda a: a != [], res))
        if type(res) == type([]) and len(res) == 1:
            return res[0]
        return res
    if chunk[0][0] == "open":
        end = chunk.index(("close", chunk[0][1]))

        
        cunny = []
        cunny.append(chunk[1])

        jc = splitlist(chunk[2:end], ("sep", None))

        for i in jc:
            if chunk[0][0] == "open":
                #chunk.append(structurize(jc))
                #break
                print(chunk)
            cunny.append(structurize(i))
        print(cunny, len(cunny), jc)
        return cunny
    else:
        return chunk

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
program = structurize(lex(tokenize(f)))
#lib.execute(structurize(lex(tokenize(f))))

#print(program)

lib.execute(program)
