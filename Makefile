CXX=clang++
CXXFLAGS=-Wall -Wextra
CXXFLAGS+=-O2

TARGETS=day_15 day_23
all: $(TARGETS)

clean:
	rm -f $(TARGETS)

.phony: all clean
