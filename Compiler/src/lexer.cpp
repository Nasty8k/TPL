#include <stdlib.h>
#include "lexer.h"

void Lexer::initFile(std::string file) {
    inputFile.open(file.c_str(), std::ios_base::in);
    inputFile.seekg(0, std::ios_base::beg);
    this->flagFile = true;
}
void Lexer::initString(char *str) {
    inputStr = str;
    this->flagFile = false;
}
int Lexer::notEnd() {
    return !(this->flagEndWork);
}

struct Token Lexer::getNextToken() {
    std::string l = "NONE";
    TokenClass t = TokenClass::Ot_Unknown;
    l = searchLexeme();
    if (!isToken) {
        t = searchType(l);
        formTokenOut(t, l);
    }
    isToken = false;
    return this->tokOut;
}
Lexer::Lexer() {
    //SET MAP from ABS_Lexer.txt (+ Map)
    //    Lexeme      Type
    //----------------------------------
    // Number 1 -> Key_lexeme
    mapKey["def"]       = TokenClass::Kw_Def;
    mapKey["if"]        = TokenClass::Kw_If;
    mapKey["else"]      = TokenClass::Kw_Else;
    mapKey["print"]     = TokenClass::Kw_Print;
    mapKey["input"]     = TokenClass::Kw_Input;
    mapKey["while"]     = TokenClass::Kw_While;
    mapKey["min"]       = TokenClass::Kw_Min;
    mapKey["max"]       = TokenClass::Kw_Max;
    mapKey["return"]    = TokenClass::Kw_Return;
    mapKey["str"]       = TokenClass::Kw_toStr;
    mapKey["int"]       = TokenClass::Kw_toInt;
    // Number 2 -> Operation_lexeme
    mapOperation["="]   = TokenClass::Op_Assign;
    mapOperation["=="]  = TokenClass::Op_Equal;
    mapOperation["!="]  = TokenClass::Op_NonEqual;
    mapOperation[">"]   = TokenClass::Op_More;
    mapOperation["<"]   = TokenClass::Op_Less;
    mapOperation[">="]  = TokenClass::Op_MorEq;
    mapOperation["<="]  = TokenClass::Op_LesEq;
    mapOperation["+"]   = TokenClass::Op_Add;
    mapOperation["++"]  = TokenClass::Op_AddAdd;
    mapOperation["-"]   = TokenClass::Op_Sub;
    mapOperation["--"]  = TokenClass::Op_SubSub;
    mapOperation["*"]   = TokenClass::Op_Mul;
    mapOperation["//"]  = TokenClass::Op_Div;
    mapOperation["%"]   = TokenClass::Op_Mod;
    mapOperation["not"] = TokenClass::Op_Not;
    mapOperation["and"] = TokenClass::Op_And;
    mapOperation["or"]  = TokenClass::Op_Or;
    // Number 3 -> Space_lexeme
    mapSpace["("]       = TokenClass::Sp_LCParen;
    mapSpace[")"]       = TokenClass::Sp_RCParen;
    mapSpace["["]       = TokenClass::Sp_LQParen;
    mapSpace["]"]       = TokenClass::Sp_RQParen;
    mapSpace[":"]       = TokenClass::Sp_Colon;
    mapSpace[","]       = TokenClass::Sp_Comma;
    mapSpace["\'"]      = TokenClass::Sp_Quot1;
    mapSpace["."]       = TokenClass::Sp_Point;
    mapSpace[" "]       = TokenClass::Sp_Space;
    mapSpace["\n"]      = TokenClass::Sp_NewL;
    mapSpace["#"]       = TokenClass::Sp_Comment;
    mapSpace[""]        = TokenClass::Sp_END;

    posR = 1, posC = 1, posLast = 0;
    flagEndWork = false, flagFile = false, isToken = false, isNewLine = false;
}

