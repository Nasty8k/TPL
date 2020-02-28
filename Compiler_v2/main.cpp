#include <iostream>
#include "compiler.h"
using namespace std;
#define OUT(x, y, t, l) printf("Loc_<%2d: %2d>\t<%10s>\t[%10s]\n", x, y, t, l)
//--dump-tokens Examples\Example_1.py
int main(int argc, char **argv) {
    if (argc != 3) exit(1);
    Start start;
    Lexer lexer;
    Token out;
    cout << "Args: " << argv[1] << " " << argv[2] << endl;
    char strExample[] = "String\n\t for EXAMPLE\0";

    int res = start.checkInput(argv[1], argv[2]);
    switch (res) { // TODO Завернуть это все в красивый метод Start.Compile
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
            cout << "Error " << res << endl;
            break;
        case 1: // Lexer file work
            cout << "File work" << endl;
            lexer.initFile(argv[2]);
            while (lexer.notEnd()) {

                out = lexer.getNextToken();
                //cout << "\n" << r << " " << lexer.getPosLast() <<  " | ";
                OUT(out.x, out.y, out.type.c_str(), out.word.c_str());
            }
            break;
        case 2:
            cout << "Ast" << endl;
            break;
        case 3:
            cout << "Asm" << endl;
            break;
        case 4:
            cout << "Input: " << strExample << endl;
            lexer.initString(strExample);
            cout << ">Lexer output:\n";
            while (lexer.notEnd()) {
                out = lexer.getNextToken();
                OUT(out.x, out.y, out.type.c_str(), out.word.c_str());
            }
            break;
    }
    return 0;
}
