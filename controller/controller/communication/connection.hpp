#pragma once

#include <controller/common.hpp>
#include <controller/communication/state.hpp>
#include <controller/communication/json.hpp>
#include <controller/console_io.hpp>

#include <ixwebsocket/IXWebSocket.h>
#include <ixwebsocket/IXNetSystem.h>

#include <mutex>


namespace ts {
    class connection {
    public:
        [[nodiscard]] static connection& instance(void) {
            static connection i;
            return i;
        }
        
        
        void transmit_changes(void) {
            auto& state = simulation_state::instance();
            std::scoped_lock lock { mtx, state.mtx };
            
            if (!connected) return;
            
            ws.send(to_json(state.changes));
            state.changes.clear();
        }
    private:
        std::mutex mtx;
        ix::WebSocket ws;
        bool connected = false;
        
        
        connection(void) {
            std::lock_guard lock { mtx };
            
            ix::initNetSystem();
            
            auto url = console_io::in<std::string>("Please enter a URL to connect to", "ws://127.0.0.1:6969");
            ws.setUrl(url);
            
            console_io::out("Connecting to ", url, "...");
            
            ws.setOnMessageCallback([this](const ix::WebSocketMessagePtr& msg) {
                if (msg->type == ix::WebSocketMessageType::Open) {
                    console_io::out("Connection established.");
                    
                    std::scoped_lock lock { mtx };
                    connected = true;
                } else if (msg->type == ix::WebSocketMessageType::Close) {
                    // Program will exit before this function returns, no further actions necessary.
                    console_io::type_to_exit("Connection was closed. Press any key to exit");
                } else if (msg->type == ix::WebSocketMessageType::Message) {
                    on_msg_received(msg->str);
                }
            });
            
            ws.start();
        }
    
    
        void on_msg_received(std::string_view msg) {
            auto new_states = from_json(msg);
    
            auto& state = simulation_state::instance();
            std::scoped_lock lock { state.mtx };
            
            for (auto& route : new_states) {
                auto& old = state.routes[route.id];
                
                if (route.most_recent_msg > old.most_recent_msg) {
                    std::swap(route.crosses,       old.crosses);
                    std::swap(route.clearing_time, old.clearing_time);
                    std::swap(route.coming,        old.coming);
                    std::swap(route.waiting,       old.waiting);
                    std::swap(route.emergency,     old.emergency);
                }
            }
        }
    };
}