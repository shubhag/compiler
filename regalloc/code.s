.section .data
.section .text
.globl _start

 
_start: 
pushl %ebp
movl %esp, %ebp
subl $156, %esp
movl $10, %eax
movl %eax, 16(%esp)
movl 56(%esp), %eax
movl %eax, 100(%esp)
movl $0, %eax
movl %eax, 104(%esp)
movl 104(%esp), %eax
imull $4, %eax
movl %eax, 108(%esp)
movl $100, %eax
subl 108(%esp), %eax
addl %esp, %eax
movl %eax, 112(%esp)
movl $11, %eax
movl %eax, 116(%esp)
movl 116(%esp), %eax
movl 112(%esp), %ebx
movl %eax, (%ebx)
movl $10, %eax
movl %eax, 120(%esp)
movl 120(%esp), %eax
movl %eax, 168(%esp)
movl $1111, %eax
movl %eax, 124(%esp)
movl 124(%esp), %eax
movl %eax, 164(%esp)
movl $1100, %eax
movl %eax, 128(%esp)
movl 128(%esp), %eax
movl %eax, 132(%esp)
movl %esp, %eax
addl $100, %eax
pushl %eax
pushl 168(%esp)
pushl 140(%esp)
call Main.HelloWorld.newmain
addl $12, %esp
movl %eax, 136(%esp)
movl 136(%esp), %eax
movl %eax, 168(%esp)
pushl 168(%esp)
call print_int
popl %eax
movl $0, %eax
movl %eax, 144(%esp)
movl 144(%esp), %eax
imull $4, %eax
movl %eax, 148(%esp)
movl $100, %eax
subl 148(%esp), %eax
addl %esp, %eax
movl %eax, 152(%esp)
movl 152(%esp), %ebx
pushl (%ebx)
call print_int
popl %eax
popl %ebp
jmp exit

 
Main.HelloWorld.newmain: 
pushl %ebp
movl %esp, %ebp
subl $52, %esp
pushl 60(%esp)
call print_int
popl %eax
movl $9, %eax
movl %eax, 20(%esp)
movl 20(%esp), %eax
movl %eax, 64(%esp)
movl $0, %eax
movl %eax, 24(%esp)
movl 24(%esp), %eax
imull $4, %eax
movl %eax, 28(%esp)
movl 68(%esp), %eax
subl 28(%esp), %eax
movl %eax, 32(%esp)
movl $7, %eax
movl %eax, 36(%esp)
movl 36(%esp), %eax
movl 32(%esp), %ebx
movl %eax, (%ebx)
movl $0, %eax
movl %eax, 40(%esp)
movl 40(%esp), %eax
imull $4, %eax
movl %eax, 44(%esp)
movl 68(%esp), %eax
subl 44(%esp), %eax
movl %eax, 48(%esp)
movl 48(%esp), %ebx
pushl (%ebx)
call print_int
popl %eax
movl 64(%esp), %eax
addl $52, %esp
popl %ebp
ret 
popl %ebp
jmp exit
exit:
	movl $1, %eax
	movl $0, %ebx
	int $0x80
