## [Android] Dalvik(JIT) vs ART(AOT)

---



>일반적으로, 컴파일 언어는 `CPU`의 `Architecture`와 `Platform`의 환경에 맞추어 기계어로 번역된다.
>
>즉, 사람이 작성한 언어를 CPU가 `readable`한 언어로 번역하는 것이다.
>
>그러나 `Java`의 경우, 하나의 `CPU`의 `Architecture` 또는 환경에 맞추는 것이 아닌 `Byte code`로 컴파일 되며, 이를 실행하기 위해서는 `VM(Virtual Machine)`이 필요하다.
>
>자바는 `Byte code`만으로 다양한 `Architecture`또는 플랫폼에서 작동할 수 있도록 하는 크로스 컴파일을 위함이 목표이다.
>
>일반적으로 사용하던 `JavaVM`은 라이선스의 문제로 구글이 `Dalvik VM`을 개발하여 안드로이드에 넣었다.
>
>`Dalvik VM`과 `ART VM`에 대해 비교해본다.



### Dalvik VM

---

>- 32bit만 지원
>- **JIT** Compiler 사용. (Just - In - Time)
>- <u>앱 실행할 때 마다, 컴파일 진행.</u>
>- CPU, 메모리 사용량 높음.
>- 설치 파일의 크기가 작음.
>- 배터리 소모량 큼 -> 앱 실행시 마다 컴파일을 진행하기 때문에 전반적인 하드웨어에 상당한 부하가 생김.



### ART VM

---

>- 32bit, 64bit 지원
>- **AOT** Compiler 사용. (Ahead - Of - Time)
>- 안드로이드의 `Nougat` 버전 부터, JIT와 AOT를 모두 탑재하여 최초 설치시에는 **JIT**를 이용하여 설치시간과 용량을 적게 소모한 뒤, 차후 기기를 사용하지 않을 때나 충전 중일 경우 컴파일을 조금씩 진행하여, 자주 사용되는 앱을 AOT 방식으로 전환하도록 변환함.
>- <u>설치시에 컴파일을 진행하여 모든 코드를 변환하고 저장 -> 실행할 때 마다 저장해놓은 변환된 코드를 읽어들인다.</u>
>- CPU, 메모리 사용량 낮음.
>- 설치 파일의 크기가 큼.
>- 배터리 성능 향상.
>- Garbage Collector 향상.
>
>