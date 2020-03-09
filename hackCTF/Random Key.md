**HackCTF - Random Key**

| layout | title                         | auther   | categories | tags           |
| ------ | ----------------------------- | -------- | ---------- | -------------- |
| post   | HackCTF - Random Key | Y3oj4eng | writeup    | writeupwargame |

# Analysis
---

## `file & checksec`
```bash
mac at ubuntu in ~/Desktop/hackCTF
$ file random 
random: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/l, for GNU/Linux 2.6.32, BuildID[sha1]=450986f67ff81eb7b09287fc517c25f9ba89bac6, not stripped

mac at ubuntu in ~/Desktop/hackCTF
$ checksec random 
[*] '/home/mac/Desktop/hackCTF/random'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
```

`ELF 64 bit` 바이너리이며 `NX` 보호기법이 적용되었다.
따라서, 스택과 힙 그리고 데이터 영역의 실행권한이 제한된다.
f본격적 분석에 앞서 바이너리를 한번 실행시켜보도록 한다.

```bash
mac at ubuntu in ~/Desktop/hackCTF
$ ./random 
============================
======= 인증 프로그램 ======
============================
Input Key : AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
Nah...

```
바이너리를 실행하면 일련의 문자열을 출력한 뒤, 값을 입력받고 이에따라 분기한다.

느낌이 특정 시리얼 값을 찾아내야 하는 문제 같다.

메인 함수부터 살펴보도록 한다.

```c
int __cdecl __noreturn main(int argc, const char **argv, const char **envp)
{
  unsigned int v3; // eax
  int v4; // [rsp+0h] [rbp-10h]
  int v5; // [rsp+4h] [rbp-Ch]
  unsigned __int64 v6; // [rsp+8h] [rbp-8h]

  v6 = __readfsqword(0x28u);
  setbuf(_bss_start, 0LL);
  v4 = 0;
  v3 = time(0LL);
  srand(v3);
  v5 = rand();
  puts("============================");
  puts(asc_400948);
  puts("============================");
  printf("Input Key : ", 0LL, *(_QWORD *)&v4, v6);
  __isoc99_scanf("%d", &v4);
  if ( v5 == v4 )
  {
    puts("Correct!");
    system("cat /home/random/flag");
    exit(0);
  }
  puts("Nah...");
  exit(0);
}
```

로직은 매우 간단하다.

`v3` 변수를 `time(0)`의 결과값으로 초기화한다.

해당 변수에는 1970년 1월 1일 자정부터 현재까지 흐른 시간의 초를 반환한다고 한다.

이후 이를 `seed`로 설정하여 난수값을 생성한 뒤 `v5`에 저장한다.

다음으로 사용자에게 값을 입력받고 이를 `v4`에 저장하여 `v5`와 값을 비교한다.

두 값이 같을 경우 `flag`를 읽어오고 다를 경우 `Nah...` 문자열과 함께 프로그램을 종료한다.

이 문제를 풀기 위해서는 `v5`의 값을 알아내는 것이 핵심이다.

결론적으로 `c` 언어를 이용해야 할 것 같고 `.so` 파일로 컴파일하여 파이썬 내에서 불러오는 방법도 있으며 그냥 프로그램의 출력값을 nc를 통해 `pipe`로 전달하는 방법도 있다.

따라서 그냥 `c`언어로 위와 같은 로직으로 `rand` 값을 만들어 출력하는 코드를 작성하여 컴파일 한 뒤 `nc` 연결로 입력값을 전달했다.



# Exploit
---

### answer.c
```c
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main(void) {
    
    int v3;
    int answer;
    v3 = time(0);
    srand(v3);
    answer = rand();
    printf("%d\n", answer);

}
```

해당 코드를 `gcc`를 이용해 컴파일 한 뒤 `nc`를 이용하여 서버에 전달한다.

`./answer|nc ctf.j0n9hyun.xyz 3014`


