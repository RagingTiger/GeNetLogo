#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "szip" for configuration "Release"
set_property(TARGET szip APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(szip PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "C"
  IMPORTED_LINK_INTERFACE_LIBRARIES_RELEASE "m"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libszip.a"
  )

list(APPEND _IMPORT_CHECK_TARGETS szip )
list(APPEND _IMPORT_CHECK_FILES_FOR_szip "${_IMPORT_PREFIX}/lib/libszip.a" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
