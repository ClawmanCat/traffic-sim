#pragma once

#include <controller/common.hpp>
#include <controller/traffic_manager/strategy/strategy.hpp>
#include <controller/communication/state.hpp>

#include <unordered_map>


namespace ts {
    class strategy_accumulative_priority : public traffic_strategy {
    public:
        constexpr static inline seconds orange_time = 3s;
        
        strategy_accumulative_priority(void) {
            route_urgency = *simulation_state::instance().view()
                | views::keys
                | views::transform([](auto route) { return std::pair { route, 0.0f }; })
                | ranges::to<std::unordered_map>;
            
            last_change = *simulation_state::instance().view()
                | views::keys
                | views::transform([](auto route) { return std::pair { route, steady_clock::now() }; })
                | ranges::to<std::unordered_map>;
        }
        
        
        std::vector<route_state> update(void) override {
            auto state = simulation_state::instance().view();
            
            std::vector<route_state> result;
            auto push_route = [&](auto&& state) -> decltype(auto) {
                result.push_back(std::forward<decltype(state)>(state));
                return result.back();
            };
            
            
            // Assign new priorities to all routes.
            for (const auto& route : *state | views::values) {
                float& urgency = route_urgency[route.id];
                
                if (route.emergency) {
                    urgency += 1e6f;
                } else if (route.blocked) {
                    urgency = -1e6f;
                } else if (route.bus) {
                    urgency += 1e3f;
                } else if (route.waiting) {
                    if (route.state != route_state::light_state::GREEN) {
                        urgency += 1.0f;
                    }
                } else if (route.coming) {
                    if (route.state == route_state::light_state::GREEN) {
                        urgency += 5.0f;
                    }
                } else {
                    urgency = 0.0f;
                }
            }
            
            
            for (const auto& route : *state | views::values) {
                // Set green routes to orange if clearing time has elapsed.
                if (
                    route.state == route_state::light_state::GREEN &&
                    time_since(last_change[route.id]) > route.clearing_time &&
                    !route.coming
                ) {
                    auto& r = push_route(route);
                    ++r.state;
                    
                    last_change[route.id] = steady_clock::now();
                }
                
                // Advance orange & blocking red routes if the clearing time has elapsed.
                if (
                    (
                        route.state == route_state::light_state::RED_BLOCKING &&
                        time_since(last_change[route.id]) > route.clearing_time
                    ) ||
                    (
                        route.state == route_state::light_state::ORANGE &&
                        time_since(last_change[route.id]) > orange_time
                    )
                ) {
                    auto& r = push_route(route);
                    ++r.state;
                    
                    last_change[route.id] = steady_clock::now();
                }
            }
            
            
            // Starting from the route with the highest priority, keep setting routes to green if they don't have
            // a currently green route crossing them.
            // Don't set routes to green if they would block a road with higher priority, as this could cause that road
            // to remain perpetually red, due to timing differences.
            std::unordered_set<route_id> blocked;
            std::vector<route_id> ordered = order_routes();
            
            for (const auto& route : *state | views::values) {
                if (route.state != route_state::light_state::RED_SAFE) {
                    blocked.insert(route.crosses.begin(), route.crosses.end());
                }
            }
            
            for (const auto& route_id : ordered | views::reverse) {
                const route_state& route = state->at(route_id);
                
                if (!blocked.contains(route_id) && route.state == route_state::light_state::RED_SAFE) {
                    bool skip = false;
                    for (auto crossing : route.crosses) {
                        if (route_urgency[crossing] > route_urgency[route.id]) {
                            skip = true;
                            break;
                        }
                    }
                    
                    if (skip) continue;
                    
                    
                    auto& r = push_route(route);
                    ++r.state;
                    
                    route_urgency[route_id] = 0.0f;
                    last_change[route_id] = steady_clock::now();
                    blocked.insert(route.crosses.begin(), route.crosses.end());
                }
            }
            
            
            return result;
        };
    
    private:
        std::unordered_map<route_id, float> route_urgency;
        std::unordered_map<route_id, steady_clock::time_point> last_change;
        
        
        std::vector<route_id> order_routes(void) const {
            std::vector<std::pair<route_id, float>> pairs = route_urgency
                | views::transform([](const auto& kv) { return std::pair { kv.first, kv.second }; })
                | ranges::to<std::vector>;
            
            std::sort(
                pairs.begin(),
                pairs.end(),
                [](const auto& a, const auto& b) { return a.second < b.second; }
            );
            
            return pairs | views::keys | ranges::to<std::vector>;
        }
    };
}