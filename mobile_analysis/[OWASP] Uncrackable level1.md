# [OWASP] Uncrackable level1 

---



### [Frida Command]

---

>Usage: frida [options] target
>
>
>
>Options:
>
>--verison								show program's version number and exit
>
>-h, --help								show this help message and exit
>
>-D ID, --device==ID				connect to device with the given ID
>
>-U, --usb								connect to USB device
>
>-R, --remote							connect to oremote frida-server
>
>-H Host, --host=HOST		  connect to remote frida-server on HOST
>
>-f FILE, --file=FILE				spawn FILE
>
>-n NAME, --attach-name=NAME	attach to NAME
>
>-p PID, --attach-pid=PID		attach to PID
>
>
>
>##### -D, -R, -U, -H opt를 통해 타겟을 지정하고, -P opt를 통해 원하는 pid를 후킹한다.

cf) 에뮬레이터 환경의 경우, -U 옵션을 통해   frida-server가 잘 돌고 있는지 앞서 확인해준다.

![image](https://user-images.githubusercontent.com/33051018/70034297-47db9d80-15f4-11ea-9daa-b741d6595f3b.png)

이와 같이 결과가 출력되면 정상적으로 서버가 돌고있는것이다.



## Uncrackable level 1 Write-up

---

본격적으로 풀이를 진행한다.

앱을 다운받고 `adb install`을 통해 앱을 설치한다.

![image](https://user-images.githubusercontent.com/33051018/70033838-9a688a00-15f3-11ea-9b57-85d1874cee17.png)

정상적으로 설치하면, 위 그림과 같은 앱을 확인할 수 있다.

해당 앱을 실행해보자.

![image](https://user-images.githubusercontent.com/33051018/70033920-c1bf5700-15f3-11ea-8bb4-3475274b9802.png)

실행과 동시에 위와 같이 `Root detected!`라는 alert창이 뜬다.

`OK`버튼을 클릭하면 앱이 종료된다.

루팅 탐지와 비슷한 루틴이 있는것으로 확인된다.

앱 내부 소스코드를 살펴보자.

![image](https://user-images.githubusercontent.com/33051018/70044949-9eea6e00-1606-11ea-9700-988317166729.png)

`onCreate()`를 살펴보면 아까 살펴보았던 경고문에 출력된 문자열을 확인할 수 있다.

`Root detected`가 출력되는 부분이다. c.a() | c.b() | c.c() 메서드를 통해 루팅을 탐지한다.

그 이후, a()메서드에게 `"Root detected!"` 라는 문자열을 인자로 전달한다.

a()메서드가 프로그램 종료와 관련이 있을것으로 예상된다, 해당 메서드를 살펴보자.

![image](https://user-images.githubusercontent.com/33051018/70045106-e07b1900-1606-11ea-826d-7b79ecfa485d.png)

전달받은 인자를 Title로 set한 이후, `OK` 버튼 클릭시 System.exit() 메서드가 호출되어 프로그램이 종료되는 것을 확인할 수 있다.

일단, 프로그램 종료를 막기 위해 해당 메서드 (`System.exit()`)를 후킹해보도록 하자.

```python
# Uncrackable level1 Hooking with Frida

import frida, sys

def on_message(message, data):
    print(message)

PACKAGE_NAME = "owasp.mstg.uncrackable1"

jscode = """

console.log("[*] start script");

    Java.perform(function() {

        console.log("[*] Hook System.exit");
        var hook_target = Java.use("java.lang.System");       
        hook_target.exit.implementation = function() {
            console.log("[*] System.exit called");
        }
});

"""

process = frida.get_usb_device().attach(PACKAGE_NAME)
script = process.create_script(jscode)
script.on('message', on_message)
print('[*] Running Hook')
script.load()
sys.stdin.read()

```



**`PACKAGE_NAME`은 동작하는 앱의 Full Package 명을 의미한다.**

위 코드에서는 `jscode`가 핵심이다.
**`frida`의 경우, 자바스크립트의 코드를 통해 동작한다.** 실제로는 C와 같은 코드로 구성되어 있으나, 자바스크리븥 코드를 통하여 접근하게 되어져 있기 때문에 API를 제공해주는 자바스크립트 코드를 쓰면 된다.

**`Java.use`를 통해 System.exit(후킹 대상) 함수가 존재하는 곳의 클래스 명을 적는다.** (Well-Known 메서드 들은 검색하면 바로바로 나옵니다!) (cf, https://docs.oracle.com/javase/9/docs/api/java/lang/System.html)

**`Java.use`를 통해 현재 클래스를 hook_target로 새로 구성하였다.** 새로 구성한 hook_target이 현재 앱에서 동작하고 있는 **`System.exit`메서드**가 존재하는 클래스를 대신하게 된다.

이 `hook_target.exit.implementation`의 의미는 새로 구성한 클래스의 `exit`메서드를 구성하는 것이다.

자바스크립트 내장함수를 이용해 로그를 찍도록 진행했다.

이와 같이 구성한 자바스크립트 코드를 그냥 로드하면 된다.

실행시 아래와 같은 결과를 확인할 수 있다.

![image](https://user-images.githubusercontent.com/33051018/70045839-27b5d980-1608-11ea-93d6-c98670fb43e0.png)

![image](https://user-images.githubusercontent.com/33051018/70045922-47e59880-1608-11ea-86d6-f5f11a5b140e.png)

이와 같이, `OK`버튼을 클릭했음에도 불구하고 앱이 죽지 않는다.

이제 앱이 죽지않는것 까지는 해결했다. 다음으로 `Secret String`값을 맞춰보자!

어떠한 입력값을 입력하고 `VERIFY`버튼을 클릭하면 검증 루틴에 따라 분기한다.

만일 틀린 값을 입력할 경우,

![image](https://user-images.githubusercontent.com/33051018/70046170-d22dfc80-1608-11ea-8ea5-18e26c1059ed.png)

위와 같은 그림을 확인할 수 있다.

그렇다면, 인증하는 루틴이 위치하는 코드를 살펴보자!

![image](https://user-images.githubusercontent.com/33051018/70046222-f25dbb80-1608-11ea-9c3e-49b829b6098b.png)

MainActivity 내 `verify`라는 메서드가 존재한다.

전달받은 입력값을 String값으로 변환하여 `obj`라는 변수에 초기화한다.

그 이후, 예상했던 바 와 같이 `a.a()`라는 메서드의 인자로 전달하여 검증 이후 해당 메서드의 반환값에 따라 분기를 진행한다. 그렇다면 입력값에 대한 검증 루틴은 `a.a()`메서드 내 존재할 것이기에 해당 메서드를 분석해보도록 한다.

![image](https://user-images.githubusercontent.com/33051018/70046401-541e2580-1609-11ea-809d-b7c2f7ba2958.png)

`a.a()`메서드 내용이다.

return의 과정에서 `str.equals()` 메서드를 통해 값을 확인하여 True 또는 False값을 리턴하도록 한다.

이번에는 저 bArr이라는 시크릿 키를 알아내고 무조건 True를 반환하도록 후킹하는 코드를 작성한다.

```python
import frida, sys

def on_message(message, data):
    print(message)

PACKAGE_NAME = "owasp.mstg.uncrackable1"

jscode = """

console.log("[+] jscode start");
Java.perform(function() {
    console.log("[+] Hooking str.equals()");
    var target = Java.use("java.lang.String");
    console.log(target)
    target.equals.implementation = function(arg1) {
        console.log(arg1);
        return true;
    }
});

"""

process = frida.get_usb_device().attach(PACKAGE_NAME)
script = process.create_script(jscode)
script.on('message', on_message)
print('[+] Hook Start')
script.load()
sys.stdin.read()

```

앞서 보였던 코드와 매우 유사하다.

`jscode`부분만 조금 차이가 있다.

이번 후킹의 대상은 `str.equals()`메서드였기에 해당 메서드의 클래스 , `java.lang.String`을 `Java.use()`의 인자로 전달해준다.

그 이후, java.lang.String.equals 메서드를 `implementation` 하여 해당 메서드를 새로 구성한다.

인자로 전달받은 값을, `console.log()`를 통해 출력시키고 매번 `true`값을 반환하도록 한다.

![image](https://user-images.githubusercontent.com/33051018/70048192-0b686b80-160d-11ea-93db-5c184426cb8a.png)

검증 루틴의 반환값을 `true`로 조작하였으니 Success값을 확인할 수 있었다.

또한, `arg1`을 출력시켰더니 아래와 같이 많은 문자열들이 출력되었다.

![image](https://user-images.githubusercontent.com/33051018/70047947-77969f80-160c-11ea-9078-0231213e6c60.png)

이 중에 `secret key`가 존재하며 해당 값은 밝히지 않겠다.

