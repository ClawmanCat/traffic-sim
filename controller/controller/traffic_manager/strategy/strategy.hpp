#pragma once

#include <controller/common.hpp>
#include <controller/communication/state.hpp>


namespace ts {
    struct traffic_strategy {
        virtual ~traffic_strategy(void) = default;
        virtual std::vector<route_state> update(void) = 0;
    };
}