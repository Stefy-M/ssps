# Programmer: Jesse Chisholm
# Program: Static Simple PostScript (CptS 355 HW6)
#
# Description: This is a compiler for a variation on the PostScript programming language. This
#              variation has most of the non-graphical language features of PostScript except that
#              there are no dictionary commands like dictz begin and end. Instead, the language
#              is dynamically scoped by default (with an optional flag to behave as if statically
#              scoped), so that the dictionary stack is handled by the compiler instead of the user.
#              Floating point numbers are not currently supported in SSPS.
#
# How to use: Run the command "python ssps.py [flags] input-filename" or "python3 [flags] ssps.py input-filename",
#             depending on how python is installed on your system. The program defaults with debug mode off and
#             static mode off.
#
#             Optional Flags:
#                    -x : Run in debug mode, producing detailed debugging output while interpreting the program code.
#                    -s : Run in static mode, running the program as if SSPS is statically scoped.
#                    -d : Run in dynamic mode, running the program code as if SSPS is dynamically scoped.


# -------------------------\
# Operand Stack Operations |
# -------------------------/


def op_push(operand):
    """
    Push operand onto the operand stack.
    Throws an error if the operand is a float.
    """
    if is_float(operand):
        error("op_push", "float argument encountered", [operand])
    op_stack.append(operand)


def op_pop():
    """
    Remove and return top of the operand stack.
    Throws an error if the operand stack is empty.
    """
    if is_empty(op_stack):
        error("op_pop", "empty operand stack")
    return op_stack.pop()


def dup_op():
    """
    Duplicates the top operand on the operand stack.
    """
    debug("***dup_op performed***")
    debug("Operand Stack (Before): " + str(op_stack)[1:-1])
    val = op_pop()
    dup = val
    op_push(val)
    op_push(dup)
    debug("Operand Stack (After): " + str(op_stack)[1:-1])
    debug()


def exch_op():
    """
    Swaps the top two operands on the operand stack.
    """
    debug("***exch_op performed***")
    debug("Operand Stack (Before): " + str(op_stack)[1:-1])
    second = op_pop()
    first = op_pop()
    op_push(second)
    op_push(first)
    debug("Operand Stack (After): " + str(op_stack)[1:-1])
    debug()


def stack_op():
    """
    Prints contents of operand and dictionary stacks.
    """
    print("==============")

    op_stack.reverse()
    for operand in op_stack:
        print(operand)
    op_stack.reverse()

    print("==============")

    dict_stack.reverse()
    index = len(dict_stack) - 1
    for (d, link) in dict_stack:
        print("----", index, "---- ", end="")
        if static:
            print(link, "----", end="")
        print()
        for (k, v) in d.items():
            print(k, " [", v, "]", sep="")
        index -= 1
    dict_stack.reverse()

    print("==============")


def top_op():
    """
    Pops operand off of operand stack and prints it.
    """
    print(op_pop())


# ----------------------\
# Arithmetic Operations |
# ----------------------/


def add_op():
    """
    Takes two operands from the operand stack,
    performs an integer addition operation,
    and pushes the integer result to the operand stack.
    Throws an error if any operand is not an integer.
    """
    debug("***add_op performed***")
    debug("Operand Stack (Before): " + str(op_stack)[1:-1])
    second = op_pop()
    first = op_pop()
    if is_int(first) and is_int(second):
        op_push(first + second)
    else:
        error("add_op", "non-int operand encountered", [first, second])
    debug("Operand Stack (After): " + str(op_stack)[1:-1])
    debug()


def sub_op():
    """
    Takes two operands from the operand stack,
    performs an integer subtraction operation,
    and pushes the integer result to the operand stack.
    Throws an error if any operand is not an integer.
    """
    debug("***sub_op performed***")
    debug("Operand Stack (Before): " + str(op_stack)[1:-1])
    second = op_pop()
    first = op_pop()
    if is_int(first) and is_int(second):
        op_push(first - second)
    else:
        error("sub_op", "non-int operand encountered", [first, second])
    debug("Operand Stack (After): " + str(op_stack)[1:-1])
    debug()


