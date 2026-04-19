create table users (
    user_ID varchar2(30) primary key,
    password varchar2(50) not null,
    name varchar2(30),
    phone varchar2(20),
    address varchar2(100),
    role varchar2(20) default 'user',
    CONSTRAINT ck_user_role CHECK (role IN ('user', 'admin')),
    CONSTRAINT ck_user_name CHECK (length(name) > 0)
);

create table accounts (
    account_number varchar2(20) primary key,
    userid varchar2(30) references users (user_ID),
    bankid varchar2(20) references bank (bank_name),
    balance number(20),
    nickname varchar2(20),
    CONSTRAINT ck_acc_balance CHECK (balance >= 0),
    CONSTRAINT ck_acc_num CHECK (length(account_number) >= 10),
    constraint uq_acc_nick unique(userid, nickname)
);

create table bank (
    bank_code varchar2(5) primary key,
    bank_name varchar2(20) unique
);

create sequence log_no;
create table log(
    log_ID number primary key,
    userid varchar2(30) references users (user_ID),
    account_number varchar2(20) references accounts (account_number),
    log_type varchar2(30),
    log_money number(20),
    log_date date,
    constraint ck_log_money check(log_money >= 0)
);