#pragma once

#include <controller/common.hpp>
#include <controller/traffic_manager/strategy/strategy.hpp>
#include <controller/communication/state.hpp>


namespace ts {
    class strategy_test : public traffic_strategy {
    public:
        strategy_test(void) {
            routes = *simulation_state::instance().view() | views::keys | to<std::vector>;
        }
        
        
        std::vector<route_state> update(void) override {
            auto states = simulation_state::instance().view();
            
            std::vector<route_state> result = routes
                | views::transform([&](auto id) { return states->at(id); })
                | views::cycle
                | views::drop(3 * n)
                | views::take(3)
                | views::transform([&](auto state) { return ++state.state, state; })
                | to<std::vector>;
            
            n += 3;
            
            return result;
        };
    
    private:
        std::vector<route_id> routes;
        unsigned n = 0;
    };
}