def mul_op():
    """
    Takes two operands from the operand stack,
    performs an integer multiplication operation,
    and pushes the integer result to the operand stack.
    Throws an error if any operand is not an integer.
    """
    debug("***mul_op performed***")
    debug("Operand Stack (Before): " + str(op_stack)[1:-1])
    second = op_pop()
    first = op_pop()
    if is_int(first) and is_int(second):
        op_push(first * second)
    else:
        error("mul_op", "non-int operand encountered", [first, second])
    debug("Operand Stack (After): " + str(op_stack)[1:-1])
    debug()


def div_op():
    """
    Takes two operands from the operand stack,
    performs an integer division operation,
    and pushes the integer result to the operand stack.
    Throws an error if any operand is not an integer,
    or if dividing by zero.
    """
    debug("***div_op performed***")
    debug("Operand Stack (Before): " + str(op_stack)[1:-1])
    second = op_pop()
    first = op_pop()
    if is_int(first) and is_int(second):
        if second != 0:
            op_push(first // second)
        else:
            error("div_op", "dividing by zero", [first, second])
    else:
        error("div_op", "non-int operand encountered", [first, second])
    debug("Operand Stack (After): " + str(op_stack)[1:-1])
    debug()


# ----------------------\
# Comparison Operations |
# ----------------------/


def eq_op():
    """
    Takes two operands from the operand stack,
    performs an integer or boolean equality comparison,
    and pushes the boolean result to the operand stack.
    Throws an error if the operands are not either
    both booleans or both integers.
    """
    debug("***eq_op performed***")
    debug("Operand Stack (Before): " + str(op_stack)[1:-1])
    second = op_pop()
    first = op_pop()
    if is_int(first) and is_int(second):
        op_push(first == second)
    elif is_bool(first) and is_bool(second):
        op_push(first == second)
    else:
        error("eq_op", "non-matching operand types encountered", [first, second])
    debug("Operand Stack (After): " + str(op_stack)[1:-1])
    debug()


def lt_op():
    """
    Takes two operands from the operand stack,
    performs an integer less-than comparison,
    and pushes the boolean result to the operand stack.
    Throws an error if any operand is not an integer.
    """
    debug("***lt_op performed***")
    debug("Operand Stack (Before): " + str(op_stack)[1:-1])
    second = op_pop()
    first = op_pop()
    if is_int(first) and is_int(second):
        op_push(first < second)
    else:
        error("lt_op", "non-int operand encountered", [first, second])
    debug("Operand Stack (After): " + str(op_stack)[1:-1])
    debug()


def gt_op():
    """
    Takes two operands from the operand stack,
    performs an integer greater-than comparison,
    and pushes the boolean result to the operand stack.
    Throws an error if any operand is not an integer.
    """
    debug("***gt_op performed***")
    debug("Operand Stack (Before): " + str(op_stack)[1:-1])
    second = op_pop()
    first = op_pop()
    if is_int(first) and is_int(second):
        op_push(first > second)
    else:
        error("gt_op", "non-int operand encountered", [first, second])
    debug("Operand Stack (After): " + str(op_stack)[1:-1])
    debug()


# -------------------\
# Boolean Operations |
# -------------------/


def and_op():
    """
    Takes two operands from the operand stack,
    performs a boolean 'and' operation,
    and pushes the boolean result to the operand stack.
    Throws an error if any operand is not a boolean.
    """
    debug("***and_op performed***")
    debug("Operand Stack (Before): " + str(op_stack)[1:-1])
    second = op_pop()
    first = op_pop()
    if is_bool(first) and is_bool(second):
        op_push(first and second)
    else:
        error("and_op", "non-bool operand encountered", [first, second])
    debug("Operand Stack (After): " + str(op_stack)[1:-1])
    debug()


def or_op():
    """
    Takes two operands from the operand stack,
    performs a boolean 'or' operation,
    and pushes the boolean result to the operand stack.
    Throws an error if any operand is not a boolean.
    """
    debug("***or_op performed***")
    debug("Operand Stack (Before): " + str(op_stack)[1:-1])
    second = op_pop()
    first = op_pop()
    if is_bool(first) and is_bool(second):
        op_push(first or second)
    else:
        error("or_op", "non-bool operand encountered", [first, second])
    debug("Operand Stack (After): " + str(op_stack)[1:-1])
    debug()


def not_op():
    """
    Takes one operand from the operand stack,
    performs a boolean 'not' operation,
    and pushes the boolean result to the operand stack.
    Throws an error if the operand is not a boolean.
    """
    debug("***not_op performed***")
    debug("Operand Stack (Before): " + str(op_stack)[1:-1])
    value = op_pop()
    if is_bool(value):
        op_push(not value)
    else:
        error("not_op", "non-bool operand encountered", [value])
    debug("Operand Stack (After): " + str(op_stack)[1:-1])
    debug()


# -------------\
# Conditionals |
# -------------/


def if_op():
    """
    Takes a boolean and a code array from the operand stack,
    and only interprets the code array if the boolean is True.
    """
    debug("***if_op performed***")
    debug("Operand Stack (Before): " + str(op_stack)[1:-1])
    if_code = op_pop()
    boolean = op_pop()
    if is_bool(boolean):
        if boolean:
            interpret(if_code)
    else:
        error("if_op", "non-bool operand encountered", [boolean])
    debug("Operand Stack (After): " + str(op_stack)[1:-1])
    debug()


def if_else_op():
    """
    Takes a boolean and two code arrays from the stack,
    only interprets the first code array if the boolean is True,
    and only interprets the second code array if the boolean is False.
    """
    debug("***if_else_op performed***")
    debug("Operand Stack (Before): " + str(op_stack)[1:-1])
    else_code = op_pop()
    if_code = op_pop()
    boolean = op_pop()
    if is_bool(boolean):
        if boolean:
            interpret(if_code)
        else:
            interpret(else_code)
    else:
        error("if_else_op", "non-bool operand encountered", [boolean])
    debug("Operand Stack (After): " + str(op_stack)[1:-1])
    debug()


# ----------------------\
# Dictionary Operations |
# ----------------------/


def is_in_dict(d, name):
    """
    Checks if the dictionary d contains the key name.
    Returns True if the key is found, False otherwise.
    """
    return name in d


def get_from_dict(d, name):
    """
    Returns the value associated with the key name in dictionary d.
    Throws an error if key does not exist in d.
    """
    if is_in_dict(d, name):
        return d[name]
    # May be unnecessary to ever throw this error, but why not just in case.
    error("get_from_dict", "name not found", [name])


def add_to_dict(d, name, value):
    """
    Adds the name-value association pair to dictionary d.
    """
    d[name] = value


# ----------------------------\
# Dictionary Stack Operations |
# ----------------------------/


def dict_push(d, link):
    """
    Push dictionary d with access link onto the dictionary stack.
    """
    dict_stack.append((d, link))


def dict_pop():
    """
    Remove and return top of the dictionary stack.
    Throws an error if the dictionary stack is empty.
    """
    if is_empty(dict_stack):
        error("dict_pop", "empty dictionary stack")
    return dict_stack.pop()


def def_op():
    """
    Takes a name and a value from the operand stack,
    gets the top dictionary d from the dictionary stack,
    adds the name-value association to d,
    and pushes d back on the dictionary stack.
    Throws an error if the name is formatted incorrectly.
    """
    debug("***def_op performed***")
    debug("Operand Stack (Before): " + str(op_stack)[1:-1])
    debug("Top Dictionary and Link (Before): " + str(dict_stack[-1])[1:-1])
    value = op_pop()
    name = op_pop()
    if not is_name(name):
        error("def_op", "trying to define non-name", [name])
    (d, link) = dict_pop()
    add_to_dict(d, name[1:], value)
    dict_push(d, link)
    debug("Operand Stack (After): " + str(op_stack)[1:-1])
    debug("Top Dictionary and Link (After): " + str(dict_stack[-1])[1:-1])
    debug()


def get_link(name):
    """
    Searches for the name in each dictionary on the dictionary stack,
    starting with the top dictionary working down.
    If the name is found in any dictionary, returns the positive index of the
    dictionary that contains the name.
    Throws error if the name is not found in any dictionary.
    """
    index = 0
    dict_stack.reverse()
    for (d, link) in dict_stack:
        if is_in_dict(d, name):
            dict_stack.reverse()
            return len(dict_stack) - index - 1
        index += 1
    error("get_link", "name is undefined", [name])


def lookup(name):
    """
    If the name is found in or below the current scope, returns the value of the name.
    Follows static links if static, goes top-down if dynamic.
    Throws error if the name is not found in or below the current scope.
    """
    if static:
        index = -1
        while True:
            (d, link) = dict_stack[index]
            debug("Current dictionary: " + str(d))
            debug("Static link: " + str(link))
            if is_in_dict(d, name):
                return get_from_dict(d, name)
            else:
                if not is_int(link):
                    error("lookup", "name is undefined in current static scope", [name])
                if index == link:
                    error("lookup", "infinite loop", [name])
                debug("Following static link to index " + str(link) + "...")
                index = link
    else:
        link = get_link(name)
        debug("Following dynamic links, the name \"" + str(name) + "\" was found at index " + str(link))
        if not is_int(link):
            error("lookup", "name is undefined in current dynamic scope", [name])
        (d, link) = dict_stack[link]
        return get_from_dict(d, name)


# ----------------\
# Other Functions |
# ----------------/


def debug(message="", sep=" ", end="\n"):
    """
    Debugging output, only prints if debugging is enabled.
    """
    if debugging:
        print(message, sep, end)


def is_bool(value):
    """
    Helper function that checks if value is a boolean.
    Returns True if value is boolean, False if not.
    """
    return type(value) is bool


def is_int(value):
    """
    Helper function that checks if value is an integer.
    Returns True if value is an integer, False if not.
    """
    return type(value) is int


def is_float(value):
    """
    Helper function that checks if value is a float.
    Returns True if value is an float, False if not.
    """
    return type(value) is float


def is_string(value):
    """
    Helper function that checks if value is a string.
    Returns True if value is an string, False if not.
    """
    return type(value) is str


def is_dict(value):
    """
    Helper function that checks if value is a dictionary.
    Returns True if value is an dict, False if not.
    """
    return type(value) is dict


def is_name(value):
    """
    Helper function that checks if value is a /name.
    Returns True if value is a /name, False if not.
    """
    if not is_string(value):
        return False
    if value[0] != '/':
        return False
    return True


def is_empty(stack):
    """
    Helper function that checks if a stack is empty.
    Returns True if the stack is empty, False if not.
    """
    return len(stack) < 1


def error(criminal, crime, accomplices=[]):
    """
    Prints semi-detailed error message and exits program.
    """
    print("Error in ", criminal, ": ", crime, ".", sep="")
    if accomplices != []:
        print("Problem Arguments: ", str(accomplices)[1:-1])
    op_stack.reverse()
    dict_stack.reverse()
    print("SPS Operand Stack: ", str(op_stack)[1:-1])
    print("SPS Dictionary Stack: ", str(dict_stack)[1:-1])
    dict_stack.reverse()
    op_stack.reverse()
    print("Exiting program.")
    sys.exit()


def condense(code):
    """
    Tokenize code string and, additionally, condense outermost code arrays
    from code into singular token strings with curly braces included.
    """
    tokens = re.findall("/?[a-zA-Z][a-zA-Z0-9_]*|[-]?[0-9]+|[}{]+|%.*|[^ \t\n]", code)
    if '{' not in code:
        return tokens
    count = 0
    code_arr = ""
    res = []
    for token in tokens:
        if count != 0:
            if token == '{':
                count += 1
            if token == '}':
                count -= 1
            if count == 0:
                res.append('{' + code_arr[:-1] + '}')
                code_arr = ""
            else:
                code_arr += token + " "
        else:
            if token == '{':
                count += 1
            else:
                res.append(token)
    return res


def interpret(code):
    """
    Takes a string of an SPS program as an argument, tokenizes it,
    and for each token, performs the appropriate SPS action accordingly.
    """
    debug("=======================Interpreting Code=======================")
    debug("Code: \"" + code + "\"")
    debug("Operand stack: " + str(op_stack)[1:-1])
    debug("Dictionary stack: " + str(dict_stack)[1:-1])
    debug("Top dictionary: " + str(dict_stack[-1])[1:-1])
    debug()

    # Tokenize and condense the code.
    tokens = condense(code)
    for token in tokens:
        # Handling operations....
        if token == "add":
            add_op()
        elif token == "sub":
            sub_op()
        elif token == "mul":
            mul_op()
        elif token == "div":
            div_op()
        elif token == "eq":
            eq_op()
        elif token == "lt":
            lt_op()
        elif token == "gt":
            gt_op()
        elif token == "and":
            and_op()
        elif token == "or":
            or_op()
        elif token == "not":
            not_op()
        elif token == "if":
            if_op()
        elif token == "ifelse":
            if_else_op()
        elif token == "dup":
            dup_op()
        elif token == "exch":
            exch_op()
        elif token == "stack":
            stack_op()
        elif token == "=":
            top_op()
        elif token == "pop":
            op_pop()
        elif token == "def":
            def_op()
        # ...handling pushing bools and code arrays.
        elif token == "true":
            op_push(True)
        elif token == "false":
            op_push(False)
        elif token[0] == '{':
            op_push(token[1:-1])
        else:
            # Could now be an integer, /name or name lookup; if int, push the int.
            try:
                num = int(token)
                op_push(num)
            except ValueError:
                # Could now be a /name or a name lookup; if /name, push the /name.
                if is_name(token):
                    op_push(token)
                else:
                    debug("***Name lookup***")
                    debug("Name being looked up: \"" + token + "\"")
                    debug("Dictionary stack: " + str(dict_stack)[1:-1])

                    # lookup name and receive code.
                    code = lookup(token)

                    debug("Code found: \"" + str(code) + "\"")
                    debug()

                    # Create dummy link if dynamic.
                    # Using scientific number of the beast for the lols.
                    link = 666
                    if static:
                        debug("***Getting Link***")
                        debug("Name being looked up: \"" + token + "\"")
                        debug("Dictionary stack: " + str(dict_stack)[1:-1])

                        # Get link before interpreting if static.
                        link = get_link(token)

                        debug("Link made: index " + str(link))
                        debug()

                    # Recursively interpret the string version of the code received.
                    dict_push({}, link)
                    interpret(str(code))
                    dict_pop()


# ----------------\
# Main Code Block |
# ----------------/


if __name__ == "__main__":

    import sys
    import re

    # Our operand and dictionary stacks, as well as static and debugging flags.
    global op_stack
    global dict_stack
    global static
    global debugging
    op_stack = []
    dict_stack = [({}, None)]
    static = False
    debugging = False

    # Gather command line arguments and filename in clean format.
    args = ""
    filename = ""
    for arg in sys.argv:
        if arg[0] == '-':
            for c in arg[1:]:
                args += c
        else:
            filename = arg

    # Set static and debugging flags based on command line arguments.
    for c in args:
        if c == 's':
            static = True
        elif c == 'd':
            static = False
        elif c == 'x':
            debugging = True
        else:
            print("Command line argument '", c, "' not recognized. Skipping...", sep="")

    # Open file passed in via command line, store file's lines as one code string.
    lines = []
    try:
        lines = open(filename).readlines()
    except IOError:
        error("reading file", "file does not exist", [filename])
    program = ""
    for line in lines:
        program += line[:-1] + " "

    # Finally, interpret the program code, and cross your fingers...
    interpret(program)