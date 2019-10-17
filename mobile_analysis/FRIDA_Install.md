# About Frida

---

이번 글은 `Frida`에 대한 소개글이다.
[FRIDA](https://www.frida.re/docs/examples/android/) 참고

### [ What is Frida? ]

---

><img width="361" alt="스크린샷 2019-10-17 오후 1 42 48" src="https://user-images.githubusercontent.com/33051018/66978229-09416080-f0e4-11e9-8046-c673ddb33092.png">
>
>
>
>`Frida`란 파이썬 기반의 라이브러리 + 명령어로 구성되어 있고 Native App 에 대한 후킹을 통해 분석에 도움을 줄 수 있는 프로그램이다.
>
>Frida는 JS Injecton을 이용하여 Windows, Linux , IOS, Android, macOS ...등 기반의 네이티브 앱에 대해 후킹을 돕는 `파이썬 라이브러리`이다. (갓갓 파이썬!)
>
>`Frida`는 크게 패키지와 서버로 이루어져 있으며 분석하는 장치에는 패키지를 설치하고 분석의 대상이 되는 
>모바일 또는 에뮬레이터에는 서버를 삽입하여 구동하게 된다.
>
>대표적으로는 IOS, Android 등 모바일 분석 덕에 널리 알려져 있으나 타 플랫폼에서도 사용이 가능하기 때문에 확장적인 면에서 매우 용이하다.



### [ Install frida Lib ]

---

>필자는 macOS를 사용중이므로 macOS 기반 설치방법임을 미리 알린다.
>
>`pip`을 다운로드 한 이후 , `pip`을 통해 `frida`를 설치하도록 한다.
>	`$ pip install frida`
>
>Frida Server를 AVD에 삽입한 뒤 구동시킨다.
>
>이는 모바일 또는 에뮬레이터에 연결시킨 이후 실행하여아 한다.
>
>[Frida Server](https://github.com/frida/frida/releases) 설치파일 다운로드
>
><img width="609" alt="스크린샷 2019-10-17 오후 2 18 26" src="https://user-images.githubusercontent.com/33051018/66979557-0432e000-f0e9-11e9-9ad5-415a20cb8163.png">
>
>adb push 명령어를 통해 Frida-server 파일을 /data/local/tmp 경로로 밀어넣는다.
>
><img width="270" alt="스크린샷 2019-10-17 오후 2 20 04" src="https://user-images.githubusercontent.com/33051018/66979634-3e9c7d00-f0e9-11e9-9e9b-e7088bd4c538.png">
>
>그 이후, shell에 붙어서 해당 경로로 이동한다.
>
>해당 파일의 권한을 `755`로 변경 한 뒤, `./frida-server &` 명령을 통해 실행시킨다.
>
>그 이후, 실제 서버가 정상적으로 작동중인지 `ps | grep frida`를 통해 확인한다.
>
><img width="645" alt="스크린샷 2019-10-17 오후 2 23 18" src="https://user-images.githubusercontent.com/33051018/66979806-c97d7780-f0e9-11e9-8d62-10376b63f97a.png">
>
>위와같은 결과가 나온다면 정상적으로 서버가 작동중인 것이다.
>
>정상적으로 설치가 완료되었다.
