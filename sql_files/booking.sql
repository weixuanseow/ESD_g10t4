-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:889
-- Generation Time: Mar 11, 2023 at 05:18 AM
-- Server version: 8.0.27
-- PHP Version: 7.4.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";
SET GLOBAL event_scheduler = ON;

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--

CREATE DATABASE IF NOT EXISTS `bookings` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `bookings`;

-- Create the bookings table
DROP TABLE IF EXISTS `mri`;
CREATE TABLE mri (
    bid INT AUTO_INCREMENT PRIMARY KEY,
    slot DATETIME NOT NULL,
    available BOOLEAN DEFAULT TRUE,
    pid INT
);

DROP TABLE IF EXISTS `xray`;
CREATE TABLE xray (
    bid INT AUTO_INCREMENT PRIMARY KEY ,
    slot DATETIME NOT NULL,
    available BOOLEAN DEFAULT TRUE,
    pid INT
);

DROP TABLE IF EXISTS `ctscan`;
CREATE TABLE ctscan (
    bid INT AUTO_INCREMENT PRIMARY KEY,
    slot DATETIME NOT NULL,
    available BOOLEAN DEFAULT TRUE,
    pid INT
);

DROP TABLE IF EXISTS `bloodtest`;
CREATE TABLE bloodtest (
    bid INT AUTO_INCREMENT PRIMARY KEY,
    slot DATETIME NOT NULL,
    available BOOLEAN DEFAULT TRUE,
    pid INT
);

-- Create an index on the slot column for faster querying
CREATE INDEX slot_index ON mri (slot);
CREATE INDEX slot_index ON xray (slot);
CREATE INDEX slot_index ON ctscan (slot);
CREATE INDEX slot_index ON bloodtest (slot);

-- Create a stored procedure to check for available slots
DROP PROCEDURE IF EXISTS get_available_slots;
DELIMITER //
CREATE PROCEDURE get_available_slots()
BEGIN
    SELECT slot
    FROM available_slots
    WHERE slot NOT IN (
        SELECT slot
        FROM bookings
    );
END //
DELIMITER ;

-- Create a stored procedure to insert a booking
DROP PROCEDURE IF EXISTS book_slot;
DELIMITER //
CREATE PROCEDURE book_slot(IN booking_slot DATETIME, IN booking_user VARCHAR(255))
BEGIN
    INSERT INTO bookings (slot, user)
    VALUES (booking_slot, booking_user);
END //
DELIMITER ;

-- Create an event to delete expired bookings 
DROP PROCEDURE IF EXISTS delete_expired_bookings;
DELIMITER //
CREATE PROCEDURE delete_expired_bookings()
BEGIN
    DELETE FROM mri;
    DELETE FROM xray;
    DELETE FROM ctscan;
    DELETE FROM bloodtest;
END //
DELIMITER ;

DROP EVENT IF EXISTS delete_expired_bookings_event;
CREATE EVENT delete_expired_bookings_event
ON SCHEDULE
EVERY 1 DAY
STARTS '2023-03-13 00:00:00'
DO
CALL delete_expired_bookings();


-- -- Create an event to insert bookings everyday
DROP PROCEDURE IF EXISTS create_booking_slots;
DELIMITER //
CREATE PROCEDURE create_booking_slots()
BEGIN
  DECLARE start_time datetime;
  DECLARE the_end datetime;
  DECLARE the_start datetime;
  DECLARE num_slots int;

  SET start_time = CURDATE() + INTERVAL 9 HOUR;
  SET num_slots = 16;
  SET the_start = start_time;
  SET the_end = the_start + INTERVAL 30 MINUTE;
  WHILE num_slots > 0 DO
    INSERT INTO mri (slot)
    VALUES (the_start);
    SET the_start = the_end;
    SET the_end = the_start + INTERVAL 30 MINUTE;
    SET num_slots = num_slots - 1;
  END WHILE;
  SET start_time = CURDATE() + INTERVAL 9 HOUR;
  SET num_slots = 16;
  SET the_start = start_time;
  SET the_end = the_start + INTERVAL 30 MINUTE;
    WHILE num_slots > 0 DO
    INSERT INTO xray (slot)
    VALUES (the_start);
    SET the_start = the_end;
    SET the_end = the_start + INTERVAL 30 MINUTE;
    SET num_slots = num_slots - 1;
  END WHILE;
  SET start_time = CURDATE() + INTERVAL 9 HOUR;
  SET num_slots = 16;
  SET the_start = start_time;
  SET the_end = the_start + INTERVAL 30 MINUTE;
    WHILE num_slots > 0 DO
    INSERT INTO ctscan (slot)
    VALUES (the_start);
    SET the_start = the_end;
    SET the_end = the_start + INTERVAL 30 MINUTE;
    SET num_slots = num_slots - 1;
  END WHILE;
  SET start_time = CURDATE() + INTERVAL 9 HOUR;
  SET num_slots = 16;
  SET the_start = start_time;
  SET the_end = the_start + INTERVAL 30 MINUTE;
    WHILE num_slots > 0 DO
    INSERT INTO bloodtest (slot)
    VALUES (the_start);
    SET the_start = the_end;
    SET the_end = the_start + INTERVAL 30 MINUTE;
    SET num_slots = num_slots - 1;
  END WHILE;

END //
DELIMITER ;

DROP EVENT IF EXISTS create_booking_slots_event;
CREATE EVENT create_booking_slots_event
ON SCHEDULE
  EVERY 1 DAY
  STARTS '2023-03-13 00:00:00'
DO
    CALL create_booking_slots();

CALL create_booking_slots();


/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;