-- create database diagnostic_test;
-- use diagnostic_test;
-- create table if not exists test(
-- test_id int AUTO_INCREMENT not null PRIMARY KEY,
-- test_datetime datetime not null,
-- test_type varchar(64) not null,
-- test_results varchar(64) not null,
-- );
CREATE DATABASE IF NOT EXISTS `diagnostic_test` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `diagnostic_test`;

-- Create the bookings table
DROP TABLE IF EXISTS `test`;
CREATE TABLE test (
    test_id INT AUTO_INCREMENT PRIMARY KEY,
    test_datetime DATETIME NOT NULL,
    test_type VARCHAR(64) NOT NULL,
    test_results VARCHAR(64) NOT NULL
);