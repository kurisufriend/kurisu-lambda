this language belongs to makise kurisu. there are many like it, but this one is hers.

the interpreter is currently written in python 3. when I feel comfortable with the 
implemented features, a "real" spec will be frozen and I will make a native one.
this implementation does not rely on any modules or libraries outside of the python
standard library.

syntax:

a program is a series of functions executed using one environment -- that is, sharing 
some defined variables and functions.
these functions are executed homoiconic objects made up of language types:
- list, `()` and everything inside. items are delimited by whitespace.
- string, everything between `"` double quotes
- number, everything capable of being represented as a decimal float value
- lambda, an anonymous expression containing the args and procedure
- identifier, everything else
an identifier previously defined in the scope will expand upon execution
to the expression it is defined to. e.g. (def add (lambda (a b) a+b)) will
cause any executed instance of `add` to expand to (lambda (a b) a+b)).
lists starting with lambda are executed with the rest of the list as parameters,
i.e. (spit "hello~" (+ 9000 1)). runs the lambda `spit` refers to using "hello" 
and (+ 9000 1). the lower-order function is calculated for the higher-order one,
so it ends up calling `spit` with "hello" and 9001.
there are also pre-processor macros:
- INCLUDE:<path>, for expanding and inserting another file
- DEFINE:<name>:macro:<arg1>:<arg2>:<argn>, for defining macros
- <defined macro>:<arg1>:<arg2>:<argn>, for expanding macros
- :<misc>, for adding comments (lines removed in pre-processing)
you may notice that the language looks like a lisp/scheme and the preprocessor keywords
are similar to m4/cpp. I'm a fan of homoiconicity, and this provides both a familiar and
delightfully simple syntax. note that it doesn't actually function like a lisp under the
hood: there's no cons, for instance. no church numerals either, so it isn't pure(tm).

examples:

<===
(thesis)
===>
this language belongs to makise kurisu. there are many like it, but this one is hers.

<===
(def a (id "desu"))
(spit
	("lol swej" (+ 9000 1) a))
===>
lol swej 9001.0 desu

<===
(spit "how old are you? > ")
(def age (conv number (input)))
(spit
	(cond (> age 18)
		"adult (hag)"
		"not adult (uoh)"))
=='9' STDIN=>
not adult (uoh)