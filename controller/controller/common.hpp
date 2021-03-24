#pragma once

#include <range/v3/all.hpp>

#include <unordered_map>
#include <unordered_set>
#include <vector>
#include <chrono>
#include <string>
#include <string_view>
#include <optional>
#include <compare>
#include <memory>
#include <limits>
#include <functional>
#include <type_traits>


namespace ts {
    using namespace ranges;
    
    using namespace std::chrono;
    using namespace std::chrono_literals;
    
    using namespace std::string_literals;
    using namespace std::string_view_literals;
    
    
    template <typename T> constexpr inline T min_value = std::numeric_limits<T>::lowest();
    template <typename T> constexpr inline T max_value = std::numeric_limits<T>::max();
    
    template <typename Ret, typename... Args> using fn = Ret(*)(Args...);
    
    
    const inline steady_clock::time_point epoch = [](){
        auto now = steady_clock::now();
        return now - now.time_since_epoch();
    }();
    
    
    inline milliseconds time_since(steady_clock::time_point time) {
        return duration_cast<milliseconds>(steady_clock::now() - time);
    }
}