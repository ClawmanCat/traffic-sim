#pragma once

#include <controller/common.hpp>


namespace ts {
    using route_id = signed int;
    
    struct route_state {
        route_id id;
        enum class light_state { GREEN, ORANGE, RED_BLOCKING, RED_SAFE } state;
        std::vector<route_id> crosses;
        milliseconds clearing_time;
        bool waiting = false, coming = false, emergency = false;
        int most_recent_msg = min_value<int>;
        
        
        [[nodiscard]] constexpr auto operator<=>(const route_state& o) const {
            if (auto cmp = id <=> o.id; cmp != 0) return cmp;
            return state <=> o.state;
        }
        
        [[nodiscard]] constexpr bool operator==(const route_state& o) const {
            return ((*this) <=> o) == 0;
        }
    
        [[nodiscard]] constexpr bool operator!=(const route_state& o) const {
            return ((*this) <=> o) != 0;
        }
    };
    
    
    inline route_state::light_state& operator++(route_state::light_state& s) {
        s = (s == route_state::light_state::RED_SAFE)
            ? route_state::light_state::GREEN
            : (route_state::light_state) (((int) s) + 1);
            
        return s;
    }
    
    
    inline std::string_view light_state_to_string(route_state::light_state s) {
        using ls = route_state::light_state;
        
        switch (s) {
            case ls::GREEN:         return "green";
            case ls::ORANGE:        return "orange";
            case ls::RED_BLOCKING:  [[fallthrough]];
            case ls::RED_SAFE:      return "red";
        }
    }
    
    
    class simulation_state {
    public:
        [[nodiscard]] static simulation_state& instance(void) {
            static simulation_state i;
            return i;
        }
        
        
        void update(route_state&& value) {
            std::lock_guard lock { mtx };
            
            auto id = value.id;
            auto [it, inserted] = routes.insert_or_assign(id, std::move(value));
            auto& route = it->second;
            
            auto changed_it = std::find_if(
                changes.begin(),
                changes.end(),
                [&](const auto* rs) { return rs->id == id; }
            );
            
            if (changed_it == changes.end()) {
                changes.push_back(&route);
            } else {
                (*changed_it) = &route;
            }
        }
        
        
        [[nodiscard]] auto view(void) const {
            return owning_view { };
        }
        
        
        template <typename Pred> void foreach(const Pred& pred) {
            std::lock_guard lock { mtx };
            for (auto& [k, v] : routes) pred(k, v);
        }
    
    
        template <typename Pred> void foreach(const Pred& pred) const {
            std::lock_guard lock { mtx };
            for (const auto& [k, v] : routes) pred(k, v);
        }
        
        
        bool empty(void) const {
            return routes.empty();
        }
    private:
        friend class connection;
        friend struct owning_view;
        
        simulation_state(void) = default;
        
        std::unordered_map<route_id, route_state> routes;
        std::vector<route_state*> changes;
        std::recursive_mutex mtx;
    
    
        struct owning_view {
            using value_type = const decltype(routes);
            
            [[nodiscard]] value_type* operator->(void) const { return &simulation_state::instance().routes; }
            [[nodiscard]] value_type& operator*(void) const { return simulation_state::instance().routes; }
            
            std::unique_lock<std::recursive_mutex> lock { simulation_state::instance().mtx };
        };
    };
}