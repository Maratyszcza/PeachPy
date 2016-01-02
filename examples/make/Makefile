all: test
.PHONY: clean

PEACHPY_SOURCES = matmul-opt.py
C_SOURCES = matmul-ref.c test.c
OBJECTS = $(PEACHPY_SOURCES:.py=.o) $(C_SOURCES:.c=.o)
DEPENDENCIES = $(PEACHPY_SOURCES:.py=.d) $(C_SOURCES:.c=.d)

-include $(DEPENDENCIES)

%.o: %.py
	python -m peachpy.x86_64 -MMD -MF $(<:.py=.d) -o $(@:.py=.o) $<

%.o: %.c
	$(CC) -m64 -std=gnu99 $(CFLAGS) -MMD -MF $(<:.c=.d) -o $(@:.c=.o) -c $<

test: $(OBJECTS)
	$(CC) -m64 -g $(LDFLAGS) $^ -o $@ $(LDLIBS)

clean:
	-rm -f $(OBJECTS) $(DEPENDENCIES) test
