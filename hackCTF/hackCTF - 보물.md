# HackCTF - 보물

---



![image](https://user-images.githubusercontent.com/33051018/69005169-6b021e00-0961-11ea-973d-1d85ad956a69.png)

HackCTF 의 **보물** 문제이다.



### 문제풀이

---

>문제 설명에 기재되어진 URL로 이동한다.
>
>![image](https://user-images.githubusercontent.com/33051018/69005171-853bfc00-0961-11ea-9f35-13bf1f5e535e.png)
>
>이와 같은 페이지가 나오며 아래 각각의 Page 버튼들을 눌러보면 이상한 Hash값 들을 출력해준다.
>
>문제에서 **내 페이지 숫자 중에 비밀**이 있다고 했다.
>
>각각의 Page버튼을 누를때마다, **Get**방식으로 page=1, page=2, page=3을 전송한다.
>
>간단무식하게 브루트포스로 해당 문제를 풀어보도록 한다.
>
>```python
>import requests
>
>URL = 'http://ctf.j0n9hyun.xyz/?page='
>reset = 'http://ctf.j0n9hyun.xyz/?page='
>cnt = 0
>
>while True:
>    URL += str(cnt)
>    response = requests.get(URL)
>    if 'HackCTF{' in response.text:
>        print(response.text)
>        break
>    else:
>        cnt += 1
>        print('cnt : ' + str(cnt))
>        URL = reset
>```
>
>`page` 파라미터에 인자를 0부터 시작하여 풀릴때까지 1씩 증가시키며 계속하여 request를 보내는 파이썬 코드를 작성한다.
>
>만일, `request`에 대한 `response` 내에 Flag 형식의 문자열이 발견되면 이를 출력하고 종료하도록 한다.
>
>생각보다 꽤 많은 시간이 지난 이후에 플래그를 알려준다!



### 배운점

---

>####Requests Module
>
>
>
>####0.사용법
>
>Python에서 HTTP 요청을 보내는 모듈인 Requests모듈은 다양한 문제를 푸는데 매우 유용하다.
>
>기본적인 사용방법은 아래와 같다.
>
>```python
>import requests
>
>URL = 'http://duwjdtn11.tistory.com'
>response = requests.get(URL)	
>response.status_code	# 상태코드 
>response.text			# 내용
>```
>
>해당 코드는 나의 `http://duwjdtn11.tistory.com`의  주소로 GET 요청 `Request`를 보냈고 서버에서는 해당 요청을 받아 처리한 이후 나에게 응답 `Response`를 준다. 이를 `response`라는 변수로 받아 이를 이용하여 사용하는 것이다.
>
>
>#### 1. GET 요청시 parameter 전달법
>
>```python
>params = {'key' : 'value'}
>
>res = requests.get('http://duwjdtn11.tistory.com'. param=params)
>```
>
>
>#### 2. POST 요청시 parameter 전달법
>
>```python
>import requests, json
>data = {'outer': {'inner':'value'}}
>res = requests.post(URL, data=json.dumps(data))
>```
>
>GET 방식에 비하여 조금 더 복잡한 구조로 `json` 모듈을 이용한다.