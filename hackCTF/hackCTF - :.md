# HACKCTF - /

---



![image](https://user-images.githubusercontent.com/33051018/68993832-b532c300-08bf-11ea-8c1b-73b112001fe9.png)



### 문제풀이

---

HackCTF Web문제 1번 '/' 이다.

문제를 클릭하면 url이 있으며 해당 url로 이동해본다.



![image](https://user-images.githubusercontent.com/33051018/68993853-d5628200-08bf-11ea-87c3-e36c7bcbde97.png)



...? 다짜고짜 ""**Hidden Flag**"라는 문자열을 상단에 띄워주며 위와 같은 사진을 띄워준다.

음... 다소 당황스럽다. 사진에 플래그가 숨어있는 스테가노그래피 문제인가?

별 생각이 다 들었다, 페이지 소스도 살펴보았으나 별다른 특이점을 찾을수 없었다.

이 문제는 **Web** 분야 문제이다. 또한 사진의 출처는 'www.irobotnews.com'이다.

![image](https://user-images.githubusercontent.com/33051018/68993915-5883d800-08c0-11ea-821f-12289682d290.png)

설마 robots.txt에서 robots를 연상시키기 위한 의미에서 robot인가...? 싶어서 robots.txt로 이동해봤다

![image](https://user-images.githubusercontent.com/33051018/68993960-9254de80-08c0-11ea-86c8-528b339fc388.png)

`ctf.j0n9hyun.xyz/robots.txt` 페이지로 이동한 결과 위와 같은 페이지를 확인할 수 있었다.

위 `robots.txt`의미는 홈페이지의 디렉토리 중 /robot_flag/ 디렉토리의 일부만 검색엔진의 노출을 차단하겠다는 의미이다.

`flag`라는 단어가 매우 의미심장하게 보였기에 해당 디렉토리로 이동해보았다.

**굳...**



### 배운점

---

`robots.txt` 란, 

인터넷 검색엔진에서 보안이 필요한 내용이 검색엔진에 의해 검색등을 통한 노출이 되지 않도록 웹 페이지를 작성하는 방법을 기술하는 텍스트파일이다.

모든 검색로봇이 해당 표준을 따르지는 않으나 일반 웹 사이트 개발자들이 손쉽게 작성할 수 있기 때문에 이용이 확산되고 있다.



