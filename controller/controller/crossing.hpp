#pragma once

#include <controller/utility.hpp>

#include <vector>
#include <optional>


namespace traffic {
    using id_type = u32;
    constexpr inline id_type illegal_id = max_value<id_type>;
    
    
    struct crossing {
        enum class light_type  { TWO_LIGHTS, THREE_LIGHTS };
        enum class light_state { GREEN, ORANGE, RED };
        
        id_type id;
        std::vector<id_type> crosses;
        light_type type = light_type::THREE_LIGHTS;
        mutable light_state state = light_state::RED;
        float clearing_time;
        
        // Assumed to be (true, false, false) if these are not provided.
        bool vehicles_waiting = true, vehicles_coming = false, emergency = false;
        
        eq_comparable_fields(crossing, id);
        hashable(id);
    };
    
    // Used for heterogeneous lookup.
    inline crossing dummy_crossing(id_type id) {
        return crossing { .id = id };
    }
}