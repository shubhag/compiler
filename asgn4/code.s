.section .data
.section .text
.globl _start

 
_start: 
pushl %ebp
movl %esp, %ebp
subl $196, %esp
movl $5, %eax
movl %eax, 8(%esp)
movl 28(%esp), %eax
movl %eax, 52(%esp)
movl $5, %eax
movl %eax, 56(%esp)
movl 56(%esp), %eax
movl %eax, 60(%esp)
movl $0, %eax
movl %eax, 64(%esp)
movl 64(%esp), %eax
movl %eax, 68(%esp)
movl $1, %eax
movl %eax, 72(%esp)
movl 60(%esp), %eax
subl 72(%esp), %eax
movl %eax, 76(%esp)
movl 76(%esp), %eax
movl %eax, 80(%esp)
movl $0, %eax
movl %eax, 88(%esp)
movl 88(%esp), %eax
imull $4, %eax
movl %eax, 92(%esp)
movl $52, %eax
subl 92(%esp), %eax
addl %esp, %eax
movl %eax, 96(%esp)
movl $2, %eax
movl %eax, 100(%esp)
movl 100(%esp), %eax
movl 96(%esp), %ebx
movl %eax, (%ebx)
movl $1, %eax
movl %eax, 104(%esp)
movl 104(%esp), %eax
imull $4, %eax
movl %eax, 108(%esp)
movl $52, %eax
subl 108(%esp), %eax
addl %esp, %eax
movl %eax, 112(%esp)
movl $1, %eax
movl %eax, 116(%esp)
movl 116(%esp), %eax
movl 112(%esp), %ebx
movl %eax, (%ebx)
movl $3, %eax
movl %eax, 120(%esp)
movl 120(%esp), %eax
imull $4, %eax
movl %eax, 124(%esp)
movl $52, %eax
subl 124(%esp), %eax
addl %esp, %eax
movl %eax, 128(%esp)
movl $5, %eax
movl %eax, 132(%esp)
movl 132(%esp), %eax
movl 128(%esp), %ebx
movl %eax, (%ebx)
movl $4, %eax
movl %eax, 136(%esp)
movl 136(%esp), %eax
imull $4, %eax
movl %eax, 140(%esp)
movl $52, %eax
subl 140(%esp), %eax
addl %esp, %eax
movl %eax, 144(%esp)
movl $6, %eax
movl %eax, 148(%esp)
movl 148(%esp), %eax
movl 144(%esp), %ebx
movl %eax, (%ebx)
movl $2, %eax
movl %eax, 152(%esp)
movl 152(%esp), %eax
imull $4, %eax
movl %eax, 156(%esp)
movl $52, %eax
subl 156(%esp), %eax
addl %esp, %eax
movl %eax, 160(%esp)
movl $0, %eax
movl %eax, 164(%esp)
movl 164(%esp), %eax
movl 160(%esp), %ebx
movl %eax, (%ebx)
movl %esp, %eax
addl $52, %eax
pushl %eax
pushl 72(%esp)
pushl 88(%esp)
call Main.Qsort.quicksort
addl $12, %esp
movl %eax, 168(%esp)
movl $0, %eax
movl %eax, 172(%esp)
movl 172(%esp), %eax
movl %eax, 84(%esp)
LabelGoto2: 
movl $1, %eax
movl %eax, 176(%esp)
movl 84(%esp), %eax
cmpl 60(%esp), %eax
jl Label1
movl $0, %eax
movl %eax, 176(%esp)
Label1: 
movl 176(%esp), %eax
cmpl $1, %eax
je LabelGoto0
jmp LabelGoto1
LabelGoto3: 
movl $1, %eax
movl %eax, 180(%esp)
movl 180(%esp), %eax
addl 84(%esp), %eax
movl %eax, 184(%esp)
movl 184(%esp), %eax
movl %eax, 84(%esp)
jmp LabelGoto2
LabelGoto0: 
movl 84(%esp), %eax
imull $4, %eax
movl %eax, 188(%esp)
movl $52, %eax
subl 188(%esp), %eax
addl %esp, %eax
movl %eax, 192(%esp)
movl 192(%esp), %ebx
pushl (%ebx)
call print_int
popl %eax
jmp LabelGoto3
LabelGoto1: 
popl %ebp
jmp exit

 
Main.Qsort.quicksort: 
pushl %ebp
movl %esp, %ebp
subl $204, %esp
movl $1, %eax
movl %eax, 44(%esp)
movl 216(%esp), %eax
cmpl 212(%esp), %eax
jl Label2
movl $0, %eax
movl %eax, 44(%esp)
Label2: 
movl 44(%esp), %eax
cmpl $1, %eax
je LabelGoto4
jmp LabelGoto5
LabelGoto4: 
movl 216(%esp), %eax
movl %eax, 16(%esp)
movl 216(%esp), %eax
movl %eax, 28(%esp)
movl 212(%esp), %eax
movl %eax, 20(%esp)
LabelGoto15: 
movl $1, %eax
movl %eax, 48(%esp)
movl 28(%esp), %eax
cmpl 20(%esp), %eax
jl Label3
movl $0, %eax
movl %eax, 48(%esp)
Label3: 
movl 48(%esp), %eax
cmpl $1, %eax
je LabelGoto6
jmp LabelGoto7
LabelGoto6: 
movl 28(%esp), %eax
imull $4, %eax
movl %eax, 52(%esp)
movl 220(%esp), %eax
subl 52(%esp), %eax
movl %eax, 56(%esp)
movl 16(%esp), %eax
imull $4, %eax
movl %eax, 60(%esp)
movl 220(%esp), %eax
subl 60(%esp), %eax
movl %eax, 64(%esp)
movl $1, %eax
movl %eax, 68(%esp)
movl 56(%esp), %ebx
movl (%ebx), %eax
movl 64(%esp), %ebx
cmpl (%ebx), %eax
jle Label4
movl $0, %eax
movl %eax, 68(%esp)
Label4: 
movl 68(%esp), %eax
cmpl $1, %eax
je LabelGoto8
jmp LabelGoto9
LabelGoto8: 
movl $1, %eax
movl %eax, 72(%esp)
movl 28(%esp), %eax
cmpl 212(%esp), %eax
jl Label5
movl $0, %eax
movl %eax, 72(%esp)
Label5: 
movl 72(%esp), %eax
cmpl $1, %eax
je LabelGoto10
jmp LabelGoto9
LabelGoto10: 
movl $1, %eax
movl %eax, 76(%esp)
movl 28(%esp), %eax
addl 76(%esp), %eax
movl %eax, 80(%esp)
movl 80(%esp), %eax
movl %eax, 28(%esp)
jmp LabelGoto6
LabelGoto9: 
movl 20(%esp), %eax
imull $4, %eax
movl %eax, 84(%esp)
movl 220(%esp), %eax
subl 84(%esp), %eax
movl %eax, 88(%esp)
movl 16(%esp), %eax
imull $4, %eax
movl %eax, 92(%esp)
movl 220(%esp), %eax
subl 92(%esp), %eax
movl %eax, 96(%esp)
movl $1, %eax
movl %eax, 100(%esp)
movl 88(%esp), %ebx
movl (%ebx), %eax
movl 96(%esp), %ebx
cmpl (%ebx), %eax
jg Label6
movl $0, %eax
movl %eax, 100(%esp)
Label6: 
movl 100(%esp), %eax
cmpl $1, %eax
je LabelGoto11
jmp LabelGoto12
LabelGoto11: 
movl $1, %eax
movl %eax, 104(%esp)
movl 20(%esp), %eax
subl 104(%esp), %eax
movl %eax, 108(%esp)
movl 108(%esp), %eax
movl %eax, 20(%esp)
jmp LabelGoto9
LabelGoto12: 
movl $1, %eax
movl %eax, 112(%esp)
movl 28(%esp), %eax
cmpl 20(%esp), %eax
jl Label7
movl $0, %eax
movl %eax, 112(%esp)
Label7: 
movl 112(%esp), %eax
cmpl $1, %eax
je LabelGoto13
jmp LabelGoto14
LabelGoto13: 
movl 28(%esp), %eax
imull $4, %eax
movl %eax, 116(%esp)
movl 220(%esp), %eax
subl 116(%esp), %eax
movl %eax, 120(%esp)
movl 120(%esp), %ebx
movl (%ebx), %eax
movl %eax, 24(%esp)
movl 28(%esp), %eax
imull $4, %eax
movl %eax, 124(%esp)
movl 220(%esp), %eax
subl 124(%esp), %eax
movl %eax, 128(%esp)
movl 20(%esp), %eax
imull $4, %eax
movl %eax, 132(%esp)
movl 220(%esp), %eax
subl 132(%esp), %eax
movl %eax, 136(%esp)
movl 136(%esp), %ebx
movl (%ebx), %eax
movl 128(%esp), %ebx
movl %eax, (%ebx)
movl 20(%esp), %eax
imull $4, %eax
movl %eax, 140(%esp)
movl 220(%esp), %eax
subl 140(%esp), %eax
movl %eax, 144(%esp)
movl 24(%esp), %eax
movl 144(%esp), %ebx
movl %eax, (%ebx)
LabelGoto14: 
jmp LabelGoto15
LabelGoto7: 
movl 16(%esp), %eax
imull $4, %eax
movl %eax, 148(%esp)
movl 220(%esp), %eax
subl 148(%esp), %eax
movl %eax, 152(%esp)
movl 152(%esp), %ebx
movl (%ebx), %eax
movl %eax, 24(%esp)
movl 16(%esp), %eax
imull $4, %eax
movl %eax, 156(%esp)
movl 220(%esp), %eax
subl 156(%esp), %eax
movl %eax, 160(%esp)
movl 20(%esp), %eax
imull $4, %eax
movl %eax, 164(%esp)
movl 220(%esp), %eax
subl 164(%esp), %eax
movl %eax, 168(%esp)
movl 168(%esp), %ebx
movl (%ebx), %eax
movl 160(%esp), %ebx
movl %eax, (%ebx)
movl 20(%esp), %eax
imull $4, %eax
movl %eax, 172(%esp)
movl 220(%esp), %eax
subl 172(%esp), %eax
movl %eax, 176(%esp)
movl 24(%esp), %eax
movl 176(%esp), %ebx
movl %eax, (%ebx)
movl $1, %eax
movl %eax, 180(%esp)
movl 20(%esp), %eax
subl 180(%esp), %eax
movl %eax, 184(%esp)
movl 184(%esp), %eax
movl %eax, 32(%esp)
movl $1, %eax
movl %eax, 188(%esp)
movl 20(%esp), %eax
addl 188(%esp), %eax
movl %eax, 192(%esp)
movl 192(%esp), %eax
movl %eax, 36(%esp)
pushl 220(%esp)
pushl 220(%esp)
pushl 40(%esp)
call Main.Qsort.quicksort
addl $12, %esp
movl %eax, 196(%esp)
pushl 220(%esp)
pushl 40(%esp)
pushl 220(%esp)
call Main.Qsort.quicksort
addl $12, %esp
movl %eax, 200(%esp)
LabelGoto5: 
movl $0, %eax
movl %eax, 204(%esp)
movl 204(%esp), %eax
addl $204, %esp
popl %ebp
ret 
popl %ebp
jmp exit
exit:
	movl $1, %eax
	movl $0, %ebx
	int $0x80
