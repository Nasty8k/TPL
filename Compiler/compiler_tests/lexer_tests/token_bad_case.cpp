#include <gtest/gtest.h>
#include "../src/lexer.h"
using testing::Eq;
/*
struct Token {
    unsigned int row;
    unsigned int col;
    TokenClass type;
    std::string typeStr;
    std::string word;
};
*/

::testing::AssertionResult tokens_equal(Token Right, Token Left) {
    if (Right.row != Left.row)
        return ::testing::AssertionFailure() << Left.row <<" row!!!";
    if (Right.col != Left.col)
        return ::testing::AssertionFailure() << Left.col <<" col!!!";;
    if (Right.type != Left.type)
        return ::testing::AssertionFailure() << "type!!!";;
    if (std::strcmp(Right.word.c_str(), Left.word.c_str()) != 0)
        return ::testing::AssertionFailure() << "word!!!";;
    return ::testing::AssertionSuccess() << "+";;
}

namespace {
class TestLexer : public ::testing::Test {
    public:
        Lexer obj;

        Token BadString = {1,7, TokenClass::Ot_Unknown, "???", "'Input string -_- " }; //Token 3
        Token BadNumber = {2,5, TokenClass::Ot_Unknown, "???", "123x4"}; //Token 7
        Token BadVar    = {3,1, TokenClass::Ot_Unknown, "???", "var$bad"}; //Token 8
        Token BadOp     = {3,12, TokenClass::Ot_Unknown, "???", "+++"}; //Token 11
        Token TestName[4];

        Token TokenIn[4];
        unsigned int idx[4] = {3, 7, 8, 11};

        TestLexer() {
            std::string file = "..\\Examples\\Bad_cases.py";
            obj.initFile(file); // could put here a make method

            TestName[0] = BadString;
            TestName[1] = BadNumber;
            TestName[2] = BadVar;
            TestName[3] = BadOp;

            int i = 0, N = 0;
            while (obj.flagEndWork != true) {
                if (i == idx[N] && N < sizeof(idx)) {
                    TokenIn[N] = obj.getNextToken();
                    ++N;
                }
                obj.getNextToken();
                i += 1;
            }
        }
    };
}
TEST_F(TestLexer, bad_case_1) {
    EXPECT_TRUE(tokens_equal(TestName[0], TokenIn[0]));
}
TEST_F(TestLexer, bad_case_2) {
    EXPECT_TRUE(tokens_equal(TestName[1], TokenIn[1]));
}
TEST_F(TestLexer, bad_case_3) {
    EXPECT_TRUE(tokens_equal(TestName[2], TokenIn[2]));
}
TEST_F(TestLexer, bad_case_4) {
    EXPECT_TRUE(tokens_equal(TestName[3], TokenIn[3]));
}
