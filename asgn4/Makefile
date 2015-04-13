all:
	as code.s -32 -o code.o
	as print_int.s -32 -o print_int.o
	as print_string.s -32 -o print_string.o
	ld code.o print_int.o print_string.o -m elf_i386 -o code_print
	./code_print

clean:
	rm *.o code_print