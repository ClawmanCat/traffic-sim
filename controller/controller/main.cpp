#include <controller/controller_generator.hpp>
#include <controller/strategy/strategy_timewise_urgency.hpp>

#include <iostream>
#include <thread>


int main(int argc, char** argv) {
    std::cout << "Traffic Controller -- Version "
              << TRAFFICCONTROLLER_VERSION_MAJOR << "."
              << TRAFFICCONTROLLER_VERSION_MINOR << "."
              << TRAFFICCONTROLLER_VERSION_PATCH << "\n";
    
    std::cout << "Project Group 5 -- Rob Klein Ikink & Dante Klijn\n\n";
    
    
    // Construct a controller for each intersection.
    auto controllers = traffic::controller_generator::generate_controllers(
        traffic::strategy_timewise_urgency { }
    );
    
    // Launch each controller on a separate thread.
    std::vector<std::thread> threads;
    for (auto&& controller : controllers) {
        threads.emplace_back(std::thread {
            [controller = std::move(controller)]() mutable { controller.main(); }
        });
    }
    
    // Prevent the program from exiting until all controllers have exited.
    // Note: controllers currently have no exit condition. They will run until the program is closed.
    for (auto& thread : threads) thread.join();
}