#ifndef COMPILER_LEXER_H
#define COMPILER_LEXER_H

#include <iostream>
#include <cstring>
#include <fstream>
#include <map>

enum class TokenClass;

struct Token {
    unsigned int row;
    unsigned int col;
    TokenClass type;
    std::string typeStr;
    std::string word;
};
enum class TokenClass {
    /* mapKey */
    Kw_Def,
    Kw_If,
    Kw_Else,
    Kw_Print,
    Kw_Input,
    Kw_While,
    Kw_Min,
    Kw_Max,
    Kw_Return,
    Kw_toStr,
    Kw_toInt,
    /* mapOperation */
    Op_Assign,
    Op_Equal,
    Op_NonEqual,
    Op_More,
    Op_Less,
    Op_MorEq,
    Op_LesEq,
    Op_Add,
    Op_AddAdd,
    Op_Sub,
    Op_SubSub,
    Op_Mul,
    Op_Div,
    Op_Mod,
    Op_Not,
    Op_And,
    Op_Or,
    /* mapSpace */
    Sp_LCParen,
    Sp_RCParen,
    Sp_LQParen,
    Sp_RQParen,
    Sp_Colon,
    Sp_Comma,
    Sp_Quot1,
    Sp_Point,
    Sp_Space,
    Sp_NewL,
    Sp_Comment,
    Sp_END,
    /* Other */
    Ot_Var,
    Ot_String,
    Ot_Digit,
    Ot_Number,
    Ot_Unknown,
};

class Lexer {
public:
    bool flagEndWork;
    void initFile(std::string file);
    void initString(char *str);
    int notEnd();

    struct Token getNextToken();
    Lexer();

private:
    typedef std::map<std::string, TokenClass> IDType_map; //<Lexeme(key), Type(value)>
    IDType_map mapKey, mapOperation, mapSpace; // Number 1, 2, 3
    IDType_map::iterator itType;

    std::ifstream inputFile;
    std::string   inputStr;

    unsigned int  posLast, posR, posC;
    bool isNewLine, flagFile, isToken;

    Token tokOut;
    void formTokenOut(TokenClass type, std::string word);
    std::string token_class_to_string(TokenClass tok);
    //Lexeme work help
    bool is_2Type(char elem);
    bool is_3Type(char elem);
    bool inMap(int number, std::string word);

    bool is_char(char elem);
    bool is_digit(char elem);
    bool isNormalVariable (std::string word);
    bool isNormalString   (std::string word);
    bool isNormalDigit    (std::string word);
    bool isNormalNumber   (std::string word);

    char getNextCh();
    void goBackCh();

    //Lexeme work buffer
    std::string searchLexeme();
    TokenClass searchType(std::string word);
};

#endif //COMPILER_LEXER_H
