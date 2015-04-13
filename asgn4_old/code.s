.section .data
.section .text
.globl _start

 
_start: 
pushl %ebp
movl %esp, %ebp
subl $64, %esp
movl $30, %eax
movl %eax, 8(%esp)
movl 8(%esp), %eax
movl %eax, 12(%esp)
movl $10, %eax
movl %eax, 16(%esp)
movl 16(%esp), %eax
movl %eax, 20(%esp)
movl $30, %eax
movl %eax, 24(%esp)
movl $1, %eax
movl %eax, 28(%esp)
movl 12(%esp), %eax
cmpl 24(%esp), %eax
je Label1
movl $0, %eax
movl %eax, 28(%esp)
Label1: 
movl 28(%esp), %eax
cmpl $1, %eax
je LabelGoto0
jmp LabelGoto1
LabelGoto0: 
movl $10, %eax
movl %eax, 32(%esp)
movl $1, %eax
movl %eax, 36(%esp)
movl 20(%esp), %eax
cmpl 32(%esp), %eax
je Label2
movl $0, %eax
movl %eax, 36(%esp)
Label2: 
movl 36(%esp), %eax
cmpl $1, %eax
je LabelGoto1
jmp LabelGoto1
LabelGoto1: 
movl $30, %eax
movl %eax, 40(%esp)
movl 40(%esp), %eax
movl %eax, 12(%esp)
movl $20, %eax
movl %eax, 44(%esp)
movl $1, %eax
movl %eax, 48(%esp)
movl 12(%esp), %eax
cmpl 44(%esp), %eax
jg Label3
movl $0, %eax
movl %eax, 48(%esp)
Label3: 
movl 48(%esp), %eax
cmpl $1, %eax
je LabelGoto2
jmp LabelGoto3
LabelGoto2: 
jmp LabelGoto3
LabelGoto3: 
movl $1, %eax
movl %eax, 56(%esp)
movl 12(%esp), %eax
cmpl 20(%esp), %eax
jg Label4
movl $0, %eax
movl %eax, 56(%esp)
Label4: 
movl 56(%esp), %eax
cmpl $1, %eax
je LabelGoto4
jmp LabelGoto5
LabelGoto4: 
movl 12(%esp), %eax
movl %eax, 60(%esp)
jmp LabelGoto6
LabelGoto5: 
movl 20(%esp), %eax
movl %eax, 60(%esp)
LabelGoto6: 
movl 60(%esp), %eax
movl %eax, 52(%esp)
pushl 52(%esp)
call print_int
popl %eax
popl %ebp
jmp exit
exit:
	movl $1, %eax
	movl $0, %ebx
	int $0x80
