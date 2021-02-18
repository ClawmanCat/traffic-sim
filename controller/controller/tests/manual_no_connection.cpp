// Insert mock connection.
#include <controller/tests/mock_connection.hpp>

#define TRAFFICCONTROLLER_VERSION_MAJOR "TEST"
#define TRAFFICCONTROLLER_VERSION_MINOR "TEST"
#define TRAFFICCONTROLLER_VERSION_PATCH "TEST"

// Mock connection is set up, just run normally.
// TODO: Do this properly. This will fail with multiple translation units.
#include <controller/main.cpp>