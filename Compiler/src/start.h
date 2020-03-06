#ifndef COMPILER_START_H
#define COMPILER_START_H
#include <iostream>
#include <cstring>


class Start {
public:
    int checkInput(char* option, char* input);
    void erMessageArgs();
    void erMessageFileType();
    void erMessageFileOpen();
};
#endif //COMPILER_START_H
