.section .data
_t1:
	.ascii "HelloWorld\n"
.section .text
.globl _start

 
_start: 
pushl %ebp
movl %esp, %ebp
subl $24, %esp
movl $8, %eax
movl %eax, 16(%esp)
movl 16(%esp), %eax
movl %eax, 36(%esp)
movl 36(%esp), %eax
movl %eax, 32(%esp)
movl $(_t1), %eax
movl %eax, 20(%esp)
pushl 20(%esp)
pushl $11
call print_string
addl $8, %esp
popl %ebp
jmp exit
exit:
	movl $1, %eax
	movl $0, %ebx
	int $0x80
