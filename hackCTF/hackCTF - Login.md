# HackCTF - Login

---

![image](https://user-images.githubusercontent.com/33051018/69028364-1e781a80-0a15-11ea-8532-6cb9bf9713c7.png)



HackCTF의 **Login**문제이다.

문제명부터 뭔가 SQLi 느낌이 강하게난다.

문제를 살펴보자.



### 문제풀이

---

>![image](https://user-images.githubusercontent.com/33051018/69028417-45365100-0a15-11ea-994c-395997cd4045.png)
>
>문제 설명에 기재된 URL로 이동하면 위와 같은 로그인 폼이 존재한다.
>
>또한, `Login` 버튼과 친절하게도 코드 소스를 보여주는  `View Source` 버튼을 확인할 수 있다.
>
>`View Source`를 눌러 어떻게 데이터를 전송하는지 살펴본다.
>
>![image](https://user-images.githubusercontent.com/33051018/69028490-7d3d9400-0a15-11ea-9a8b-cf917e014a48.png)
>
>`id`와 `pw`를 `GET`방식을 통해 전달받아 초기화 한뒤, `pw`는 `sha2565` 해쉬를 통하여 재정의한다.
>
>그 이후, SQL 쿼리를 전송하게 된다.
>
>`sql`쿼리를 집중해서 보자. 
>
>`where binary id='$id'` 부분에서 취약점이 존재한다.
>
>`id`값을 넣어준 이후, `'`를 통해 쿼리문을 닫아줄수 있으며 `#`을 이용해 뒷부분을 모두 주석처리 할 수 있다.
>
>일반적인 SQLi 문제이다.
>
>`select * from jhyeonuser where binary id='admin'#` 을 이용해 값을 작성한 이후 
>
> `admin`으로 로그인을 시도하였더니 플래그가 출력되었다.

