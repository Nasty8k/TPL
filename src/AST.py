marker = 0
unknown_type = 0
last_shift = 0
marker_break = -1

typeSize_num = 4
typeSize_string = 1

bytes_space = {
    typeSize_num: 4,
    typeSize_string: 1
}

ast_node_types = {
    "expression_ast": 1,
    "number_ast": 2,
    "string_ast": 3,
    "variable_ast": 4,
    "binary_ast": 5,
    "unary_ast": 6,
    "array_ast": 7,
    "assignment_ast": 8,
    "init_array_ast": 9,
    "call_function_ast": 10,
    "while_ast": 11,
    "for_ast": 12,
    "if_ast": 13,
    "elif_ast": 14,
    "else_ast": 15
}

init_type_function = {
    "print": unknown_type,
    "len": typeSize_num,
}

code_assembler = ".intel_syntax noprefix\n\n.globl main\n.LC0:\n.string \"%d\\n\"\nmain:\npush rbp\nmov rbp, rsp\n"


def get_type_word(type):
    if type == typeSize_num:
        return "DWORD PTR"
    elif type == typeSize_string:
        return "BYTE PTR"


def get_type_mov(type):
    if type == typeSize_num:
        return "mov"
    elif type == typeSize_string:
        return "movzx"


class symTable:
    def __init__(self, parent=None):
        self.parent = parent
        self.nod_list = []
        self.var_list = []

    def print_table(self, level):
        tabs = ""
        for i in range(level):
            tabs += "|   "
        print(tabs + str(self.var_list))

        for child in self.nod_list:
            child.print_table(level + 1)

    def get_var_type(self, var_name):
        i = 0
        iter_node = self
        while iter_node:
            for i in range(len(iter_node.var_list)):
                if var_name == iter_node.var_list[i][0]:
                    return iter_node.var_list[i][1]
            else:
                iter_node = iter_node.parent
        return unknown_type

    def get_var_node(self, var_name):
        i = 0
        iter_node = self
        while iter_node:
            for i in range(len(iter_node.var_list)):
                if var_name == iter_node.var_list[i][0]:
                    return iter_node.var_list[i]
            else:
                iter_node = iter_node.parent
        return None

    def make_assembler(self):
        pass


class AST:
    def __init__(self):
        pass

    def print(self, param):
        pass

    def find_declaration(self, curr_node, error):
        pass


class ExpressionAST(AST):
    def __init__(self, parent, first, second):
        super().__init__()
        self.first = first
        self.second = second
        self.parent = parent

    def find_declaration(self, curr_node, error):
        pass

    def check_type(self, curr_node):
        pass

    def get_type_node(self):
        return ast_node_types['expression_ast']


class NumberExpressionAST(ExpressionAST):
    def __init__(self, value, parent, first=None, second=None):
        super().__init__(parent, first, second)
        self.value = value

    def print(self, level):
        tabs = ""
        for i in range(level):
            tabs += "|   "
        print(tabs + "[NUM] " + str(self.value))

    def find_declaration(self, curr_node, error):
        pass

    def check_type(self, curr_node=None):
        return typeSize_num

    def get_type_node(self):
        return ast_node_types['number_ast']

    def make_assembler(self):
        pass


class StringExpressionAST(ExpressionAST):
    def __init__(self, str_, parent, first=None, second=None):
        super().__init__(parent, first, second)
        self.str_ = str_

    def print(self, level):
        tabs = ""
        for i in range(level):
            tabs += "|   "
        print(tabs + "[STR] " + self.str_)

    def find_declaration(self, curr_node, error):
        pass

    def check_type(self, curr_node=None):
        return typeSize_string

    def get_type_node(self):
        return ast_node_types['string_ast']

    def make_assembler(self):
        pass


class VariableExpressionAST(ExpressionAST):
    def __init__(self, name, parent, first=None, second=None):
        super().__init__(parent, first, second)
        self.name = name
        self.st_data = None

    def print(self, level):
        tabs = ""
        for i in range(level):
            tabs += "|   "
        print(tabs + "[VAR] " + self.name)

    def find_declaration(self, curr_node, error):
        pass

    def check_type(self, curr_node):
        iter_node = curr_node
        found = unknown_type
        while iter_node:
            for i in range(len(iter_node.var_list)):
                if self.name == iter_node.var_list[i][0]:
                    found = iter_node.var_list[i]
                    break
            iter_node = iter_node.parent
        self.st_data = found
        return found[1]

    def get_type_node(self):
        return ast_node_types['variable_ast']

    def make_assembler(self):
        pass


