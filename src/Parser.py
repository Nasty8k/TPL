from src import AST
from src.Lexer import Lexer

priority = {
    "KeyW_OR": 1,
    "KeyW_AND": 2,
    "More": 3, "Less": 3, "Comparison": 3, "Not_Comparison": 3,
    "More_Comparison": 3, "Less_Comparison": 3, "KeyW_NOT": 3,
    "Plus": 4, "Minus": 4,
    "Multiplication": 5, "Division": 5, "Residual_Division": 5, "Integer_Division": 5,
}

assignment_op = ["Assignment", "Plus_Assignment", "Minus_Assignment", "Multi_Assignment", "Div_Assignment",
                 "Int_Div_Assignment", "Residual_Assignment", "Exp_Assignment"]


class Parser:
    def __init__(self, _filename_=None):
        self.root = None
        self.lexer = Lexer()
        self.lexer.file_in(_filename_)
        self.buffer = [None, None]

    def get_next_token(self):
        self.buffer[0] = self.buffer[1]
        self.buffer[1] = self.lexer.lexer()

    def make_list(self):
        self.get_next_token()
        args = list()

        if self.buffer[0].lexeme == "]":
            return AST.CreateListAST(None, None)

        while self.buffer[0].lexeme != "]":
            if not (self.buffer[1].token_class in priority):
                if self.buffer[0].token_class == "Num" or self.buffer[0].token_class == "Real_Num" or \
                        self.buffer[0].token_class == "Num_Oct" or \
                        self.buffer[0].token_class == "Num_Hex":
                    args.append(AST.NumberExpressionAST(int(self.buffer[0].lexeme), None))
                elif self.buffer[0].token_class == "Id" and self.buffer[1].token_class == "L_Sq_Bracket":
                    args.append(self.handle_arithmetical_expression())
                elif self.buffer[0].token_class == "Id" and self.buffer[1].token_class == "L_Paren_Bracket":
                    args.append(self.handle_arithmetical_expression())
                elif self.buffer[0].token_class == "Id":
                    args.append(AST.VariableExpressionAST(self.buffer[0].lexeme, None))
                elif self.buffer[0].token_class == "String":
                    args.append(AST.StringExpressionAST(self.buffer[0].lexeme, None))
                elif self.buffer[0].token_class == "Minus":
                    op = self.buffer[0].lexeme
                    self.get_next_token()
                elif self.buffer[0].token_class == "L_Sq_Bracket":
                    args.append(self.make_list())
                elif self.buffer[0].token_class == "Unknown":
                    print("Неизвестный тип в создании списка в строке " + str(self.buffer[0].line))
                    return None
            else:
                if self.buffer[0].token_class == "Comma":
                    self.get_next_token()
                args.append(self.handle_arithmetical_expression())

            self.get_next_token()
        return AST.CreateListAST(args)

    def arrays_rule(self, name):
        self.get_next_token()
        self.get_next_token()
        index = None
        if self.buffer[0].lexeme == "]":
            pass
        else:
            if not (self.buffer[1].token_class in priority):
                if self.buffer[0].token_class == "Num" or self.buffer[0].token_class == "Real_Num" or \
                        self.buffer[0].token_class == "Num_Oct" or \
                        self.buffer[0].token_class == "Num_Hex":
                    index = AST.NumberExpressionAST(int(self.buffer[0].lexeme), None)
                    # index = self.handle_arithmetical_expression()
                elif self.buffer[0].token_class == "Id" and self.buffer[1].token_class == "L_Paren_Bracket":
                    index = self.handle_arithmetical_expression()
                elif self.buffer[0].token_class == "Id" and self.buffer[1].token_class == "L_Sq_Bracket":
                    index = self.handle_arithmetical_expression()
                elif self.buffer[0].token_class == "Id":
                    index = AST.VariableExpressionAST(self.buffer[0].lexeme, None)
                elif self.buffer[0].token_class == "String":
                    index = AST.StringExpressionAST(self.buffer[0].lexeme, None)
                elif self.buffer[0].token_class == "Minus":
                    op = self.buffer[0].lexeme
                    self.get_next_token()
                elif self.buffer[0].token_class == "L_Sq_Bracket":
                    index = self.make_list()
            else:
                if self.buffer[0].token_class == "Comma":
                    self.get_next_token()
                index = self.handle_arithmetical_expression()
            self.get_next_token()
            if index is None:
                self.get_next_token()
        return AST.ArrayExpressionAST(name, None, index)

    def handle_call_function(self, name):
        self.get_next_token()
        self.get_next_token()
        args = list()

        if self.buffer[0].lexeme == ")":
            return AST.CallFunctionExpressionAST(name, None, None)

        while self.buffer[0].lexeme != ")":
            if not (self.buffer[1].token_class in priority):
                if self.buffer[0].token_class == "Num" or self.buffer[0].token_class == "Real_Num" or \
                        self.buffer[0].token_class == "Num_Oct" or \
                        self.buffer[0].token_class == "Num_Hex":
                    args.append(AST.NumberExpressionAST(int(self.buffer[0].lexeme), None))
                elif self.buffer[0].token_class == "Id" and self.buffer[1].token_class == "L_Sq_Bracket":
                    args.append(self.handle_arithmetical_expression())
                elif self.buffer[0].token_class == "Id" and self.buffer[1].token_class == "L_Paren_Bracket":
                    args.append(self.handle_arithmetical_expression())
                elif self.buffer[0].token_class == "Id":
                    args.append(AST.VariableExpressionAST(self.buffer[0].lexeme, None))
                elif self.buffer[0].token_class == "String":
                    args.append(AST.StringExpressionAST(self.buffer[0].lexeme, None))
                elif self.buffer[0].token_class == "Minus":
                    op = self.buffer[0].lexeme
                    self.get_next_token()
                elif self.buffer[0].token_class == "L_Sq_Bracket":
                    args.append(self.make_list())
            else:
                if self.buffer[0].token_class == "Comma":
                    self.get_next_token()
                args.append(self.handle_arithmetical_expression())
            self.get_next_token()
        return AST.CallFunctionExpressionAST(name, args, None)



    def handle_while(self, shift):
        self.get_next_token()
        while_obj = AST.WhileExpressionAST(self.handle_arithmetical_expression(), None)
        self.get_next_token()
        if self.buffer[0].token_class == "Colon":
            self.get_next_token()
            while_obj.body, shift = self.handle_body(shift + 1)
        else:
            print("Отсутствие двоеточия у while в строке " + str(self.buffer[0].line))
            exit()
        return while_obj, shift

    def handle_if(self, shift):
        self.get_next_token()
        if_obj = AST.IfExpressionAST(self.handle_arithmetical_expression(), None)
        self.get_next_token()
        if self.buffer[0].token_class == "Colon":
            self.get_next_token()
            if_obj.body, shift = self.handle_body(shift + 1)
            # self.get_next_token()
            if self.buffer[1].token_class == "KeyW_ELSE":
                self.get_next_token()
                self.get_next_token()
                if_obj.else_body, shift = self.handle_body(shift + 1)
        else:
            print("Отсутствие двоеточия у if в строке " + str(self.buffer[0].line))
            exit()
        return if_obj, shift

    def handle_for(self, shift):
        self.get_next_token()
        for_obj = AST.ForExpressionAST(AST.VariableExpressionAST(self.buffer[0].lexeme, None), None, None)
        self.get_next_token()
        if self.buffer[0].token_class == "KeyW_IN":
            self.get_next_token()
            for_obj.condition = self.handle_arithmetical_expression()
            self.get_next_token()
            if self.buffer[0].token_class == "Colon":
                for_obj.body, shift = self.handle_body(shift + 1)
            else:
                print("Отсутствие двоеточия у for в строке " + str(self.buffer[0].line))
                exit()
        else:
            print("Отсутствие in в цикле в строке " + str(self.buffer[0].line))
            exit()
        return for_obj, shift

    def handle_elif(self, shift):
        self.get_next_token()
        if_obj = AST.ElifExpressionAST(self.handle_arithmetical_expression(), None)
        self.get_next_token()
        if self.buffer[0].token_class == "Colon":
            self.get_next_token()
            if_obj.body, shift = self.handle_body(shift + 1)
        else:
            print("Отсутствие двоеточия у elif в строке " + str(self.buffer[0].line))
            exit()
        return if_obj, shift

    def handle_else(self, shift):
        self.get_next_token()
        else_obj = AST.ElseExpressionAST(None)
        if self.buffer[0].token_class == "Colon":
            self.get_next_token()
            else_obj.body, shift = self.handle_body(shift + 1)
        else:
            print("Отсутствие двоеточия у else в строке " + str(self.buffer[0].line))
            exit()
        return else_obj, shift

    def handle_body(self, shift):
        body = AST.BodyAST()
        while self.buffer[1] and self.buffer[0]:
            if self.buffer[0].token_class == "KeyW_RETURN":
                self.get_next_token()
                body.nodes.append(AST.ReturnAST(self.handle_arithmetical_expression()))
            elif self.buffer[0].token_class == "KeyW_BREAK":
                body.nodes.append(AST.BreakAST())
            elif self.buffer[0].token_class == "KeyW_CONTINUE":
                body.nodes.append(AST.ContinueAST())
            elif (self.buffer[0].token_class == "Num" or self.buffer[0].token_class == "Id" or
                  self.buffer[0].token_class == "RealNum" or self.buffer[0].token_class == "Num_Oct" or
                  self.buffer[0].token_class == "Num_Hex") \
                    and (self.buffer[1].token_class in priority or
                         self.buffer[1].token_class == "L_Paren_Bracket" or
                         self.buffer[1].token_class == "L_Sq_Bracket"):
                body.nodes.append(self.handle_arithmetical_expression())
            elif self.buffer[0].token_class == "Num" or self.buffer[0].token_class == "RealNum":
                body.nodes.append(AST.NumberExpressionAST(int(self.buffer[0].lexeme), None))
            elif self.buffer[0].token_class == "Minus":
                op = self.buffer[0].lexeme
                self.get_next_token()
                body.nodes.append(AST.UnaryExpressionAST(op, None, self.handle_arithmetical_expression()))
            elif self.buffer[0].token_class == "Id":
                body.nodes.append(AST.VariableExpressionAST(self.buffer[0].lexeme, None))
            elif len(body.nodes) and self.buffer[0].token_class in assignment_op and \
                    (isinstance(body.nodes[-1], AST.VariableExpressionAST) or isinstance(body.nodes[-1], AST.ArrayExpressionAST)):
                op = self.buffer[0].lexeme
                self.get_next_token()
                body.nodes[-1] = AST.AssignmentExpressionAST(op, body.nodes[-1], self.handle_arithmetical_expression())
            elif self.buffer[0].token_class == "\\n":
                new_shift = self.handle_shifts()
                if new_shift < shift:
                    shift = new_shift
                    break
                elif new_shift == shift:
                    pass
                elif new_shift > shift:
                    print("Ошибка. Неправильное количество \\t в строке " + str(self.buffer[0].line))
                    exit()
                    break
            elif self.buffer[0].token_class == "KeyW_WHILE":
                while_obj, while_shift = self.handle_while(shift)
                body.nodes.append(while_obj)
                if while_shift < shift:
                    shift = while_shift
                    break
            elif self.buffer[0].token_class == "KeyW_FOR":
                for_obj, for_shift = self.handle_for(shift)
                body.nodes.append(for_obj)
                if for_shift < shift:
                    shift = for_shift
                    break
            elif self.buffer[0].token_class == "KeyW_IF":
                if_obj, if_shift = self.handle_if(shift)
                body.nodes.append(if_obj)
                if if_shift < shift:
                    shift = if_shift
                    break
            self.get_next_token()
        return body, shift

    def handle_arithmetical_expression(self):
        left = None  # Объект левый дочерний узел
        if self.buffer[0].token_class == "Num" or self.buffer[0].token_class == "Real_Num" or \
                self.buffer[0].token_class == "Num_Oct" or self.buffer[
            0].token_class == "Num_Hex":
            left = AST.NumberExpressionAST(int(self.buffer[0].lexeme), None)
        elif self.buffer[1] and self.buffer[0].token_class == "Id" and self.buffer[1].token_class == "L_Paren_Bracket":
            left = self.handle_call_function(self.buffer[0].lexeme)
        elif self.buffer[1] and self.buffer[0].token_class == "Id" and self.buffer[1].token_class == "L_Sq_Bracket":
            left = self.arrays_rule(self.buffer[0].lexeme)
        elif self.buffer[0].token_class == "Id":
            left = AST.VariableExpressionAST(self.buffer[0].lexeme, None)
        elif self.buffer[0].token_class == "String":
            left = AST.StringExpressionAST(self.buffer[0].lexeme, None)
        elif self.buffer[0].token_class == "Minus":
            op = self.buffer[0].lexeme
            self.get_next_token()

        elif self.buffer[0].token_class == "L_Sq_Bracket":
            left = self.make_list()
            if left is None:
                self.get_next_token()

        if not self.buffer[1] or not self.buffer[1].token_class in priority:
            return left
        node = AST.BinaryExpressionAST(self.buffer[1].lexeme, None, left, None, priority[self.buffer[1].token_class])
        left.parent = node
        local_root = node

        while self.buffer[1].token_class in priority:
            right = None
            self.get_next_token()
            self.get_next_token()

            if self.buffer[0].token_class == "Num" or self.buffer[0].token_class == "Real_Num" or \
                    self.buffer[0].token_class == "Num_Oct" or self.buffer[
                0].token_class == "Num_Hex":
                right = AST.NumberExpressionAST(int(self.buffer[0].lexeme), node)
            elif self.buffer[1] and self.buffer[0].token_class == "Id" and \
                    self.buffer[1].token_class == "L_Paren_Bracket":
                right = self.handle_call_function(self.buffer[0].lexeme)
                right.parent = node
            elif self.buffer[1] and self.buffer[0].token_class == "Id" and self.buffer[1].token_class == "L_Sq_Bracket":
                right = self.arrays_rule(self.buffer[0].lexeme)
                right.parent = node
            elif self.buffer[0].token_class == "Id":
                right = AST.VariableExpressionAST(self.buffer[0].lexeme, node)
            elif self.buffer[0].token_class == "String":
                right = AST.StringExpressionAST(self.buffer[0].lexeme, node)
            elif self.buffer[0].token_class == "Minus":
                op = self.buffer[0].lexeme
                self.get_next_token()
            node.second = right

            if self.buffer[1] is None or (self.buffer[1].token_class in priority) == False:
                break
            if priority[self.buffer[1].token_class] > node.priority:
                new_node = AST.BinaryExpressionAST(self.buffer[1].lexeme, node, node.second, None,
                                                   priority[self.buffer[1].token_class])
                node.second = new_node
            else:
                while node.parent and node.parent.priority >= priority[self.buffer[1].token_class]:
                    node = node.parent
                new_node = AST.BinaryExpressionAST(self.buffer[1].lexeme, node.parent, node, None,
                                                   priority[self.buffer[1].token_class])
                if node == local_root:
                    local_root = new_node
                else:
                    node.parent.second = new_node
                node.parent = new_node

            node = new_node
        return local_root

    def symbols_table(self):
        table = AST.symTable()
        error = [False]
        self.root.find_declaration(table, error)
        # table.print_table(0)
        self.root.make_assembler()
        AST.code_assembler += "leave\n"
        # print(AST.code_assembler)
        return error[0]

    def handle_shifts(self):
        shift = 0
        while self.buffer[1].token_class == "Tab":
            shift += 1
            self.get_next_token()
        return shift

    def create_AST(self):
        self.buffer[0] = self.lexer.lexer()
        self.buffer[1] = self.lexer.lexer()
        self.root, shift = self.handle_body(0)
        return self.root

    def print_AST(self):
        self.root.print(0)


