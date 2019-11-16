# HACKCTF - Hidden

---



![image-20191116224041310](/Users/mac/Library/Application Support/typora-user-images/image-20191116224041310.png)



HackCTF의 Web분야 **Hidden** 문제이다.



### 문제풀이

---

>![image-20191116224252052](/Users/mac/Library/Application Support/typora-user-images/image-20191116224252052.png)
>
>5번 파일에 플래그가 있다고 한다!!!
>
>그리고, 역시 1~4번 까지의 박스는 존재하나 5번 박스는 존재하지 않는다!
>
>사실, 페이지 소스를 살펴보기 전에 풀었지만 보다 더욱 친절한 풀이를 위해 사진을 첨부한다.
>
>![image](https://user-images.githubusercontent.com/33051018/68994147-1ad47e80-08c3-11ea-98d4-0778ca19c1b1.png)
>
>각각의 버튼을 누르면 **get** 방식을 통해 `id` 라는 파라미터로 `value` 값을 전송한다.
>
>그렇다면 동일하게 `id`라는 파라미터에 `5` 라는 `value` 를 전송해주면 5번 파일에 접근이 가능할 것으로 생각된다.
>
>`get`  방식의 특성을 이용해 url을 통해 `value`  를 전송해준다.
>
>![image](https://user-images.githubusercontent.com/33051018/68994300-c5996c80-08c4-11ea-9734-7fbc1d0fa5f9.png)
>
>**굳...**



### 다시 배운점

---

>**Web service 에서 Server에 요청하는 대표적 메소드**
>
>
>
>**Get** : 브라우저(클라이언트)의 데이터를 URL 뒤에 붙여서 보낸다. 
>
>`www.example.com?id=test&pw=1234` 와 같은 예시가 존재한다고 가정한다면,
>
>이는, `www.example.com` 에 `id=test` && `pw=1234` 라는 데이터를 전송하므로써 요청을 하는 것이다.
>
>`url` 뒤에 '?'를 통해 URL의 끝을 구분해주며 데이터 표현의 시작을 알린다.
>
>중간 `&` 은 구분자로 2개 이상의 `Key - Value` 쌍 데이터를 보낼때 사용한다.
>
>
>
>**Post** : Post 방식은 Get 방식과는 달리, 데이터 전송을 기반으로 한 요청 메소드이다.
>
>GET 방식은 URL 뒤에 데이터를 붙여 보내는 반면, POST 방식은 `BODY` 에 데이터를 넣어서 전송한다.
>
>따라서, 헤더 필드 중 BODY의 데이터를 설명하는 `Content-Type` 이라는 헤더 필드가 들어가며 어떤 데이터 타입인지 명시한다.