class BinaryExpressionAST(ExpressionAST):
    def __init__(self, operation, parent, first=None, second=None, priority=None):
        super().__init__(parent, first, second)
        self.priority = priority
        self.operation = operation

    def print(self, level):
        tabs = ""
        for i in range(level):
            tabs += "|   "
        print(tabs + "[SIGN] " + str(self.operation))
        self.first.print(level + 1)
        self.second.print(level + 1)

    def find_declaration(self, curr_node, error):
        pass

    def check_type(self, curr_node):
        left = self.first.check_type(curr_node)
        right = self.second.check_type(curr_node)
        if left == right:
            return left
        else:
            return unknown_type

    def get_type_node(self):
        return ast_node_types['binary_ast']

    def make_assembler(self):
        global code_assembler
        neg_state = 0

        cdq = ""
        if self.operation == "+":
            op = "add eax, "
        elif self.operation == "-":
            op = "sub eax, "
        elif self.operation == "*":
            op = "imul eax, "
        elif self.operation == "/" \
                or self.operation == "%":
            op = "idiv "
            cdq = "cdq"
        else:
            return

        first_str = ""
        second_str = ""
        if self.first.get_type_node() == ast_node_types["number_ast"]:
            first_str = str(self.first.value)
        elif self.first.get_type_node() == ast_node_types["variable_ast"]:
            first_str = "DWORD PTR [rbp-" + str(self.first.st_data[2]) + "]"
        elif self.first.get_type_node() == ast_node_types["unary_ast"]:
            if self.first.first.get_type_node() == ast_node_types["number_ast"]:
                first_str = "-" + str(self.first.first.value)
            elif self.first.first.get_type_node() == ast_node_types["variable_ast"]:
                if self.second.get_type_node() == ast_node_types["unary_ast"] and self.second.first.get_type_ast() == \
                        ast_node_types["variable_ast"]:
                    neg_state = 2
                else:
                    self.first.make_assembler()
                    neg_state = 1
        else:
            return

        if self.second.get_type_node() == ast_node_types["number_ast"]:
            second_str = str(self.second.value)
        elif self.second.get_type_node() == ast_node_types["variable_ast"]:
            second_str = get_type_word(self.second.st_data[1]) + " [rbp-" + str(self.second.st_data[2]) + "]"
        elif self.second.get_type_node() == ast_node_types["unary_ast"]:
            if self.second.first.get_type_node() == ast_node_types["number_ast"]:
                second_str = "-" + str(self.second.first.value)
            elif self.second.first.get_type_node() == ast_node_types["variable_ast"]:
                if neg_state == 2:
                    self.second.make_assembler()
                    code_assembler += "mov edx, eax\n"
                    self.first.make_assembler()
                else:
                    self.second.make_assembler()
                    code_assembler += "mov edx, eax\n"
                second_str = "edx"
        else:
            return

        if neg_state == 0:
            code_assembler += "#ret_val\nmov eax, " + first_str + "\n"
        if cdq == "cdq":
            code_assembler += cdq + "\n"
        code_assembler += op + second_str + "\n"


class CreateListAST(ExpressionAST):
    def __init__(self, first, second=None, parent=None):
        super().__init__(parent, first, second)

    def print(self, level):
        space = ""
        for i in range(level):
            space += "|   "
        print(space + "[LIST] ")
        if self.first is None:
            return 0
        for obj in self.first:
            obj.print(level + 1)

    def find_declaration(self, curr_node, error):
        pass

    def check_type(self, curr_node):
        if len(self.first) == 0:
            return unknown_type
        for i in range(len(self.first)):
            if type(self.first[i]) != type(self.first[i - 1]):
                if isinstance(self.first[i], UnaryExpressionAST) or isinstance(self.first[i - 1], UnaryExpressionAST):
                    continue
                return unknown_type
            else:
                return self.first[0].check_type(curr_node)

    def get_type_node(self):
        return ast_node_types['init_array_ast']


class UnaryExpressionAST(ExpressionAST):
    def __init__(self, operation, parent, first, second=None):
        super().__init__(parent, first, second)
        self.operation = operation
        self.first = first

    def print(self, level):
        tabs = ""
        for i in range(level):
            tabs += "|   "
        print(tabs + "[UNARY] " + self.operation)
        self.first.print(level + 1)

    def find_declaration(self, curr_node, error):
        pass

    def check_type(self, curr_node):
        return self.first.check_type(curr_node)

    def get_type_node(self):
        return ast_node_types['unary_ast']

    def make_assembler(self):
        global code_assembler
        if self.first.get_type_node() == ast_node_types["variable_ast"]:
            code_assembler += "mov eax, DWORD PTR [rbp-" + str(self.first.st_data[2]) + "]\n"
            code_assembler += "neg eax\n"


