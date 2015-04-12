.section .data
.section .text
.globl _start

 
_start: 
pushl %ebp
movl %esp, %ebp
subl $36, %esp
movl $10, %eax
movl %eax, 16(%esp)
movl 16(%esp), %eax
movl %eax, 48(%esp)
movl $1111, %eax
movl %eax, 20(%esp)
movl 20(%esp), %eax
movl %eax, 44(%esp)
movl $2, %eax
movl %eax, 24(%esp)
movl 24(%esp), %eax
movl %eax, 28(%esp)
pushl 48(%esp)
pushl 44(%esp)
pushl 28(%esp)
call Main.HelloWorld.newmain
addl $12, %esp
movl %eax, 32(%esp)
movl 32(%esp), %eax
movl %eax, 48(%esp)
pushl 48(%esp)
call print_int
popl %eax
popl %ebp
jmp exit

 
Main.HelloWorld.newmain: 
pushl %ebp
movl %esp, %ebp
subl $20, %esp
pushl 28(%esp)
call print_int
popl %eax
movl $1, %eax
movl %eax, 20(%esp)
movl 20(%esp), %eax
movl %eax, 32(%esp)
movl 32(%esp), %eax
addl $20, %esp
popl %ebp
ret 
popl %ebp
jmp exit
exit:
	movl $1, %eax
	movl $0, %ebx
	int $0x80
