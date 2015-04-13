.section .data
.section .text
.globl _start

 
_start: 
	pushl %ebp
	movl %esp, %ebp
	subl $120, %esp
	movl $10, %eax
	movl %eax, 16(%esp)
	movl 56(%esp), %eax
	movl %eax, 100(%esp)
	movl $2, %eax
	movl %eax, 104(%esp)
	movl 104(%esp), %eax
	imull $4, %eax
	movl %eax, 108(%esp)
	movl $100, %eax
	subl 108(%esp), %eax
	addl %esp, %eax
	movl %eax, 112(%esp)
	movl $234, %eax
	movl %eax, 116(%esp)
	movl 116(%esp), %eax
	movl 112(%esp), %ebx
	movl %eax, (%ebx)
	###################
	movl %esp, %eax
	addl $100, %eax
	pushl %eax
	###################
	call Main.HelloWorld.newmain
	addl $40, %esp
	movl %eax, 120(%esp)
	popl %ebp
	jmp exit

 
Main.HelloWorld.newmain: 
	pushl %ebp
	movl %esp, %ebp
	subl $52, %esp
	movl $1, %eax
	movl %eax, 8(%esp)
	movl 8(%esp), %eax
	imull $4, %eax
	movl %eax, 12(%esp)
	#####################
	movl 60(%esp), %eax
	subl 12(%esp), %eax
	# addl %esp, %eax
	#####################
	movl %eax, 16(%esp)
	movl $23, %eax
	movl %eax, 20(%esp)
	movl 20(%esp), %eax
	movl 16(%esp), %ebx
	movl %eax, (%ebx)
	movl $1, %eax
	movl %eax, 24(%esp)
	movl 24(%esp), %eax
	imull $4, %eax
	movl %eax, 28(%esp)
	#####################
	movl 60(%esp), %eax
	subl 28(%esp), %eax
	# addl %esp, %eax
	#####################
	movl %eax, 32(%esp)
	movl 32(%esp), %ebx
	pushl (%ebx)
	call print_int
	popl %eax
	movl $2, %eax
	movl %eax, 40(%esp)
	movl 40(%esp), %eax
	imull $4, %eax
	movl %eax, 44(%esp)
	####################
	movl 60(%esp), %eax
	subl 44(%esp), %eax
	# addl %esp, %eax
	####################
	movl %eax, 48(%esp)
	movl 48(%esp), %ebx
	pushl (%ebx)
	call print_int
	popl %eax
	popl %ebp
	jmp exit

exit:
	movl $1, %eax
	movl $0, %ebx
	int $0x80
