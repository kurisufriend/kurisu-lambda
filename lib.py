# MISSNG UR LEYEBRARY?!!?!!
# BET UR MAD BAKADESU HAHAHAHHAHAHAHAH
# t. cirno

idspace = {}
funcspace = {}

def execute(program):
    import traceback, copy
    def _execute(ctx, ids, fns):
        import sys, functools
        lids = copy.deepcopy(ids)
        lfns = copy.deepcopy(fns)
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


            if ctx[0] == _ident("defun"):
                fns[ctx[1]] = ctx[2]
                return fns[ctx[1]]
            elif ctx[0] == _ident("cond"):
                return _execute(ctx[2], lids, lfns) if _truthy(_execute(ctx[1], lids, lfns)) else _execute(ctx[3], lids, lfns)

            subs = _fixarr(list(map(lambda a: _execute(a, lids, lfns), ctx)))

            if ctx[0][1][0] == "$":
                return subs
            elif ctx[0][1] == "id":
                return subs[1] if len(subs[1:]) == 1 else subs[1:]
            elif ctx[0] == _ident("miracle"):
                return _box(eval(_destr(subs[1]))[_destr(subs[2])](*[i[1] for i in _fixarr(subs[3])]))
            elif ctx[0] == _ident("def"):
                ids[ctx[1]] = subs[2]
                return ids[ctx[1]]
            elif ctx[0] == _ident("+"):
                return (subs[1][0], subs[1][1]+subs[2][1])
            elif ctx[0] == _ident("-"):
                return (subs[1][0], subs[1][1]-subs[2][1])
            elif ctx[0] == _ident("*"):
                return (subs[1][0], subs[1][1]*subs[2][1])
            elif ctx[0] == _ident("/"):
                return (subs[1][0], subs[1][1]/subs[2][1])
            elif ctx[0] == _ident("%"):
                return (subs[1][0], subs[1][1]%subs[2][1])
            elif ctx[0] == _ident("!"):
                return ("number", 0.0 if subs[1] else 1.0)
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
                ret = _execute(subs[1], lids, lfns)
                for statement in subs[2:]:
                    ret = _execute(statement, lids, lfns)
                return ret
            elif ctx[0] == _ident("at"):
                return subs[2][int(subs[1][1])]
            elif ctx[0] == _ident("insert"):
                subs[3].insert(int(subs[1][1]), subs[2])
                return subs[3]
            elif ctx[0] in fns:
                #print(subs)
                prototype = fns[ctx[0]]
                for idx, arg in enumerate(subs[1:]):
                    idx += 1
                    prototype = _recursereplace(prototype, ("identifier", f"${idx}"), arg)
                    #print(f"${idx}", prototype)
                #print(prototype)
                return _execute(prototype, lids, lfns)
            else:
                print("no such function", ctx[0])
                return None

        else:
            #print("base", ctx)
            if type(ctx) == type([]):
                return list(
                    map(lambda a: _execute(a, lids, lfns), ctx)
                )
            return ctx
    for strand in program:
        try: _execute(strand, idspace, funcspace)
#        _execute(strand)
        except Exception as e: 
            print("failed in", strand, "with", e)
            _execute(strand, idspace, funcspace)
    #input()

