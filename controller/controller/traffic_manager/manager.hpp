#pragma once

#include <controller/common.hpp>
#include <controller/console_io.hpp>
#include <controller/traffic_manager/strategy/strategy.hpp>
#include <controller/traffic_manager/strategy/test_strategy.hpp>
#include <controller/traffic_manager/strategy/accumulative_priority_strategy.hpp>
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
            // Wait for the simulation to initialize the state.
            connection::instance().await_init_message();
            auto strategy = strategy_fn();
            
            while (true) {
                last_update = steady_clock::now();
                
                if (!simulation_state::instance().empty()) {
                    auto changes = strategy->update();
                    if (!changes.empty()) console_io::out("Changed ", changes.size(), " lights.");
    
                    for (auto&& change : changes) {
                        auto old_state = simulation_state::instance().view()->find(change.id)->second.state;
                        auto new_state = change.state;
                        
                        console_io::out("Light ", change.id, ": ", light_state_to_string(old_state), " => ", light_state_to_string(new_state));
                        simulation_state::instance().update(std::move(change));
                    }
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
                { "Testing",         []() { return (strategy_t) std::make_unique<strategy_test>(); } },
                { "Accum. Priority", []() { return (strategy_t) std::make_unique<strategy_accumulative_priority>(); } }
            };
            
            
            auto strategy_names = strategies
                | views::keys
                | views::enumerate
                | views::transform([](const auto& pair) { return "[Strategy "s + std::to_string(pair.first) + "]: " + pair.second; })
                | to<std::vector>;
            
            // Joining the result of the transform isn't allowed for some reason, so use an intermediary container.
            auto strategy_string = strategy_names | views::join('\n') | to<std::string>;
            
            
            console_io::out("Please pick a strategy:\n" + strategy_string);
            
            unsigned strategy_type = max_value<unsigned>;
            while (strategy_type >= strategies.size()) {
                strategy_type = console_io::in<unsigned>("Choice", 0);
            }
            
            strategy_fn = strategies[strategy_type].second;
            
            
            unsigned ms = console_io::in<unsigned>("Please pick an update interval in milliseconds", 1000);
            interval = milliseconds(ms);
        }
        
        
        producer_t strategy_fn;
        milliseconds interval;
        steady_clock::time_point last_update = epoch;
    };
}