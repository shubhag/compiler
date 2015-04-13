.section .data
.section .text
.globl _start

 
_start: 
pushl %ebp
movl %esp, %ebp
subl $28, %esp
movl $10, %eax
movl %eax, 8(%esp)
movl 8(%esp), %eax
movl %eax, 12(%esp)
movl $5, %eax
movl %eax, 16(%esp)
movl 12(%esp), %eax
addl 16(%esp), %eax
movl %eax, 20(%esp)
movl 20(%esp), %eax
movl %eax, 24(%esp)
pushl 24(%esp)
call print_int
popl %eax
popl %ebp
jmp exit
exit:
	movl $1, %eax
	movl $0, %ebx
	int $0x80
