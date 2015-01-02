ssps
====

Static Simple PostScript compiler created in Python for CptS 355 - Programming Language Design.

Description: This is a compiler for a variation on the PostScript programming language. This variation has most of the non-graphical language features of PostScript except that there are no dictionary commands like dictz begin and end. Instead, the language is dynamically scoped by default (with an optional flag to behave as if statically scoped), so that the dictionary stack is handled by the compiler instead of the user. Floating point numbers are not currently supported in SSPS.

How to use: Run the command "python ssps.py [flags] input-filename" or "python3 [flags] ssps.py input-filename", depending on how python is installed on your system. The program defaults with debug mode off and static mode off.

Optional Flags:
	-x : Run in debug mode, producing detailed debugging output while interpreting the program code.
	-s : Run in static mode, running the program as if SSPS is statically scoped.
	-d : Run in dynamic mode, running the program code as if SSPS is dynamically scoped.