class IfExpressionAST(AST):
    def __init__(self, condition, body):
        super().__init__()
        self.condition = condition
        self.body = body
        self.else_body = None

    def print(self, level):
        tabs = ""
        for i in range(level):
            tabs += "|   "
        print(tabs + "[IF]")
        self.condition.print(level + 1)
        self.body.print(level + 1)
        if self.else_body is not None:
            self.else_body.print(level + 1)

    def find_declaration(self, curr_node, error):
        new_node = symTable(curr_node)
        if new_node:
            curr_node.nod_list.append(new_node)
        type_ = self.condition.check_type(curr_node)
        if type_ == unknown_type:
            error[0] = True
            print("Некорректное условние в if")
            exit()
        self.body.find_declaration(new_node, error)
        if self.else_body:
            self.else_body.find_declaration(new_node, error)

    def get_type_node(self):
        return ast_node_types['if_ast']

    def make_assembler(self):
        global code_assembler
        global marker
        marker += 1
        marker_end = marker
        marker_else = marker_end
        if self.else_body:
            marker += 1
            marker_else = marker

        jump = ""
        if self.condition.operation == "==":
            jump = "jne"
            # jump = "je"
        elif self.condition.operation == "!=":
            jump = "je"
            # jump = "jne"
        elif self.condition.operation == ">":
            jump = "jle"
            # jump = "jg"
        elif self.condition.operation == ">=":
            jump = "jl"
            # jump = "jge"
        elif self.condition.operation == "<":
            jump = "jge"
            # jump = "jl"
        elif self.condition.operation == "<=":
            jump = "jg"
            # jump = "jle"
        else:
            return
        if self.condition.first.get_type_node() == ast_node_types["number_ast"]:
            code_assembler += "mov edx, " + str(self.condition.first.value) + "\n"
        elif self.condition.first.get_type_node() == ast_node_types["variable_ast"]:
            code_assembler += get_type_mov(self.condition.first.st_data[1]) + " edx, " + get_type_word(
                self.condition.first.st_data[1]) + " [rbp-" + str(self.condition.first.st_data[2]) + "]\n"
        elif self.condition.first.get_type_node() == ast_node_types["unary_ast"]:
            if self.condition.first.first.get_type_node() == ast_node_types["number_ast"]:
                code_assembler += "mov edx, -" + str(self.condition.first.first.value) + "\n"
            elif self.condition.first.first.get_type_node() == ast_node_types["number_ast"]:
                code_assembler += "mov edx, DWORD PTR [rbp-" + str(self.condition.first.first.st_data[2]) + "]\n"
                code_assembler += "neg edx\n"
        elif self.condition.first.get_type_node() == ast_node_types["array_ast"]:
            if self.condition.first.first.get_type_node() == ast_node_types["number_ast"]:
                code_assembler += get_type_mov(self.condition.first.first.st_data[1]) + " eax, " + get_type_word(
                    self.condition.first.first.st_data[1]) + " [rbp-" + str(self.condition.first.st_data[2] -
                                                                            self.condition.first.first.value *
                                                                            bytes_space[
                                                                                self.condition.first.first]) + "]\n"
            elif self.condition.first.first.get_type_node() == ast_node_types["variable_ast"]:
                code_assembler += get_type_mov(self.condition.first.first.st_data[1]) + \
                                  " eax, " + get_type_word(self.condition.first.first.st_data[1]) + " [rbp-" + str(
                    self.condition.first.first.st_data[2]) + "]\n"
                code_assembler += "cdqe\n"
                code_assembler += get_type_mov(self.condition.first.st_data[1]) + " eax, " + get_type_word(
                    self.condition.first.st_data[1]) + " [rbp-" + str(self.condition.first.st_data[2]) + "+rax*" + str(
                    self.condition.first.st_data[1]) + "]\n"
            code_assembler += "mov edx, eax\n"
        else:
            return

        if self.condition.second.get_type_node() == ast_node_types["number_ast"]:
            code_assembler += "mov eax, " + str(self.condition.second.value) + "\n"
        elif self.condition.second.get_type_node() == ast_node_types["variable_ast"]:
            code_assembler += get_type_mov(self.condition.second.st_data[1]) + " eax, " + get_type_word(
                self.condition.second.st_data[1]) + " [rbp-" + str(self.condition.second.st_data[2]) + "]\n"
        elif self.condition.second.get_type_node() == ast_node_types["unary_ast"]:
            if self.condition.second.first.get_type_node() == ast_node_types["number_ast"]:
                code_assembler += "mov eax, -" + str(self.condition.second.first.value) + "\n"
            elif self.condition.second.first.get_type_node() == ast_node_types["variable_ast"]:
                code_assembler += get_type_mov(self.condition.second.first.st_data[1]) + " eax, " + get_type_word(
                    self.condition.second.first.st_data[1]) + " [rbp-" + str(
                    self.condition.second.first.st_data[2]) + "]\n"
        elif self.condition.second.get_type_node() == ast_node_types["array_ast"]:
            if self.condition.second.first.get_type_node() == ast_node_types["number_ast"]:
                code_assembler += get_type_mov(self.condition.second.st_data[1]) + " eax, " + get_type_word(
                    self.condition.second.st_data[1]) + " [rbp-" + str(self.condition.second.st_data[2] -
                                                                       self.condition.second.first.value * 4) + "]\n"
            elif self.condition.second.first.get_type_node() == ast_node_types["variable_ast"]:
                code_assembler += "mov eax, " + get_type_word(self.condition.second.first.st_data[1]) + " [rbp-" + str(
                    self.condition.second.first.st_data[2]) + "]\n"
                code_assembler += "cdqe\n"
                code_assembler += get_type_mov(self.condition.second.st_data[1]) + " eax, " + get_type_word(
                    self.condition.second.st_data[1]) + " [rbp-" + str(
                    self.condition.second.st_data[2]) + "+rax*" + str(self.condition.second.st_data[1]) + "]\n"
        else:
            return
        code_assembler += "cmp edx, eax\n"
        code_assembler += jump + " .L" + str(marker) + "\n"
        self.body.make_assembler()
        if self.else_body:
            code_assembler += "jmp .L" + str(marker_end) + "\n"
            code_assembler += ".L" + str(marker_else) + ":\n"
            self.else_body.make_assembler()
        code_assembler += ".L" + str(marker_end) + ":\n"


