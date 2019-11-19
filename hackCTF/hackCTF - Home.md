# HackCTF - Home

---



![image](https://user-images.githubusercontent.com/33051018/69157465-4b692200-0b28-11ea-98c0-dfb597bfa50b.png)

HackCTF의 **Home**문제다.

문제 설명에 기재된 URL로 이동한다.



### 문제풀이

---

>
>![image](https://user-images.githubusercontent.com/33051018/69157526-69368700-0b28-11ea-90c1-840039a6a81c.png)
>
>해당 URL로 이동하면 위와 같은 웹 페이지를 확인할 수 있다.
>
>>이 사이트에서는 일부 IP를 필터링하고 있다.
>>
>>해결하기 위한 단서는 **머리말**을 생각해보는 것 뿐이다.
>
>흠... IP Filtering을 진행하고 있으며 머리말을 생각해보라고 한다..
>
>웹 통신에서의 머리말이 뭘까 생각해보니 **Header**가 생각났고 **IP와 Header**를 기반으로 검색을 해보았다.
>
>그 결과, **XFF(X-Forwarded-For)**란 개념을 찾을수 있었다.
>
>XFF는 HTTP Header 중 하나로 HTTP Server에 요청한 Client의 IP를 식별하기 위한 표준으로 사용된다.
>
>Proxy툴을 이용하여 XFF를 통해 Client의 IP를 조작해보자.
>
>![image](https://user-images.githubusercontent.com/33051018/69157970-0e515f80-0b29-11ea-81de-5a8d8625fc11.png)
>
>해당 워게임 페이지에서 Proxy를 통해 잡은 결과다.
>
>헤더부에 XFF를 포맷에 맞춰 기입해주도록 한다.
>
>처음에는 본인의 IP를 적었으나 플래그를 주지 않아 루프백을 적어봤다.
>
>`X-Forwarded-For: 127.0.0.1`
>
>![image](https://user-images.githubusercontent.com/33051018/69158178-5b353600-0b29-11ea-9cc0-a6c42197ca60.png)
>
>이와같이 XFF를 헤더부에 추가한 뒤, Forwarding 해주었다.
>
>![image](https://user-images.githubusercontent.com/33051018/69158291-89b31100-0b29-11ea-9d55-1862264c3d75.png)



### 배운점

---

>#### XFF(X - Forwarded - For)
>
>`XFF`란, `HTTP Header`중 하나로 `HTTP Server`에 요청한 `Client`의 IP를 식별하기 위한 표준으로 사용된다.
>
>웹 서버 또는 WAS 앞 L4 같은 `Proxy & caching Server`가 존재할 경우 웹 서버는 Proxy 또는 장비 IP에 접속한 것으로 인식한다. 
>
>그렇기 때문에 웹 서버는 실제 클라이언트의 IP가 아닌 앞단에 있는 Proxy서버 IP를 Request IP로 인식하고, Proxy IP로 웹 로그를 남기게 된다.
>
>>`Client IP -> Proxy Server -> Web Server`
>
>이 떄, 웹 애플리케이션에서는 `X-Forwarded-For HTTP Header`에 있는 Client IP를 찾아 실제 요청한 클라이언트 IP를 알 수 있고, 웹 로그에도 실제 Request를 보낸 Client IP를 남길 수 있다.
>
>X-Forwarded-For는 다음과 같이 콤마(,) 구분자를 통해 `Client`와 `Proxy IP`가 들어가게 되므로 첫번쨰 IP를 가져오면 `Client`를 식별할 수 있다.
>
>>`X-Forwarded-For: client, Proxy1, Proxy2`