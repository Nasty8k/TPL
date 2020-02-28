#include <stdlib.h>
#include "lexer.h"

void Lexer::initFile(char *file) {
    inputFile.open(file, ios_base::in);
    inputFile.seekg(0, ios_base::beg);
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
    string l = "NONE", t = "NONE";
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
    mapKey["def"]       = "def";
    mapKey["if"]        = "if";
    mapKey["else"]      = "else";
    mapKey["print"]     = "print";
    mapKey["input"]     = "input";
    mapKey["while"]     = "while";
    mapKey["min"]       = "min";
    mapKey["max"]       = "max";
    mapKey["return"]    = "return";
    mapKey["str"]       = "to_str";
    mapKey["int"]       = "to_int";
    // Number 2 -> Operation_lexeme
    mapOperation["="]   = "op_assign";
    mapOperation["=="]  = "op_equal";
    mapOperation["=="]  = "op_!equal";
    mapOperation[">"]   = "op_more";
    mapOperation["<"]   = "op_less";
    mapOperation[">="]  = "op_moeq";
    mapOperation["<="]  = "op_leeq";
    mapOperation["+"]   = "op_add";
    mapOperation["-"]   = "op_sub";
    mapOperation["*"]   = "op_mul";
    mapOperation["//"]  = "op_div";
    mapOperation["%"]   = "op_mod";
    mapOperation["!"]   = "op_not";
    // Number 3 -> Space_lexeme
    mapSpace["("]       = "l_paren";
    mapSpace[")"]       = "r_paren";
    mapSpace["["]       = "l_paren";
    mapSpace["]"]       = "r_paren";
    mapSpace[":"]       = "colon";
    mapSpace[","]       = "comma";
    mapSpace["\'"]      = "quot1";
    mapSpace["."]       = "point";
    mapSpace[" "]       = "space";
    mapSpace["\n"]       = "newL";
    mapSpace["#"]       = "comment";
    mapSpace[""]        = "END";

    posS = 1, posC = 1, posLast = 0;
    flagEndWork = false, flagFile = false, isToken = false, isNewLine = false;
}

// Private
void Lexer::formTokenOut (string type, string word) {
    this->tokOut.x = this->posS;
    this->tokOut.y = this->posC;
    this->tokOut.type = type;
    this->tokOut.word = word;
    this->posC += word.size();
}

//Lexeme work help
bool Lexer::is_char(char elem)  { return ((elem <= 'A' && elem >= 'Z') || (elem >= 'a' && elem <= 'z') );}
bool Lexer::is_2Type(char elem) { string ch = ""; ch += elem; return inMap(2, ch);}
bool Lexer::is_3Type(char elem) { string ch = ""; ch += elem; return inMap(3, ch);}

char Lexer::getNextCh() {
    char out;
    if (this->flagFile) {
        inputFile.seekg(this->posLast, ios_base::beg);
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
        inputFile.seekg(-1, ios_base::cur);
}


//Lexeme work buffer
string Lexer::searchLexeme() {
    string buf = "";
    int deep = 0;
    bool flag = true;
    char ch = getNextCh();

    while (flag) {
        if (this->isNewLine)
            if (!(ch == ' ' || ch == '\t'))
                this->isNewLine = false;
        //cout << "{" << ch << "}";
        switch (ch) {
            case ' ' :
            case '\t':
                //cout << "{WORK SPACE T}" << endl;
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
                    formTokenOut("space", itoa(deep, num, 10));
                    this->isToken = true;
                    this->posC += deep - 1;
                    goBackCh();
                    this->isNewLine = false;
                    return "#";
                }
                this->posC += 1;
                break;

            case '0' ... '9':
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
                    this->posS += 1;
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
                    formTokenOut("comment", "#");
                    isToken = true;
                    while (ch != '\n' && ch != '\0' && ch != EOF) {
                        ch = getNextCh();
                        //cout << ch;
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
                    formTokenOut("EOF", "");
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
}

string Lexer::searchType(string lex) {
    if (inMap(1, lex))  return itType->second;
    if (inMap(2, lex))  return itType->second;
    if (inMap(3, lex))  return itType->second;
    if (isNormalVariable(lex))  return "var";
    if (isNormalString(lex))    return "string";
    if (isNormalDigit(lex))     return "digit";
    if (isNormalNumber(lex))    return "number";
    return "???";
}

bool Lexer::isNormalVariable(string lex) {
    for (int i = 1; i < lex.size(); ++i)
        if (!(is_char(lex[i]) || isdigit(lex[i])))
            return false;
    return  (!lex.empty() && is_char(lex[0]));
}
bool Lexer::isNormalString(string lex) {
    return  (!lex.empty() && lex[0] == '\'' && lex[lex.size()-1] == '\'');
}
bool Lexer::isNormalDigit(string lex) {
    return ((lex.size() == 1) && isdigit(lex[0]));
}
bool Lexer::isNormalNumber(string lex) {
    if (lex.size() < 2) return false;
    if (!(isdigit(lex[0]) && lex[0] != '0')) return false;
    for (char i : lex) if (!isdigit(i)) return false;
    return true;
}

bool Lexer::inMap(int number, string str) {
    switch (number) {
        case 1:
            itType = mapKey.find(str);
            return (itType != mapKey.end()) ? true : false;
        case 2:
            itType = mapOperation.find(str);
            return (itType != mapOperation.end()) ? true : false;
        case 3:
            itType = mapSpace.find(str);
            return (itType != mapSpace.end()) ? true : false;
        default:
            return false;
    }
}
