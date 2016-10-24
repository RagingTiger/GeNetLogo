#-----------------------------------------------------------------------------
# HDFJAVA Config file for compiling against HDFJAVA install directory
#-----------------------------------------------------------------------------
get_filename_component (SELF_DIR "${CMAKE_CURRENT_LIST_FILE}" PATH)
get_filename_component (_IMPORT_PREFIX "${SELF_DIR}" PATH)
get_filename_component (_IMPORT_PREFIX "${_IMPORT_PREFIX}" PATH)
if (NOT WIN32)
  get_filename_component (_IMPORT_PREFIX "${_IMPORT_PREFIX}" PATH)
endif (NOT WIN32)

#-----------------------------------------------------------------------------
# User Options
#-----------------------------------------------------------------------------
set (HDF_ENABLE_PARALLEL OFF)
set (HDF_ENABLE_JPEG_LIB_SUPPORT ON)
set (HDF_ENABLE_Z_LIB_SUPPORT ON)
set (HDF_ENABLE_SZIP_SUPPORT  ON)
set (HDF_ENABLE_SZIP_ENCODING ON)
set (BUILD_SHARED_LIBS    OFF)
set (HDF_PACKAGE_EXTLIBS ON)

#-----------------------------------------------------------------------------
# Version Strings
#-----------------------------------------------------------------------------
set (HDFJAVA_VERSION_STRING 2.11.0)
set (HDFJAVA_VERSION_MAJOR  2)
set (HDFJAVA_VERSION_MINOR  11)

#-----------------------------------------------------------------------------
# Directories
#-----------------------------------------------------------------------------
set (HDFJAVA_LIBRARY "${_IMPORT_PREFIX}/lib")
set (HDFJAVA_LIBRARIES "${HDFJAVA_LIBRARY}")

#-----------------------------------------------------------------------------
# Don't include targets if this file is being picked up by another
# project which has already build HDFJAVA as a subproject
#-----------------------------------------------------------------------------
if (NOT TARGET "hdf-java")
  if (HDF_PACKAGE_EXTLIBS AND NOT TARGET "jpeg")
    include (${SELF_DIR}/../JPEG/jpeg-targets.cmake)
  endif (HDF_PACKAGE_EXTLIBS AND NOT TARGET "jpeg")
  if (HDF_PACKAGE_EXTLIBS AND NOT TARGET "zlib")
    include (${SELF_DIR}/../ZLIB/zlib-targets.cmake)
  endif (HDF_PACKAGE_EXTLIBS AND NOT TARGET "zlib")
  if (HDF_PACKAGE_EXTLIBS AND NOT TARGET "szip")
    include (${SELF_DIR}/../SZIP/szip-targets.cmake)
  endif (HDF_PACKAGE_EXTLIBS AND NOT TARGET "szip")
  if (HDF_PACKAGE_EXTLIBS AND NOT TARGET "hdf4")
    include (${SELF_DIR}/../hdf4/hdf4-targets.cmake)
  endif (HDF_PACKAGE_EXTLIBS AND NOT TARGET "hdf4")
  if (HDF_PACKAGE_EXTLIBS AND NOT TARGET "hdf5")
    include (${SELF_DIR}/../hdf5/hdf5-targets.cmake)
  endif (HDF_PACKAGE_EXTLIBS AND NOT TARGET "hdf5")
  include (${SELF_DIR}/hdf-java-targets.cmake)
endif (NOT TARGET "hdf-java")

set (HDFJAVA_INCLUDE_DIRS 
    ${HDFJAVA_LIBRARY}/jarhdf-2.11.0.jar
    ${HDFJAVA_LIBRARY}/jarhdf5-2.11.0.jar
    ${HDFJAVA_LIBRARY}/jarhdfobj.jar
    ${HDFJAVA_LIBRARY}/jarfitsobj.jar
    ${HDFJAVA_LIBRARY}/jarh4obj.jar
    ${HDFJAVA_LIBRARY}/jarh5obj.jar
    ${HDFJAVA_LIBRARY}/jarnc2obj.jar
    ${HDFJAVA_LIBRARY}/fits.jar
    ${HDFJAVA_LIBRARY}/netcdf.jar
    ${HDFJAVA_LIBRARY}/slf4j-api-1.7.5.jar
    ${HDFJAVA_LIBRARY}/slf4j-nop-1.7.5.jar
)
