// > Main.asm
// function Main.main 0
(Main.main)
// push constant 1
  @1
  D=A
  @SP
  A=M
  M=D
  @SP
  M=M+1
// push constant 1
  @1
  D=A
  @SP
  A=M
  M=D
  @SP
  M=M+1
// call Math.add 2
  @Main.main$ret.1
  D=A
  @SP
  A=M
  M=D
  @SP
  M=M+1
  @LCL
  D=M
  @SP
  A=M
  M=D
  @SP
  M=M+1
  @ARG
  D=M
  @SP
  A=M
  M=D
  @SP
  M=M+1
  @THIS
  D=M
  @SP
  A=M
  M=D
  @SP
  M=M+1
  @THAT
  D=M
  @SP
  A=M
  M=D
  @SP
  M=M+1
  @SP
  D=M
  @5
  D=D-A
  @2
  D=D-A
  @ARG
  M=D
  @SP
  D=M
  @LCL
  M=D
  @Math.add
  0;JMP
(Main.main$ret.1)
// return
  @LCL
  D=M
  @R13
  M=D
  @5
  D=D-A
  A=D
  D=M
  @R14
  M=D
  @SP
  M=M-1
  A=M
  D=M
  @ARG
  A=M
  M=D
  @ARG
  D=M
  D=D+1
  @SP
  M=D
  @R13
  D=M
  @1
  D=D-A
  A=D
  D=M
  @THAT
  M=D
  @R13
  D=M
  @2
  D=D-A
  A=D
  D=M
  @THIS
  M=D
  @R13
  D=M
  @3
  D=D-A
  A=D
  D=M
  @ARG
  M=D
  @R13
  D=M
  @4
  D=D-A
  A=D
  D=M
  @LCL
  M=D
  @R14
  A=M
  0;JMP
// > Math.asm
// function Math.add 2
(Math.add)
  @SP
  A=M
  M=0
  @SP
  M=M+1
  @SP
  A=M
  M=0
  @SP
  M=M+1
// push argument 0
  @ARG
  D=M
  @0
  A=D+A
  D=M
  @SP
  A=M
  M=D
  @SP
  M=M+1
// push argument 1
  @ARG
  D=M
  @1
  A=D+A
  D=M
  @SP
  A=M
  M=D
  @SP
  M=M+1
// add
  @SP
  M=M-1
  A=M
  D=M
  @SP
  M=M-1
  A=M
  D=D+M
  @SP
  A=M
  M=D
  @SP
  M=M+1
// return
  @LCL
  D=M
  @R13
  M=D
  @5
  D=D-A
  A=D
  D=M
  @R14
  M=D
  @SP
  M=M-1
  A=M
  D=M
  @ARG
  A=M
  M=D
  @ARG
  D=M
  D=D+1
  @SP
  M=D
  @R13
  D=M
  @1
  D=D-A
  A=D
  D=M
  @THAT
  M=D
  @R13
  D=M
  @2
  D=D-A
  A=D
  D=M
  @THIS
  M=D
  @R13
  D=M
  @3
  D=D-A
  A=D
  D=M
  @ARG
  M=D
  @R13
  D=M
  @4
  D=D-A
  A=D
  D=M
  @LCL
  M=D
  @R14
  A=M
  0;JMP
