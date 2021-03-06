cmake_minimum_required(VERSION 2.8.10 FATAL_ERROR)
###############################################################################################################
# This script will build and run the examples from a compressed file
# Execute from a command line:
#     ctest -S HDFJAVA_Examples.cmake,HDFJavaExamples-0.1.1-Source -C Release -V -O test.log
###############################################################################################################

set(INSTALLDIR "/usr/local")
set(CTEST_CMAKE_GENERATOR "Unix Makefiles")
set(CTEST_SOURCE_NAME ${CTEST_SCRIPT_ARG})
set(CTEST_DASHBOARD_ROOT ${CTEST_SCRIPT_DIRECTORY})
set(CTEST_BUILD_CONFIGURATION "Release")
set(CTEST_USE_TAR_SOURCE "true")

###############################################################################################################
#     Adjust the following SET Commands as needed
###############################################################################################################
if(WIN32)
  set(ENV{HDFJAVA_DIR} "${INSTALLDIR}/cmake/hdf-java")
  set(CTEST_BINARY_NAME ${CTEST_SOURCE_NAME}\\build)
  set(CTEST_SOURCE_DIRECTORY "${CTEST_DASHBOARD_ROOT}\\${CTEST_SOURCE_NAME}")
  set(CTEST_BINARY_DIRECTORY "${CTEST_DASHBOARD_ROOT}\\${CTEST_BINARY_NAME}")
else(WIN32)
  set(ENV{HDFJAVA_DIR} "${INSTALLDIR}/share/cmake/hdf-java")
  set(ENV{LD_LIBRARY_PATH} "${INSTALLDIR}/lib")
  set(CTEST_BINARY_NAME ${CTEST_SOURCE_NAME}/build)
  set(CTEST_SOURCE_DIRECTORY "${CTEST_DASHBOARD_ROOT}/${CTEST_SOURCE_NAME}")
  set(CTEST_BINARY_DIRECTORY "${CTEST_DASHBOARD_ROOT}/${CTEST_BINARY_NAME}")
endif(WIN32)

###############################################################################################################
# For any comments please contact cdashhelp@hdfgroup.org
#
###############################################################################################################
 
#-----------------------------------------------------------------------------
set(CTEST_CMAKE_COMMAND "\"${CMAKE_COMMAND}\"")
## --------------------------
if(CTEST_USE_TAR_SOURCE)
  ## Uncompress source if tar or zip file provided
  ## --------------------------
  if(WIN32)
    set(CTEST_7Z_COMMAND "C:/Program Files/7-Zip/7z.exe")
    message(STATUS "extracting... [${CTEST_7Z_COMMAND} x ${CTEST_SOURCE_NAME}.zip]")
    execute_process(COMMAND ${CTEST_7Z_COMMAND} x ${CTEST_SOURCE_NAME}.zip RESULT_VARIABLE rv)
  else(WIN32)
    message(STATUS "extracting... [${CTEST_CMAKE_COMMAND} -E tar -xvf ${CTEST_SOURCE_NAME}.tar.gz]")
    execute_process(COMMAND tar -xvf ${CTEST_SOURCE_NAME}.tar.gz RESULT_VARIABLE rv)
  endif(WIN32)
 
  if(NOT rv EQUAL 0)
    message(STATUS "extracting... [error-(${rv}) clean up]")
    file(REMOVE_RECURSE "${CTEST_SOURCE_DIRECTORY}")
    message(FATAL_ERROR "error: extract of ${CTEST_SOURCE_NAME} failed")
  endif(NOT rv EQUAL 0)
endif(CTEST_USE_TAR_SOURCE)
 
#-----------------------------------------------------------------------------
## Clear the build directory
## --------------------------
set(CTEST_START_WITH_EMPTY_BINARY_DIRECTORY TRUE)
file(MAKE_DIRECTORY "${CTEST_BINARY_DIRECTORY}")
ctest_empty_binary_directory(${CTEST_BINARY_DIRECTORY})

# Use multiple CPU cores to build
include(ProcessorCount)
ProcessorCount(N)
if(NOT N EQUAL 0)
  if(NOT WIN32)
    set(CTEST_BUILD_FLAGS -j${N})
  endif(NOT WIN32)
  set(ctest_test_args ${ctest_test_args} PARALLEL_LEVEL ${N})
endif()
set (CTEST_CONFIGURE_COMMAND
    "${CTEST_CMAKE_COMMAND} -C \"${CTEST_SOURCE_DIRECTORY}/config/cmake/cacheinit.cmake\" -DCMAKE_BUILD_TYPE:STRING=${CTEST_BUILD_CONFIGURATION} ${BUILD_OPTIONS} \"-G${CTEST_CMAKE_GENERATOR}\" \"${CTEST_SOURCE_DIRECTORY}\""
)
 
#-----------------------------------------------------------------------------
## -- set output to english
set($ENV{LC_MESSAGES}  "en_EN")
 
#-----------------------------------------------------------------------------
  ## NORMAL process
  ## --------------------------
  CTEST_START (Experimental)
  CTEST_CONFIGURE (BUILD "${CTEST_BINARY_DIRECTORY}")
  CTEST_READ_CUSTOM_FILES ("${CTEST_BINARY_DIRECTORY}")
  CTEST_BUILD (BUILD "${CTEST_BINARY_DIRECTORY}" APPEND)
  CTEST_TEST (BUILD "${CTEST_BINARY_DIRECTORY}" APPEND ${ctest_test_args} RETURN_VALUE res)
  if(res GREATER 0)
    message (FATAL_ERROR "tests FAILED")
  endif(res GREATER 0)
#-----------------------------------------------------------------------------
############################################################################################################## 
message(STATUS "DONE")
