cmake_minimum_required(VERSION 3.18)

project(BOOST_BUILD)

set(_terminal_option)
if(THEROCK_INTERACTIVE)
  set(_terminal_option "USES_TERMINAL")
endif()

set(_bootstrap_exec bash "bootstrap.sh")
if(WIN32)
  set(_bootstrap_exec "cmd.exe" "/C" "bootstrap.bat")
endif()

add_custom_target(
  bootstrap_and_build ALL
  ${_terminal_option}
  WORKING_DIRECTORY "${BOOST_SOURCE_DIR}"
  COMMAND
    ${_bootstrap_exec} "--with-libraries=${THEROCK_BOOST_LIBRARIES}"
  COMMAND
    "${BOOST_SOURCE_DIR}/b2" link=static threading=multi
  COMMAND
    "${BOOST_SOURCE_DIR}/b2" headers
)

install(DIRECTORY "${BOOST_SOURCE_DIR}/stage/lib" DESTINATION ".")
