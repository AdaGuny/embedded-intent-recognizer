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

    py::print("Hello, from embedded Python!"); // use the Python API


    // append source dir to sys.path, and python interpreter would find your custom python file
    py::module_ sys = py::module_::import("sys");
    py::list path = sys.attr("path");
    py::print(path);
    path.attr("append")("..");

    // import python function from module
    // .py file has to be in the working directory 
    // check last line of cmake, it copies file to the working directory
    py::function find_intent = py::module::import("model").attr("find_intent");
    
    // save the result of user input 
    py::object intent = find_intent(user_input);  // automatic conversion from `std::string` 
    
    // print intent
    py::print(intent); // print intent 

}