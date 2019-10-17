# Arm Assembly

---



* **ARM (Advanced Risc Machine)**

  x86으로 대표되는 CISC 라인과는 반대로 모바일이 대세가 되며 ARM(RISC) 프로세서도 많이 사용되어 지고 있다.

  이번엔 ARM architecture 에 대해서 공부해본다.



* **Thumb mode / Arm mode**

  ARM 과 x86의 가장 큰 차이점은 `Thumb` 모드의 존재다. ARM 자체가 mobile/embedded 등 PC와는 다른 환경에 맞춰 설계하였기 때문에 저전력이 핵심 기술중 하나였으며, 처음 설계될 당시 임베디드 계열에서는 32bit가 아닌 16bit가 추세였다고 한다. 이러한 여러가지 상황에 맞추기 위해 2가지 모드를 지원하게 되었고 당연 리버싱을 하게 될 때도 이를 고려해야 한다. 

  >* `Thumb mode`
  > * 레지스터 : R0 ~ R15 (총 16개)
  > * 기계어코드의 길이 : 16bit (2bytes)
  >
  >
  >
  >* `ARM mode`
  >
  > * 레지스터 : R0 ~ R7 (8개)
  > * 기계어코드의 길이 : 32bit (4bytes)
  >
  >* `Thumb <-> ARM 전환`
  >
  > * `BLX` / `BX` 등 `X` 로 끝나는 분기문 명령으로 모드를 전환한다.
  >
  >
  >
  >* `Calling Convention`
  >
  >`x86` 에서는 `cdecl`, `fastcall`, `stdcall`드ㅇ의 다양한 함수 호출규약이 존재했다.
  >
  > * R0 ~ R12 : 범용 레지스터, 인자값 및 임시 게산 저장소 등
  > * R13(SP) : Stack Pointer, x86의 ESP와 비슷한 역할
  >
  >
  >* `ARM Instruction`
  >
  >처리 속도를 우선시 할 경우 Thumb 명령어 보다는 ARM 명령어가 유리하다.
  >
  >왜냐하면 Thumb 명령의 경우 16bit라서 처리가 빠를것으로 예상하지만 ARM은 언제까지나 32bit processor이라는 점 때문이다. 이 프로세서에서 16bit 명령어를 처리하기 위해선 이를 지원해주는 하드웨어적 지원이 필요한 것이고 이 하드웨어의 지원을 받아서 16bit 명령어가 32bit 명령어로 확장되어서 프로세서에게 전달되어 처리되는 것이다.
  >즉, 32bit 버스라고 해서 한번에 16bit 명령을 두번 실행하지 않는다는 것이다.
  >
  >



* **자주 사용하는 명령어**

  1) **산술 연산**

  * ADD : +연산 , Rd = Rn + Rm
  * SUB :  -연산 , Rd = Rn - Rm

  

  2) **비트 연산**

  * AND : & 비트 연산, Rd = Rn & Rm

    Ex 1) AND R0, R1, #0xF8

    	-> R1과 0xF8을 AND 연산하여 R0에 저장.

    Ex 2) AND R0, R1, R2, lsl #2

    	-> R2를 left shift 2 ( << 2)한 값과 R1을 AND 연산하여 R0에 저장

  * ORR : | 비트 연산, Rd = Rn | Rm

    Ex 1) ORR R0, R1, #0x2

    	->  R1과 0x2를 OR 연산하여 R0에 저장.

  * EOR : ^ 비트 연산, Rd = Rn ^ Rm

    Ex 1) EOR R0, R1, #0xF8

    	-> R1과 0xF8을 XOR 연산을 진행하여 그 결과값을 R0에 저장

  * BIC : &! 비트 연산, Rd = Rn & !Rm

    Ex 1) BIC R0, R0, #0x3



	3) **대입 연산**

* MOV : Rd = Rm , 레지스터에 값을 대입한다.

  ex1) MOV R0, #100

  	-> R0 레지스터에 100을 대입한다.

  ex2) MOV R0, R1

  	-> R0 레지스터에 R1 레지스터 값을 대입한다.



	4) **쉬프트 연산**

* LSL : << (Left Shift)
* RSL : >> (Right Shift)



	5) **분기 명령**

* B : goto 명령, return을 진행하지 않는다. 

* BL : 분기했다가 해당 명령이 끝나면 다시 복귀하는 명령 .(Sub-Routine Call)

  서브루틴이 끝난 이후 복귀를 위하여, ARM에서는 BL을 사용하면 복귀할 주소를 R14(LR) 레지스터에 저장한다.



	6) **비교 연산**

* CMP : if(Rn- Rm == 0) , Rn과 Rm의 값이 같은지 산술적 비교를 하는 명령어.

  해당 연산 결과를 Status Register에 저장한 뒤 이후에 오는 명령어에서 Status 레지스터의 값을 참조하여 조건 명령을 내릴 수 있다.



	7) **메모리 연산**

* STR : [Rm] = Rd , 메모리 주소에 레지스터 값을 저장한다.

* LDR : Rd = [Rm], 해당 메모리 주소의 값을 레지스터에 저장한다.

  ex) MOV R0, #0x100

  	  MOV R1, #0xFF
	
  	  STR R1, [R0]
	
  	  -> 0x100 번지에 0xFF값을 저장한다, 레지스터에 []를 적용하면 해당 레지스터의 값이 있는 메모리 주소를 의미한다. C언어의 Pointer 역할이라고 생각하면 된다.

  