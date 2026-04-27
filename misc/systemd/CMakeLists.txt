find_package(PkgConfig REQUIRED)

pkg_search_module(Systemd QUIET IMPORTED_TARGET systemd)
if (Systemd_FOUND)
    set(SYSTEMD_PKG_NAME systemd)
else()
    pkg_search_module(Systemd REQUIRED IMPORTED_TARGET libsystemd)
    set(SYSTEMD_PKG_NAME libsystemd)
endif()

if (NOT DEFINED SYSTEMD_SYSTEM_UNIT_DIR)
    pkg_get_variable(SYSTEMD_SYSTEM_UNIT_DIR ${SYSTEMD_PKG_NAME} systemdsystemunitdir)
    if (NOT SYSTEMD_SYSTEM_UNIT_DIR)
        set(SYSTEMD_SYSTEM_UNIT_DIR "${CMAKE_INSTALL_PREFIX}/lib/systemd/system")
    endif()
endif()

if (NOT DEFINED SYSTEMD_USER_UNIT_DIR)
    pkg_get_variable(SYSTEMD_USER_UNIT_DIR ${SYSTEMD_PKG_NAME} systemduserunitdir)
    if (NOT SYSTEMD_USER_UNIT_DIR)
        set(SYSTEMD_USER_UNIT_DIR "${CMAKE_INSTALL_PREFIX}/lib/systemd/user")
    endif()
endif()

macro(install_symlink filepath wantsdir)
    file(MAKE_DIRECTORY ${PROJECT_BINARY_DIR}/link/${wantsdir}/)
    execute_process(COMMAND ${CMAKE_COMMAND} -E create_symlink ${CMAKE_INSTALL_PREFIX}/lib/systemd/user/${filepath} ${PROJECT_BINARY_DIR}/link/${wantsdir}/${filepath})
    install(FILES ${PROJECT_BINARY_DIR}/link/${wantsdir}/${filepath} DESTINATION ${SYSTEMD_USER_UNIT_DIR}/${wantsdir}/)
endmacro(install_symlink)

configure_file("dde-session-pre.target.wants/treeland-sd.service.in" "dde-session-pre.target.wants/treeland-sd.service" IMMEDIATE @ONLY)
configure_file("dde-session-pre.target.wants/treeland-xwayland.service.in" "dde-session-pre.target.wants/treeland-xwayland.service" IMMEDIATE @ONLY)
configure_file("dde-session-pre.target.wants/treeland-shortcut.service.in" "dde-session-pre.target.wants/treeland-shortcut.service" IMMEDIATE @ONLY)
configure_file("dde-session-pre.target.wants/treeland.service.in" "dde-session-pre.target.wants/treeland.service" IMMEDIATE @ONLY)
configure_file("treeland-session-helper.service.in" "treeland-session-helper.service" IMMEDIATE @ONLY)
configure_file("treeland-screensaver.service.in" "treeland-screensaver.service" IMMEDIATE @ONLY)
configure_file("treeland.service.in" "treeland.service" IMMEDIATE @ONLY)

install(FILES ${SERVICES} DESTINATION ${SYSTEMD_USER_UNIT_DIR})
install(FILES ${CMAKE_CURRENT_BINARY_DIR}/treeland.service DESTINATION ${SYSTEMD_SYSTEM_UNIT_DIR})
install(FILES ${CMAKE_CURRENT_BINARY_DIR}/treeland-session-helper.service DESTINATION ${SYSTEMD_USER_UNIT_DIR})
install(FILES ${CMAKE_CURRENT_BINARY_DIR}/treeland-screensaver.service DESTINATION ${SYSTEMD_USER_UNIT_DIR})

install(DIRECTORY DESTINATION ${SYSTEMD_USER_UNIT_DIR}/dde-session-pre.target.wants/)
install(DIRECTORY DESTINATION ${SYSTEMD_USER_UNIT_DIR}/dde-session-shutdown.target.wants/)
set(DDE_SESSION_PRE_WANTS
    dde-session-pre.target.wants/treeland-sd.socket
    dde-session-pre.target.wants/treeland-xwayland.socket
    dde-session-shutdown.target.wants/treeland-session-shutdown.service
    ${CMAKE_CURRENT_BINARY_DIR}/dde-session-pre.target.wants/treeland-sd.service
    ${CMAKE_CURRENT_BINARY_DIR}/dde-session-pre.target.wants/treeland-xwayland.service
    ${CMAKE_CURRENT_BINARY_DIR}/dde-session-pre.target.wants/treeland-shortcut.service
    ${CMAKE_CURRENT_BINARY_DIR}/dde-session-pre.target.wants/treeland.service
)

install(FILES ${DDE_SESSION_PRE_WANTS} DESTINATION ${SYSTEMD_USER_UNIT_DIR})
install_symlink(treeland-sd.socket dde-session-pre.target.wants)
install_symlink(treeland-sd.service dde-session-pre.target.wants)
install_symlink(treeland-xwayland.socket dde-session-pre.target.wants)
install_symlink(treeland-xwayland.service dde-session-pre.target.wants)
install_symlink(treeland-shortcut.service dde-session-pre.target.wants)
install_symlink(treeland.service dde-session-pre.target.wants)
install_symlink(treeland-session-shutdown.service dde-session-shutdown.target.wants)
install_symlink(treeland-session-helper.service treeland.service.wants)
install_symlink(treeland-screensaver.service treeland.service.wants)
