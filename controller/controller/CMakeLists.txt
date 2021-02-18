include(create_target)

create_target(
    TrafficController
    EXECUTABLE
    0 0 1
    # Dependencies:
    PUBLIC CONAN_PKG::boost
    PUBLIC CONAN_PKG::ixwebsocket
    PUBLIC CONAN_PKG::range-v3
    PUBLIC CONAN_PKG::magic_enum
)