class ForExpressionAST(AST):
    def __init__(self, init, condition, body):
        super().__init__()
        self.init = init
        self.condition = condition
        self.body = body

    def print(self, level):
        tabs = ""
        for i in range(level):
            tabs += "|   "
        print(tabs + "[FOR]")
        self.init.print(level + 1)
        self.condition.print(level + 1)
        self.body.print(level + 1)

    def find_declaration(self, curr_node, error):
        new_node = symTable(curr_node)
        if new_node:
            curr_node.nod_list.append(new_node)

        iter_node = curr_node
        found = False
        while iter_node:
            if not (self.init.name in iter_node.var_list):
                iter_node = iter_node.parent
            else:
                found = True
                break

        if found is False:
            new_node.var_list.append([self.init.name, typeSize_num])
        type_ = self.condition.check_type(curr_node)
        if type_ == unknown_type:
            print("Error in statement: for")
            exit()
            error[0] = True
        self.body.find_declaration(new_node, error)

    def get_type_node(self):
        return ast_node_types['for_ast']


class ElifExpressionAST(AST):
    def __init__(self, condition, body):
        super().__init__()
        self.condition = condition
        self.body = body

    def print(self, level):
        tabs = ""
        for i in range(level):
            tabs += "|   "
        print(tabs + "[ELIF]")
        self.condition.print(level + 1)
        self.body.print(level + 1)

    def find_declaration(self, curr_node, error):
        new_node = symTable(curr_node)
        if new_node:
            curr_node.nod_list.append(new_node)
        type_ = self.condition.check_type(curr_node)
        if type_ == unknown_type:
            print("Error in statement: elif")
            exit()
            error[0] = True
        self.body.find_declaration(new_node, error)

    def get_type_node(self):
        return ast_node_types['elif_ast']


class ElseExpressionAST(AST):
    def __init__(self, body):
        super().__init__()
        self.body = body

    def print(self, level):
        tabs = ""
        for i in range(level):
            tabs += "|   "
        print(tabs + "[ELSE]")
        self.body.print(level + 1)

    def find_declaration(self, curr_node, error):
        new_node = symTable(curr_node)
        if new_node:
            curr_node.nod_list.append(new_node)
        self.body.find_declaration(new_node, error)

    def get_type_node(self):
        return ast_node_types['else_ast']

    def make_assembler(self):
        self.body.make_assembler()


