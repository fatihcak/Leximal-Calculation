INPUT_PATH = r"C:\Users\yusuf\OneDrive\Masaüstü\Python Projects\input.txt"
KEYWORDS = {"for": "FOR",
            "while": "WHILE",
            "if": "IF",
            "else": "ELSE",
            "|": "BITWISE_OR",
            "||": "LOGICAL_OR",
            "&": "BITWISE_AND",
            "&&": "LOGICAL_AND"}


class SymbolTable:
    """Symbol Table for lexical analyzer"""
    # count is index of last inserted element
    # initialized with 3 since first 4 elements are keywords
    count = 3

    def __init__(self):
        self.table = {"FOR": 0,
                      "WHILE": 1,
                      "IF": 2,
                      "ELSE": 3}
        # keeping inverse table ease the process of printing SymbolTable
        self.inv_table = {val: key for key, val in self.table.items()}

    def insert(self, identifier):
        if identifier in self.table:
            return self.table[identifier]
        # update the tables when identifier not already present
        self.count += 1
        self.table[identifier] = self.count
        self.inv_table[self.count] = identifier
        return self.count

    def __str__(self):
        headline = "==> SYMBOL TABLE <==\n"
        return headline + "\n".join([
            "{} -> {}".format(key, val) for key, val in self.inv_table.items()
        ]) + "\n" + "="*10


# initialize symbol table first time the file executes
symbol_table = SymbolTable()


class LexResult:
    """Object that lex() returns"""

    def __init__(self,
                token,
                integer_value=None,
                float_value=None,
                index=None,
                unrecognized_string=None):
        self.token = token
        self.integer_value = integer_value
        self.float_value = float_value
        self.index = index
        self.unrecognized_string = unrecognized_string

    def __str__(self):
        if self.token == "INTEGER":
            return "<token={}, integer_value = {}>".format(self.token,
                                                           self.integer_value)
        elif self.token == "FLOAT":
            return "<token={}, float_value = {}>".format(self.token,
                                                         self.float_value)
        elif self.token == "ID":
            return "<token={}, index = {}>".format(self.token, self.index)
        elif self.token == "ERROR":
            return "<token={}, unrecognized_string = {}>".format(self.token,
                                                                 self.unrecognized_string)
        else:
            return "<token={}>".format(self.token)


def read_file(path):
    """Read input file and return contents of file as single string"""
    with open(path) as f:
        input_string = f.read().replace("\n", ' ')
    return input_string


def show_menu():
    print("1. Call lex()")
    print("2. Show symbol table")
    print("3. Exit")


def get_tokens(string):
    """Get list of tokens from input string"""
    tokens = string.split(' ')
    valid_tokens = []
    for s in tokens:
        if s != ' ' and s != '':
            if '\n' in s:
                valid_tokens += s.split('\n')
            else:
                valid_tokens.append(s)
    return valid_tokens


def is_int(string):
    """Check whether a token is an int"""
    try:
        int(string)
        return True
    except ValueError:
        return False


def is_float(string):
    """Check whether a token is a float"""
    try:
        float(string)
        return True
    except ValueError:
        return False


def is_identifier(string):
    """Check whether a token is an identifier"""
    return not is_int(string[0])


def analyze(token):
    """Analyze the given token and return corresponding LexResult object"""
    if token in KEYWORDS:
        return LexResult(KEYWORDS[token])
    elif is_int(token):
        return LexResult("INTEGER", integer_value=int(token))
    elif is_float(token):
        return LexResult("FLOAT", float_value=float(token))
    elif is_identifier(token):
        # add to symbol table
        idx = symbol_table.insert(token)
        return LexResult("ID", index=idx)
    else:
        return LexResult("ERROR", unrecognized_string=token)


def lex(token):
    lex_result = analyze(token)
    return lex_result


if __name__ == "__main__":
    input_string = read_file(INPUT_PATH)
    tokens = get_tokens(input_string)
    while True:
        show_menu()
        chosen_option = input("Choose one option:")
        if chosen_option == "3":
            break
        elif chosen_option == "2":
            print(symbol_table)
        elif chosen_option == "1":
            for i, token in enumerate(tokens):
                result = lex(token)
                print(result)
        else:
            print("ERROR: invalid option!")
