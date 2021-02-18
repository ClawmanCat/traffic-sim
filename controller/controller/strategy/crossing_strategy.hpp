#pragma once

#include <controller/utility.hpp>
#include <controller/crossing.hpp>

#include <unordered_set>


namespace traffic {
    class controller;
    
    
    struct crossing_strategy {
        struct result {
            std::vector<id_type> crossings;
            milliseconds green_duration;
        };
        
        
        virtual ~crossing_strategy(void) = default;
        
        virtual void init(controller* controller, const std::unordered_set<crossing>& state) {}
        virtual result select_crossings(const std::unordered_set<crossing>& state) = 0;
    };
}