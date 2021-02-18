#pragma once


namespace traffic {
    class websockets_connection;
    
    namespace tests {
        websockets_connection& get_mock_connection();
    }
};


#define ws_mock_insert return tests::get_mock_connection();
#include <controller/communication.hpp>


namespace traffic::tests {
    class mock_connection : public websockets_connection {
    public:
        mock_connection(void) : websockets_connection() {
            // Hardcoded state. Should produce two intersections.
            remote_crossings = {
                crossing { .id = 0, .crosses = { 2, 3 }, .clearing_time = 5.0f },
                crossing { .id = 1, .crosses = { 2, 3 }, .clearing_time = 5.0f },
                crossing { .id = 2, .crosses = { 0, 1 }, .clearing_time = 3.0f },
                crossing { .id = 3, .crosses = { 0, 1 }, .clearing_time = 3.0f },
                crossing { .id = 4, .crosses = { 6, 7 }, .clearing_time = 5.0f },
                crossing { .id = 5, .crosses = { 6    }, .clearing_time = 5.0f },
                crossing { .id = 6, .crosses = { 4, 5 }, .clearing_time = 9.5f },
                crossing { .id = 7, .crosses = { 4    }, .clearing_time = 9.5f }
            };
            
            // Base constructor will call non-overridden method.
            get_remote_state();
        }
        
    protected:
        void get_remote_state(void) override {
            state = remote_crossings;
        }
    
        void set_remote_state(void) override {
            remote_crossings = state;
        }
        
    private:
        std::unordered_set<crossing> remote_crossings;
    };
    
    
    inline websockets_connection& get_mock_connection(void) {
        static mock_connection conn { };
        return conn;
    }
}