# Android Structure

---



### Android Program

- Program -> APK
  - Android application package
- 흔히들 알고 있는 앱의 파일 포맷은 apk
  apk 는 '서명된' zip파일.

- How to Analysis?
  - 우선적으로 Manifest.xml파일을 본다, 이에는 안드로이드 앱의 구동을 위한 내용을 명시해놓음.
  - AndroidManifest.xml
    - Encoded XML File
    - Description
    - Package name
    - Permissions
    - SDK Version
    - **intent** : 액티비티 등의 전환이 일어날 때 호출이나 메시지를 전달하는 매개체



- classes.dex

  - .dex(Dalvik Executable) is a compiled android app code file
  - Compiler(java) = .dex
  - Have to understand the DEX Structure

  .dex파일은 Android에서 App이 구동하기 위한 핵심적 파일 포맷이다. 

  Dalvik이 인식할 수 있도록 `.class`파일을 바이트 코드로 변환된 파일. 

  .dex파일을 jvm 코드로 디컴파일하여 .class파일을 추출할 수 있다면, Android App의 Java코드 또한 추출 가능하다.

  자바를 기반으로 코드를 짜면 안드로이드 프레임워크를 통해 달빅 코드로 바꾸는데 그 내용들이 .dex안에 들어가있다.



### Android Program Info

- ADB ( Android Debug Bridge )

  - ADB는 Android를 위한  Debugging Tool이다.

    Debug Bridge는 JTAG와 유사한 개념으로, Android가 올라가는 Target Board의 Debugging에 사용된다.

    ![image](https://user-images.githubusercontent.com/33051018/69339710-4e3f5080-0ca9-11ea-89ee-f1b69f16ec08.png)

    