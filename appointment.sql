create database appointment_schema;
use appointment_schema;
create table if not exists prescribed_medicine(
medicine_name varchar(64) not null,
frequency varchar(64) not null,
amount int not null,
primary key (medicine_name));
create table if not exists appointment(
appt_id int not null,
appt_datetime datetime not null,
medicine_name varchar(64) not null,
diagnosis varchar(64) not null,
primary key (appt_id),
foreign key (medicine_name) references prescribed_medicine(medicine_name)
);




