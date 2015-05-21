all: test
.PHONY: clean

OSNAME := $(shell uname -s)
ifeq ($(OSNAME),Darwin)
    PEACHPY_IMAGE_FORMAT=mach-o
else
    PEACHPY_IMAGE_FORMAT=elf
endif

matmul-opt.o: matmul-opt.py
	python -m peachpy.x86_64 -mabi=sysv -mimage-format=$(PEACHPY_IMAGE_FORMAT) -mcpu=default -o $@ $<

matmul-ref.o: matmul-ref.c
	$(CC) -m64 -std=gnu99 $(CFLAGS) -o $@ -c $<

test.o: test.c
	$(CC) -m64 -std=gnu99 $(CFLAGS) -o $@ -c $<

test: test.o matmul-ref.o matmul-opt.o
	$(CC) -m64 -g $^ -o $@

clean:
	-rm -f matmul-opt.o matmul-ref.o test.o test
