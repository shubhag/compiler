.globl print_string

print_string:
    pushl %ebp
    movl %esp, %ebp

    movl 8(%esp), %edx              # taking value from memory into register
	movl 12(%esp), %ecx 				# taking value from memory into register
    movl $4, %eax                   # 4 is the system call number
    movl $1, %ebx                   # 1 stands for stdout
    # movl %esp, %ecx                 # Location of the buffer
    # movl $1, %edx                   # Size of the buffer
    int $0x80

exit_print:
    popl %ebp
    ret
