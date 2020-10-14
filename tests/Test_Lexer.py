import sys
import unittest

sys.path.append("../pythonCompiler/")

from src.Lexer import Lexer
from src.Analyzer import Token


class Tests(unittest.TestCase):

    def test_lexer_KeyW(self):
        lex = Lexer()
        lex.text = "while a != 0 and b != 0:\n"
        test = lex.lexer()
        templ = [Token("KeyW_WHILE", "while", 1, 1), Token("KeyW_AND", "and", 1, 5),
                 Token("KeyW_WHILE", "while", 1, 1), Token("KeyW_WHILE", "while", 1, 1),
                 Token("KeyW_WHILE", "while", 1, 1), Token("KeyW_WHILE", "while", 1, 1),]
        self.assertEqual(test.line, templ[0].line)
        self.assertEqual(test.token_class, templ[0].token_class)
        self.assertEqual(test.lexeme, templ[0].lexeme)
        self.assertEqual(test.token_id, templ[0].token_id)

    def test_lexer_NoneType(self):
        text = Lexer()
        text.text = "*= 3"
        result = text.lexer()
        result_str = str(result.token_class)
        self.assertEqual(result_str, "Unknown")


unittest.main()
