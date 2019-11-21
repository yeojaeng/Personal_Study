# Android #1

---



### Architecture

- Android Platform Architecture
  - Linux Kernel
  - Native Library
  - Android Runtime
  - Java API Framework



### Android Runtime

- Android based on Android API which almost like Java

- Java application over JavaVM -> Android application Dalvik

- ![image](https://user-images.githubusercontent.com/33051018/69334996-3b278300-0c9f-11ea-9ee1-24117ea55461.png)

- 안드로이드 대부분의 앱은 자바 기반으로 만들어진다.

  자바를 빌드하면 .class 파일이 생성되며 이를 실행하기 위해서는 JavaVM이 필요하다.

  하지만, 자바로 열심히 개발해봐야 디컴파일 하면 코드가 모두 보인다. 이를 방어하기 위해 난독화 등을 진행하지만 이는 절대적 방어 솔루션이 아닌 그저 분석을 방해하는 목적으로 사용된다.

  **애초에 개발시 코드를 시큐어하게 작성한다면 아무런 문제가 없다.**

- 안드로이드는 Dalvik Byte code로 변환을 진행한다.
  Dalvik VM은 안드로이드 프레임워크 내부에 위치한다.



- Dalvik VM is a New JVM made by Google

  - Register - based versus stack - based JVM
  - Diff set of Java libraries than JDK

- Dalvik VM has been optimized for mobile devices

  - Non Powerful CPU
  - memory shortage
  - Dalvik Executable .dex format is compact
  - run multiple VMs efficiently
    

- 대형 앱이 느린 이유 : 앱 안에 정말 많은게 들어있기 때문이다. 
  `.dex`파일은 기본적으로 파일 안에 담을 수 있는 함수가 65536개로 제한되어있다.

  `.dex`파일이 2개라면 최소한 함수가 65537개 사용되었다는 의미.

  현 상태로 app size를 살펴보면 용량이 엄청 큰 앱이 많이 존재한다.

  아무리 잘 만들어도 VM을 거쳐서 `IL(intermediate Language)`로 해석한 뒤 실행되어지는 구조.

  ![image](https://user-images.githubusercontent.com/33051018/69335409-40d19880-0ca0-11ea-949e-872425ace266.png)

  -> 이는 느릴 수 밖에 없음. 안그래도 느린 자바를 가상머신에서 실행하니 다소 퍼포먼스가 좋지 않음.



* Davlik VS ART

  * Dalvik : < Android 5.0

  * ART : >= Android 5.0

  * ART and Dalvik are compatible runtimes running Dalvik bytecode

  * Apps developed for Dalvik should work when running with ART
    ART -> Dalvik , !Dalvik -> ART

  * 앱을 설치하는 동안 최대한 앱을 빠르게 실행할 수 있는 기능 및 개념이 ART안에 존재한다.
    ( ART는 설치단계에서 달빅 바이트 코드를 변환하는 단계를 실행한다. )

    달빅에서 ART로 온전한 Converting은 불가능, 그러나 ART에서 달빅으로의 Converting은 완벽한 호환성을 제공한다.
    

  * ![image](https://user-images.githubusercontent.com/33051018/69335813-d836eb80-0ca0-11ea-853f-82db43bdb7d0.png)

    런타임 Dalvik 과 ART는 구조적 차이가 존재한다.

    두 런타임 모두 `Input`은 `DEX`로 동이라핟.

    그러나, 달빅은 이를 `odex`로 변환하고, ART는 이를 `oat`로 변환한다.

    또한, 달빅은 VM 위에서 돌고 ART는 그냥 쉘 상에서 돈다.

    -> 속도 차이가 존재할 수 밖에 없다.

  * ART는 한꺼번에 다 Optimizing, Ahead Of Time,  달빅은 한 줄 한 줄 Just In Time

  * JIT : 앱이 실행되면 Dalvik bytecode는 JIT 방식에 따라 머신코드로 변환
    ART : 앱이 설치되면 bytecode는 ART로 변환

* Comparison

  * **Dalvik**

    * Lower storage, Space cossumption from JIT

    * **Take a time for cache, Faster booting time**

    * Lower internal Storage(Old model)

      

  * **ART**

    * Fast load time, lower processor usage
    * Long booting time (cause when the boot, translated into )
    * More internal storage -> Compiled app + APK



### Android Rooting

- Android devices such as tabs, smartphone's etc, by default comes with a set of restricted set of permissions for its users

- By rooting an android device a user can bypass all the restrictions implemented by hardware manufacturers and carries

- Advantage of Rooting

  - Increasing 🔋  Life
  - Using custom Recoveries, Rom's
  - Increasing speed of the device
    

- Disadvantage of Rooting

  - It can be Brick or breaking your device beyound repair
  - Security ( Malware, Virus )
  - Voiding Warranty
  - Data Loss
    

- Detection

  - Almost rooting detection

    - Focus on the final result(Exe file) on some specified path

  - Disadvantage

    - Detection based on signature(Fixed file name and path)

      -> but easy to bypass

    - Because of false positive, use limited signature

  일반적인 루팅 탐지는 특정파일 존재 유무를 확인한다. 반대로 생각해보면 우회가 가능하다.

  루팅을 탐지한다 -> 일반적으로 생각해보면 이기기 힘든 게임

