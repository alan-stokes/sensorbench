; @Harness: disassembler
; @Result: PASS
  section .text  size=0x00000046 vma=0x00000000 lma=0x00000000 offset=0x00000034 ;2**0 
  section .data  size=0x00000000 vma=0x00000000 lma=0x00000000 offset=0x0000007a ;2**0 

start .text:

label 0x00000000  ".text":
      0x0: 0x0d 0x92  st  X+,  r0
      0x2: 0x09 0x92  st  Y+,  r0
      0x4: 0x01 0x92  st  Z+,  r0
      0x6: 0x0d 0x92  st  X+,  r0
      0x8: 0x1d 0x92  st  X+,  r1
      0xa: 0x2d 0x92  st  X+,  r2
      0xc: 0x3d 0x92  st  X+,  r3
      0xe: 0x4d 0x92  st  X+,  r4
     0x10: 0x5d 0x92  st  X+,  r5
     0x12: 0x6d 0x92  st  X+,  r6
     0x14: 0x7d 0x92  st  X+,  r7
     0x16: 0x8d 0x92  st  X+,  r8
     0x18: 0x9d 0x92  st  X+,  r9
     0x1a: 0xad 0x92  st  X+,  r10
     0x1c: 0xbd 0x92  st  X+,  r11
     0x1e: 0xcd 0x92  st  X+,  r12
     0x20: 0xdd 0x92  st  X+,  r13
     0x22: 0xed 0x92  st  X+,  r14
     0x24: 0xfd 0x92  st  X+,  r15
     0x26: 0x0d 0x93  st  X+,  r16
     0x28: 0x1d 0x93  st  X+,  r17
     0x2a: 0x2d 0x93  st  X+,  r18
     0x2c: 0x3d 0x93  st  X+,  r19
     0x2e: 0x4d 0x93  st  X+,  r20
     0x30: 0x5d 0x93  st  X+,  r21
     0x32: 0x6d 0x93  st  X+,  r22
     0x34: 0x7d 0x93  st  X+,  r23
     0x36: 0x8d 0x93  st  X+,  r24
     0x38: 0x9d 0x93  st  X+,  r25
     0x3a: 0xad 0x93  st  X+,  r26  ;  undefined
     0x3c: 0xbd 0x93  st  X+,  r27  ;  undefined
     0x3e: 0xcd 0x93  st  X+,  r28
     0x40: 0xdd 0x93  st  X+,  r29
     0x42: 0xed 0x93  st  X+,  r30
     0x44: 0xfd 0x93  st  X+,  r31

start .data:
