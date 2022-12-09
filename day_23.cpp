#include <cstdlib>
#include <cstdint>
#include <cassert>

#include <iostream>
#include <fstream>
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
            
//             dst_cup = (cup == 1) ? max : (cup - 1);
            (dst_cup = (cup - 1)) ? : (dst_cup = max);
            while ((dst_cup == pick0) || dst_cup == pick1 || dst_cup == pick2) {
                // g++ won't optimize this expression
                // should be a sub and cmove
                // clang++ wins by ko
//                 dst_cup = (dst_cup == 1) ? max : (dst_cup - 1);
                (--dst_cup) ? : (dst_cup = max); 
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
        Circle test("389125467");
        test.do_moves(10);
        assert(test.p1() == "92658374");
        test.do_moves(90);
        assert(test.p1() == "67384529");
        
        test = Circle("389125467", 1000000);
        test.do_moves(10000000);
        assert(test.p2() == 149245887792);
    }
    {
        std::ifstream input("input_23");
        if (!input.is_open()) {
            return 1;
        }
        std::string line;
        std::getline(input, line);
        input.close();
    
        Circle work(line);
        work.do_moves(100);
        std::cout << work.p1() << std::endl;
        
        work = Circle(line, 1000000);
        work.do_moves(10000000);
        std::cout << work.p2() << std::endl;
    }
}
