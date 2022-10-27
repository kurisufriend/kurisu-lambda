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

demonstrative examples:

<===
:comments are pre-processed (i.e. ignored) when the `:` character starts 
: a line. for this example page, multi-line comments will have an extra
:   space before continuation of the text.

:the identifier `hello` will henceforth expand to "world"
(def hello "world")

(def hello (+ "goodbye, " hello "!!"))
:this sets `hello`'s expansion to the following (executed in steps):

: (+ "goodbye, " hello "!!"))

:then `hello` gets expanded to its set value, "world"...
: (+ "goodbye, " "world" "!!"))

:then the `+` builtin executes, using "goodbye, ", "world", and "!!" as
: parameters, which concatenates them
:finally, we end up with
: "goodbye, world!!"
:which `hello` will henceforth expand to

===>
-

<===
:define the identifier `spit-raw` to a lambda expansion that 
: takes one argument (`cunny`)
(def spit-raw (lambda (cunny) 
    (w "/dev/fd/1" cunny)))
:it writes the passed argument to /dev/fd/1, a.k.a STDOUT

:define another lambda expansion, this time appending a newline
: escape to the parameter and calling `split-raw` on it
(def spit (lambda (cunny)
    (spit-raw (+ (conv string cunny) "\n"))))

:a final lambda expansion, here defining `thesis` as an lambda
: process that prints a particular string
(def thesis (lambda ()
	(spit
		"this language belongs to makise kurisu. there are many like it, but this one is hers.")))

(thesis)
===>
this language belongs to makise kurisu. there are many like it, but this one is hers.

<===
:use our ability to pass code around for the creation of a recursive looping macro 
(def loop (lambda (min i statement)
    (all 
        statement
        (cond (= i min)
            false
            (loop min (- i 1) (id statement))))))

:use the loop macro to define another macro executing for each item in a list
(def each
    (lambda (it action)
        (loop 0 (- (length it) 1)
            (id all 
                (def item (at i it))
                action))))

:define a modulo operation recursively
(def % (lambda (a m)
    (cond (== m a)
        0
        (cond (< m a)
            (% (- a m) m)
            (- a 0)))))
===>

<===
:call our loop macro, passing the loop range (from 0 to 100 inclusive) and the statement
:since the statement is being called in the macro scope, `i` successfully expands
: to the current value of the counter
(loop 0 100 
	(id spit (cond (% i 15) (cond (% i 5) (cond (% i 3) i "fizz") "buzz") "fizzbuzz")))
:the statement is wrapped in a call to the id function, preventing it from being executed
: before getting to the macro
===>
fizzbuzz
1.0
2.0
fizz
4.0
buzz
fizz
7.0
8.0
fizz
buzz
11.0
fizz
13.0
14.0
fizzbuzz
16.0
17.0

[...]

fizz
97.0
98.0
fizz
buzz

<===
:define a variable, `moeblob`, that expands to a list
(def moeblob ("moe" "moe~" "kyun!!"))
:iterate over said list, passing each item to a statement
:the statement is only executed in the scope of the macro, so `item` expands to the
: actual value of each item
(each moeblob
	(id spit item))
===>
moe
moe~
kyun!!