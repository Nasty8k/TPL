#include <fstream>
#include "start.h"

int Start::checkInput(char* option, char* input) {
    int res = 0, forStrWork = 3;

    if (!strcmp(option, "--dump-tokens")) {
        res = 1;
    }
    if (!strcmp(option, "--dump-ast")) {
        std::cout << "\n>AST output:";
        res = 2;
    }
    if (!strcmp(option, "--dump-asm")) {
        std::cout << "\n>Assembler output:";
        res = 3;
    }
    // Error args check
    if (res == 0)
        return res;
    // File or string input
    std::string in = input;
    if (in.rfind(".py") == std::string::npos) {
        // That is string format work
        (!strcasecmp(input, "string")) ? res += forStrWork : res = -1;
        return res;
    }

    std::ifstream fin;
    fin.open(input);
    if (!fin.is_open()) res = -2;
    else fin.close();

    return res;
}

void Start::erMessageArgs() {
    std::cout << "Need Format: ./compiler [Options] <input_file.py || <string>" << std::endl;
    std::cout << "Options:" << std::endl;
    std::cout << "  --dump-tokens - is result of LEXER analyser" << std::endl;
    std::cout << "  --dump-ast    - is Abstract Syntax Tree" << std::endl;
    std::cout << "  --dump-asm    - is Assembler translation" << std::endl;
}

void Start::erMessageFileType() {
    std::cout << "Need Format: ./compiler [Options] <input_file.py>" << std::endl;
    std::cout << "  File needs format <fileName.py>" << std::endl;
}

void Start::erMessageFileOpen() {
    std::cout << "Need Format: ./compiler [Options] <input_file.py>" << std::endl;
    std::cout << "  File open error" << std::endl;
}