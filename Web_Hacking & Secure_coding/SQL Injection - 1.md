# SQL Injection -1

---



### 1. SQL injection

---

>**외부 입력 값이 직접 쿼리에 삽입**되는 `Statement` 방식의 경우, 
>
>공격 문자열에 의해 SQL 쿼리가 변조되기 때문에 'SQL Inejction'에 취약할 수 있다.
>
>즉, SQL 쿼리에 상요되는 파라미터가 변경될 떄 마다 전체를 다른 쿼리로 인식하기 때문에 공격 문자열도 함께 인식되는 취약점이 있다.
>
>아래 예시는 'HTTP request header' 필드 값 중 **X-Forwarded-For** 라는 값에 공격 문자열을 삽입하는 경우이다.
>
>**cf) X-Forwarded-For란?**
>
>>XFF는 HTTP Header 필드 중 하나로 HTTP Server에 요청한 Client의 IP를 식별하기 위한 표준이다.
>>
>>이전에 HackCTF 워게임 문제중 이를 이용하여 문제를 풀어본 적이 있다.
>
>
>
>```html
>GET / HTTP / 1.1
>Accept:/
>Referer: http://xxx.xxx.xxx
>Accept-Language:Ko
>User-Agent: Mozila xxxx
>Host: xxx.xxx
>X-Forwarded-For:ck_ips=(select user()) WHERE ck_comment_id=2#
>...중략...
>```
>
>**X-Forwarded-For: ck_ips=(select user()) WHERE ck_comment_id=2#**
>
>해당 필드를 주목하자.
>
>그리고 이를 처리하는 서버 코드(php)는 아래와 같다.
>
>```php
>if($row = @mysql_fetech_assoc($result))
>    $ip = getenv("HTTP_X_FORWARDED_FOR") ? getenv("HTTP_X_FORWARDED_FOR") : 
>		getenv("REMOTE_ADDR");
>	if(strstr($row['ck_ips'], $ip)) {
>        $duplicated = 1;
>        $ck_ips = $row['ck_ips'];
>    }
>	if(!$duplicated)
>    {
>        $query = "UPDATE '$table_name' SET ck_rating_$direction = '$rating', ck_ips = '". $ck_ips . "'WHERE ck_comment_id = $k_id";
>		$result = mysql_query($query)
>    }
>...중략...
>```
>
>
>
>2번 라인에서 `getenv`함수를 통해 Client의 IP를 식별한다.
>
>이후, DB에서 추출한 IP와 HTTP_X_FORWARDED_FOR로 추출한 IP를 strrstr 함수를 통해 비교를 진행하고 만일 존재하는 경우 $row(['ck_ips']를 변수를 ck_ips변수에 할당한다.
>
>즉, 해당 변수의 최종목적은 update 쿼리에 ck_ips값을 업데이트 하기 위해 삽입되었다.
>
>또한, 위 코드에는 취약점 관련 SQL 쿼리 (SELECT, INSERT ,UPDATE, DELETE)가 보인다.
>
>해당 변수 ID가 쿼리에 직접 삽입 되었으며 쿼리가 실행되므로 SQL Injection으로 의심할 수 있다.
>
>X-Forwarded-For에 ck_ips=(select user()) WHERE ck_comment_id=2#를 삽입할 경우, 
>
>Select user() 함수를 통해 DB 내 계정정보를 획득할 수 있다.
>
>`#`은 MySQL에서 주석을 의미하므로, 내부 쿼리 처리 시 존재하는 추가적 쿼리 부분을 제거하는 역할을 한다.