cmake_minimum_required(VERSION 3.21)

project(werock_codecs LANGUAGES CXX)

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
        COMMENT "Generating Sbe...current source dir: ${CMAKE_CURRENT_SOURCE_DIR}")
add_custom_target(${PROJECT_NAME} DEPENDS sbe.stub)

set_target_properties(
        ${PROJECT_NAME}
        PROPERTIES
        INTERFACE_INCLUDE_DIRECTORIES
        ${CMAKE_CURRENT_SOURCE_DIR}/WeRock_Share_Sbe
)
