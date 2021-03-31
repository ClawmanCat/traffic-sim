#pragma once

#include <controller/common.hpp>
#include <controller/communication/state.hpp>

#include <nlohmann/json.hpp>


namespace ts {
    using json = nlohmann::json;
    
    
    // Assuming that 'str' is a valid message of type 'notify_state_change',
    // decodes the message into the route objects encoded within it.
    inline std::vector<route_state> from_json(std::string_view str) {
        json message { str };
        
        auto value_or = [] <typename T>(const json& j, std::string_view key, T default_value) {
            auto it = j.find(key);
            return (it == j.end()) ? default_value : (T) *it;
        };
        
        std::vector<route_state> result;
        for (const auto& j : (std::vector<json>) message["data"]) {
            result.push_back(route_state {
                .id              = j["id"],
                .crosses         = j["crosses"],
                .clearing_time   = milliseconds(long(1000 * ((float) j["clearing_time"]))),
                .waiting         = value_or(j, "vehicles_waiting",  true),
                .coming          = value_or(j, "vehicles_coming",   true),
                .emergency       = value_or(j, "emergency_vehicle", true),
                .most_recent_msg = message["msg_id"]
            });
        }
        
        return result;
    }
    
    
    // Given a set of routes, constructs a message of type 'perform_state_change'.
    inline std::string to_json(const std::vector<route_state*>& routes) {
        static unsigned counter = 0;
        
        json message;
        message["msg_type"] = "perform_state_change";
        message["msg_id"]   = counter++;
        message["data"]     = { };
        
        for (const auto& route : routes | views::indirect) {
            message["data"] += {
                { "id", route.id },
                { "state", light_state_to_string(route.state) }
            };
        }
        
        return message.dump(3);
    }
}