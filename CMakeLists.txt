cmake_minimum_required(VERSION 3.16)
project("console_intent")
set(CMAKE_CXX_STANDARD 17)

set(APP_SOURCE "${PROJECT_SOURCE_DIR}/source")
set(EXTERNALS "${PROJECT_SOURCE_DIR}/external")
set(TESTS "${PROJECT_SOURCE_DIR}/test")

find_package(Python COMPONENTS Interpreter Development)

# pybind11
add_subdirectory(${EXTERNALS}/pybind11)

# app
add_executable (
    recognizerApp
    ${APP_SOURCE}/app.cpp)

target_include_directories (
    recognizerApp 
    PRIVATE ${APP_SOURCE}
)

target_link_libraries(
    recognizerApp
    PRIVATE pybind11::embed
)

file(COPY ${APP_SOURCE}/model.py DESTINATION ${CMAKE_BINARY_DIR})

include(FetchContent)
FetchContent_Declare(
  googletest
  URL https://github.com/google/googletest/archive/609281088cfefc76f9d0ce82e1ff6c30cc3591e5.zip
)
# For Windows: Prevent overriding the parent project's compiler/linker settings
set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
FetchContent_MakeAvailable(googletest)

enable_testing()

add_executable(
  tester
  ${TESTS}/tester.cpp
  )
target_link_libraries(
  tester
  gtest_main
)

include(GoogleTest)
gtest_discover_tests(tester)
