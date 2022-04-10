# Project Title

Embedded intent recognizer 

## Description

A simple embedded intetn recognition tool using pybind11 and cpp to run a simple multiclass-multioutput classification (also known as multitask classification) python scirpt. 

The script uses a deep-pre trained transformer architecture-based model for feature extraction (distill-BERT in our case) and predicts the multitask intent using a trained probabilistic classifier (random forest in our case).  

## Getting Started

### Dependencies

* Python 3.10.0
* Numpy 1.22.3
* Sklearn 1.0.2
* PyTorch 1.11.0
* Transformers 4.17.0

* CMake 3.16
* Modern cpp >17

### Installing

* git clone https://github.com/AdaGuny/embedded-intent-recognizer.git
* cd embedded-intent-recognizer/

### Executing program

* mkdir build && cd build && cmake .. && make

## Authors

Ada
[@linkedIn](https://www.linkedin.com/in/ada-g%C3%BCney-arslan/)

## Version History

* 0.1
    * Initial Release
    * Works on console 
   

## To Do

* Tests
* Python function to python class   

## License

This project is licensed under the [GNU General Public License v3.0] License - see the LICENSE.md file for details
