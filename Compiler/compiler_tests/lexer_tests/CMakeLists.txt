include_directories(../lib/googletest-master/googletest/include)

add_executable(runCompilerTests
        token_bad_case.cpp
        )

target_link_libraries(runCompilerTests gtest gtest_main)
target_link_libraries(runCompilerTests compiler)