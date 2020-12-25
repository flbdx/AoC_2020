#include <cstdlib>
#include <cstdint>
#include <cassert>

#include <iostream>
#include <string>
#include <algorithm>
#include <vector>

class Circle
{
private:
    std::vector<uint32_t> nxt;
    uint32_t cup;
    uint32_t max;
    
public:
    Circle(const std::string &line, uint32_t extend=uint32_t(-1)) :
        nxt()
      , cup(0)
      , max(0)
    {
        nxt.resize(1 + ((extend != uint32_t(-1)) ? extend : line.size()));
        max = nxt.size() - 1;
        
        auto ctoui = [](char c) -> uint32_t { return c - '0'; };
        std::vector<uint32_t> uline(line.size());
        std::transform(line.begin(), line.end(), uline.begin(), ctoui);
        
        for (size_t i = 0; i < uline.size() - 1; i++) {
            nxt[uline.at(i)] = uline.at(i+1);
        }
        
        if (extend != uint32_t(-1)) {
            nxt[uline.back()] = uline.size() + 1;
            for (size_t i = uline.size() + 1; i < extend; i++) {
                nxt[i] = i + 1;
            }
            // loop to front
            nxt[extend] = uline.front();
        }
        else {
            // loop to front
            nxt[uline.back()] = uline.front();
        }
        
        cup = ctoui(line.front());
    }
    
    void do_moves(uint32_t moves) {
        uint32_t pick0, pick1, pick2;
        uint32_t dst_cup;
        for (uint32_t move = 0; move < moves; move++) {
            pick0 = nxt[cup];
            pick1 = nxt[pick0];
            pick2 = nxt[pick1];
            
            dst_cup = (cup == 1) ? max : (cup - 1);
            while (dst_cup == pick0 || dst_cup == pick1 || dst_cup == pick2) {
                dst_cup = (dst_cup == 1) ? max : (dst_cup - 1);
            }
            nxt[cup] = nxt[pick2];
            nxt[pick2] = nxt[dst_cup];
            nxt[dst_cup] = pick0;
            cup = nxt[cup];
        }
    }
    
    std::string p1() {
        std::string ret;
        for (uint32_t c = nxt[1]; c != 1; c = nxt[c]) {
            ret += std::to_string(c);
        }
        return ret;
    }
    
    uint64_t p2() {
        return uint64_t(nxt[1]) * nxt[nxt[1]];
    }
};

int main() {
    {
        Circle test_p1("389125467");
        test_p1.do_moves(10);
        assert(test_p1.p1() == "92658374");
        test_p1.do_moves(90);
        assert(test_p1.p1() == "67384529");
    }
    {
        Circle p1("716892543");
        p1.do_moves(100);
        std::cout << p1.p1() << std::endl;
    }
    {
        Circle test_p2("389125467", 1000000);
        test_p2.do_moves(10000000);
        assert(test_p2.p2() == 149245887792);
    }
    {
        Circle p2("716892543", 1000000);
        p2.do_moves(10000000);
        std::cout << p2.p2() << std::endl;
    }
}
