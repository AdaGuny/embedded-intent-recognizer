#include <iostream>
#include <vector>
#include <pybind11/pybind11.h>
#include <pybind11/embed.h>  // python interpreter
#include <pybind11/stl.h>  // type conversion

namespace py = pybind11;
using namespace py::literals;

int main() {
    
    std::string user_input;

    std::cout << "What do you want to know?" << std::endl;
    std::getline(std::cin, user_input);

    std::cout << "Going embedded..." << std::endl;

    //Start interpreter dies at the end of scope
    py::scoped_interpreter guard{}; // start the interpreter and keep it alive

}