void Lexer::formTokenOut (TokenClass type, std::string word) {
    this->tokOut.row = this->posR;
    this->tokOut.col = this->posC;
    this->tokOut.type = type;
    this->tokOut.typeStr = token_class_to_string(type);
    this->tokOut.word = word;
    this->posC += word.size();
}
std::string Lexer::token_class_to_string(TokenClass tok) {
    switch (tok) {
        case TokenClass::Kw_Def:
            return "DEF";
        case TokenClass::Kw_If:
            return "IF";
        case TokenClass::Kw_Else:
            return "ELSE";
        case TokenClass::Kw_Print:
            return "PRINT";
        case TokenClass::Kw_Input:
            return "INPUT";
        case TokenClass::Kw_While:
            return "WHILE";
        case TokenClass::Kw_Min:
            return "MIN";;
        case TokenClass::Kw_Max:
            return "MAX";
        case TokenClass::Kw_Return:
            return "RETURN";
        case TokenClass::Kw_toStr:
            return "TO_STR";
        case TokenClass::Kw_toInt:
            return "TO_INT";
        case TokenClass::Op_Assign:
            return "OP(=)";
        case TokenClass::Op_Equal:
            return "OP(==)";
        case TokenClass::Op_NonEqual:
            return "OP(!=)";
        case TokenClass::Op_More:
            return "OP(>)";
        case TokenClass::Op_Less:
            return "OP(<)";
        case TokenClass::Op_MorEq:
            return "OP(>=)";
        case TokenClass::Op_LesEq:
            return "OP(<=)";
        case TokenClass::Op_Add:
            return "OP(+)";
        case TokenClass::Op_AddAdd:
            return "OP(++)";
        case TokenClass::Op_Sub:
            return "OP(-)";
        case TokenClass::Op_SubSub:
            return "OP(--)";
        case TokenClass::Op_Mul:
            return "OP(*)";
        case TokenClass::Op_Div:
            return "OP(//)";
        case TokenClass::Op_Mod:
            return "OP(%)";
        case TokenClass::Op_Not:
            return "OP(NOT)";
        case TokenClass::Op_And:
            return "OP(AND)";
        case TokenClass::Op_Or:
            return "OP(OR)";
        case TokenClass::Sp_LCParen:
            return "(";
        case TokenClass::Sp_RCParen:
            return ")";
        case TokenClass::Sp_LQParen:
            return "[";
        case TokenClass::Sp_RQParen:
            return "]";
        case TokenClass::Sp_Colon:
            return ":";
        case TokenClass::Sp_Comma:
            return ",";
        case TokenClass::Sp_Quot1:
            return "\'";
        case TokenClass::Sp_Point:
            return ".";
        case TokenClass::Sp_Space:
            return " ";
        case TokenClass::Sp_NewL:
            return "NewLine";
        case TokenClass::Sp_Comment:
            return "#comment";
        case TokenClass::Sp_END:
            return "EOF";
        case TokenClass::Ot_Var:
            return "VAR";
        case TokenClass::Ot_String:
            return "STRING";
        case TokenClass::Ot_Digit:
            return "DIGIT";
        case TokenClass::Ot_Number:
            return "NUMBER";
        case TokenClass::Ot_Unknown:
            return "???";
        default:
            return "ERROR";
    }
}

//Lexeme work help
bool Lexer::is_char(char elem)  { return ((elem <= 'A' && elem >= 'Z') || (elem >= 'a' && elem <= 'z') );}
bool Lexer::is_digit(char elem) { return (elem <= '9' && elem >= '0'); }
bool Lexer::is_2Type(char elem) { std::string ch; ch = elem; return inMap(2, ch);}
bool Lexer::is_3Type(char elem) { std::string ch; ch = elem; return inMap(3, ch);}

char Lexer::getNextCh() {
    char out;
    if (this->flagFile) {
        inputFile.seekg(this->posLast, std::ios_base::beg);
        out = inputFile.get();
    } else {
        out = inputStr[this->posLast];
    }
    if (out == EOF || out == '\0')
        flagEndWork = true;
    this->posLast += 1;
    return out;
}
void Lexer::goBackCh() {
    posLast -= 1;
    if (this->flagFile)
        inputFile.seekg(-1, std::ios_base::cur);
}


