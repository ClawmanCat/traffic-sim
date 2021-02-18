#pragma once

#include <boost/preprocessor.hpp>
#include <boost/container_hash/hash.hpp>
#include <range/v3/range.hpp>
#include <range/v3/view.hpp>
#include <range/v3/action.hpp>

#include <cstddef>
#include <cstdint>
#include <memory>
#include <limits>
#include <string_view>
#include <exception>
#include <iostream>
#include <algorithm>
#include <chrono>
#include <mutex>


// Given an object, gets a field from that object.
#define get_field(x) [](const auto& v) { return v.x; }

// Returns a comparator to compare objects on the given field.
#define compare_on(x) [](const auto& a, const auto& b) { return a.x < b.x; }

// Given a name and a function, returns a comparator which compares fn(obj).
#define compare_fn(name, fn)                        \
[&](const auto& a, const auto& b) {                 \
    auto tf = [&](const auto& name) { return fn; }; \
    return tf(a) < tf(b);                           \
}


#define IMPL_NEQ_RETURN(Rep, Data, Elem) if (Elem != o.Elem) return false;

// Makes the given class equality comparable on the given fields.
#define eq_comparable_fields(cls, ...)                                  \
[[nodiscard]] bool operator==(const cls& o) const {                     \
    BOOST_PP_SEQ_FOR_EACH(                                              \
        IMPL_NEQ_RETURN,                                                \
        _,                                                              \
        BOOST_PP_VARIADIC_TO_SEQ(__VA_ARGS__)                           \
    );                                                                  \
                                                                        \
    return true;                                                        \
}


#define IMPL_HASH_COMBINE(Rep, Data, Elem) boost::hash_combine(seed, this->Elem);

// Makes the current class hashable on the given fields.
#define hashable(...)                                   \
[[nodiscard]] std::size_t hash(void) const {            \
    std::size_t seed = 0;                               \
                                                        \
    BOOST_PP_SEQ_FOR_EACH(                              \
        IMPL_HASH_COMBINE,                              \
        _,                                              \
        BOOST_PP_VARIADIC_TO_SEQ(__VA_ARGS__)           \
    );                                                  \
                                                        \
    return seed;                                        \
}


// Allow overloading the hash operator from within the class so we can use hashable
// where out-of-class definitions are not possible.
template <typename T> requires requires (T t, std::size_t h) { h = t.hash(); }
struct std::hash<T> {
    std::size_t operator()(const T& val) const {
        return val.hash();
    }
};


namespace traffic {
    using u8  =  uint8_t;
    using i8  =   int8_t;
    using u16 = uint16_t;
    using i16 =  int16_t;
    using u32 = uint32_t;
    using i32 =  int32_t;
    using u64 = uint64_t;
    using i64 =  int64_t;
    
    using f32 = float;
    using f64 = double;
    
    
    template <typename T> constexpr T min_value = std::numeric_limits<T>::lowest();
    template <typename T> constexpr T max_value = std::numeric_limits<T>::max();
    template <typename T> constexpr T infinity  = std::numeric_limits<T>::infinity();
    
    
    template <typename Ret, typename... Args>
    using Fn = Ret(*)(Args...);
    
    template <typename Class, typename Ret, typename... Args>
    using MemFn = Ret(Class::*)(Args...);
    
    template <typename Class, typename Ret, typename... Args>
    using ConstMemFn = Ret(Class::*)(Args...) const;
    
    template <typename Class, typename T>
    using MemVar = T(Class::*);
    
    template <typename T, std::size_t N>
    using ArrayRef = T(&)[N];
    
    
    template <typename T, typename Deleter = std::default_delete<T>>
    using unique = std::unique_ptr<T>;
    
    template <typename T> using shared = std::shared_ptr<T>;
    template <typename T> using weak   = std::weak_ptr<T>;
    
    
    using namespace std::chrono;
    using namespace std::chrono_literals;
    
    using clock      = std::chrono::steady_clock;
    using time_point = clock::time_point;
    using duration   = clock::duration;
    
    
    using namespace ranges;
    
    
    template <typename Set>
    inline bool sets_equal(const Set& a, const Set& b) {
        if (a.size() != b.size()) return false;
        
        for (const auto& elem : a) {
            if (!b.contains(elem)) return false;
        }
        
        return true;
    }
    
    
    template <typename Ctr, typename Val>
    inline bool contains(const Ctr& ctr, const Val& value) {
        return std::find(
            ctr.begin(),
            ctr.end(),
            value
        ) != ctr.end();
    }
    
    
    template <typename Ctr, typename Pred>
    inline bool contains_such(const Ctr& ctr, Pred pred) {
        return std::find_if(
            ctr.begin(),
            ctr.end(),
            pred
        ) != ctr.end();
    }
    
    
    inline float milliseconds_since(const time_point& when) {
        return duration_cast<milliseconds>(clock::now() - when).count();
    }
    
    
    class controller_logger {
        template <typename... Ts> constexpr static bool streamable
            = requires (std::ostream s, Ts... ts) { ((s << ts), ...); };
    public:
        controller_logger(u32 id) : id(id) {}
        
        
        template <typename... Ts> requires streamable<Ts...>
        void log(const Ts&... message) {
            std::lock_guard lock { mtx };
            
            std::cout << "[Controller " << id << "] ";
            ((std::cout << message), ...);
            std::cout << "\n";
            
            std::cout.flush();
        }
    
    
        template <typename... Ts> requires streamable<Ts...>
        void core_assert(bool condition, const Ts&... message) {
            if (!condition) [[unlikely]] {
                std::lock_guard lock { mtx };
                
                std::cout << "A fatal error occurred:\n";
                ((std::cout << message), ...);
                std::cout << "\n\n";
        
                std::cout << "Press any key to exit... ";
                std::cin.get();
        
                std::exit(-1);
            }
        }
        
    private:
        static inline std::mutex mtx;
        u32 id;
    };
}