#pragma once

#include <controller/utility.hpp>
#include <controller/crossing.hpp>

#include <range/v3/view/filter.hpp>

#include <unordered_set>
#include <algorithm>
#include <mutex>


namespace traffic {
    // Actual WebSockets connection.
    class websockets_connection {
    public:
        constexpr static inline milliseconds min_request_delay = 200ms;
        
        
        static websockets_connection& instance(void) {
            static websockets_connection i { };
            
            #ifdef ws_mock_insert
                ws_mock_insert
            #endif
            
            return i;
        }
        
        
        std::unordered_set<crossing> get_client_state(void) {
            std::lock_guard lock { mtx };
            return state;
        }
        
        
        void set_client_state(const std::unordered_set<crossing>& state) {
            std::lock_guard lock { mtx };
            
            for (const auto& elem : state) {
                if (auto it = this->state.find(elem); it != this->state.end()) {
                    auto old_elem = this->state.extract(elem).value();
                    this->state.insert(elem);
                    
                    if (old_elem.state != elem.state) client_outdated = true;
                }
            }
            
            update();
        }
    
        
        void update(void) {
            std::lock_guard lock { mtx };
            
            if (client_outdated && milliseconds_since(last_update) > min_request_delay.count()) {
                set_remote_state();
                client_outdated = false;
            }
        }
    
    protected:
        websockets_connection(void) {
            get_remote_state();
        }
        
    
        std::unordered_set<crossing> state;
        bool client_outdated = false;
        time_point last_update = clock::now();
        std::recursive_mutex mtx;
        
        
        // Virtual & protected for testing purposes.
        virtual void get_remote_state(void) {
            // Fetch client state.
        }
        
        virtual void set_remote_state(void) {
            // Set client state.
        }
    };
    
    
    
    // Provides a view over a subsection of the actual state of the socket connection.
    // Can be used as the connection for a controller, making it appear as if only a subsection of the crossings exist.
    class intersection_connection {
    public:
        intersection_connection(std::vector<id_type>&& associated_crossings) : crossings(std::move(associated_crossings)) {}
        
        
        std::unordered_set<crossing> get_client_state(void) {
            auto state = websockets_connection::instance().get_client_state();
            
            return state
                | views::filter([&](const crossing& cross) { return contains(crossings, cross.id); })
                | to<std::unordered_set>;
        }
        
        
        void set_client_state(const std::unordered_set<crossing>& state) {
            websockets_connection::instance().set_client_state(state);
        }
    private:
        std::vector<id_type> crossings;
    };
}