class WhileExpressionAST(AST):
    def __init__(self, condition, body):
        super().__init__()
        self.condition = condition
        self.body = body

    def print(self, level):
        tabs = ""
        for i in range(level):
            tabs += "|   "
        print(tabs + "[WHILE]")
        self.condition.print(level + 1)
        self.body.print(level + 1)

    def find_declaration(self, curr_node, error):
        new_node = symTable(curr_node)
        if new_node:
            curr_node.nod_list.append(new_node)
        type_ = self.condition.check_type(curr_node)

        if type_ == unknown_type:
            print("Error in statement: while")
            exit()
            error[0] = True
        self.body.find_declaration(new_node, error)

    def get_type_node(self):
        return ast_node_types['while_ast']

    def make_assembler(self):
        jump = ""
        global code_assembler
        global marker
        marker += 1
        if self.condition.operation == "and":
            marker_start = marker
            marker += 1
            marker_end = marker
            code_assembler += ".L" + str(marker_start) + ":\n"
            jump_left = ""
            if self.condition.first.operation == "==":
                jump_left = "jne"
            elif self.condition.first.operation == "!=":
                jump_left = "je"
            elif self.condition.first.operation == ">":
                jump_left = "jle"
            elif self.condition.first.operation == ">=":
                jump_left = "jl"
            elif self.condition.first.operation == "<":
                jump_left = "jge"
            elif self.condition.first.operation == "<=":
                jump_left = "jg"
            else:
                return
            jump_right = ""
            if self.condition.second.operation == "==":
                jump_right = "jne"
            elif self.condition.second.operation == "!=":
                jump_right = "je"
            elif self.condition.second.operation == ">":
                jump_right = "jle"
            elif self.condition.second.operation == ">=":
                jump_right = "jl"
            elif self.condition.second.operation == "<":
                jump_right = "jge"
            elif self.condition.second.operation == "<=":
                jump_right = "jg"
            else:
                return

            operand_ll = ""
            if self.condition.first.first.get_type_node() == ast_node_types["number_ast"]:
                operand_ll = str(self.condition.first.first.value)
            elif self.condition.first.first.get_type_node() == ast_node_types["variable_ast"]:
                operand_ll = get_type_word(self.condition.first.first.st_data[1]) + " [rbp-" + str(
                    self.condition.first.first.st_data[2]) + "]"
            else:
                return
            operand_lr = ""
            if self.condition.first.second.get_type_node() == ast_node_types["number_ast"]:
                operand_lr = str(self.condition.first.second.value)
            elif self.condition.first.second.get_type_node() == ast_node_types["variable_ast"]:
                operand_lr = get_type_word(self.condition.first.second.st_data[1]) + " [rbp-" + str(
                    self.condition.first.second.st_data[2]) + "]"
            else:
                return
            operand_rl = ""
            if self.condition.second.first.get_type_node() == ast_node_types["number_ast"]:
                operand_rl = str(self.condition.second.first.value)
            elif self.condition.second.first.get_type_node() == ast_node_types["variable_ast"]:
                operand_rl = get_type_word(self.condition.second.first.st_data[1]) + " [rbp-" + str(
                    self.condition.second.first.st_data[2]) + "]"
            else:
                return
            operand_rr = ""
            if self.condition.second.second.get_type_node() == ast_node_types["number_ast"]:
                operand_rr = str(self.condition.second.second.value)
            elif self.condition.second.second.get_type_node() == ast_node_types["variable_ast"]:
                operand_rr = get_type_word(self.condition.second.second.st_data[1]) + " [rbp-" + str(
                    self.condition.second.second.st_data[2]) + "]"
            else:
                return

            code_assembler += "cmp " + operand_ll + ", " + operand_lr + "\n"
            code_assembler += jump_left + " .L" + str(marker_end) + "\n"
            code_assembler += "cmp " + operand_rl + ", " + operand_rr + "\n"
            code_assembler += jump_right + " .L" + str(marker_end) + "\n"

            self.body.make_assembler()

            code_assembler += "jmp .L" + str(marker_start) + "\n"
            code_assembler += ".L" + str(marker_end) + ":\n"
            return
        elif self.condition.operation == "==":
            jump = "jne"
        elif self.condition.operation == "!=":
            jump = "je"
        elif self.condition.operation == ">":
            jump = "jle"
        elif self.condition.operation == ">=":
            jump = "jl"
        elif self.condition.operation == "<":
            jump = "jge"
        elif self.condition.operation == "<=":
            jump = "jg"
        else:
            return

        code_assembler += ".L" + str(marker) + ":\n"

        if self.condition.first.get_type_node() == ast_node_types["number_ast"]:
            code_assembler += "mov edx, " + str(self.condition.first.value) + "\n"
        elif self.condition.first.get_type_node() == ast_node_types["variable_ast"]:
            code_assembler += get_type_mov(self.condition.first.st_data[1]) + " edx, " + get_type_word(
                self.condition.first.st_data[1]) + " [rbp-" + str(self.condition.first.st_data[2]) + "]\n"
        elif self.condition.first.get_type_node() == ast_node_types["unary_ast"]:
            if self.condition.first.first.get_type_node() == ast_node_types["number_ast"]:
                code_assembler += "mov edx, -" + str(self.condition.first.first.value) + "\n"
            elif self.condition.first.first.get_type_node() == ast_node_types["variable_ast"]:
                code_assembler += get_type_mov(self.condition.first.first.st_data[1]) + " edx, " + get_type_word(
                    self.condition.first.first.st_data[1]) + " [rbp-" + str(
                    self.condition.first.first.st_data[2]) + "]\n"
                code_assembler += "neg edx\n"
        elif self.condition.first.get_type_node() == ast_node_types["array_ast"]:
            if self.condition.first.first.get_type_node() == ast_node_types["number_ast"]:
                code_assembler += get_type_mov(self.condition.first.st_data[1]) + " eax, " + get_type_word(
                    self.condition.first.st_data[1]) + " [rbp-" + str(self.condition.first.st_data[2] -
                                                                      self.condition.first.first.value * bytes_space[
                                                                          self.condition.first.check_type()]) + "]\n"
            elif self.condition.first.first.get_type_node() == ast_node_types["variable_ast"]:
                code_assembler += "mov eax, DWORD PTR [rbp-" + str(self.condition.first.first.st_data[2]) + "]\n"
                code_assembler += "cdqe\n"
                code_assembler += get_type_mov(self.condition.first.st_data[1]) + " eax, " + get_type_word(
                    self.condition.first.st_data[1]) + " [rbp-" + str(self.condition.first.st_data[2]) + "+rax*" + str(
                    bytes_space[self.condition.first.check_type()]) + "]\n"
            code_assembler += "mov edx, eax\n"
        else:
            return

        if self.condition.second.get_type_node() == ast_node_types["number_ast"]:
            code_assembler += "mov eax, " + str(self.condition.second.value) + "\n"
        elif self.condition.second.get_type_node() == ast_node_types["variable_ast"]:
            code_assembler += get_type_mov(self.condition.second.st_data[1]) + " eax, " + get_type_word(
                self.condition.second.st_data[1]) + " [rbp-" + str(self.condition.second.st_data[2]) + "]\n"
        elif self.condition.second.get_type_node() == ast_node_types["unary_ast"]:
            if self.condition.second.first.get_type_node() == ast_node_types["number_ast"]:
                code_assembler += "mov eax, -" + str(self.condition.second.first.value) + "\n"
            elif self.condition.second.first.get_type_node() == ast_node_types["variable_ast"]:
                code_assembler += "mov eax, DWORD PTR [rbp-" + str(self.condition.second.first.st_data[2]) + "]\n"
        elif self.condition.second.get_type_node() == ast_node_types["array_ast"]:
            if self.condition.second.first.get_type_node() == ast_node_types["number_ast"]:
                code_assembler += get_type_mov(self.condition.second.st_data[1]) + " eax, " + get_type_word(
                    self.condition.second.st_data[1]) + " [rbp-" + str(self.condition.second.st_data[2] -
                                                                       self.condition.second.first.value *
                                                                       self.condition.second.st_data[1]) + "]\n"
            elif self.condition.second.first.get_type_node() == ast_node_types["variable_ast"]:
                code_assembler += "mov eax, DWORD PTR [rbp-" + str(self.condition.second.first.st_data[2]) + "]\n"
                code_assembler += "cdqe\n"
                code_assembler += get_type_mov(self.condition.second.st_data[1]) + " eax, " + get_type_word(
                    self.condition.second.st_data[1]) + " [rbp-" + str(
                    self.condition.second.st_data[2]) + "+rax*" + str(self.condition.second.check_type()) + "]\n"
        else:
            return
        code_assembler += "cmp edx, eax\n"

        marker_start = marker
        marker += 1
        marker_end = marker

        code_assembler += jump + " .L" + str(marker) + "\n"
        global marker_break
        marker_break_end = marker_break
        marker_break = marker_end
        self.body.make_assembler()
        marker_break = marker_break_end
        code_assembler += "jmp .L" + str(marker_start) + "\n"
        code_assembler += ".L" + str(marker_end) + ":\n"


