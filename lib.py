# MISSNG UR LEYEBRARY?!!?!!
# BET UR MAD BAKADESU HAHAHAHHAHAHAHAH
# t. cirno

def execute(program):
    import traceback, copy
    from functools import reduce
    def _execute(ctx, ids):
        import sys, functools
        lids = copy.copy(ids)
        def _ident(name):
            return ("identifier", name)
        def _destr(t):
            return t[1] if t[0] == "string" else ""
        def _fixarr(a):
            a = [a] if not type(a) == type([]) else a
            for i in a:
                if i[0] == "identifier" and i in ids:
                    a[a.index(i)] = ids[i]
            return a
        def _recursereplace(i, fr, to):
            if type(i) == type([]):
                subs = list(
                    map(lambda a: _recursereplace(a, fr, to), i)
                )
                return subs
            else:
                return to if i == fr else i
        def _truthy(i):
            if i[0] == "string":
                return True if i[1] else False
            elif i[0] == "number":
                return False if i[1] == 0 else True
            elif type(i) == type([]):
                good = False
                for j in i:
                    if _truthy(j):
                        good = True
                        break
                return good
            else:
                return False
        def _box(item):
            if type(item) == type(0) or type(item) == type(0.0):
                return ("number", item)
            elif type(item) == type(""):
                return ("string", item)
            elif type(item) == type([]):
                return list(map(lambda a: _box(a), item))
            else:
                return ("identifier", item)
        if type(ctx) == type([]) and ctx[0][0] == "identifier":
            #print("abba", ctx, subs)


            if ctx[0] == _ident("lambda"):
                return ("lambda", (ctx[1], ctx[2]))
            elif ctx[0] == _ident("cond"):
                return _execute(ctx[2], lids) if _truthy(_execute(ctx[1], lids)) else _execute(ctx[3], lids)
            elif ctx[0][1] == "id":
                return ctx[1] if len(ctx[1:]) == 1 else ctx[1:]

            subs = _fixarr(list(map(lambda a: _execute(a, lids), ctx)))

            if ctx[0][1][0] == "$":
                return subs

            elif ctx[0] == _ident("miracle"):
                return _box(getattr(eval(_destr(subs[1])), _destr(subs[2]))(*[(i if type(i) == type([]) else i[1]) for i in _fixarr(subs[3])]))
            elif ctx[0] == _ident("def"):
                ids[ctx[1]] = subs[2]
                return ids[ctx[1]]
            elif ctx[0] == _ident("+"):
                return reduce(lambda a, b: (a[0], a[1]+b[1]), subs[1:])
            elif ctx[0] == _ident("-"):
                return reduce(lambda a, b: (a[0], a[1]-b[1]), subs[1:])
            elif ctx[0] == _ident("*"):
                return reduce(lambda a, b: (a[0], a[1]*b[1]), subs[1:])
            elif ctx[0] == _ident("/"):
                return reduce(lambda a, b: (a[0], a[1]/b[1]), subs[1:])
            elif ctx[0] == _ident("%"):
                return (subs[1][0], subs[1][1]%subs[2][1])
            elif ctx[0] == _ident("!"):
                return ("number", 0.0 if _truthy(subs[1]) else 1.0)
            elif ctx[0] == _ident("=="):
                return ("number", 1.0 if subs[1] == subs[2] else 0.0)
            elif ctx[0] == _ident("="):
                return ("number", 1.0 if str(float(subs[1][1])) == str(float(subs[2][1])) else 0.0)
            elif ctx[0] == _ident(">"):
                return ("number", 1.0 if subs[1][1] > subs[2][1] else 0.0)
            elif ctx[0] == _ident("<"):
                return ("number", 1.0 if subs[1][1] < subs[2][1] else 0.0)
            elif ctx[0] == _ident("conv"):
                return (subs[1][1], float(subs[2][1]) if subs[1][1] == "number" else str(subs[2][1]))
            elif ctx[0] == _ident("all"):
                ret = _execute(subs[1], lids)
                for statement in subs[2:]:
                    ret = _execute(statement, lids)
                return ret
            elif ctx[0] == _ident("at"):
                return subs[2][int(subs[1][1])]
            elif ctx[0] == _ident("insert"):
                subs[3].insert(int(subs[1][1]), subs[2])
                return subs[3]
            else:
                #print(f"{subs[0]} is not a valid function")
                return _execute(subs, lids)
        elif ctx[0][0] == "lambda":
            prototype = ctx[0][1][1]
            ephemeral_space = copy.copy(ids)
            for idx, arg in enumerate(ctx[0][1][0]):
                ephemeral_space[arg] = ctx[1:][idx]
                #prototype = _recursereplace(prototype, arg, ctx[1:][idx])
            return _execute(prototype, ephemeral_space)
        else:
            if type(ctx) == type([]):
                return list(
                    map(lambda a: _execute(a, lids), ctx)
                )
                
            return ctx
    idspace = {}
    for strand in program:
        try: _execute(strand, idspace)
#        _execute(strand)
        except Exception as e: 
            print("failed in top-level", strand, "with", e)
            _execute(strand, idspace)
    #input()

