.section .data
_t4:
	.ascii "Only 1 fruit\n"
_t8:
	.ascii "Two fruits\n"
_t12:
	.ascii "Three fruits\n"
_t16:
	.ascii "Four fruits\n"
_t20:
	.ascii "Great! Five fruits\n"
_t22:
	.ascii "Not sure how many fruits are there\n"
.section .text
.globl _start

 
_start: 
pushl %ebp
movl %esp, %ebp
subl $100, %esp
movl $6, %eax
movl %eax, 8(%esp)
movl 8(%esp), %eax
movl %eax, 12(%esp)
movl $1, %eax
movl %eax, 16(%esp)
movl $1, %eax
movl %eax, 20(%esp)
movl 12(%esp), %eax
cmpl 16(%esp), %eax
jne Label1
movl $0, %eax
movl %eax, 20(%esp)
Label1: 
movl 20(%esp), %eax
cmpl $1, %eax
je LabelGoto0
movl $(_t4), %eax
movl %eax, 24(%esp)
pushl 24(%esp)
pushl $13
call print_string
addl $8, %esp
jmp LabelGoto1
LabelGoto0: 
movl $2, %eax
movl %eax, 32(%esp)
movl $1, %eax
movl %eax, 36(%esp)
movl 12(%esp), %eax
cmpl 32(%esp), %eax
jne Label2
movl $0, %eax
movl %eax, 36(%esp)
Label2: 
movl 36(%esp), %eax
cmpl $1, %eax
je LabelGoto2
movl $(_t8), %eax
movl %eax, 40(%esp)
pushl 40(%esp)
pushl $11
call print_string
addl $8, %esp
jmp LabelGoto1
LabelGoto2: 
movl $3, %eax
movl %eax, 48(%esp)
movl $1, %eax
movl %eax, 52(%esp)
movl 12(%esp), %eax
cmpl 48(%esp), %eax
jne Label3
movl $0, %eax
movl %eax, 52(%esp)
Label3: 
movl 52(%esp), %eax
cmpl $1, %eax
je LabelGoto3
movl $(_t12), %eax
movl %eax, 56(%esp)
pushl 56(%esp)
pushl $13
call print_string
addl $8, %esp
jmp LabelGoto1
LabelGoto3: 
movl $4, %eax
movl %eax, 64(%esp)
movl $1, %eax
movl %eax, 68(%esp)
movl 12(%esp), %eax
cmpl 64(%esp), %eax
jne Label4
movl $0, %eax
movl %eax, 68(%esp)
Label4: 
movl 68(%esp), %eax
cmpl $1, %eax
je LabelGoto4
movl $(_t16), %eax
movl %eax, 72(%esp)
pushl 72(%esp)
pushl $12
call print_string
addl $8, %esp
jmp LabelGoto1
LabelGoto4: 
movl $5, %eax
movl %eax, 80(%esp)
movl $1, %eax
movl %eax, 84(%esp)
movl 12(%esp), %eax
cmpl 80(%esp), %eax
jne Label5
movl $0, %eax
movl %eax, 84(%esp)
Label5: 
movl 84(%esp), %eax
cmpl $1, %eax
je LabelGoto5
movl $(_t20), %eax
movl %eax, 88(%esp)
pushl 88(%esp)
pushl $19
call print_string
addl $8, %esp
jmp LabelGoto1
LabelGoto5: 
movl $(_t22), %eax
movl %eax, 96(%esp)
pushl 96(%esp)
pushl $35
call print_string
addl $8, %esp
LabelGoto1: 
popl %ebp
jmp exit
exit:
	movl $1, %eax
	movl $0, %ebx
	int $0x80
