# [OWASP] Uncrackable level 2

---

해당 apk파일을 다운받고 `adb`를 통해 install 을 진행한다.

![image](https://user-images.githubusercontent.com/33051018/70050910-6309d580-1613-11ea-8f7a-a869fa955f50.png)

정상적으로 앱을 설치하면 기기 내에서 위와 같은 그림을 확인할 수 있다.

일단 바로 실행시켜보도록 한다.

![image](https://user-images.githubusercontent.com/33051018/70050964-7f0d7700-1613-11ea-869a-70073ab98eb3.png)

이전에 풀었던 Uncrackable level 1 과 똑같이 루팅 검증을 진행하고 있다.

해당 부분을 확인해보자.

![image](https://user-images.githubusercontent.com/33051018/70051091-baa84100-1613-11ea-98b8-515565ac96be.png)

`b.a()`, `b.b()`, `b.c()` 메서드를 통해 루팅을 검증한다.

![image](https://user-images.githubusercontent.com/33051018/70051191-ed523980-1613-11ea-9b1e-5545da044ca2.png)

3개의 메서드를 하나하나 후킹하여 반환값 조작하는 것은 매우 비효율적이다.

![image](https://user-images.githubusercontent.com/33051018/70051254-0955db00-1614-11ea-985f-3b86142b1fda.png)

따라서, `System.exit()`메서드 하나만 후킹하여 프로그램이 죽는것을 막아보도록 한다.

```python
import frida, sys

def on_message(message, data):
    print(message)

PACKAGE_NAME="owasp.mstg.uncrackable2"

jscode = """

console.log("[+] jscode start");

    Java.perform(function() {

        console.log("[+] Hook start");
        var target = Java.use("java.lang.System");
        target.exit.implementation = function() {
        console.log("[+] System.exit() called");
        }

});

"""
process = frida.get_usb_device().attach(PACKAGE_NAME)
script = process.create_script(jscode)
script.on('message', on_message)
print('[+] Running Hook')
script.load()
sys.stdin.read()
```

![image](https://user-images.githubusercontent.com/33051018/70052943-ba11a980-1617-11ea-897a-43a11291a87e.png)

![image](https://user-images.githubusercontent.com/33051018/70052956-c433a800-1617-11ea-8901-27a0f38df8f6.png)

계획대로 `OK`버튼을 클릭하여도 기존 `system.exit()`가 호출되지 않도록 되었다.

다음으로, `Secret String`을 해봤다.

![image](https://user-images.githubusercontent.com/33051018/70053078-ffce7200-1617-11ea-839b-bc440103bd83.png)

역시 에러가 뜬다. 해당 검증 루틴을 확인해보자.


![image](https://user-images.githubusercontent.com/33051018/70053220-4ae88500-1618-11ea-9554-deeea3626b5d.png)

이번에도 `verify`라는 메서드에서 검증을 진행한다.

입력받은 문자열을 `str`로 변환하여 `obj`라는 변수에 초기화한다.

이후, `MainActivity.m.a()`에 인자로 전달하여 해당 반환값이 1인경우 `Success!`를 출력한다.

`MainActivity.m.a()`를 살펴보도록 하였으나, 해당 메서드는 외부 라이브러리에서 참조되었으며 볼 수가 없었다.

![image](https://user-images.githubusercontent.com/33051018/70053499-ed086d00-1618-11ea-9ad6-9afa3064d1ff.png)

방법을 찾던 도중 `CodeCheck`라는 클래스를 확인할 수 있었다.

![image](https://user-images.githubusercontent.com/33051018/70053604-2214bf80-1619-11ea-8a83-435891dbe1f5.png)

이를 통해, `MainActivity.m.a()`는 `Codecheck.a()`와 같음을 알 수 있다.

`Codecheck.a()`메서드를 살펴보자!

![image](https://user-images.githubusercontent.com/33051018/70053666-407abb00-1619-11ea-9433-cee224bf2068.png)

유효성 검사는  bar()라는 외부 라이브러리에서 진행한다.

