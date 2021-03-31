#pragma once

#include <controller/common.hpp>
#include <controller/traffic_manager/strategy/strategy.hpp>
#include <controller/communication/state.hpp>


namespace ts {
    class strategy_round_robin : public traffic_strategy {
    public:
        strategy_round_robin(void) {
            routes = *simulation_state::instance().view() | views::keys | to<std::vector>;
        }
        
    
        std::vector<route_state> update(void) override {
            std::vector<route_state> result;
            
            auto current_state_view = simulation_state::instance().view();
            auto& current_state = *current_state_view;
            
    
            // Update currently non-red lights.
            for (auto& route : routes) {
                auto state = current_state.at(route);
                
                if (state.state != route_state::light_state::RED_SAFE) {
                    if (time_since(last_change[route]) >= state.clearing_time) {
                        ++state.state;
                        last_change[route] = steady_clock::now();
                    }
                }
                
                result.push_back(state);
            }
            
            
            // Set lights to green.
            std::unordered_set<route_id> blocked;
            std::vector<std::size_t> greenlit_indices;
            
            for (auto [i, route] : routes | views::enumerate) {
                auto state = current_state.at(route);
                
                if (state.state == route_state::light_state::RED_SAFE && !blocked.contains(route)) {
                    state.state = route_state::light_state::GREEN;
                    blocked.insert(state.crosses.begin(), state.crosses.end());
                    
                    result.push_back(std::move(state));
                    greenlit_indices.push_back(i);
                }
            }
            
            
            // Deprioritize lights that were set to green.
            for (auto [swapped, idx] : greenlit_indices | views::reverse | views::enumerate) {
                std::swap(
                    *(routes.begin() + idx),
                    *(routes.end() - (1 + swapped))
                );
            }
            
            
            return result;
        };
        
    private:
        std::vector<route_id> routes;
        std::unordered_map<route_id, steady_clock::time_point> last_change;
    };
}