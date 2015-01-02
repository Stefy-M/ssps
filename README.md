ssps
====

Staticly-scoped Simple PostScript compiler created in Python for CptS 355 - Programming Language Design.

This is a compiler for a variation on the PostScript programming language. This variation has most of the non-graphical language features of PostScript except that floating point numbers are not handled, and there are no dictionary commands like dictz begin and end. Instead, the language is statically scoped, so the dictionarystack is handled by the compiler instead of the user.
