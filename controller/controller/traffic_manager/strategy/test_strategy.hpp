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
            
            std::size_t num_lights = std::min(16ull, states->size());
            std::vector<route_state> result = routes
                | views::transform([&](auto id) { return states->at(id); })
                | views::cycle
                | views::drop(num_lights * n)
                | views::take(num_lights)
                | views::transform([&](auto state) { return ++state.state, state; })
                | to<std::vector>;
            
            n += num_lights;
            
            return result;
        };
    
    private:
        std::vector<route_id> routes;
        unsigned n = 0;
    };
}