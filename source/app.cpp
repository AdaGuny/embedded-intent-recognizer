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


    // borrow a python function from python file 

    py::function find_intent = py::module::import("model").attr("find_intent");
    /*py::function find_intent =
        py::reinterpret_borrow<py::function>( // cast from 'object' to 'function - use `borrow` (copy) or `steal` (move)
            py::module::import("model").attr("find_intent") // import method "find_intent" from python "module"
            );
    */

    // send user_input to borrowed python function
    py::object result = find_intent(user_input);  // automatic conversion from `std::string` 
    py::print(result); // print intent 
}