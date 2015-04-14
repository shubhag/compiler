.section .data
.section .text
.globl _start

 
_start: 
pushl %ebp
movl %esp, %ebp
subl $60, %esp
movl 20(%esp), %eax
movl %eax, 28(%esp)
movl $28, %eax
subl $8, %eax
addl %esp, %eax
movl %eax, 32(%esp)
movl $1, %eax
movl %eax, 36(%esp)
movl 36(%esp), %eax
movl 32(%esp), %ebx
movl %eax, (%ebx)
movl $28, %eax
subl $8, %eax
addl %esp, %eax
movl %eax, 40(%esp)
movl $4, %eax
movl %eax, 44(%esp)
movl 40(%esp), %ebx
movl (%ebx), %eax
addl 44(%esp), %eax
movl %eax, 48(%esp)
movl 48(%esp), %eax
movl %eax, 12(%esp)
movl $100, %eax
movl %eax, 52(%esp)
movl 52(%esp), %eax
movl %eax, 8(%esp)
movl %esp, %eax
addl $28, %eax
pushl %eax
pushl 12(%esp)
pushl 20(%esp)
call Main.employee.hello
addl $12, %esp
movl %eax, 56(%esp)
movl 56(%esp), %eax
movl %eax, 8(%esp)
pushl 8(%esp)
call print_int
addl $4, %esp
popl %ebp
jmp exit

 
Main.employee.hello: 
pushl %ebp
movl %esp, %ebp
subl $24, %esp
movl 40(%esp), %eax
subl $4, %eax
movl %eax, 12(%esp)
movl 36(%esp), %eax
movl 12(%esp), %ebx
movl %eax, (%ebx)
movl 40(%esp), %eax
subl $4, %eax
movl %eax, 20(%esp)
movl 20(%esp), %eax
movl (%eax), %eax
addl $24, %esp
popl %ebp
ret 
popl %ebp
jmp exit
exit:
	movl $1, %eax
	movl $0, %ebx
	int $0x80
