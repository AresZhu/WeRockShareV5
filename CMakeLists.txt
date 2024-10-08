cmake_minimum_required(VERSION 3.21)

project(werock_codecs LANGUAGES CXX)

message(STATUS "Build werockshare...")

if (NOT DEFINED STANDALONE_PROJECT)
    if (CMAKE_CURRENT_SOURCE_DIR STREQUAL CMAKE_SOURCE_DIR)
        set(STANDALONE_PROJECT ON)
    else()
        set(STANDALONE_PROJECT OFF)
    endif ()
endif()

add_custom_command(
        OUTPUT sbe.stub
        COMMAND java
        ARGS
        -Dsbe.target.language=Cpp
        -Dsbe.errorLog=yes
        -Dsbe.output.dir=${CMAKE_CURRENT_SOURCE_DIR}
        -jar ${CMAKE_CURRENT_SOURCE_DIR}/sbe/sbe-all-1.33.0.jar
        "${CMAKE_CURRENT_SOURCE_DIR}/sbe/schema.xml"

        COMMAND cp ${CMAKE_CURRENT_SOURCE_DIR}/sbe/schema.xml sbe.stub
        COMMENT "Generating Sbe...current source dir: ${CMAKE_CURRENT_SOURCE_DIR}")

file(MAKE_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/fbs-headers)

add_custom_command(
        OUTPUT flatbuffers.stub
        COMMAND flatc --cpp -o ${CMAKE_CURRENT_SOURCE_DIR}/fbs-headers "${CMAKE_CURRENT_SOURCE_DIR}/fbs/Enum.fbs"
		"${CMAKE_CURRENT_SOURCE_DIR}/fbs/Shared.fbs"
		"${CMAKE_CURRENT_SOURCE_DIR}/fbs/Strategy.fbs"
		"${CMAKE_CURRENT_SOURCE_DIR}/fbs/Rpc.fbs"
		COMMAND cp ${CMAKE_CURRENT_SOURCE_DIR}/fbs/Enum.fbs flatbuffers.stub
        COMMENT "Generating Fbs...current source dir: ${CMAKE_CURRENT_SOURCE_DIR}")

add_library(${PROJECT_NAME} INTERFACE sbe.stub flatbuffers.stub)


if (STANDALONE_PROJECT)
else()
    target_include_directories(
    ${PROJECT_NAME}
    SYSTEM INTERFACE
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/WeRock_Share_Sbe>
    $<INSTALL_INTERFACE:include>)
	
	target_include_directories(
    ${PROJECT_NAME}
    SYSTEM INTERFACE
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/fbs-headers>
    $<INSTALL_INTERFACE:include>)
	

    message("Installing WeRockCodecs")

    include(GNUInstallDirs)

    install(
            TARGETS ${PROJECT_NAME}
            EXPORT ${PROJECT_NAME}-targets
    )

    install(
        DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/WeRock_Share_Sbe
        DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
        FILES_MATCHING
        PATTERN
        "*.h")
		
	install(
        DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/fbs-headers
        DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
        FILES_MATCHING
        PATTERN
        "*.h")

    install(
        EXPORT ${PROJECT_NAME}-targets
        NAMESPACE ::
        DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/${PROJECT_NAME})
endif()