class CallFunctionExpressionAST(ExpressionAST):
    def __init__(self, name, args, parent, second=None):
        super().__init__(parent, args, second)
        self.name = name
        self.args = args

    def print(self, level):
        tabs = ""
        for i in range(level):
            tabs += "|   "
        print(tabs + "[CALL] " + self.name)
        if self.args is None:
            return 0
        for obj in self.first:
            obj.print(level + 1)

    def find_declaration(self, curr_node, error):
        self.check_type(curr_node)

    def check_type(self, curr_node):
        for arg in self.args:
            type_ = arg.check_type(curr_node)
            if type_ == unknown_type:
                print("Error in statement: function call types")
                exit()
        return init_type_function[self.name]

    def get_type_node(self):
        return ast_node_types['call_function_ast']

    def make_assembler(self):
        global code_assembler
        if self.name == "print" and self.args[0].get_type_node() == ast_node_types["variable_ast"] and len(
                self.args) == 1:
            code_assembler += "mov eax, DWORD PTR [rbp-" + str(self.args[0].st_data[2]) + "]\n"
            code_assembler += "mov esi, eax\nmov edi, OFFSET FLAT:.LC0\nmov eax, 0\ncall printf\nmov eax, 0\n"


class ArrayExpressionAST(ExpressionAST):
    def __init__(self, name, parent, arg, second=None):
        super().__init__(parent, arg, second)
        self.name = name
        self.st_data = None

    def print(self, level):
        tabs = ""
        for i in range(level):
            tabs += "|   "
        print(tabs + "[ARRAY] " + self.name)
        self.first.print(level + 1)

    def find_declaration(self, curr_node, error):
        pass

    def check_type(self, curr_node):
        self.first.check_type(curr_node)
        iter_node = curr_node
        found = unknown_type
        while iter_node:
            for i in range(len(iter_node.var_list)):
                if self.name == iter_node.var_list[i][0]:
                    found = iter_node.var_list[i]
                    break
            iter_node = iter_node.parent
            self.st_data = found
        return found[1]

    def get_type_node(self):
        return ast_node_types['array_ast']

    def make_assembler(self):
        pass


