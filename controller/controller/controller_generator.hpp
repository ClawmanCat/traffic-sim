#pragma once

#include <controller/controller.hpp>
#include <controller/communication.hpp>
#include <controller/strategy/crossing_strategy.hpp>

#include <unordered_map>


namespace traffic {
    // Analyzes the different crossings and generates controllers for each intersection.
    class controller_generator {
    public:
        template <typename Strategy>
        [[nodiscard]] static std::vector<controller> generate_controllers(const Strategy& strategy) {
            auto crossings = websockets_connection::instance().get_client_state();
            std::cout << "Received " << crossings.size() << " crossings.\n";
            
    
            // Finds all crossings in the same intersection as the given crossing.
            auto crossing_search = [&](const auto& self, const crossing& start, std::unordered_set<id_type>& found) -> void {
                auto get_crossing = [&](auto id) { return *(crossings.find(dummy_crossing(id))); };
                
                for (auto crossed : start.crosses) {
                    if (found.contains(crossed)) continue;
                    
                    found.insert(crossed);
                    self(self, get_crossing(crossed), found);
                }
            };
    
    
            // Construct a list of intersections.
            std::unordered_set<id_type> handled;
            std::vector<std::unordered_set<id_type>> intersections;
            
            for (const auto& cross : crossings) {
                if (handled.contains(cross.id)) continue;
                
                std::unordered_set<id_type> intersection;
                crossing_search(crossing_search, cross, intersection);
                
                for (auto id : intersection) handled.insert(id);
                intersections.push_back(std::move(intersection));
            }
            
            std::cout << "Split simulation into " << intersections.size() << " unique intersections.\n";
            
            
            // Construct a controller for each intersection.
            return intersections
                | views::transform([&](auto intersection) {
                    return controller {
                        intersection_connection { intersection | to<std::vector> },
                        std::make_unique<Strategy>(strategy)
                    };
                })
                | to<std::vector>;
        }
    private:
        controller_generator(void) = delete;
    };
}