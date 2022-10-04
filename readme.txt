this language belongs to makise kurisu. there are many like it, but this one is hers.


syntax:

a program is a series of functions executed using one environment -- that is, sharing 
defined variables and functions.
these functions are executed homoiconic objects made up of language types:
- list, `()` and everything inside. items are delimited by whitespace.
- string, everything between `"` double quotes
- number, everything capable of being represented as a decimal float value
- identifier, everything else
lists starting with defined function identifiers are executed with the rest of the list
as parameters, i.e. (spit "hello~" (+ 9000 1)). runs `spit` using "hello" and (+ 9000 1).
the lower-order function is calculated for the higher-order one, so it ends up calling
`spit` with "hello" and 9001.

examples:

<===
(thesis)
===>
this language belongs to makise kurisu. there are many like it, but this one is hers.

<===
(def a (id (id "desu")))
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