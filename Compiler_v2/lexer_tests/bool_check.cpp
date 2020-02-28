#include <gtest/gtest.h>

#include "../src/lexer.h"

using testing::Eq;

namespace {
    class TestLexer : public testing::Test {
    public:
        Lexer obj;
        TestLexer() {
            obj; // could put here a make method
        }
    };
}
TEST_F(TestLexer, lexem_isNumber) {
    ASSERT_TRUE(obj.isNormalNumber("123"))  << "Ok Number 123";
    ASSERT_FALSE(obj.isNormalNumber("012")) << "Bad Number 012";
    ASSERT_FALSE(obj.isNormalNumber("0x3")) << "Bad Number 0x3";
}

TEST_F(TestLexer, lexem_isString) {
    ASSERT_TRUE(obj.isNormalString("'Okey'"))    << "Ok 'String'";
    ASSERT_FALSE(obj.isNormalString("'Okey \n")) << "Bad 'String ";
}