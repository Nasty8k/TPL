cmake_minimum_required(VERSION 3.15)
project(compiler)

add_definitions(-std=c++11)

set(SOURCE_FILES main.cpp)
add_executable(compiler_run ${SOURCE_FILES})

include_directories(src)

add_subdirectory(src)
add_subdirectory(compiler_tests)

target_link_libraries(compiler_run compiler)
