# 🏦 Banking Management System with Python & Oracle

오라클 데이터베이스(Oracle DB)와 파이썬(Python)을 연동하여 구축한 **객체 지향 기반 은행 관리 시스템**입니다. 실제 금융 서비스의 핵심 로직인 계좌 개설, 입출금, 계좌 이체 및 트랜잭션 관리 기능을 구현했습니다.

## 주요 기능 (Key Features)

  * **회원 관리**: 회원가입 및 보안 로그인 시스템.
  * **계좌 관리**: 신규 계좌 개설 및 보유 계좌 조회.
  * **금융 거래**:
      * **입/출금**: 실시간 잔액 업데이트 및 데이터 유효성 검사.
      * **계좌 이체**: 트랜잭션의 원자성을 보장하는 이체 로직 (`Commit`, `Rollback` 적용).
  * **보안 및 안정성**:
      * **SQL Injection 방어**: 바인딩 변수를 활용한 쿼리 처리.
      * **데이터 무결성**: DB 제약조건과 파이썬 예외 처리를 통한 데이터 검증.
  * **UI/UX**: `tabulate` 라이브러리를 활용한 깔끔한 CLI 기반 데이터 시각화.

## 기술 스택 (Tech Stack)

  * **Language**: `Python 3.13.9`
  * **Database**: `Oracle Database`
  * **Library**:
      * `oracledb`: DB 연동
      * `tabulate`: 데이터 출력 최적화
      * `hashlib`: (선택 사항) 비밀번호 암호화
      * 'dotenv / os': 환경변수 활용 DB접속정보 숨기기

## 프로젝트 구조 (Architecture)

유지보수와 가독성을 높이기 위해 **모듈화된 클래스 구조**로 설계되었습니다.

```text
├── login.py              # 프로그램 실행 및 데이터베이스 연결 엔트리 포인트
├── login_modul.py        # 회원가입, 로그인 처리 및 SHA-256 기반 보안 로직
├── bank.py               # 사용자/관리자 권한에 따른 메뉴 분기 및 서비스 라우팅
├── bank_modul.py         # 입출금, 계좌 생성, 거래내역 조회 등 사용자 금융 서비스 핵심 로직
├── admin_modul.py        # 관리자 전용 사용자 정보 조회, 수정 및 삭제 관리 기능
├── def_modul.py          # 계좌 생성/검색 유틸리티 및 계좌 이체(로컬/통합) 처리 로직
└── bank_system.sql       # Oracle DB 테이블(Users, Accounts, Log 등) 및 시퀀스 생성 스크립트
```

## 시작하기 (Getting Started)

### 1\. 전제 조건

  * Oracle Database 설치 및 실행 중
  * Python 환경 설치

### 2\. 라이브러리 설치

```bash
pip install oracledb tabulate python-dotenv
```

### 3\. 데이터베이스 설정

`bank_system.sql` 파일을 오라클 계정에서 실행하여 테이블(Users, Accounts, Transactions 등)을 생성합니다.

### 4\. 실행

```bash
python login.py
```

## 주요 구현 포인트

  * **트랜잭션 관리**: 계좌 이체 시 발신 계좌 출금과 수신 계좌 입금이 하나의 단위로 처리되도록 하여, 오류 발생 시 `Rollback`을 통해 데이터의 일관성을 유지했습니다.
  * **객체 지향 설계**: 각 기능을 독립적인 클래스로 분리하여 코드 재사용성을 높이고 결합도를 낮췄습니다.
  * **사용자 경험**: CLI 환경에서도 사용자가 데이터를 쉽게 파악할 수 있도록 표 형식의 레이아웃을 적용했습니다.

-----

### 프로젝트 기간

  * 2026.04.18 - 2026.04.23

### PPT 및 시연동영상
[Python bank PPT.pptx](https://github.com/user-attachments/files/26866323/Python.bank.PPT.pptx)

### 작성자

  * **이름**: 김민석
  * **GitHub**: [kms3356](https://github.com/kms3356/bank-system.git)
  * **Email**: john563322@gmail.com
