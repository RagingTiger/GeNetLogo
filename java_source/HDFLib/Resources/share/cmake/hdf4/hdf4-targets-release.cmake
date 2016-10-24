#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "hdf" for configuration "Release"
set_property(TARGET hdf APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(hdf PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "C"
  IMPORTED_LINK_INTERFACE_LIBRARIES_RELEASE "m;jpeg;zlib;szip"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libhdf.a"
  )

list(APPEND _IMPORT_CHECK_TARGETS hdf )
list(APPEND _IMPORT_CHECK_FILES_FOR_hdf "${_IMPORT_PREFIX}/lib/libhdf.a" )

# Import target "mfhdf" for configuration "Release"
set_property(TARGET mfhdf APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(mfhdf PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "C"
  IMPORTED_LINK_INTERFACE_LIBRARIES_RELEASE "hdf"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libmfhdf.a"
  )

list(APPEND _IMPORT_CHECK_TARGETS mfhdf )
list(APPEND _IMPORT_CHECK_FILES_FOR_mfhdf "${_IMPORT_PREFIX}/lib/libmfhdf.a" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
