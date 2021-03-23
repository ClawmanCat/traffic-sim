#pragma once

#include <controller/common.hpp>
#include <controller/communication/state.hpp>
#include <controller/console_io.hpp>

#include <boost/json.hpp>
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
            ws.send("Hello this is controller");
            
            /*auto& state = simulation_state::instance();
            std::scoped_lock lock { mtx, state.mtx };
            
            if (!connected) return;
            
            unsigned count = 0;
            for (auto& change : state.changes | views::indirect) {
                ws.send("Change light "s + std::to_string(count++));
            }
            
            state.changes.clear();*/
        }
    private:
        std::mutex mtx;
        ix::WebSocket ws;
        bool connected = false;
        
        
        connection(void) {
            std::lock_guard lock { mtx };
            
            ix::initNetSystem();
            
            auto url = console_io::in<std::string>("Please enter a URL to connect to", "wss://127.0.0.1:80");
            ws.setUrl(url);
            
            console_io::out("Connecting to ", url, "...");
            
            ws.setOnMessageCallback([this](const ix::WebSocketMessagePtr& msg) {
                if (msg->type == ix::WebSocketMessageType::Open) {
                    console_io::out("Connection established.");
                    
                    std::lock_guard lock { mtx };
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
            console_io::out("Received message: ", msg);
        }
    };
}