project(helloworld)
cmake_minimum_required(VERSION 2.8.12)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup(TARGETS)

find_package(GDAL REQUIRED)

add_executable(helloworld main.cpp)

target_link_libraries(helloworld
    PUBLIC
    GDAL::GDAL
)
