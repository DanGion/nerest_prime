set(PROJECT amqp-tutorial)
project(${PROJECT} C CXX)
cmake_minimum_required(VERSION 2.8.11)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11 -Wextra -pedantic")

include_directories(AMQP-CPP-2.1.4)

add_subdirectory(AMQP-CPP-2.1.4)
add_library(poco_simple_handler SimplePocoHandler.cpp SimplePocoHandler.h)
target_link_libraries(poco_simple_handler PocoNet PocoFoundation)

set(PROGS rpc_server)

foreach(item ${PROGS})
    add_executable(${item} "${item}.cpp")
    target_link_libraries(${item} amqp-cpp poco_simple_handler)    
endforeach(item)
