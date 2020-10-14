from src.Lexer import Lexer
from src.Parser import Parser
from src import AST
import os
import sys


if __name__ == "__main__":
    if len(sys.argv) == 2:
        do = Parser(sys.argv[1])
        do.create_AST()
        do.symbols_table()
        output_filename = sys.argv[1].split(".")
        output_filename = output_filename[1].split("/")
        exe_file = output_filename[-1]
        output_filename = exe_file + ".s"
        os.system("mkdir -p asm")
        os.system("mkdir -p exe")
        with open("./asm/" + output_filename, "w") as file:
            file.write(AST.code_assembler)
            file.close()
        os.system("gcc -Wall -no-pie ./asm/" + output_filename + " -o ./exe/" + output_filename[:-2])
    else:
        if sys.argv[1] == "--dump-tokens":
            do = Lexer()
            do.file_in(sys.argv[2])

            lexeme_struct = None
            while True:
                lexeme_struct = do.lexer()
                if lexeme_struct is None:
                    break
                if lexeme_struct.lexeme.isspace():
                    lexeme = str("ascii(%d)") % ord(lexeme_struct.lexeme)
                else:
                    lexeme = lexeme_struct.lexeme
                print("Loc<%2d: %2d> %12s\t%12s"
                      % (lexeme_struct.line, lexeme_struct.pos, lexeme, lexeme_struct.token_class))

        elif sys.argv[1] == "--dump-ast":
            do = Parser(sys.argv[2])
            do.create_AST()
            do.print_AST()
        elif sys.argv[1] == "--dump-asm":
            do = Parser(sys.argv[2])
            do.create_AST()
            do.symbols_table()
            print(AST.code_assembler)

