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

    //Start interpreter dies automatically end of the scope
    py::scoped_interpreter guard{};

    py::print("Hello, from embedded Python!"); 


    // append source dir to sys.path, and python interpreter would find your custom python file
    py::module_ sys = py::module_::import("sys");
    py::list path = sys.attr("path");
    py::print(path);
    path.attr("append")("..");

    // load the python function from module 
    py::function find_intent = py::module::import("model").attr("find_intent");

    // send user_input to function
    // automatic conversion from `std::string`
    py::object result = find_intent(user_input); 
    // print intent
    py::print(result); // print intent 
}