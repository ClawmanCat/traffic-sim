# Traffic Simulation Controller
A controller for the traffic simulation written in C++.

### Setup
To run this project, you will need the following:
- CMake, version 3.12 or newer
- Python
- Conan (`pip install conan`)
- Ninja (https://ninja-build.org/, probably already installed with your IDE.)
- Clang 11 or newer (Project currently does not build with MSVC due to lack of C++20 feature support.)

To build the project:
```
mkdir out
cd out
cmake -DCMAKE_BUILD_TYPE=[DEBUG|RELEASE] -G Ninja -DCMAKE_C_COMPILER=[clang++|clang-cl] -DCMAKE_CXX_COMPILER=[clang++|clang-cl] ../
cmake --build ./[debug|release] --target all
```
(or use an IDE like a normal person.)
