INSERT INTO DWH_DIM_CARDS (card_num, account_num, create_dt, update_dt)
select card_num, account, create_dt, update_dt from cards;

INSERT INTO DWH_DIM_ACCOUNTS (account_num, valid_to, client, create_dt, update_dt)
select account, valid_to, client, create_dt, update_dt from accounts;

INSERT INTO DWH_DIM_CLIENTS (client_id, last_name, first_name, patronymic,
    date_of_birth, passport_num, passport_valid_to, phone, create_dt, update_dt)
select client_id, last_name, first_name, patronymic, date_of_birth,
    passport_num, passport_valid_to, phone, create_dt, update_dt from clients;

INSERT INTO DWH_FACT_TRANSACTIONS (trans_id, trans_date, amt, card_num,
    oper_type, oper_result, terminal)
select transaction_id, transaction_date, amount, card_num, oper_type,
    oper_result, terminal from STG_TRANSACTIONS;

INSERT INTO DWH_FACT_PASSPORT_BLACKLIST (passport_num, entry_dt)
select passport, date from STG_PASSPORT_BLACKLIST;

INSERT INTO DWH_DIM_TERMINALS_HIST (terminal_id, terminal_type, terminal_city,
    terminal_address)
select terminal_id, terminal_type, terminal_city, terminal_address
    from STG_TERMINALS;
