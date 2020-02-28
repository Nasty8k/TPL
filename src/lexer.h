#ifndef COMPILER_LEXER_H
#define COMPILER_LEXER_H

#include <iostream>
#include <cstring>
#include <fstream>
#include <map>

using namespace std;

struct Token {
    unsigned int x;
    unsigned int y;
    string type;
    string word;
};


class Lexer {
public:
    bool flagEndWork, flagFile, isToken;
    void initFile(char *file);
    void initString(char *str);
    int notEnd();

    struct Token getNextToken();
    Lexer();

    //FOR TEST
    string searchType(string lex);
    bool is_char(char elem);
    bool isNormalVariable (string lex);
    bool isNormalString   (string lex);
    bool isNormalDigit    (string lex);
    bool isNormalNumber   (string lex);

private:
    typedef map<string,string> IDType_Lexem; //<Lexeme(key), Type(value)>
    IDType_Lexem mapKey, mapOperation, mapSpace; // Number 1, 2, 3
    IDType_Lexem::iterator itType;

    ifstream inputFile;
    string   inputStr;

    unsigned int  posLast, posS, posC;
    bool isNewLine;

    Token tokOut;
    void formTokenOut(string type, string buf);

    //Lexeme work help
    bool is_2Type(char elem);
    bool is_3Type(char elem);
    bool inMap(int number, string str);

//    bool is_char(char elem);
//    bool isNormalVariable (string lex);
//    bool isNormalString   (string lex);
//    bool isNormalDigit    (string lex);
//    bool isNormalNumber   (string lex);

    char getNextCh();
    void goBackCh();

    //Lexeme work buffer
    string searchLexeme();
    //string searchType(string lex);
};

#endif //COMPILER_LEXER_H
