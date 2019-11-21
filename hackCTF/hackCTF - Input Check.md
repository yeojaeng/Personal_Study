# hackCTF - Input Check

---



![image](https://user-images.githubusercontent.com/33051018/69303578-e82edb00-0c60-11ea-8bad-4266e5c862cb.png)

HackCTF의 `Input Check` 문제이다.

문제 설명에 표기된 URL을 타고 따라 들어가 문제를 푼다.





### 문제풀이

---

>![image](https://user-images.githubusercontent.com/33051018/69303619-03014f80-0c61-11ea-9cb8-329143f71e19.png)
>
>
>문제의 흐름은 간단했다.
>
>`Input box`가 하나 주어지고 해당 박스에 `flag`라는 **명령어**를 넣으면 되는것 같다.
>
>바로 `flag`를 입력하고 OK버튼을 클릭해봤다.
>
>![image](https://user-images.githubusercontent.com/33051018/69303687-43f96400-0c61-11ea-8da6-91961413a90b.png)
>
>`No Hack`이라고 하신다. 일종의 에러 출력으로 확인된다.
>
>타 문자열을 입력했을때는 해당 페이지가 안뜨는것으로 보아 `flag`라는 문자열을 필터링하는 것으로 확인된다.
>
>![image](https://user-images.githubusercontent.com/33051018/69303701-4bb90880-0c61-11ea-9f7e-18e5fca549db.png)
>
>또한, `flag`라는 입력값을 주었을 때 URL을 살펴보면, 
>
>`GET`방식을 통해 `text`라는 변수에 사용자의 입력값이 전달되는 것을 알 수 있다.
>
>![image](https://user-images.githubusercontent.com/33051018/69303753-828f1e80-0c61-11ea-9f24-084e2a9af9c1.png)
>
>소스코드를 참조하기 위하여 개발자 도구를 켰더니, 힌트가 적혀있었다.
>
>**Hint : Input Command Check is Array Type**
>
>`입력값에 대한 검증은 배열 자료형이다.` 라고 한다.
>
>`배열` 이라는 힌트를 바탕으로 입력값으로 array('flag'), ["flag"]등 여러 입력을 진행해 보았으나 플래그가 출력되지 않아 다시 문제의 원점으로 돌아가서 살펴보았다.
>
>본 문제는 **입력값에 대한 검증**을 우회해야 한다.
>
>문자열에 대한 검증을 하기 위해서는 어떠한 비교 루틴의 함수가 분명히 이용될 것이며 이를 바탕으로 서칭을 진행한 결과 `strcmp`함수에 대한 취약점을 발견할 수 있었다.
>
>`strcmp`함수에 문자열을 인자로 넣어야 하는데 배열을 인자로 넣으면 반환값이 0이 된다.
>
>![image](https://user-images.githubusercontent.com/33051018/69306425-ba4e9400-0c6a-11ea-93b3-80630b87d0aa.png)
>
>위와 같이 인자로 전달되는 변수 자체를 배열 형식으로 전달한 결과 플래그를 확인할 수 있었다.
>
>![image](https://user-images.githubusercontent.com/33051018/69306470-dd794380-0c6a-11ea-8abb-ce4a86d40580.png)





### 배운점

---

>#### strcmp 취약점 인증 우회
>
>아래 예시와 같이 인증 루틴을 갖는 `login.php` 가 있다고 가정해보자.
>
>```php
><?php
>    $ps = 'password_num';
>	if(!isset($_GET['user_id']) || !isset($_GET['password']))
>        die('paramrs error');
>
>	if(($_GET['user_id'] == 'admin') && (strcmp($ps, $_GET['password']) == 0))
>        die("login success");
>	else
>        die("login failed");
>?>
>```
>
>`user_id`와 `password`가 정상적으로 `set`되어 있는지 확인 한 뒤, `user_id`와 `password`가 정상적인 값인지 인증을 진행한다.
>
>여기서 6번 라인의 `strcmp`함수에서 취약점이 발생한다.
>
>`strcmp($a, $b)`를 실행할 때 만일 우리가 password를 몰라도 `strcmp`함수서 0을 리턴하는 방법이 있다면 이러한 인증 루틴을 우회할 수 있다.
>
>
>
>```php
><?php
>    $a = array('a');
>	$b = 'password_num';
>	
>	if(strcmp($a, $b) == 0)
>        echo('strings are smae');
>	else
>        echo('strings are diff');
>?>
>```
>
>
>위 코드의 결과는 `strings are same`이다.
>
>이는 `strcmp`함수의 취약점으로 인한 인증 우회 방법으로 `strcmp`함수에 문자열을 인자로 넣어야 하는데 배열을 인자로 넣을 경우 반환값이 0임을 알 수 있다.
>
>이는, NULL이 숫자 0과 같이 때문에  NULL == 0이 True를 반환하는 논리에 의한 오류다.
>
>그러나, NULL은 0과 같은 `Type`이 아니기 때문에 NULL === 0 으로 검증을 진행할 경우에는 False 결과를 얻게 된다.
>
>따라서, 해당 취약점을 보완하기 위해서는 `strcmp` 비교 구문을 기존에서 == 연산 대신 ===연산을 통해 보다 엄격한 비교를 진행하는 것이 바람직하다.







