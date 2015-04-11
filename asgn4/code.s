.section .data
.section .text
.globl _start
_start: 
subl $36, %esp
movl $5, %eax
movl %eax, 12(%esp)
movl $3, %eax
movl %eax, 16(%esp)
movl 12(%esp), %eax
divl 16(%esp)
movl %edx, 20(%esp)
movl 20(%esp), %eax
movl %eax, 8(%esp)
movl $5, %eax
movl %eax, 24(%esp)
movl $5, %eax
movl %eax, 28(%esp)
movl $1, %eax
movl %eax, 32(%esp)
movl 24(%esp), %eax
cmpl 28(%esp), %eax
jne Label1
movl $0, %eax
movl %eax, 32(%esp)
Label1: 
movl 32(%esp), %eax
cmpl $1, %eax
je LabelGoto0
jmp LabelGoto1
LabelGoto0: 
movl $1, %eax
movl %eax, 36(%esp)
movl 36(%esp), %eax
movl %eax, 8(%esp)
LabelGoto1: 
pushl 8(%esp)
call print_int
popl %eax
exit:
	movl $1, %eax
	movl $0, %ebx
	int $0x80
