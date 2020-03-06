#include <iostream>
#include "compiler.h"

#define OUT(x, y, t, l) printf("Loc_<%2d: %2d>\t<%10s>\t[%10s]\n", x, y, t, l)
//--dump-tokens Examples\Example_1.py

int main(int argc, char **argv) {
    if (argc != 3) exit(1);
    Start start;
    Lexer lexer;
    Token out;
    std::cout << "Args: " << argv[1] << " " << argv[2] << std::endl;
    char strExample[] = "String\n\t for EXAMPLE\0";
    std::string fileName;

    int res = start.checkInput(argv[1], argv[2]);
    switch (res) {
        case 0: // Error args
            start.erMessageArgs();
            break;
        case -1:
            start.erMessageFileType();
            break;
        case -2:
            start.erMessageFileOpen();
            break;
        default:
            std::cout << "Error " << res << std::endl;
            break;
        case 1: // Lexer file work
            std::cout << "File work" << std::endl;
            fileName = argv[2];
            lexer.initFile(fileName);
            while (lexer.notEnd()) {
                out = lexer.getNextToken();
                //cout << "\n" << r << " " << lexer.getPosLast() <<  " | ";
                OUT(out.row, out.col, out.typeStr.c_str(), out.word.c_str());
            }
            break;
        case 2:
            std::cout << "Ast" << std::endl;
            break;
        case 3:
            std::cout << "Asm" << std::endl;
            break;
        case 4:
            std::cout << "Input: " << strExample << std::endl;
            lexer.initString(strExample);
            std::cout << ">Lexer output:\n";
            while (lexer.notEnd()) {
                out = lexer.getNextToken();
                OUT(out.row, out.col, out.typeStr.c_str(), out.word.c_str());
            }
            break;
    }
    return 0;
}
