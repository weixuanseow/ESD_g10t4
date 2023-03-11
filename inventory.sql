create database inventory;
use inventory;
drop table if exists inventory;
create table if not exists inventory(
drug_full_name varchar(64) not null,
threshold_amt int not null,
current_amt int not null,
topup_amt int not null, 
primary key (drug_full_name)
);