class AssignmentExpressionAST(ExpressionAST):
    def __init__(self, operation, first, second, parent=None):
        super().__init__(parent, first, second)
        self.operation = operation

    def print(self, level):
        tabs = ""
        for i in range(level):
            tabs += "|   "
        print(tabs + "[ASSIGN] " + str(self.operation))
        self.first.print(level + 1)
        self.second.print(level + 1)

    def find_declaration(self, curr_node, error):
        if self.first.get_type_node == ast_node_types["array_ast"]:
            self.first.check_type(curr_node)
            return

        iter_node = curr_node
        found = False
        while iter_node:
            if not (self.first.name in (iter_node.var_list[i][0] for i in range(len(iter_node.var_list)))):
                iter_node = iter_node.parent
            else:
                found = True
                break
        prev_type = curr_node.get_var_type(self.first.name)
        type_ = self.second.check_type(curr_node)
        if found is False:
            global last_shift
            if self.second.get_type_node() == ast_node_types["number_ast"] or self.second.get_type_node() == \
                    ast_node_types["binary_ast"] or self.second.get_type_node() == ast_node_types["variable_ast"] or \
                    self.second.get_type_node() == ast_node_types["unary_ast"] or self.second.get_type_node() == \
                    ast_node_types["array_ast"]:
                last_shift += bytes_space[type_]
            elif self.second.get_type_node() == ast_node_types["init_array_ast"]:
                last_shift += bytes_space[type_] * len(self.second.first)
            elif self.second.get_type_node() == ast_node_types["string_ast"]:
                last_shift += len(self.second.str_)
            new_var = [self.first.name, type_, last_shift]
            curr_node.var_list.append(new_var)
            self.first.st_data = new_var
        else:
            self.first.check_type(curr_node)
            self.first.st_data = curr_node.get_var_node(self.first.name)
            if prev_type != type_:
                print("Error id type '" + self.first.name + "'")
                exit()
                error[0] = True
        if type_ == unknown_type:
            print("Unexpected type")
            error[0] = True

    def check_type(self, curr_node):
        pass

    def make_assembler(self):
        global code_assembler
        if self.first.get_type_node() == ast_node_types["variable_ast"]:  # a
            if self.second.get_type_node() == ast_node_types["number_ast"]:  # a = 2
                code_assembler += "mov DWORD PTR [rbp-" + str(self.first.st_data[2]) + "], " + str(
                    self.second.value) + "\n"
            elif self.second.get_type_node() == ast_node_types["variable_ast"]:  # a = b
                code_assembler += "mov eax, DWORD PTR [rbp-" + str(self.second.st_data[2]) + "]\n"
                code_assembler += "mov DWORD PTR [rbp-" + str(self.first.st_data[2]) + "], eax\n"
            elif self.second.get_type_node() == ast_node_types["binary_ast"]:
                self.second.make_assembler()
                if self.second.operation == "%":
                    code_assembler += "mov DWORD PTR [rbp-" + str(self.first.st_data[2]) + "], edx\n"
                else:
                    code_assembler += "mov DWORD PTR [rbp-" + str(self.first.st_data[2]) + "], eax\n"
            elif self.second.get_type_node() == ast_node_types["unary_ast"]:
                if self.second.first.get_type_node() == ast_node_types["number_ast"]:
                    code_assembler += "mov DWORD PTR [rbp-" + str(self.first.st_data[2]) + "], -" + str(
                        self.second.first.value) + "\n"
                elif self.second.first.get_type_node() == ast_node_types["variable_ast"]:
                    self.second.make_assembler()
                    code_assembler += "mov DWORD PTR [rbp-" + str(self.first.st_data[2]) + "], eax\n"
            elif self.second.get_type_node() == ast_node_types["init_array_ast"]:
                for i in range(len(self.second.first)):
                    if isinstance(self.second.first[i], NumberExpressionAST):
                        code_assembler += "mov DWORD PTR [rbp-" + str(self.first.st_data[2] - 4 * i) + "], " + str(
                            self.second.first[i].value) + "\n"
                    elif isinstance(self.second.first[i], UnaryExpressionAST):
                        code_assembler += "mov DWORD PTR [rbp-" + str(self.first.st_data[2] - 4 * i) + "], -" + str(
                            self.second.first[i].first.value) + "\n"
            elif self.second.get_type_node() == ast_node_types["array_ast"]:
                if self.second.first.get_type_node() == ast_node_types["number_ast"]:
                    code_assembler += "mov eax, DWORD PTR [rbp-" + str(
                        self.second.st_data[2] - 4 * self.second.first.value) + "]\n"
                    code_assembler += "mov DWORD PTR[rbp-" + str(self.first.st_data[2]) + "], eax\n"
                elif self.second.first.get_type_node() == ast_node_types["variable_ast"]:
                    code_assembler += "mov eax, DWORD PTR [rbp-" + str(self.second.first.st_data[2]) + "]\n"
                    code_assembler += "cdqe\n"
                    code_assembler += "mov eax, DWORD PTR [rbp-" + str(self.second.st_data[2]) + "+rax*4]\n"
                    code_assembler += "mov DWORD PTR [rbp-" + str(self.first.st_data[2]) + "], eax\n"
                elif self.second.first.get_type_node() == ast_node_types["binary_ast"]:
                    self.second.first.make_assembler()
                    code_assembler += "cdqe\n"
                    code_assembler += "mov eax, DWORD PTR [rbp-" + str(self.second.st_data[2]) + "+rax*4]\n"
                    code_assembler += "mov DWORD PTR [rbp-" + str(self.first.st_data[2]) + "], eax\n"
            elif self.second.get_type_node() == ast_node_types["string_ast"]:
                for i in range(len(self.second.str_)):
                    code_assembler += "mov BYTE PTR [rbp-" + str(self.first.st_data[2] - i) + "], '" + str(
                        self.second.str_[i]) + "'\n"
        elif self.first.get_type_node() == ast_node_types["array_ast"]:  # a[] =
            if self.first.first.get_type_node() == ast_node_types["number_ast"]:  # a[1] =
                if self.second.get_type_node() == ast_node_types["number_ast"]:  # a[1] = 1
                    code_assembler += "mov eax, " + str(self.second.value) + "\n"
                    code_assembler += "mov DWORD PTR [rbp-" + str(
                        self.first.st_data[2] - 4 * self.first.first.value) + "], eax\n"
                elif self.second.get_type_node() == ast_node_types["variable_ast"]:  # a[1] = b
                    code_assembler += "mov eax, DWORD PTR [rbp-" + str(self.second.st_data[2]) + "]\n"
                    code_assembler += "mov DWORD PTR [rbp-" + str(
                        self.first.st_data[2] - 4 * self.first.first.value) + "], eax\n"
                elif self.second.get_type_node() == ast_node_types["binary_ast"]:  # a[1] = a + c
                    self.second.make_assembler()
                    code_assembler += "mov DWORD PTR [rbp-" + str(self.first.st_data[2]) + "], eax\n"
                elif self.second.get_type_node() == ast_node_types["unary_ast"]:
                    if self.second.first.get_type_node() == ast_node_types["number_ast"]:
                        code_assembler += "mov DWORD PTR [rbp-" + str(self.first.st_data[2]) + "], -" + str(
                            self.second.first.value) + "\n"
                    elif self.second.first.get_type_node() == ast_node_types["variable_ast"]:
                        self.second.make_assembler()
                        code_assembler += "mov DWORD PTR [rbp-" + str(self.first.st_data[2]) + "], eax\n"
            elif self.first.first.get_type_node() == ast_node_types["binary_ast"]:  # a[b + с] =
                self.first.first.make_assembler()
                code_assembler += "cdqe\n"
                if self.second.get_type_node() == ast_node_types["number_ast"]:  # a[b + с] = 1
                    code_assembler += "mov DWORD PTR [rbp-" + str(self.first.st_data[2]) + "+rax*4], " + str(
                        self.second.value) + "\n"
                elif self.second.get_type_node() == ast_node_types["variable_ast"]:  # a[b + с] = b
                    code_assembler += "mov edx, DWORD PTR [rbp-" + str(self.second.st_data[2]) + "]\n"
                    code_assembler += "mov DWORD PTR [rbp-" + str(self.first.st_data[2]) + "+rax*4], edx\n"
            elif self.first.first.get_type_node() == ast_node_types["variable_ast"]:  # a[b] =
                code_assembler += "mov eax, DWORD PTR [rbp-" + str(self.first.first.st_data[2]) + "]\n"
                if self.second.get_type_node() == ast_node_types["number_ast"]:  # a[b] = 3
                    code_assembler += "cdqe\n"
                    code_assembler += "mov DWORD PTR [rbp-" + str(self.first.st_data[2]) + "+rax*4], " + str(
                        self.second.value) + "\n"
                elif self.second.get_type_node() == ast_node_types["variable_ast"]:  # a[b] = i
                    code_assembler += "cdqe\n"
                    code_assembler += "mov edx, DWORD PTR [rbp-" + str(self.second.st_data[2]) + "]\n"
                    code_assembler += "mov DWORD PTR [rbp-" + str(self.first.st_data[2]) + "+rax*4], edx\n"

    def get_type_node(self):
        return ast_node_types['assignment_ast']


