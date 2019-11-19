# HackCTF - Guess me

---



![image](https://user-images.githubusercontent.com/33051018/69026676-32b91900-0a0f-11ea-9387-bb92181455d0.png)



HackCTF 의 **Guess me** 문제이다.

바로 문제풀이로 들어가보자.



### 문제풀이

---

>![image](https://user-images.githubusercontent.com/33051018/69026711-4ebcba80-0a0f-11ea-960f-d1b7df56e830.png)
>
>문제 설명에 적혀있는 URL로 이동하면 위와 같은 페이지를 확인할 수 있다.
>
>비밀 코드를 맞출 경우, 플래그 값을 획득할 수 있다고 한다.
>
>코드를 살펴보도록 한다.
>
>```php
><?php
>    $filename = 'secret.txt';
>	extract($_GET);
>	if(isset($guess)) {
>        $secretcode = trim(file_get_contents($filename));
>        if($guess === $secretcode) {
>            $flag = file_get_contents('flag.txt');
>            echo "<p>flag is"." $flag</p>";
>        } else {
>            echo "<p>비밀 코드는 $guess (이)가 아닙니다. </p>";
>        }
>    }
>?>
>```
>
>`secret.txt`라는 파일로부터 내용을 읽어와 이를 변수 `secretcode`에 넣는다.
>
>이후, 해당 값이 클라이언트가 보낸 `guess`값과 동일한지 여부를 확인한 뒤 동일할 경우, Flag값을 출력한다.
>
>**본 문제는 `php`의 `extract` 취약점을 알고있는지 묻는 문제이다.**
>
>`extract` 취약점을 이용해 `$filename`을 조작할 수 있으며, 이를 바탕으로 문제를 풀어낼 수 있다.
>
>Flag값을 출력하기 위한 가장 중요한 부분은 Line6의 분기문이다. 사용자가 `initialize` 가능한 `$guess` 변수와 `$filename`으로부터 데이터를 가져와 초기화하는 `$secretcode`변수 모두 클라이언트가 제어할 수 있다.
>
>`filename` 변수를 조작하여 해당 웹서버에 없는 파일명을 기입하게 될 경우, `secretcode`에는 아무것도 들어가지 않을 것이다. 또한 `guess`값 또한 아무것도 넣지 않을경우 Line6의 분기를 제어하여 Flag를 출력시킬 수 있다.
>
>`GET`방식을 통해 데이터를 전송해주기 위해 URL을 이용한다.
>
>`ctf.j0n9hyun.xyz:2030/?filename=1&guess=`
>
>![image](https://user-images.githubusercontent.com/33051018/69026958-6fd1db00-0a10-11ea-9740-a188cbbadcb4.png)



### 배운점

---

>#### php - `extract` vulnerability
>
>`extract`함수에 `$_GET` 또는 `$_POST`를 통해 인자를 넘긴다면, 
>
>넘기는 파라미터와 값을 변수와 그 초기값으로 설정할 수 있다.
>
>즉, 기존값을 **Overwrite**할 수 있다.
>
>하지만, 이를 위해서는 공격자가 내부 변수명을 정확히 알고 있어야 하며
>
> `extract`이후 변수를 재정의하는 코드가 존재할 경우, 이는 공격에 이용되기 어렵다.
>
>
>
>
>#### 대응방안
>
>1. 변수를 선언하기 이전에 `extract`함수를 사용한다.
>2. `extract` 함수 사용시 **EXTR_SKIP** 옵션을 이용한다.
>   ( EXTR_SKIP : 기존 변수와의 충돌이 생길 경우, 기존 변수를 덮어쓰지 않도록 해준다. )