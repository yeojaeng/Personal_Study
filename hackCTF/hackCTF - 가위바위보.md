# HackCTF - 가위바위보

---



![image](https://user-images.githubusercontent.com/33051018/71475187-7844df00-2822-11ea-8c9a-c9f5c7b0d091.png)

HackCTF의 **가위바위보**문제다.

문제 설명에 기재된 URL로 이동한다.



#### 문제풀이

---

>![image](https://user-images.githubusercontent.com/33051018/71475205-97dc0780-2822-11ea-9e44-665873850117.png)
>
>해당 URL에 접근해보면 위와 같이 귀여운 UI의 페이지를 확인할 수 있다.
>
>문제의 이름과 같이 '가위바위보'와 관련된 문제로 생각이된다.
>
>위에 보이는 **가위바위보 시작!** 이라는 버튼을 클릭하면 , 
>
>![image](https://user-images.githubusercontent.com/33051018/71475261-d245a480-2822-11ea-8f5b-e5f2ec114cbd.png)
>
>또다른 귀여운 UI의 웹페이지를 확인할 수 있다.
>
>그냥 바위를 클릭해보았다.
>
>![image](https://user-images.githubusercontent.com/33051018/71475294-e7bace80-2822-11ea-8858-6b333d7bde34.png)
>
>?.... 이겼다고 한다..?
>
>아직 정확히 문제의 의도도 파악하지 못하였다.
>
>''문제 의도와 관련된 힌트가 존재할수도 있을 소스코드를 살펴보도록 하자.''
>
>라고 생각을 했으나, 자바스크립트 코드에서 이상한 점은 발견할 수 없었다.
>
>도대체 뭐가 문제이지.. 라고 생각하고 있던 찰나
>
>![image](https://user-images.githubusercontent.com/33051018/71475480-bf7f9f80-2823-11ea-923c-1c1b8c1fddc3.png)
>
>페이지 상단바 부분이 눈에 띄었다.
>
>**설정** 관련 버튼이 있어 해당 버튼을 클릭해보았다.
>
>![image](https://user-images.githubusercontent.com/33051018/71475511-df16c800-2823-11ea-9cd2-083c69d609d1.png)
>
>개인 User의 Config설정창으로 보인다.
>
>다만, 수상한 점이 있다면 요즘 일반적인 웹 사이트에서 보기 힘든 **파일 업로드**가 가능한 업로드 폼이 존재한다는 것이다.
>
>**파일 업로드** 취약점을 이용한 문제일수도 있겠다는 생각이 들어 간단한 웹 쉘 코드를 작성하여 업로드를 진행해보았다.
>
>![image](https://user-images.githubusercontent.com/33051018/71475585-2ef58f00-2824-11ea-829e-41d5e7b44204.png)
>
>해당 파일의 파일명은 `web_shell.php` 로 저장하고 업로드를 시도한다.
>
>![image](https://user-images.githubusercontent.com/33051018/71475610-5cdad380-2824-11ea-9c1a-359f7c799f0c.png)
>
>업로드를 시도했으나 위와 같은 에러를 띄웠다.
>
>혹시, 확장자 검증을 통한 필터링인가 싶어 이미지파일의 확장자 `.png` 로 확장자를 변경하여 재시도했다.
>
>그러나 똑같은 에러를 띄운다.
>
>이를 통해 **확장자 검증을 통한 필터링** 방법이 아닌 다른 방법을 이용해 파일을 검증하고 있다는 것을 알 수 있다.
>
> 흠... 그렇다면 이번엔 파일 내부 바이너리 값을 검색한다는 가정 하에 이를 우회하기 위해 
>
> png파일의 파일 시그니처를 삽입하는 방법을 시도해보도록 한다.
>
>![image](https://user-images.githubusercontent.com/33051018/71475799-349fa480-2825-11ea-96dc-8182a1ae5fb7.png)
>
>PNG 파일의 시그니처는 `89 50 4E 47 0D 0A 1A 0A`이다.
>
>![image](https://user-images.githubusercontent.com/33051018/71475824-5862ea80-2825-11ea-8172-72f5decbedd6.png)
>
>해당  값을 앞서 작성한 `web_shell.php`파일 최상단, 파일 시그니처 헤더부분에 삽입하여 저장한 뒤 
>
>업로드를 시도한다.
>
>![image](https://user-images.githubusercontent.com/33051018/71475839-74ff2280-2825-11ea-8d76-bf5ef4526934.png)
>
>정상적으로 업로드가 되었다.
>
>바이너리 값을 검증하는 방법을 통해 파일을 검증하고 있던 것이 맞았다.
>
>또한, 해당 이미지의 주소는 http://ctf.j0n9hyun.xyz:2037/avatars/y3oj4eng으로 확인되었다.
>
>![image](https://user-images.githubusercontent.com/33051018/71475957-15554700-2826-11ea-988a-7e8795122a5f.png)
>
>분명 파일의 이름은 `web_shell.php`로 업로드 하였으나 사진의 경로는 `avatars/y3oj4eng`이다.
>
>`y3oj4eng`은 현재 유저의 이름인 것으로 보아 파일의 이름이 현재 이름과 일치 시킨 뒤 웹 쉘을 실행 시키는 방법을 사용하는 것 같다.
>
>따라서, 유저의 이름을 `web_shell.php`로 변경해본다.
>
>![image](https://user-images.githubusercontent.com/33051018/71476037-5cdbd300-2826-11ea-992f-11a88dbbf6f8.png)
>
>이름이 정상적으로 변경되었다.
>
>![image](https://user-images.githubusercontent.com/33051018/71476055-79780b00-2826-11ea-8376-1e8edfadc67d.png)
>
>업로드한 파일의 경로 또한 정상적으로 잡혔다.
>
>이제 해당 경로로 접근을 시도한다.
>
>![image](https://user-images.githubusercontent.com/33051018/71476065-8b59ae00-2826-11ea-9c2f-4a1da16f2c33.png)
>
>정상적으로 실행되는 것으로 보인다.
>
>앞서, 우리가 작성한 웹 쉘 코드는 `cmd`라는 변수에 `GET`방식으로 값을 전달받아 `system`함수를 호출시키도록 한다.
>
>따라서, `cmd`변수에 `ls` 값을 전달해본다.
>
><u>http://ctf.j0n9hyun.xyz:2037/avatars/web_shell.php?cmd=ls</u>
>
>![image](https://user-images.githubusercontent.com/33051018/71476110-cbb92c00-2826-11ea-8086-dc6f04238395.png)
>
>현재 디렉토리를 리스팅한 결과 위와 같은 파일들이 존재하였다.
>
>그렇다면 이전 디렉토리로 이동해보자.
>
><u>[http://ctf.j0n9hyun.xyz:2037/avatars/web_shell.php?cmd=cd%20../;ls](http://ctf.j0n9hyun.xyz:2037/avatars/web_shell.php?cmd=cd ../;ls)</u>
>
>![image](https://user-images.githubusercontent.com/33051018/71476160-12a72180-2827-11ea-929e-d982fc28f16b.png)
>
>예상대로 `flag.txt` 파일이 존재한다.
>
>해당 파일을 열면 플래그를 출력해준다.
>
>