class BodyAST(AST):
    def __init__(self):
        super().__init__()
        self.nodes = []

    def print(self, level):
        tabs = ""
        for i in range(level):
            tabs += " \\   "
        print(tabs + "[BODY] ")
        for sub_root in self.nodes:
            sub_root.print(level + 1)

    def find_declaration(self, curr_node, error):
        for sub_root in self.nodes:
            sub_root.find_declaration(curr_node, error)

    def make_assembler(self):
        for sub_root in self.nodes:
            sub_root.make_assembler()


class PrototypeFunctionAST:
    pass


class FunctionAST:
    pass


class ReturnAST(AST):
    def __init__(self, first):
        super().__init__()
        self.first = first

    def print(self, level):
        tabs = ""
        for i in range(level):
            tabs += " \\   "
        print(tabs + "[RETURN]")
        self.first.print(level + 1)


class BreakAST(AST):
    def __init__(self):
        super().__init__()

    def print(self, level):
        tabs = ""
        for i in range(level):
            tabs += " " * i
            tabs += " \\   "
        print(tabs + "[BREAK]")

    def make_assembler(self):
        global code_assembler
        global marker_break
        code_assembler += "jmp .L" + str(marker_break) + "\n"


class ContinueAST(AST):
    def __init__(self):
        super().__init__()

    def print(self, level):
        tabs = ""
        for i in range(level):
            tabs += "\\   "
        print(tabs + "[CONTINUE]")
