create database diagnostic_test;
use diagnostic_test;
create table if not exists test(
test_id int not null,
test_datetime datetime not null,
test_type varchar(64) not null,
test_results varchar(64) not null,
primary key (test_id)
);