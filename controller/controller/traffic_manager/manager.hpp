#pragma once

#include <controller/common.hpp>
#include <controller/console_io.hpp>
#include <controller/traffic_manager/strategy/strategy.hpp>
#include <controller/traffic_manager/strategy/round_robin.hpp>
#include <controller/communication/state.hpp>
#include <controller/communication/connection.hpp>


namespace ts {
    class traffic_manager {
    public:
        [[nodiscard]] static traffic_manager& instance(void) {
            static traffic_manager i;
            return i;
        }
        
        
        [[noreturn]] void main(void) {
            while (true) {
                last_update = steady_clock::now();
                
                auto changed_states = strategy->update();
                for (auto&& state : changed_states) {
                    simulation_state::instance().update(std::move(state));
                }
    
                connection::instance().transmit_changes();
                std::this_thread::sleep_until(last_update + interval);
            }
        }
    private:
        using strategy_t = std::unique_ptr<traffic_strategy>;
        using producer_t = fn<strategy_t>;
        
        traffic_manager(void) {
            std::vector<std::pair<std::string, producer_t>> strategies {
                { "Round Robin", []() { return (strategy_t) std::make_unique<strategy_round_robin>(); } }
            };
            
            
            auto strategy_names = strategies
                | views::keys
                | views::enumerate
                | views::transform([](const auto& pair) { return "[Strategy "s + std::to_string(pair.first) + "]: " + pair.second; })
                | to<std::vector>;
            
            // Joining the result of the transform isn't allowed for some reason, so use an intermediary container.
            auto strategy_string = strategy_names | views::join('\n') | to<std::string>;
            
            
            console_io::out("Please pick a strategy:\n" + strategy_string);
            unsigned strategy_type = console_io::in<unsigned>("Choice", 0);
            strategy = strategies[strategy_type].second();
            
            
            unsigned ms = console_io::in<unsigned>("Please pick an update interval in milliseconds", 1000);
            interval = milliseconds(ms);
        }
        
        
        std::unique_ptr<traffic_strategy> strategy;
        milliseconds interval;
        steady_clock::time_point last_update = epoch;
    };
}