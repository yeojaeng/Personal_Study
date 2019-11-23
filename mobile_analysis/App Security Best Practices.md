# App Security best-practices

---

앱의 보안을 강화하면 사용자의 신뢰와 장치에 대한 무결성을 유지하는데 도움이 된다.

본 문서에서는 앱 보안의 중대한 영향을 미치는 모범 사례들을 분석하고 이에 대한 대응방안을 작성한다.

---

# **1.**  **Enforce secure communication (안전한 커뮤니케이션 시행)**

 

앱과 다른 앱 간 또는 앱과 웹 사이트 간의 통신을 위하여 데이터를 교환할 때 해당 데이터들을 보호하며 앱의 안정성이 향상되며 주고받는 데이터 또한 보호받을 수 있다.

 

## **1.1.** **App chooser 표시**

 ![image](https://user-images.githubusercontent.com/33051018/69475843-8bc0ec80-0e15-11ea-80eb-78207846ed6d.png) 

Implicit intent 또는 non-exported content를 제공하는 경우, 사용자의 기기에서 2개 이상의 가능한 앱을 시작할 수 있는 경우 App chooser를 명시적으로 표시하는 것이 바람직하다.

해당 상호 작용 전략을 통해 사용자는 중요 정보등을 신뢰할 수 있는 앱으로 전송할 수 있다.

이에 대해서 보다 많은 정보를 알기 위해서는 ‘App chooser, Intent’ 관련 정보를 파악하는 것이 중요하다.

 

 

 

## **1.2.** **서명 기반 권한 적용**

 ![image](https://user-images.githubusercontent.com/33051018/69475854-b0b55f80-0e15-11ea-8eae-90798bbf42d7.png) 

두 앱의 사이에서 데이터를 주고받을 때에는 서 기반 권한을 적용하는 것이 바람직하다.

해당 권한은 사용자 확인이 필요하지 않은 대신 데이터에 접근하는 앱이 동일한 서명 키를 사용하여 서명하였는지 확인하여야 한다. 이를 통해 무결성을 검증하며 보다 안전한 서비스를 제공함으로써 권한은 더욱 능률적이고 안전한 사용자 환경을 제공할 것 이다.

이에 대해서 보다 많은 정보를 알기 위해서는 ‘APK Sign, Android:protectionLevel’ 관련 정보를 파악하는 것이 중요하다.

 

## **1.3.** **앱 컨텐츠 제공 업체 접근 제어**

 ![image](https://user-images.githubusercontent.com/33051018/69475857-c3c82f80-0e15-11ea-885f-c14ad584f91e.png)

앱의 컨텐츠 제공 업체에 대한 접근을 허용하지 않는 것이 바람직하다.

앱에서 소유하지 않은 다른 앱으로 데이터를 보내려는 경우가 아니라면 다른 개발자의 앱이 `ContentProvider` 앱에 포함된 개체에 접근하지 못하도록 명시적으로 허용하지 않아야 한다.

`android:exported` 속성은 Android 4.1.1(API level 16) 이하를 실행하는 기기에 앱을 설치할 경우 더더욱 중요하다. 해당 Android 버전에서는 `<provider>` 요소의 속성의 기본값은 `true`로 적용되어 있기 때문이다.

## **1.4.** **주요 정보 요청시 자격 증명 요청**

만일 사용자가 주요 정보 및 민감 정보등에 접근할 수 있도록 자격 증명을 요청하는 경우, 얼굴 인식 또는 지문 인식과 같은 PIN/ 암호/ 패턴등의 인증 절차를 통해 접근을 제어한다.

생체 인증 정보에 대한 요청의 자세한 내용은 ‘https://developer.android.com/training/sign-in/biometric-auth’ 에서 확인할 수 있다.

 

## **1.5.** **SSL 트래픽 사용**

 ![image](https://user-images.githubusercontent.com/33051018/69475864-e3f7ee80-0e15-11ea-916a-7adcd2fc5d0c.png)

HTTP 프로토콜 사용시에는 데이터 도청 및 감청의 위험이 존재하므로 잘 알려진 CA에서 발급한 인증서가 있는 웹 서버와 통신하는 경우 HTTPS 프로토콜을 사용한 통신을 적용하는 것이 바람직하다.

 

## **1.6.** **네트워크 보안 구성요소 추가**

앱 내에서 새로운 CA 또는 사용자가 지정한 CA를 사용하는 경우, 구성 파일에서 네트워크 보안 설정을 초기화할 수 있다. 해당 절차를 이용하면 앱 코드를 수정하지 않고 적용이 가능하다.

 

1)   App manifest 구성 선언

![image](https://user-images.githubusercontent.com/33051018/69475870-f07c4700-0e15-11ea-9e2c-7ea72c372ce3.png)

 

2)   XML 리소스 파일 추가 (res/xml/network_security_config.xml)

![image](https://user-images.githubusercontent.com/33051018/69475876-012cbd00-0e16-11ea-9944-bd211778c569.png)

일반 텍스트를 비활성화하여 특정 도메인에 대한 모든 트래픽이 HTTPS를 적용하여 통신할 수 있도록 지정한다.

또한, 개발 프로세스 `<debug-overrides>`중 이 요소를 사용하여 사용자 지정 인증서를 명시적으로 허용할 수 있다. 해당 요소는 앱의 릴리즈 구성에 영향을 주지 않고 디버깅 및 테스트 중 앱의 보안에 대한 주요 옵션을 재정의한다.

아래 예시는 앱의 네트워크 보안 구성 XML파일에서의 요소를 정의하는 방법을 보여준다.

![image](https://user-images.githubusercontent.com/33051018/69475884-0f7ad900-0e16-11ea-8153-b1c9c6aa5093.png)

 

## **1.7.** **나만의 트러스트 매니저 생성**

SSL을 적용하는 것이 바람직하나 SSL 트래픽 검사시 모든 인증서를 허용해서는 안된다.

신뢰 조건 정책을 철저히 설정하고 다음 조건 중 하나가 사용 사례에 적용되는 경우 발생하는 모든 SSL 경고 처리를 진행하여야 한다.

\-    새로운 사용자 또는 지정 CA가 서명한 인증서가 있는 웹 서버와 통신하는 경우

\-    사용중인 장치에서 해당 CA를 신뢰하지 않는 경우 

\-    네트워크 보안 구성을 사용할 수 없는 경우

이에 대해서 보다 많은 정보를 알기 위해서는 ‘HTTPS 및 SSL 적용, CertificateFactory, HttpsURLConnection, TrustManager’에 대한 정보를 파악하는 것이 중요하다.

 

## **1.8.** **WebView 객체 사용**

WebView 객체를 사용할 시, 신중하게 사용하는 것이 중요하다.

가능하다면 WebView 객체에 허용된 콘텐츠만을 로드하여야 한다. WebView 앱의 개체는 사용자가 통제 할 수 없는 사이트에 접근해서는 안된다. 또한 앱 객체의 내용을 완전히 제어하고 신뢰하지 않는 한 JavaScript 지원을 활성화 해서는 안된다.

만일, 앱 내에서 Android 6.0(API level 23) 이상을 실행하는 기기에서 JavaScript 지원을 활성화 해야하는 경우, 다음과 같이 웹 사이트와 앱 간에 통신하는 대신 HTML 메시지 채널을 이용하는것이 바람직하다.

 ![image](https://user-images.githubusercontent.com/33051018/69475891-26b9c680-0e16-11ea-8474-3dbc75b2fa63.png)

 보다 자세한 내용은 `WebMessage, WebMessagePort`에 대한 검색을 통해 파악할 수 있다.

 

# **2.**  **Provide the right permissions (올바른 권한 제공)**

앱이 보다 안전하게 작동하기 위해서는 권한에 대한 철저한 정책이 필요하다. 

즉, 작동을 위한 최소한의 권한만 요청해야 하며 가능하면 앱에서 더이상 필요하지 않은 일부 권한을 포기하도록 해야 한다.

 

## **2.1.** **인텐트를 사용한 권한 획득**

다른 앱에서 완료할 수 없는 작업을 완료할 수 있는 앱에 추가하지 않는 것을 권고한다.

대신 요청을 사용하여 이미 필요한 권한이 있는 다른 앱으로 요청을 연기하는 것이 좋다.

아래 예시는 인텐트를 사용하여 `READ_CONTENTS` 및 `WRITE_CONTACTS`권한을 요청하는 대신 연락처 앱으로 사용자를 안내하는 방법을 보여준다.

  ![image](https://user-images.githubusercontent.com/33051018/69475902-3a652d00-0e16-11ea-90d2-28fbcf5d3dc7.png)

또한, 앱이 스토리지 접근 또는 파일 선택 등과 같은 파일 기반 입출력을 수행하여야 할 경우, 시스템에서 앱을 대신하여 작업을 완료할 수 있으므로 특별 권한이 필요하지 않다. 보다 바람직한 방법은 사용자가 특정 URI에서 콘텐츠를 선택한 이후에는 호출 앱에 선택된 리소스에 대한 권한이 부여되는 것이다.

보다 자세한 내용을 위해선 `Common Intents, Intent` 키워드 검색을 통해 확인하는 것이 좋다.

 

## **2.2.** **앱 간 안전한 데이터 공유**

 

보다 안전한 방식을 통해 앱 컨텐츠를 타 앱과 공유하기 위하여 아래 모범사례를 제시한다.

\-    필요에 따라 읽기 전용 또는 쓰기 전용 권한을 시행한다.

\-    `FLAG_GRANT_READ_URI_PERMISSION` 및 `FLAG_GRANT_WRITE_URI_PERMISSION` 플래그를 사용하여 클라이언트에게 데이터에 대한 단발성 접근권한을 제공한다.

\-    데이터 공유시에는 `FileProvider`를 사용하여 `file://”URI` 가 아닌 `content://”URI`를 사용한다.

아래 예시는 URI 권한 부여 플래그 및 컨텐츠 제공자 권한을 사용하여 별도의 PDF 뷰어 앱을 표시하는 방법을 보여준다.

![image](https://user-images.githubusercontent.com/33051018/69475908-4c46d000-0e16-11ea-8f9d-cbbe2a9e2500.png)



# **3.**  **Store data safely (안전한 데이터 저장)**

앱 내에서 주요 정보 및 민감 정보에 접근해야 할 수도 있지만, 사용자는 앱이 적절히 보호한다고 믿는 경우에만 데이터에 대한 접근 권한을 앱에 부여한다. 



## **3.1.** **내부 저장소 내 개인 데이터 저장**

모든 개인 사용자 데이터를 기기 내부 저장소에 저장한다. (앱 마다 샌드박스로 표시 되어짐)

앱은 이러한 파일에 접근하기 위해 권한을 요청할 필요가 없으며 다른 앱은 해당 파일에 접근할 수 없다. 보안을 강화하기 위하여 사용자가 앱을 제거한다면 기기는 앱이 내부 저장소에 저장한 모든 파일을 삭제한다.

참고) 만일 저장하려는 데이터가 특히 중요한 경우, `EncryptedFile` 객체 대신 보안 라이브러리 에서 사용 가능한 오브젝트에 대한 작업을 고려하는것이 바람직하다.

아래 예시에서는 저장소에 데이터를 쓰는 한가지 방법을 보여준다. 

![image](https://user-images.githubusercontent.com/33051018/69475912-6385bd80-0e16-11ea-9e9f-990eadacbb6c.png)

관련 정보를 위해서는 `Internal Storage, FileInputStream, FileOutputStream,

 Context.MODE_PRIVATE`의 키워드를 통해 검색하는 것을 권고한다.

 

## **3.2.** **외부 저장소 사용 보안 조치 ( 범위가 지정된 디렉토리 접근 사용)**

기본적으로 Android 시스템은 외부 저장소 내에 존재하는 데이터에 대한 보안 제한을 시행하지 않으며 저장 매체 자체가 장치에 연결되어 있다는 보장을 하지 않는다. 따라서 외부 저장소 내에 안전한 접근을 위해서는 아래와 같은 보안 조치를 적용해야 한다.

 

**범위가 지정된 디렉토리 접근 사용**

앱이 기기의 외부 저장소 내 특정 디렉토리에만 접근을 하는 경우, 범위가 지정된 디렉토리 접근을 지정하여 그에 따라 기기의 외부 저장소에 대한 앱의 접근을 제한할 수 있다. 사용자의 편의를 위하여 앱은 디렉토리 접근 URI를 저장해 놓아야 앱이 디렉토리에 접근하려고 할 때 마다 사용자가 디렉토리에 대한 접근을 승인을 할 필요가 없다. 

![image](https://user-images.githubusercontent.com/33051018/69475937-90d26b80-0e16-11ea-8162-2727a68e5c74.png)

참고) 외부 저장소의 특정 디렉토리에 범위가 지정된 디렉토리 접근을 사용하는 경우, 앱이 실행되는 동안 저장소 내 포함된 미디어를 추출할 수 있다. 따라서 `Environment.getExternalStorageState()`를 통해 사용자 동작으로 인한 반환값 변경을 정상적으로 처리하기 위한 루틴을 포함해야 한다.

 

## **3.3.** **데이터 유효값 검증**

앱이 외부 저장소의 데이터를 사용하는 경우, 데이터의 내용 손상 또는 수정 여부를 확인해야 한다. 또한 앱에는 안정적인 형식이 아닌 파일을 처리하는 루틴이 포함되어야 한다.

아래 예시에서는 파일의 유효값을 검사하는 권한 및 로직을 보여준다.

**AndroidManifest.xml**

![image](https://user-images.githubusercontent.com/33051018/69475943-a5166880-0e16-11ea-982d-1e18086ee425.png)

 

**FileValidityChecker**

![image](https://user-images.githubusercontent.com/33051018/69475947-b65f7500-0e16-11ea-9d80-dafc847d75ff.png)

이에 대한 보다 많은 정보를 위해서는 `외부 저장소 사용, getExternalFilesDir()` 키워드를 통해 검색하는 것이 바람직하다.

 

## **3.4.** **캐시 파일 내 중요 데이터 저장 금지**

중요하지 않은 앱 데이터를 더욱 빠르게 접근하기 위해서는 기기 내 캐시에 해당 데이터를 저장한다. 만일 1MB보다 큰 데이터의 경우 `getExternalCacheDir()`을, 그 외의 경우 `getCacheDir()` 메서드를 사용하는것을 권고한다. 각 방법은 `File` 앱의 캐시 된 데이터가 포함된 객체를 제공한다.

아래 예시는 최근 다운로드한 파일을 캐시하는 방법을 보여준다.

![image](https://user-images.githubusercontent.com/33051018/69475955-c8411800-0e16-11ea-9117-d34cb7f6af39.png)

만일 getExternalCacheDir() 메서드를 공유 캐시 내에 앱 캐시를 배치하는데 사용하는 경우 사용자는 앱이 실행되는 동안 저장소가 포함된 미디어를 추출할 수 있다. 따라서 사용자 동작으로 인하여 발생하는 캐시 미스를 적절히 처리하는 로직을 포함해야 한다.

 

## **3.5.** **Private mode에서 SharedPreferences 사용** 

`getSharedPreferences()`의 `SharedPreferences` 객체를 생성하거나 접근하는 경우, `MODE_PRIVATE` 플래그를 사용하길 권고한다. 이러한 경우 앱만이 공유 환경 설정 파일 정보에 접근이 가능하다.

만일, 앱 간의 데이터를 공유하려면 `SharedPreferences` 개체를 사용하지 않고 **2.2 앱 간의 데이터를 안전하게 공유** 를 따르기를 권고한다.

 

# 4.  Keep services and dependencies up-to-date (서비스 및 종속성 최신 상태 유지) 

대부분의 앱은 외부 라이브러리 또는 장치 시스템 정보 등을 사용하여 특수 작업등을 진행한다.

이러한 경우, 앱의 종속성을 최신 상태로 유지하면 보다 안전한 커뮤니케이션 영역을 제공할 수 있다.

 

## **4.1.** **Google Play 서비스 보안 제공 업체 확인**

(해당 섹션은 Google Play 서비스가 설치된 기기를 타겟팅하는 앱에만 적용된다.)

앱이 Google Play 서비스를 사용하는 경우, 앱이 설치된 기기에서 해당 앱이 업데이트 되어 있는지, 최신 상태를 유지하고 있는지 확인한다. 이 검사는 UI Thread에서 비동기적으로 수행하는 것이 바람직하며 기기가 최신 상태가 아닐 경우 앱에서 인증 오류가 발생하여야 한다.

앱이 설치된 기기에서 Google Play 서비스가 최신 상태인지 확인하려면 SSL 악용으로부터 보호하기 위해 보안 제공자 업데이트 가이드의 단계를 따르기를 권고한다.

 

## **3.2.** **모든 앱 종속성 업데이트** 

앱을 배포하기 이전, 모든 라이브러리 또는 SDK 및 기타 종속성이 최신 상태인지 확인한다.

\-    Android SDK등의 대한 종속성일 경우, SDK Manager와 같은 Android Studio 내 업데이트 도구를 사용하는 것을 권고한다.

\-    타사 종속성의 경우, 앱 내에서 사용하는 라이브러리 웹 사이트를 확인하고 사용 가능한 업데이트 및 보안 패치를 진행한다.

 

# Reference List

[1] App Security best practices - https://developer.android.com/topic/security/best-practices#services-dependencies-updated

 

[2] Core app quality security checklist - https://developer.android.com/docs/quality-guidelines/core-app-quality#sc

 

[3]AppSecurity Improvement (ASI) Program - https://developer.android.com/google/play/asi.html

 

[4] Android Developers channel on Youtube - https://www.youtube.com/user/androiddevelopers

 