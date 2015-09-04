.PHONY: clean
.SUFFIXES: .py .cpp

all: test.exe

.py.obj:
	python -m peachpy.x86_64 -mabi=ms -mimage-format=ms-coff -mcpu=default -o $@ $**

.cpp.obj:
	$(CPP) /nologo /c /EHs $(CPPFLAGS) /Fo$@ $**

test.exe: test.obj transpose4x4-ref.obj transpose4x4-opt.obj
	$(CPP) /nologo /Fo$@ $**

clean:
	-rm -f transpose4x4-opt.obj transpose4x4-ref.obj test.obj test.exe
