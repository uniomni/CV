From m8811009@mbar.dtu.dk Wed Jan 11 10:30 MET 1995
Received: from danpost2.uni-c.dk by unidhp1.uni-c.dk with SMTP
	(1.37.109.8/16.2) id AA04357; Wed, 11 Jan 1995 10:30:35 +0100
Return-Path: <m8811009@mbar.dtu.dk>
Received: from mona.mbar.dtu.dk (maude.mbar.dtu.dk [130.225.72.22]) by danpost2.uni-c.dk (8.6.4/8.6) with SMTP id KAA28408 for <uniomni@uni-c.dk>; Wed, 11 Jan 1995 10:30:16 +0100
Received: by mona.mbar.dtu.dk
	(1.38.193.4/16.2) id AA06585; Wed, 11 Jan 1995 10:28:49 +0100
From: "Elementmetoden for Partielle Diff.lign." <m8811009@mbar.dtu.dk>
Message-Id: <9501110928.AA06585@mona.mbar.dtu.dk>
Subject: no subject (file transmission)
To: uniomni@uni-c.dk
Date: Wed, 11 Jan 95 10:28:46 MET
X-Mailer: ELM [version 2.3 PL11]
Status: RO

      SUBROUTINE SYMSL(NEQMAX,KK,A,NEQ,IHBW,RV)                         SYM00010
C                                                                       SYM00020
C                                                                       SYM00030
      DOUBLE PRECISION RV(NEQMAX),A(NEQMAX,IHBW)                        SYM00040
      DOUBLE PRECISION C                                                SYM00050

C                                                                       SYM00060
C                                                                       SYM00070
      GOTO (1000,2000,1000),KK                                          SYM00080
C                                                                       SYM00090
C                                                                       SYM00100
1000  DO 1 ISBM=1,NEQ                                                   SYM00110
      DO 2 JSBM=2,IHBW                                                  SYM00120
      IF(A(ISBM,JSBM).EQ.0.0) GOTO 2                                    SYM00130
      C=A(ISBM,JSBM)/A(ISBM,1)                                          SYM00140
      IGL=ISBM+JSBM-1                                                   SYM00150
      IF(NEQ-IGL) 2,3,3                                                 SYM00160
3     JGL=0                                                             SYM00170
      DO 4 K=JSBM,IHBW                                                  SYM00180
      JGL=JGL+1                                                         SYM00190
4     A(IGL,JGL)=A(IGL,JGL)-C*A(ISBM,K)                                 SYM00200
      A(ISBM,JSBM)=C                                                    SYM00210
2     CONTINUE                                                          SYM00220
1     CONTINUE                                                          SYM00230
      IF(KK.LT.3) GOTO 12                                               SYM00240
2000  DO 5 ISBM=1,NEQ                                                   SYM00250
      DO 6 JSBM=2,IHBW                                                  SYM00260
      IF(A(ISBM,JSBM).EQ.0.0) GOTO 6                                    SYM00270
      IGL=ISBM+JSBM-1                                                   SYM00280
      IF(NEQ-IGL) 5,7,7                                                 SYM00290
7     RV(IGL)=RV(IGL)-A(ISBM,JSBM)*RV(ISBM)                             SYM00300
6     CONTINUE                                                          SYM00310
5     RV(ISBM)=RV(ISBM)/A(ISBM,1)                                       SYM00320
      ISBM=NEQ                                                          SYM00330
8     ISBM=ISBM-1                                                       SYM00340
      IF(ISBM) 9,12,9                                                   SYM00350
9     DO 11 JSBM=2,IHBW                                                 SYM00360
      IF(A(ISBM,JSBM).EQ.0.0) GOTO 11                                   SYM00370
      IGL=ISBM+JSBM-1                                                   SYM00380
      IF(NEQ-IGL) 11,10,10                                              SYM00390
10    RV(ISBM)=RV(ISBM)-A(ISBM,JSBM)*RV(IGL)                            SYM00400
11    CONTINUE                                                          SYM00410
      GOTO 8                                                            SYM00420
12    RETURN                                                            SYM00430
      END                                                               SYM00440

