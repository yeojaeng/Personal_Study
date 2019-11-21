# HackCTF - 1996

---



![image](https://user-images.githubusercontent.com/33051018/69313061-e0c4fd00-0c73-11ea-9b44-803d6a791c8f.png)

HackCTF 의 Pwnable 분야 문제 1996이다.

바이너리를 다운받고 문제를 풀어본다.



### 문제풀이

---

>![image](https://user-images.githubusercontent.com/33051018/69313303-84161200-0c74-11ea-8c81-eaf80ab45b69.png)
>
>해당 바이너리는 64bit 리눅스 실행 파일이다.
>
>바이너리에 적용되어진 메모리 보호기법들을 확인한다.
>
>![image](https://user-images.githubusercontent.com/33051018/69313177-297cb600-0c74-11ea-8222-0871becc9a7a.png)
>
>Nx bit가 활성화되어있다.
>
>스택, 힙에 대한 실행권한을 갖지 못하므로 일반적인 `shellcode inject`는 불가능 할 것으로 보인다.
>
>흠..일단 실행시켜보자
>
>![image](https://user-images.githubusercontent.com/33051018/69313248-5a5ceb00-0c74-11ea-9bdc-4a9f1c33b0ef.png)
>
>실행시켜 보았더니 `Which environment variable do you want to read?`라는 문자열을 출력한 뒤, 입력을 받는다.
>
>`env var`, 환경변수에 대한 문제로 짐작된다.
>
>IDA를 통해 분석을 이어간다.
>
>![image](https://user-images.githubusercontent.com/33051018/69313361-af006600-0c74-11ea-99ca-61808bc12a3c.png)
>
>12번 라인에서 아까 실행했을 때 살펴보았던 문자열을 확인할 수 있다.
>
>그 이후, 입력을 받던 루틴이 진행되었었는데 해당 입력값은 name으로 입력을 받는다.
>
>16번 라인을 살펴보면 `getenv`함수를 통해 입력을 받는다. 하지만 해당 함수는 입력값에 대한 길이 검증을 진행하지 않기 때문에 BOF 취약점이 존재한다.
>
>![image](https://user-images.githubusercontent.com/33051018/69313486-056da480-0c75-11ea-9902-54592094204d.png)
>
>`main+93~103` 부분을 주목하자.
>
>해당 부분이 입력을 받는 루틴의 부분이다.
>
>`getenv`함수의 입력을 받는 변수는 `name`이였다. 또한 입력값이 저장되는 위치는 `rbp-0x410`이다.
>
>따라서, `name`의 위치는 `rbp-0x410`임을 알 수 있다.
>
>우리는 해당 값을 입력받을때의 BOF 취약점을 이용해 `ret addr`를 `overwrite`할 수 있다.
>
>![image](https://user-images.githubusercontent.com/33051018/69313600-62695a80-0c75-11ea-8082-3522d7d2e346.png)
>
>`name`변수 까지의 길이 + `SFP` (8byte)를 더하여 총 더미는 1048bytes를 입력하면 `return addr`에 접근이 가능하다.
>
>해당 리턴 주소에 어떠한 값을 주냐가 문제인데 바이너리 내 `func`들을 살펴보던 중 쓸만한 함수를 발견했다.
>
>![image](https://user-images.githubusercontent.com/33051018/69313679-99d80700-0c75-11ea-9650-88dae171e06a.png)
>
>`spawn_shell()`이라는 의미심장한 이름의 함수가 존재했다.
>
>![image](https://user-images.githubusercontent.com/33051018/69313873-1b2f9980-0c76-11ea-8de8-dcff488fdc30.png)
>
>예상대로 `bash shell`을 실행시켜주는 함수 였다.
>
>따라서, `getenv`함수를 통해 입력을 받을때 `return addr`를 `spawn_shell`의 주소로 덮어씌워
>
>`getenv`함수가 호출되어 실행된 이후 복귀할 떄  `spawn_shell` 함수가 실행되도록 하여 프로그램의 흐름을 조작한다.



###payload and exploit

---

>![image](https://user-images.githubusercontent.com/33051018/69314374-52527a80-0c77-11ea-9e3e-862d5e0b1d38.png)
>
>
>![image](https://user-images.githubusercontent.com/33051018/69314531-ba08c580-0c77-11ea-8285-cfa35603b3ea.png)
>
>