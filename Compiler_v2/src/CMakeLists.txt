project(compiler)

set(HEADER_FILES
        compiler.h
        start.h
        lexer.h
        )

set(SOURCE_FILES
        start.cpp
        lexer.cpp
        )

add_library(compiler STATIC ${SOURCE_FILES} ${HEADER_FILES})
