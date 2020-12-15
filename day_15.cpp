#include <cstdlib>
#include <cstdint>
#include <cassert>

#include <iostream>
#include <fstream>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

static constexpr uint32_t nope(-1);
class P : public std::pair<uint32_t, uint32_t>
{
public:
    typedef std::pair<uint32_t, uint32_t> T;
    P() : T(nope, nope) {}
};

uint32_t work_p1(const std::string &line, uint32_t target=2020) {
    std::vector<uint32_t> start_sequence;
    {
        const char *p = line.c_str();
        const char *e = p + line.size();
        char *endp;
        while (true) {
            uint32_t v = std::strtoul(p, &endp, 10);
            if (endp == p) {
                return uint32_t(-1);
            }
            start_sequence.push_back(v);
            if (endp == e) {
                break;
            }
            else {
                p = endp + 1;
            }
        }
    }
    
    std::unordered_map<uint32_t, P> positions;
    positions.reserve(target / 3);
    uint32_t last_one;
    
    uint32_t n = 0;
    for (uint32_t i : start_sequence) {
        n += 1;
        auto &p = positions[i];
        p.first = p.second;
        p.second = n;
        last_one = i;
    }
    
    auto *p = &(positions[last_one]);
    while (n != target) {
        n += 1;
        if (p->first == nope) {
            last_one = 0;
        }
        else {
            last_one = p->second - p->first;
        }
        p = &(positions[last_one]);
        p->first = p->second;
        p->second = n;
    }
    
    return last_one;
}

int main() {
    std::ifstream input("input_15");
    if (!input.is_open()) {
        return 1;
    }
    std::string line;
    std::getline(input, line);
    input.close();
    
    assert(work_p1("0,3,6") == 436);
    std::cout << work_p1(line) << std::endl;
    
    std::cout << work_p1(line, 30000000) << std::endl;
    
}
