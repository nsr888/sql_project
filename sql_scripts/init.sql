create table if not exists DWH_DIM_CLIENTS(
    client_id varchar(128) primary key,
    last_name varchar(128),
    first_name varchar(128),
    patronymic varchar(128),
    date_of_birth date,
    passport_num varchar(128),
    passport_valid_to date,
    phone varchar(128),
    create_dt date,
    update_dt date
);

create table if not exists DWH_DIM_ACCOUNTS(
    account_num varchar(128) primary key,
    valid_to date,
    client varchar(128),
    create_dt date,
    update_dt date,
    foreign key (client) references DWH_DIM_CLIENTS (client_id)
);

create table if not exists DWH_DIM_CARDS(
    card_num varchar(128) primary key,
    account_num varchar(128),
    create_dt date,
    update_dt date,
    foreign key (account_num) references DWH_DIM_ACCOUNTS (account_num)
);

create table if not exists DWH_DIM_TERMINALS_HIST(
    id integer primary key autoincrement,
    terminal_id varchar(128),
    terminal_type varchar(128),
    terminal_city varchar(128),
    terminal_address varchar(128),
    effective_from date default current_timestamp,
    effective_to date default (datetime('2999-12-31 23:59:59')),
    deleted_flg default 0
);

create table if not exists DWH_FACT_TRANSACTIONS(
    trans_id varchar(128),
    trans_date date,
    amt decimal(10,2),
    card_num varchar(128),
    oper_type varchar(128),
    oper_result varchar(128),
    terminal varchar(128),
    foreign key (card_num) references DWH_DIM_CARDS (card_num),
    foreign key (terminal) references DWH_DIM_TERMINALS_HIST (terminal_id)
);

create table if not exists DWH_FACT_PASSPORT_BLACKLIST(
    passport_num varchar(128),
    entry_dt date
);
