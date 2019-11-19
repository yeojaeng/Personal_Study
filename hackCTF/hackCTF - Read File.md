# HacKCTF - Read File

---

![image](https://user-images.githubusercontent.com/33051018/69119036-aecb6380-0ad8-11ea-94f5-b3eb870aa053.png)

HackCTF의 Read FIle 문제이다.

파일을 읽으라 하니 뭔가 File Inclusion 취약점을 연상시킨다.

바로 문제를 풀어보도록 하자.



### 문제풀이

---

>![image](https://user-images.githubusercontent.com/33051018/69119064-d02c4f80-0ad8-11ea-9a45-484a143c76e3.png)
>
> 문제 설명에 명세되어진 URL로 접속하니 과거 구글을 연상시키는 웹 페이지를 확인할 수 있다.
>
>대문글에 **Read File**이 쓰여져있고 부제로 `File is flag.php`라는 설명이 적혀있다.
>
>![image](https://user-images.githubusercontent.com/33051018/69119134-f2be6880-0ad8-11ea-9f27-2ad3280f4396.png)
>
>이어서 URL을 살펴보았다. `command`라는 인자에 `http://google.com` 이라는 값이 전달되었다.
>
>해당 파라미터 값으로 `flag.php`를 전달해보자.
>
>![image](https://user-images.githubusercontent.com/33051018/69119187-23060700-0ad9-11ea-8ed4-f19b74b0c839.png)
>
>역시나 플래그를 출력해주지 않고 위와같은 사진만 나온다.
>
>일련의 에러페이지로 유추되어진다. 
>
>클라이언트에서 보낸 데이터값을 필터링하는 것으로 예상이 된다.
>
>이어서 `?command=flaghttp://google.com` 이라는 값을 전달해본다.
>
>![image](https://user-images.githubusercontent.com/33051018/69119277-6791a280-0ad9-11ea-9a97-8bfc58b9067f.png)
>
>앞서 살펴보았던, `command=http://google.com`의 결과와 같은 결과를 출력하였다.
>
>이로써 서버에서는 `flag`라는 문자열을 필터링하고 있는것을 알 수 있다.
>
>서버에서는 클라이언트가 전달한 데이터를 검증하는 루틴을 가지고 있으며 `flag`라는 문자열을 필터링하는 것을 확인하였다. 따라서 이를 우회하기 위해서는 해당 값을 필터링함과 동시에 해당 값을 만들어내야 한다.
>
>이를 위해, `command=flflagag.php`라는 값을 전달해본다.
>
>![image](https://user-images.githubusercontent.com/33051018/69119438-f2729d00-0ad9-11ea-8b9f-e5a082d239d4.png)



### 다시 배운점

---

>####LFI(Local File Inclusion) Vulnerability
>
>File Inclusion 취약점은 이름 그대로 서버 내부의 파일을 include 를 가능하게 하는 취약점이다.
>
>LFI는 마찬가지로 File Inclusion취약점임은 같으나 파일을 포함시킬 때 해당 파일의 위치에 따라 취약점 명이 구분되어진다. 
>
>**(LFI : Local FIle Inclusion -> 대상 파일이 공격대상 서버에 위치 ,** 
>**RFI : Remote File Incluson -> 대상 파일이 원격지에 위치 )**
>
>크게 살펴본다면 File Upload & Download 취약점과 비슷하다.
>
>만일, 서버 디렉토리 내부 Web Shell이 위치하고 있다면 File Inclusion 취약점이 존재하는 페이지를 통해 Web Shell에 접근이 가능할 것이며 이는 서버 DB 파일 까지도 접근이 가능하므로 파일 다운로드 공격으로도 이어질 수 있다. 
>
>특히 오픈소스 어플리케이션의 경우에는 디렉토리 구조가 이미 알려져 있으므로 LFI 취약점이 있을 경우 파일 다운로드 공격으로 연계될 수 있다.
>
>LFI 취약점은 SQLi와 같이 매우 빈번히 발생하는 취약점이며 클라이언트가 전달한 입력문에 대한 적절한 검증 혹은 필터링이 없을 경우 발생한다. **서버 내 파일의 내용이 유출되거나 공격자가 작성한 코드를 서버가 실행하는 등의 피해를 입을수 있기 때문에 주의가 필요하다.**
>
>
>아래 예시 코드를 살펴보자.
>
>```php
><?php
>    $file = $_GET('file');
>    if(isset($file)) {
>        include("pages/$file");
>    } else {
>        include("index.php");
>	}
>?>
>```
>
>
>GET 방식으로 전달받은 인자를 `$file`변수에 대입한 뒤, 해당 값을 `include`한다.
>
>* 올바른 사용 예시
>
>  `http://example.com/index.php?file=main.php`
>
>* 취약점 공격 예시
>
>  `http://example.com/index.php?file=../../../../../../etc/passwd`
>
>하지만 `$file`을  `include`하는데 어떠한 유효값 검증 및 제한이 없으므로 이를 이용하여 서버 내 모든 파일에 접근이 가능하다. 위 예시는 정말 단순한 공격이지만 이는 큰 위험으로 연결되어 2차피해를 불러올 수 있다.
>
>
>
>
>
>#### 대응방안
>
>```php
><?php
>    $file = str_replace('../', '', $_GET['file']);
>	if(isset($file)) {
>        include("pages/$file");
>    } else {
>        include("index.php");
>    }
>?>
>```
>
>위 코드는 `str_replace`를 통해 클라이언트의 입력값을 검증하는 루틴을 추가한 옣시이다.
>
>사용자가 지정한 주소에서 다른 디렉토리의 접근을 위해 필요한 문자 `../`를 치환시키도록 한다.
>
>그러나, 실제 공격을 훨씬 교묘하기에 이 또한 손쉽게 우회되어질 수 있다.
>
>따라서, 아래와 같이  `Whitelist` 를 통한 `allowPage`를 만들고, 이에 대한 접근만 허용하는 방법을 쓰는것을 권장한다.
>
>```php
><?php
>    $WHiteListPages = array('allow1.php', 'allow2.php', 'allow3.php');
>	$file = $_GET['file'];
>	if(isset($file) && in_array($file, $WhiteListPages)) {
>        include("pages/$file");
>    } else {
>        include("index.php");
>    }
>?>
>```
>
>