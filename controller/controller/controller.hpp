#pragma once

#include <controller/utility.hpp>
#include <controller/crossing.hpp>
#include <controller/communication.hpp>
#include <controller/strategy/crossing_strategy.hpp>

#include <magic_enum.hpp>

#include <unordered_map>
#include <unordered_set>
#include <iostream>


namespace traffic {
    class controller {
    public:
        controller(intersection_connection&& connection, unique<crossing_strategy>&& strategy)
            : id(next_id++), connection(std::move(connection)), strategy(std::move(strategy)), logger(id) {}
        
        
        [[noreturn]] void main(void) {
            init();
            while (true) loop();
        }
        
        
        controller_logger& get_logger(void) { return logger; }
    private:
        static inline u32 next_id = 0;
    
        u32 id;
        intersection_connection connection;
        unique<crossing_strategy> strategy;
        controller_logger logger;
        
        
        void init(void) {
            // Load initial state.
            auto state = connection.get_client_state();
            
            logger.core_assert(!state.empty(), "No crossings were retrieved from the simulation.");
            logger.log("Initialized ", state.size(), " traffic crossings.");
            
            strategy->init(this, state);
        }
        
        
        void loop(void) {
            logger.log("Getting simulation state...");
            auto state = connection.get_client_state();
            
            logger.log("Selecting crossings...");
            auto action = strategy->select_crossings(state);
            
            
            // Set the lights for the given crossings to the given color.
            auto set_lights = [&](const auto& crossings, crossing::light_state light_state) {
                using ltype  = crossing::light_type;
                using lstate = crossing::light_state;
                
                for (const auto& cross : crossings) {
                    auto old_cross = state.extract(dummy_crossing(cross)).value();
                    
                    if (old_cross.type == ltype::TWO_LIGHTS && light_state == lstate::ORANGE) {
                        logger.log("Ignoring light ", cross, " as it cannot be set to orange.");
                    } else {
                        logger.log("Setting light ", cross, " to state ", magic_enum::enum_name(light_state));
                        old_cross.state = light_state;
                    }
                    
                    state.insert(old_cross);
                }
            };
            
            
            // Set all lights to red.
            // If the light should be green this tick, this will be immediately undone
            // before anything is sent to the client.
            set_lights(state | views::transform(get_field(id)) | to<std::vector>, crossing::light_state::RED);
    
            // Set lights to green and wait.
            set_lights(action.crossings, crossing::light_state::GREEN);
            connection.set_client_state(state);
            std::this_thread::sleep_for(action.green_duration);
            
            // Set lights to orange and wait for the clearing time.
            float clearing_time = action.crossings.empty()
                ? 0.0f
                : *std::max_element(
                    action.crossings.begin(),
                    action.crossings.end(),
                    compare_fn(x, state.find(dummy_crossing(x))->clearing_time)
                );
            
            set_lights(action.crossings, crossing::light_state::ORANGE);
            connection.set_client_state(state);
            std::this_thread::sleep_for(milliseconds { (u64) (clearing_time / 1000) });
        }
    };
}