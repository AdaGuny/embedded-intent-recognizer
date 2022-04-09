cmake_minimum_required(VERSION 3.16)
project("console_intent")
set(CMAKE_CXX_STANDARD 17)

set(APP_SOURCE "${PROJECT_SOURCE_DIR}/source")
set(EXTERNALS "${PROJECT_SOURCE_DIR}/externals")

find_package(Python COMPONENTS Interpreter Development)

# pybind11
add_subdirectory(${EXTERNALS}/pybind11)

# app
add_executable (
    recognizerApp
    ${APP_SOURCE}/app.cpp
)

target_include_directories (
    recognizerApp 
    PRIVATE ${APP_SOURCE}
)

target_link_libraries(
    recognizerApp
    PRIVATE pybind11::embed
)

file(COPY ${APP_SOURCE}/model.py DESTINATION ${CMAKE_BINARY_DIR})