//Lexeme work buffer
std::string Lexer::searchLexeme() {
    std::string buf = "";
    int deep = 0;
    bool flag = true;
    char ch = getNextCh();

    while (flag) {
        if (this->isNewLine)
            if (!(ch == ' ' || ch == '\t'))
                this->isNewLine = false;
        //std::cout << "{" << ch << "}";
        switch (ch) {
            case ' ' :
            case '\t':
                //std::cout << "{WORK SPACE T}" << std::endl;
                if (!buf.empty() && buf[0] != ' ') {
                    goBackCh();
                    return buf;
                }
                if (this->isNewLine) {
                    while (ch == ' ' || ch == '\t') {
                        (ch == ' ') ? deep += 1 : deep += 4;
                        ch = getNextCh();
                    }
                    char num[16];
                    formTokenOut(TokenClass ::Sp_Space, itoa(deep, num, 10));
                    this->isToken = true;
                    this->posC += deep - 1;
                    goBackCh();
                    this->isNewLine = false;
                    return " ";
                }
                this->posC += 1;
                break;

            case '0':
            case '1':
            case '2':
            case '3':
            case '4':
            case '5':
            case '6':
            case '7':
            case '8':
            case '9':
                while (!is_2Type(ch) && !is_3Type(ch) && ch != '\n' && ch != '\0' && ch != EOF) {
                    buf += ch;
                    ch = getNextCh();
                }
                goBackCh();
                return buf;

            case '\n':
                //cout << "{Work NL}";
                //if (this->flagFile) ch = getNextCh();   // This is not a bug this is a feature
                this->isNewLine = true;
                if (buf.empty()) {
                    this->posR += 1;
                    this->posC = 1;
                    //cout << "[NL S:" << this->posS << " C:" << this->posC << "]\n";
                    ch = getNextCh();
                    if (ch == ' ') deep += 1;
                    break;
                } else {
                    goBackCh();
                    return buf;
                }
            case '#':
                //cout << "{Work #}" ;
                if (!buf.empty()) {
                    goBackCh();
                    return buf;
                } else {
                    formTokenOut(TokenClass::Sp_Comment, "#");
                    isToken = true;
                    while (ch != '\n' && ch != '\0' && ch != EOF) {
                        ch = getNextCh();
                    }
                    goBackCh();
                    return "#";
                }
            case EOF:
                if (!buf.empty()) {
                    flagEndWork = true;
                    return buf;
                } else {
                    isToken = true;
                    formTokenOut(TokenClass::Sp_END, "");
                    return "";
                }
            default:
                //cout << "{Work DEF}";
                if (is_2Type(ch)) {
                    if (!buf.empty()) {
                        //cout << "BEFORE " << getPosLast();
                        goBackCh();
                        //cout << " posBACK " << getPosLast() << endl;

                        return buf;
                    }
                    while (is_2Type(ch)) {
                        buf += ch;
                        ch = getNextCh();
                    }
                    goBackCh();
                    return buf;
                }
                if (is_3Type(ch)) {
                    //cout << "(TYPE3)BUF["<<buf<<"]"<<endl;
                    if (buf.empty()) {
                        if (ch != '\'') {
                            buf += ch;
                            return buf;
                        } else {
                            while (ch != EOF && ch != '\n' && ch != '#') {
                                buf += ch;
                                ch = getNextCh();
                                if (ch == '\'') {
                                    buf += ch;
                                    return buf;
                                }
                            }
                            goBackCh();
                            return buf;
                        }
                    } else {
                        goBackCh();
                        return buf;
                    }
                }
                buf += ch;
                break;
        }
        //cout<<"\n---------------\n";
        //cout << "BUF=[" << buf << "]" << endl;
        ch = getNextCh();
    }
    return "";
}

TokenClass Lexer::searchType(std::string word) {
    if (inMap(1, word))  return itType->second;
    if (inMap(2, word))  return itType->second;
    if (inMap(3, word))  return itType->second;
    if (isNormalVariable(word))  return TokenClass::Ot_Var;
    if (isNormalString(word))    return TokenClass::Ot_String;
    if (isNormalDigit(word))     return TokenClass::Ot_Digit;
    if (isNormalNumber(word))    return TokenClass::Ot_Number;
    return TokenClass::Ot_Unknown;
}

bool Lexer::isNormalVariable(std::string word) {
    if (word.empty()) return false;
    int i = 0;
    for (i; i < word.size(); ++i)
        if (!(is_char(word[i]) || is_digit(word[i]) || word[i] == '_')) return false;
    return !is_digit(word[0]);
}
bool Lexer::isNormalString(std::string word) {
    return  (!word.empty() && word[0] == '\'' && word[word.size()-1] == '\'');
}
bool Lexer::isNormalDigit(std::string word) {
    return ((word.size() == 1) && is_digit(word[0]));
}
bool Lexer::isNormalNumber(std::string word) {
    if (word.size() < 2) return false;
    if (!(is_digit(word[0]) && word[0] != '0')) return false;
    for (char i : word) if (!is_digit(i)) return false;
    return true;
}

bool Lexer::inMap(int number, std::string word) {
    switch (number) {
        case 1:
            itType = mapKey.find(word);
            return itType != mapKey.end();
        case 2:
            itType = mapOperation.find(word);
            return itType != mapOperation.end();
        case 3:
            itType = mapSpace.find(word);
            return itType != mapSpace.end();
        default:
            return false;
    }
}
