.section .data
.section .text
.globl _start

 
_start: 
subl $844, %esp
movl $101, %eax
movl %eax, 4(%esp)
movl 408(%esp), %eax
movl %eax, 812(%esp)
movl $0, %eax
movl %eax, 816(%esp)
movl 816(%esp), %eax
imull $4, %eax
movl %eax, 820(%esp)
movl $812, %eax
subl 820(%esp), %eax
addl %esp, %eax
movl %eax, 824(%esp)
movl $123, %eax
movl %eax, 828(%esp)
movl 824(%esp), %ebx
movl %eax, (%ebx)
movl $0, %eax
movl %eax, 832(%esp)
movl 832(%esp), %eax
imull $4, %eax
movl %eax, 836(%esp)
movl $812, %eax
subl 836(%esp), %eax
addl %esp, %eax
movl %eax, 840(%esp)
movl 840(%esp), %eax
pushl (%eax)
call print_int
popl %eax
jmp exit
exit:
	movl $1, %eax
	movl $0, %ebx
	int $0x80
