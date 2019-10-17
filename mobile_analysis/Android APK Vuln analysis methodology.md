# Android APK Vuln analysis methodology

---

### Android APK 취약점

- Web/ PC Software 뿐만 아니라 android APK에 대해서도 수많은 취약점이 존재한다.

  모바일 OS 시장에서 구글 안드로이드의 독주가 두드러지고 있으며 이러한 모바일 OS 시장에서 안드로이드의 성장은
  안드로이드 소프트웨어 발전에도 큰 영향을 주고 있다.

  그러나, 안드로이드 소프트웨어는 그 구조상 `Reverse Engineering`에 취약하게 되어있다.

  안드로이드 소프트웨어는 가상머신 위에서 동작하며 이는 자바를 기반으로 작성된 가상머신이다.

  이렇게 생성된 `software`는 하나의 소스코드로 다양한 플랫폼에서 동작 즉, `multi-platform` 동작이 가능하다는 장점이 존재한다.

  그러나 가상머신이 코드 해석 참고를 위해 소스코드에 있는 다양한 정보를 완성된 프로그램에 포함해야 하므로

  디컴파일을 통해 코드 내부를 분석하기 쉬운 단점이 존재한다.

  실제로 다른 모바일 OS에 비하여 안드로이드에서 동작하는 악성코드가 많은 것은 `Decompile`에 취약한 구조 때문이다.

  안드로이드 플랫폼 구조 자체를 변경하면 보안성이 상승할 수 있으나, 이미 수많은 사용자에 의해 사용중인 플랫폼의 구조를 변경하는것은 사용자 편의 측면에서나 비용적인 측면에서 적용하기 쉽지 않은 일이다.



* ###Android Vuln Analysis Guide
  * 국내의 경우

    1. #### [모바일 전자정부서비스 앱 소스코드 검증기준](https://www.kisa.or.kr/public/laws/laws3_View.jsp?cPage=6&mode=view&p_No=259&b_No=259&d_No=60&ST=T&SV=)

    2. #### [모바일 대민 서비스 보안취약점 점검 가이드](https://www.kisa.or.kr/public/laws/laws3_View.jsp?cPage=6&mode=view&p_No=259&b_No=259&d_No=58&ST=T&SV=)

  * 국외의 경우

    1. [OWASP Top 10](https://www.owasp.org/index.php/Mobile_Top_10_2016-Top_10)

  

* ### Android APK Vuln Analysis tool

  1. #### ADB (Android Debug Bridge)

     - PC에서 Android를 연결하여 CLI 기반 제어 기능을 지원하는 도구

     - ADB를 통하여 Android를 원격으로 제어하거나 직접 Android에 대한 권한 등을 획득하는 등 다양한 명령어를 분석에 응용한다.

       

  2. #### Apktool

     * APK 파일을 reversing / decoding / repacking등을 하는데 사용하는 도구.

     * APK 내 xml 또는 resource 파일에 대한 extract를 지원

       

  3. #### ABE (Android Backup Extractor)

     * APK파일을 설치한 안드로이드의 Data 백업 파일을 해제하는데 응용되어진다.

     * 안드로이드에서의 .adb에 대한 파일을 .tar파일로 변환한다.

       

  4. #### dex2jar

     * APK파일에서 추출한 .dex파일을 .jar파일로 변환해준다.

     * .dex파일의 경우 java의 class파일의 중복을 제거한 파일로써, dex2jar를 통해 .jar 파일 획득 가능

       

  5. #### JD-GUI

     * Java에서 사용하는 Class 파일을 java 소스코드로 디컴파일해주는 소프트웨어
     * APK파일로 부터 .jar파일을 extract한 뒤, java 소스로 변환하는데 이용된다.

  