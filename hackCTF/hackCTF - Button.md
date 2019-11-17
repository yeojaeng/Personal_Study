# HACKCTF - Button

---

![image](https://user-images.githubusercontent.com/33051018/69004557-a9dfa600-0958-11ea-96b2-0190fd23c7a0.png)

HackCTF의 Web분야 문제인 **Button**이다.



### 문제풀이

---

>문제 설명에 기재된 `url` 로 이동해보았다.
>
>![image](https://user-images.githubusercontent.com/33051018/69004566-e1e6e900-0958-11ea-82eb-b56d7d9a1280.png)
>
>아래의 버튼을 이용해서 플래그를 출력해달라고 한다.
>
>하지만, 해당 버튼을 눌러도 아무런 반응이없다.
>
>바로 소스를 살펴보도록 한다!
>
>![image](https://user-images.githubusercontent.com/33051018/69004571-0216a800-0959-11ea-83aa-5b0be6aef0dc.png)
>
>위 그림이 해당 버튼에 대한 소스이다. `POST` 방식을 통해 서버에게 데이터를 전송한다.
>
>`submit` Type의 `button` 이며, `default value`는 `button`으로 되어있다.
>
>버튼을 클릭하여 서버에게 전송되는 데이터 값을 프록시를 통해 가로채보자.
>
>![image](https://user-images.githubusercontent.com/33051018/69004594-74878800-0959-11ea-9f29-5945e5814401.png)
>
>`button` 이라는 파라미터로 `button`이라는 value가 전송되어진다.
>
>문제가 **아래의 버튼으로 하여금 플래그를 출력하게 해줘!** 라고 했으니, 해당 `value` 값을 수정해주면 될 것 같다.
>
>1, True, TRUE, 등등 시도해보다가 `flag` 를 전송해주니 문제가 풀렸다!