# Android App Hooking with FRIDA

---

본 글에서는 앞서 설치한 FRIDA를 사용하여 `App Hooking` 예제를 풀며 공부한 내용을 작성한다.

문제 파일은 아래 링크에서 다운로드 받을 수 있다.

[Uncrackable1 Donwload Link](https://github.com/OWASP/owasp-mstg/tree/master/Crackmes)



###[분석 환경]

---

>**OS** : macOS Mojave
>
>**Tools** : Frida, adb, Python 3.7.4, Genymotion



###[문제 풀이]

---

><img width="524" alt="스크린샷 2019-10-17 오후 2 36 28" src="https://user-images.githubusercontent.com/33051018/66980493-106c6c80-f0ec-11e9-96f5-726f3d411793.png">
>
>`adb install`명령어를 통해 다운로드 받은 .apk파일을 설치한다.
>
>그 이후, AVD에서 해당 앱을 실행시켜본다.
>
><img width="564" alt="스크린샷 2019-10-17 오후 2 55 02" src="https://user-images.githubusercontent.com/33051018/66981250-2418d280-f0ee-11e9-9b56-034086c3842c.png">
>
>프로그램을 실행시키면 **루팅 탐지**가 동작되어 `OK`버튼 클릭시 앱이 죽는다.
>
>루팅 탐지 루틴와 관련된 문제임이 느껴진다.
>
>일단 `jadx`를 이용해 `apk` 코드를 분석해보도록 한다.
>
>안드로이드 앱이 실행되면 가장 우선적으로 실행되는 `onCreate()`부터 살펴보자.
>
><img width="335" alt="스크린샷 2019-10-17 오후 3 10 36" src="https://user-images.githubusercontent.com/33051018/66982043-51668000-f0f0-11e9-9c4f-4917bcf66103.png">
>
>`MainActivity` 의 `onCreate()` 부분이다.
>
>`onCreate` 인자로 전달받는 `bundle` 객체에 대하여 잠깐 짚고가자! 이건 안드로이드 개발에서도 매우 중요!
>
>>**[Bundle]**
>>
>>최근 안드로이드 개발시 `Activity`에서 `Fragment` 를 많이 사용하는 추세로 넘어왔다.
>>`Fragment`를 사용하다 보면 `Bundle`을 통해서 데이터를 전달하는 방식을 사용하게 된다.
>>
>>이 `Bundle`을 활용하여 `String`, `int` 등 기본 `Type`은 보다 쉽게 전달할 수 있다.
>>
>>즉, `Bundle`은 클래스로 여러가지의 타입의 값을 저장하는 Map 클래스이다.
>>자바 내에는 구조체가 없기에 클래스를 이용하므로, C언어 에서의 구조체라고 생각하면 이해가 쉽다.
>>
>>**예를들면 `string`값을 `Bundle` 클래스에 Mapping(대응, 변환) 하는 것이다.**
>
>`onCreate()` 부분을 다시 살펴보면 , 분기함에 따라 `a()`함수의 인자를 다르게 전달하고 있다.
>
>첫번째 분기문에서 `if (c.a() || c.b() || c.c()) `를 통하여 `Rooting Detection`을 진행하고 있으며
>
>마찬가지로 `if (b.a(getApplicationConetext()))`를 통하여 `Debugging Detection`을 수행하고 있다.
>
>
>그렇다면, 해당 조건문들이 참이되어 실행되는 `a()` 함수에 대해 살펴보자.
>
><img width="555" alt="스크린샷 2019-10-17 오후 3 25 19" src="https://user-images.githubusercontent.com/33051018/66982979-6512e600-f0f2-11e9-8cb3-8c1506542346.png">
>
>`onClick` 핸들링을 통해 버튼 클릭시 `System.exit(0)`함수가 호출되어 앱이 죽도록 코드가 작성되어있다.
>
>그렇다면, 해당 함수를 후킹하여 버튼을 클릭하여도 앱이 죽지 않도록 하자.
>
>```python
>import sys
>import frida
>
>def on_message(message,data):
>    print "[%s] -> %s" % (message, data)
>
>PACKAGE_NAME = "owasp.mstg.uncrackable1"
>
>jscode = """
>    Java.perform(function() {
>        console.log("[*] Hooking calls to System.exit");
>        exitClass = Java.use("java.lang.System");
>        exitClass.exit.implementation = function() {
>            console.log("[*] System.exit called");
>        }
>    });
>"""
>
>try:
>    device = frida.get_usb_device(timeout=15)
>    pid = device.spawn([PACKAGE_NAME]) 
>    print("App is starting ... pid : {}".format(pid))
>    process = device.attach(pid)
>    device.resume(pid)
>    script = process.create_script(jscode)
>    script.on('message',on_message)
>    print('[*] Running Frida')
>    script.load()
>    sys.stdin.read()
>except Exception as e:
>    print(e)
>
>
>
>```
>
>
>
>