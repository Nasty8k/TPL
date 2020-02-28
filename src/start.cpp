#include <fstream>
#include "start.h"

int Start::checkInput(char* option, char* input) {
    int res = 0, forStrWork = 3;

    if (!strcmp(option, "--dump-tokens")) {
        res = 1;
    }
    if (!strcmp(option, "--dump-ast")) {
        cout << "\n>AST output:";
        res = 2;
    }
    if (!strcmp(option, "--dump-asm")) {
        cout << "\n>Assembler output:";
        res = 3;
    }
    // Error args check
    if (res == 0)
        return res;
    // File or string input
    string in = input;
    if (in.rfind(".py") == std::string::npos) {
        // That is string format work
        (!strcasecmp(input, "string")) ? res += forStrWork : res = -1;
        return res;
    }

    ifstream fin;
    fin.open(input);
    if (!fin.is_open()) res = -2;
    else fin.close();

    return res;
}

void Start::erMessageArgs() {
    cout << "Need Format: ./compiler [Options] <input_file.py || <string>" << endl;
    cout << "Options:" << endl;
    cout << "  --dump-tokens - is result of LEXER analyser" << endl;
    cout << "  --dump-ast    - is Abstract Syntax Tree" << endl;
    cout << "  --dump-asm    - is Assembler translation" << endl;
}

void Start::erMessageFileType() {
    cout << "Need Format: ./compiler [Options] <input_file.py>" << endl;
    cout << "  File needs format <fileName.py>" << endl;
}

void Start::erMessageFileOpen() {
    cout << "Need Format: ./compiler [Options] <input_file.py>" << endl;
    cout << "  File open error" << endl;
}
