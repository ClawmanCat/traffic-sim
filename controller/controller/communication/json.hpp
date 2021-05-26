#pragma once

#include <controller/common.hpp>
#include <controller/communication/state.hpp>

#include <nlohmann/json.hpp>


namespace ts {
    using json = nlohmann::json;
    
    
    // Assuming that 'str' is a valid message,
    // decodes the message into the route objects encoded within it.
    inline std::vector<route_state> from_json(std::string_view str, const std::unordered_map<route_id, route_state>& old_state = {}) {
        try {
            json message = json::parse(str);
            
            auto value_or = [] <typename T> (const json& j, std::string_view key, T default_value) {
                auto it = j.find(key);
                return (it == j.end()) ? default_value : (T) *it;
            };
            
            
            if (message["msg_type"] == "initialization") {
                std::vector<route_state> result;
                
                for (const auto& j : (std::vector<json>) message["data"]) {
                    result.push_back(route_state {
                        .id              = j["id"],
                        .state           = route_state::light_state::RED_SAFE,
                        .crosses         = j["crosses"],
                        .clearing_time   = milliseconds(long(1000 * ((float) j["clearing_time"]))),
                        .waiting         = true,
                        .coming          = false,
                        .emergency       = false,
                        .bus             = false,
                        .blocked         = false,
                        .most_recent_msg = message["msg_id"]
                    });
                }
    
                return result;
            } else if (message["msg_type"] == "notify_sensor_change") {
                std::vector<route_state> result;
    
                for (const auto& j : (std::vector<json>) message["data"]) {
                    const auto& old = old_state.at((route_id) j["id"]);
                    
                    if (old.most_recent_msg >= message["msg_id"]) {
                        console_io::out("Ignoring message for light ", old.id, ": the msg_id indicates this message is outdated.");
                    }
                    
                    result.push_back(route_state {
                        .id              = j["id"],
                        .crosses         = old.crosses,
                        .clearing_time   = value_or(j, "clearing_time",     old.clearing_time),
                        .waiting         = value_or(j, "vehicles_waiting",  old.waiting),
                        .coming          = value_or(j, "vehicles_coming",   old.coming),
                        .emergency       = value_or(j, "emergency_vehicle", old.emergency),
                        .bus             = value_or(j, "public_vehicle",    old.bus),
                        .blocked         = value_or(j, "vehicles_blocking", old.blocked),
                        .most_recent_msg = message["msg_id"]
                    });
                }
    
                return result;
            } else {
                console_io::out("Unknown message type: "s + (std::string) message["msg_type"]);
                return {};
            }
        } catch (std::exception& e) {
            console_io::out(
                "Failed to decode JSON message. No changes will be recorded:\n",
                e.what(), "\n",
                "While decoding JSON object:\n",
                str
            );
            
            return {};
        }
    }
    
    
    // Given a set of routes, constructs a message of type 'perform_state_change'.
    inline std::string to_json(const std::vector<route_state*>& routes) {
        static unsigned counter = 0;
        
        json message;
        message["msg_type"] = "notify_traffic_light_change";
        message["msg_id"]   = counter++;
        message["data"]     = std::vector<json>{};
        
        for (const auto& route : routes | views::indirect) {
            message["data"] += {
                { "id", route.id },
                { "state", light_state_to_string(route.state) }
            };
        }
        
        return message.dump(3);
    }
}