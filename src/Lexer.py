import re
from src.Analyzer import *


class Lexer:
    def __init__(self):
        self.text = ""
        self.num_line = 1
        self.num_position = 0
        self.pos_space = 0
        self.num_token = 0
        self.file_name = ""
        self.file_lines = list()

        self.name_lex = {
            "if": "KeyW_IF",
            "else": "KeyW_ELSE",
            "elif": "KeyW_ELIF",
            "for": "KeyW_FOR",
            "while": "KeyW_WHILE",
            "pass": "KeyW_PASS",
            "in": "KeyW_IN",
            "return": "KeyW_RETURN",
            "break": "KeyW_BREAK",
            "or": "KeyW_OR",
            "and": "KeyW_AND",
            "not": "KeyW_NOT",
            "None": "KeyW_NONE",
            "import": "KeyW_IMPORT",
            "from": "KeyW_FROM",
            "def": "KeyW_DEF",

            ".": "Point",
            ",": "Comma",
            "+": "Plus",
            "-": "Minus",
            "*": "Multiplication",
            "/": "Division",
            "%": "Residual_Division",
            "=": "Assignment",
            "==": "Comparison",

            ":": "Colon",
            "!": "Exclamation_Mark",
            "(": "L_Paren_Bracket",
            ")": "R_Paren_Bracket",
            "[": "L_Sq_Bracket",
            "]": "R_Sq_Bracket",

            "\\": "Carryover",
            "\n": "\\n",
            "\t": "Tab",
            ">": "More",
            "<": "Less",
            "!=": "Not_Comparison",
            ">=": "More_Comparison",
            "<=": "Less_Comparison"
        }

        self.patterns = [r"^[0-9]+\.[0-9]*$",  # Real_Num
                         r"^[0-9]+$",  # Num
                         r"^[A-Za-z_][A-Za-z0-9_]*$",  # Id
                         r"^[\"\"].*[\"\"]$",  # String
                         r"^0x[A-Fa-f0-9]+$",  # Num_Hex
                         r"^0o[0-7]+$",  # Num_Oct
                         ]

    def file_in(self, filename):
        try:
            with open(filename) as file_object:
                self.text = file_object.read()
                self.file_name = filename
                self.text_space_refactor()
                file_object.close()
        except FileNotFoundError:
            return None
        else:
            return True

    def text_space_refactor(self):
        lex_symbols = [
            ["<=", ">=", "!=", "[", ",", "]", "+", "-", "*", "!", "==", "=", "<", ">", ":", "(", ")", "/", "%", "\t",
             "\n"],
            [" <= ", " >= ", " != ", " [ ", " , ", " ] ", " + ", " - ", " * ", " ! ", " == ",
             " = ", " < ", " > ", " : ", " ( ", " ) ", " / ", " % ", " \t ", " \n "]]

        with open(self.file_name) as f:
            self.file_lines = list(f)
            f.close()
        temp = ""
        is_comment = 0
        for i in range(len(self.text)):
            if self.text[i] == "#":
                is_comment = 1
            elif self.text[i] == "\n" and is_comment == 1:
                is_comment = 0
                temp += self.text[i]
            elif is_comment == 0:
                temp += self.text[i]
        self.text = temp

        # strings
        temp = ""
        is_string = 0
        j = 0
        while j < len(self.text):
            if self.text[j] == "\"":
                is_string = 1 if is_string == 0 else 0
            i = 0
            while i < len(lex_symbols[0]):
                if self.text[j:j + len(lex_symbols[0][i])] == lex_symbols[0][i] and is_string == 0:
                    temp += lex_symbols[1][i]
                    j += len(lex_symbols[0][i]) - 1
                    break
                i += 1
            if self.text[j] == "\n":
                is_string = 0
            if i == len(lex_symbols[0]):
                temp += self.text[j]
            j += 1
        # methods
        self.text = temp
        temp = ""
        for i in range(len(self.text)):
            if self.text[i] == "." and not re.findall(self.patterns[0], self.text[i - 1:i + 2]):
                temp += " " + self.text[i] + " "
            else:
                temp += self.text[i]

        self.text = temp
        self.text = self.text.replace("    ", " \t ")
        self.text = remove_template(self.text, " ")

    def lexer(self):
        i = self.pos_space
        len_str = len(self.text)
        if self.pos_space == len_str:
            return None
        str_token = ""

        is_string = 0
        while i < len_str - 1:
            if self.text[i] == "\"":
                is_string = 1 if is_string == 0 else 0
            if not is_string and (self.text[i] == " "):
                break
            elif is_string and self.text[i] == "\n":
                break
            str_token += self.text[i]
            i += 1

        self.pos_space = i + 1
        self.num_token += 1

        token_name = self.name_lex.setdefault(str_token)
        if token_name is None:
            if re.findall(self.patterns[0], str_token):
                token_name = "Real_Num"
            elif re.findall(self.patterns[1], str_token):
                token_name = "Num"
            elif re.findall(self.patterns[2], str_token):
                token_name = "Id"
            elif re.findall(self.patterns[3], str_token):
                token_name = "String"
                str_token = str_token[1: -1]
            elif re.findall(self.patterns[4], str_token):
                token_name = "Num_Hex"
            elif re.findall(self.patterns[5], str_token):
                token_name = "Num_Oct"
            else:
                token_name = "Unknown"
                # print("Unknown token at " + str(self.num_line))
                # exit(0)
        if self.file_name != "":
            if str_token == "\t":
                self.num_position += 4
            else:
                self.num_position = self.file_lines[self.num_line - 1].find(str_token) + 1
        struct_output = Token(token_name, str_token, self.num_line, self.num_token, self.num_position)

        if str_token == "\n":
            self.num_line += 1
            self.num_token = 0
            self.num_position = 0

        return struct_output
