cmake_minimum_required(VERSION 3.21)

project(werock-codecs LANGUAGES CXX)

message(STATUS "Build werockshare...")

add_custom_command(
        OUTPUT sbe.stub
        COMMAND java
        ARGS
        -Dsbe.target.language=Cpp
        -Dsbe.errorLog=yes
        -Dsbe.output.dir=${CMAKE_CURRENT_SOURCE_DIR}
        -jar ${CMAKE_CURRENT_SOURCE_DIR}/sbe/sbe-all-1.29.0.jar
        "${CMAKE_CURRENT_SOURCE_DIR}/sbe/schema.xml"

        COMMAND cp ${CMAKE_CURRENT_SOURCE_DIR}/sbe/schema.xml sbe.stub
        DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/sbe/schema.xml
        COMMENT "Generating Sbe...")
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/WeRock_Share_Sbe)

add_custom_target(werock-codecs DEPENDS sbe.stub)