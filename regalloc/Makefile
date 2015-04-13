all:
	as code.s -32 -o code.o
	as print_int.s -32 -o print_int.o
	ld code.o print_int.o -m elf_i386 -o code_print
	./code_print

clean:
	rm *.o code_print