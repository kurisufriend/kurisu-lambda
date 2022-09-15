# MISSNG UR LEYEBRARY?!!?!!
# BET UR MAD BAKADESU HAHAHAHHAHAHAHAH
# t. cirno

idspace = {}
funcspace = {}

def execute(ctx):
    def _execute(ctx):
        import sys, functools
        def _ident(name):
            return ("identifier", name)
        def _destr(t):
            return t[1] if t[0] == "string" else ""
        def _fixarr(a):
            for i in a:
                if i[0] == "identifier":
                    a[a.index(i)] = idspace[i]
            return a
        def _recursereplace(i, fr, to):
            if type(i) == type([]):
                subs = list(
                    map(lambda a: _recursereplace(a, fr, to), i)
                )
                return subs
            else:
                return to if i == fr else i
        if type(ctx) == type([]) and ctx[0][0] == "identifier":
            subs = list(
                map(lambda a: _execute(a), ctx)
            )
            #print("abba", ctx, subs)
            if ctx[0][1] == "id":
                return subs[1] if len(subs[1:]) == 1 else subs[1:]
            elif ctx[0] == _ident("miracle"):
                return getattr(sys.modules[_destr(subs[1])], _destr(subs[2]))(*[i[1] for i in _fixarr(subs[3])])
            elif ctx[0] == _ident("def"):
                idspace[subs[1]] = subs[2]
                return idspace[subs[1]]
            elif ctx[0] == _ident("+"):
                return (subs[1][0], subs[1][1]+subs[2][1])
            elif ctx[0] == _ident("defun"):
                funcspace[subs[1]] = subs[2]
                return funcspace[subs[1]]
            elif ctx[0] in funcspace:
                prototype = funcspace[ctx[0]]
                for idx, arg in enumerate(subs[1:]):
                    idx += 1
                    prototype = _recursereplace(prototype, ("identifier", f"${idx}"), arg)
                    #print(f"${idx}", prototype)
                return _execute(prototype)
            else:
                print("no such function", ctx[0])
                return None

        else:
            #print("base", ctx)
            if type(ctx) == type([]):
                return list(
                    map(lambda a: _execute(a), ctx)
                )
            return ctx
    _execute(ctx)
    #input()


def oldexecute(ctx):
    import sys
    def _ident(name):
        return ("identifier", name)
    def _destr(t):
        return t[1] if t[0] == "string" else ""
    def _fixarr(a):
        for i in a:
            if i[0] == "identifier":
                a[a.index(i)] = idspace[i]
        return a

                
    if ctx[0] == _ident("miracle"):
        getattr(sys.modules[_destr(ctx[1])], _destr(ctx[2]))(*[i[1] for i in _fixarr(ctx[3])])
    elif ctx[0] == _ident("def"):
        idspace[ctx[1]] = ctx[2]
    elif ctx[0] == _ident("eval"):
        execute(ctx[1])