.section .data
newline:
    .ascii "\n"
end:

.section .text
.globl print_int

print_int:
    pushl %ebp
    movl %esp, %ebp

	movl 8(%esp), %eax 				# taking value from memory into register
  	movl $0, %edi					# initializing digit count

loop:
	movl $0, %edx
    movl $10, %ecx              
    divl %ecx               

    addl $48, %edx              # converting EDX to ascii value
    pushl %edx                  # pushing EDX onto the stack
    incl %edi                   # incrementing digit count

	cmp $0, %eax   				# loop back if we have something remaining in EAX
	jne loop

print:
    movl $4, %eax                   # 4 is the system call number
    movl $1, %ebx                   # 1 stands for stdout
    movl %esp, %ecx                 # Location of the buffer
    movl $1, %edx                   # Size of the buffer
    int $0x80
    add $4, %esp                    # incrementing stack pointer
                                    # adding 4 because we pushed a 32 bit register
                                    # no matter it contains just a character
	decl %edi                       # Decrementing index to ensure that the stack doesn't underflows.
    cmp $0, %edi
    jne print

print_newline:
    movl $4, %eax                   # 4 is the system call number
    movl $1, %ebx                   # 1 stands for stdout
    movl $(newline), %ecx                 # Location of the buffer
    movl $(end-newline), %edx                   # Size of the buffer
    int $0x80


exit_print:
    popl %ebp
    ret
