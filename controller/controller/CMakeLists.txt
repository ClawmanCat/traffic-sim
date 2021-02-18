include(create_target)

create_target(
    TrafficController
    EXECUTABLE
    0 0 1
    # Dependencies:
    PUBLIC CONAN_PKG::boost
    PUBLIC CONAN_PKG::ixwebsocket
)