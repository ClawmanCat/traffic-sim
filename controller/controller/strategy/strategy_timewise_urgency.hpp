#pragma once

#include <controller/strategy/crossing_strategy.hpp>
#include <controller/controller.hpp>

#include <functional>


namespace traffic {
    // For every crossing, an urgency score is generated. It is built up from several metrics:
    // - The amount of time vehicles have been waiting at the light.
    // - If the light is green and there are more cars coming.
    // - If there's an emergency vehicle waiting at the light or coming towards it.
    // If a light is switched from red to green, it will stay green for at least min_green_time.
    // If the light was already green last time, repeated_green_time is used instead.
    class strategy_timewise_urgency : public crossing_strategy {
    public:
        strategy_timewise_urgency(
            milliseconds min_green_time = 10s,
            milliseconds repeated_green_time = 5s,
            float incoming_vehicle_urgency = 250.0f,
            float emergency_urgency = infinity<float>,
            std::function<float(float)> timewise_urgency = [](float time) { return time * time; }
        ) :
            min_green_time(min_green_time),
            repeated_green_time(repeated_green_time),
            incoming_urgency(incoming_vehicle_urgency),
            emergency_urgency(emergency_urgency),
            timewise_urgency(std::move(timewise_urgency))
        {}
        
        
        void init(controller* controller, const std::unordered_set<crossing>& state) override {
            owner = controller;
            for (const auto& cross : state) last_free_time[cross.id] = clock::now();
        }
        
        
        [[nodiscard]] result select_crossings(const std::unordered_set<crossing>& state) override {
            auto& logger = owner->get_logger();
            
            
            // Reset waiting time for empty crossings & currently passable crossings.
            for (const auto& cross : state) {
                if (!cross.vehicles_waiting) {
                    logger.log("Crossing ", cross.id, " is empty and will not get any time-associated urgency boost.");
                    last_free_time[cross.id] = clock::now();
                } else if (cross.state == crossing::light_state::GREEN) {
                    logger.log("Crossing ", cross.id, " has a green light and will not get any time-associated urgency boost.");
                    last_free_time[cross.id] = clock::now();
                }
            }
    
    
            // Find crossing most urgently in need of green light.
            std::vector<crossing> sorted_state = state | to<std::vector>;
            
            std::sort(
                sorted_state.begin(),
                sorted_state.end(),
                [&](const auto& a, const auto& b) {
                    return get_urgency(a) < get_urgency(b);
                }
            );
    
    
            // Select crossings that will be green during this tick.
            id_type most_urgent_crossing = sorted_state.back().id;
            std::vector<id_type> selected_crossings;
            milliseconds new_state_duration;
    
            if (contains(prev_crossings, most_urgent_crossing)) {
                // Most urgent crossing is already green, change nothing.
                logger.log(
                    "Most urgent crossing (", most_urgent_crossing, ") is already green.\n"
                    "Current state will be maintained."
                );
        
                new_state_duration = min_green_time;
            } else {
                // Set as many crossings as possible to green, starting at the most urgent ones.
                std::unordered_set<id_type> banned_crossings;
        
                for (const auto& cross : sorted_state | views::reverse) {
                    if (banned_crossings.contains(cross.id)) continue;
            
                    selected_crossings.push_back(cross.id);
                    banned_crossings.insert(cross.crosses.begin(), cross.crosses.end());
                }
        
                new_state_duration = repeated_green_time;
            }
    
    
            prev_crossings = selected_crossings;
            
            return result {
                .crossings      = std::move(selected_crossings),
                .green_duration = new_state_duration
            };
        }
        
    private:
        controller* owner = nullptr;
        
        milliseconds min_green_time;
        milliseconds repeated_green_time;
        float incoming_urgency;
        float emergency_urgency;
        std::function<float(float)> timewise_urgency;
    
        // Time since this light was red while not being devoid of vehicles.
        std::unordered_map<id_type, time_point> last_free_time;
    
        // Crossings that were green during the last tick.
        std::vector<id_type> prev_crossings;
        
        
        [[nodiscard]] float get_urgency(const crossing& cross) {
            float urgency = 0.0f;
    
            if (cross.vehicles_waiting) {
                float waiting_time = milliseconds_since(last_free_time[cross.id]) / 1000.0f;
                urgency += timewise_urgency(waiting_time);
            }
    
            if (cross.vehicles_coming && cross.state == crossing::light_state::GREEN) {
                urgency += incoming_urgency;
            }
    
            if (cross.emergency) {
                urgency += emergency_urgency;
            }
    
            return urgency;
        }
    };
}