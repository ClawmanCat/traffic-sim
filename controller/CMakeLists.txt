cmake_minimum_required(VERSION 3.12)
project("TrafficController")

# C++20 features are required.
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Output to out directory.
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/out/${CMAKE_BUILD_TYPE}/lib)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/out/${CMAKE_BUILD_TYPE}/lib)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/out/${CMAKE_BUILD_TYPE}/bin)

set(CMAKE_BINARY_DIR "${CMAKE_SOURCE_DIR}/out")

# Allow including from the root directory.
include_directories(${CMAKE_SOURCE_DIR})

# Allow loading of scripts from cmake folder.
set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${CMAKE_SOURCE_DIR}/cmake")

# Load compiler settings profile.
# TODO: Change this for other compilers.
include(clang_cl_profile)
set_compiler_profile()

# Run Conan
include(run_conan)
run_conan()


add_subdirectory(controller)

