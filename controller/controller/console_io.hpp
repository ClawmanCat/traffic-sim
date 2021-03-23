#pragma once

#include <controller/common.hpp>

#include <iostream>
#include <mutex>
#include <sstream>


namespace ts {
    class console_io {
    public:
        template <typename T> static T in(std::string_view prompt, T default_value = T()) {
            std::lock_guard lock { mtx };
            std::cout << prompt << " (default = " << default_value << "): ";
            
            std::string input;
            std::getline(std::cin, input);
    
    
            T result = default_value;
            if constexpr (std::is_same_v<T, std::string>) {
                if (!input.empty()) result = std::move(input);
            } else {
                std::stringstream s { input };
                s >> result;
            }
            
            
            return result;
        }
    
    
        template <typename... Args> static void out(Args&&... args) {
            std::lock_guard lock { mtx };
            
            ([&](auto elem) { std::cout << elem; }(args), ...);
            std::cout << "\n";
        }
        
        
        [[noreturn]] static void type_to_exit(std::string_view prompt = "Press any key to exit", int code = 0) {
            {
                std::lock_guard lock { mtx };
                std::cout << prompt << "... ";
                std::cin.get();
            }
            
            std::exit(code);
        }
        
    private:
        static inline std::mutex mtx;
    };
}