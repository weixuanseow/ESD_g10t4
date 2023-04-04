CREATE DATABASE IF NOT EXISTS patient_records;
USE patient_records;

DROP TABLE IF EXISTS diagnostic_test;
DROP TABLE IF EXISTS prescription_medicines;
DROP TABLE IF EXISTS prescription;
DROP TABLE IF EXISTS appointment_history;
DROP TABLE IF EXISTS patient;

CREATE TABLE IF NOT EXISTS patient (
  Patient_ID int(9) UNSIGNED ZEROFILL AUTO_INCREMENT PRIMARY KEY,
  Patient_Full_Name varchar(64) not null,
  Date_Of_Birth date not null,
  Gender ENUM('male', 'female', 'other') not null,
  Phone_Num varchar(20) not null,
  Allergies varchar(255) default null
);

INSERT INTO patient (Patient_Full_Name, Date_Of_Birth, Gender, Phone_Num, Allergies) VALUES
('Alex Broth', '1988-03-27', 'male', '92345678', 'Aspirin'),
('Brit Mayers', '2023-03-01', 'female', '83456789', NULL),
('Charlie Puth', '2000-07-01', 'male', '94567890', 'Penicillin');
COMMIT;


CREATE TABLE IF NOT EXISTS appointment_history (
  Appt_DateTime datetime not null,
  Patient_ID int(9) UNSIGNED ZEROFILL,
  Diagnosis varchar(255) not null,
  PRIMARY KEY (Appt_DateTime, Patient_ID),
  FOREIGN KEY (Patient_ID) REFERENCES patient(Patient_ID),
  INDEX (Patient_ID)
) ;

INSERT INTO appointment_history (Appt_DateTime, Patient_ID, Diagnosis) VALUES
('2022-12-28 10:20:00', '000000003', 'Left Distal Radius Fracture'),
('2023-01-28 15:40:00', '000000002', 'Scoliosis'),
('2023-02-20 13:00:00', '000000001', 'Osteoarthritis'),
('2022-12-29 10:20:00', '000000003', 'Minnal inserted a disease for me'),
('2023-03-11 16:30:00', '000000003', 'Fracture Union, No further treatment required'),
('2023-04-03 16:30:00', '000000003', 'Finger Fracture'),
('2023-04-01 09:00:00', '000000001', 'Knee Pain'),
('2023-04-02 10:30:00', '000000001', 'Carpal Tunnel'),
('2023-04-03 14:15:00', '000000001', 'Arthritis'),
('2023-04-04 11:00:00', '000000001', 'Scoliosis'),
('2023-04-05 15:30:00', '000000001', 'tbd'),
('2023-04-01 08:45:00', '000000002', 'Tendinitis'),
('2023-04-02 13:00:00', '000000002', 'Rotator Cuff Injury'),
('2023-04-03 16:45:00', '000000002', 'Arthritis'),
('2023-04-04 09:30:00', '000000002', 'Slip Disk'),
('2023-04-05 11:30:00', '000000002', 'tbd'),
('2023-04-01 12:30:00', '000000003', 'Ankle Sprain'),
('2023-04-02 16:00:00', '000000003', 'ACL Tear'),
('2023-04-03 13:15:00', '000000003', 'Elbow Fracture'),
('2023-04-04 14:30:00', '000000003', 'Meniscal Tear'),
('2023-04-05 10:45:00', '000000003', 'tbd');
COMMIT;


CREATE TABLE IF NOT EXISTS prescription (
  Appt_DateTime datetime,
  Patient_ID int(9) UNSIGNED ZEROFILL,
  Prescription_ID int(9) UNSIGNED ZEROFILL,
  PRIMARY KEY (Patient_ID, Appt_DateTime, Prescription_ID),
  FOREIGN KEY (Patient_ID, Appt_DateTime) REFERENCES appointment_history(Patient_ID, Appt_DateTime),
  INDEX (Prescription_ID)
);

INSERT INTO prescription (Appt_DateTime, Patient_ID, Prescription_ID) VALUES
('2022-12-28 10:20:00', '000000003', '800000001'), /* ok */
('2023-01-28 15:40:00', '000000002', '800000002'), /* ok */
('2023-02-20 13:00:00', '000000001', '800000003'); /* ok */
COMMIT;

-- INSERT INTO prescription (Appt_DateTime, Patient_ID, Prescription_ID) VALUES
-- ('2022-12-29 10:20:00', '000000003', '800000004')
-- COMMIT;


CREATE TABLE IF NOT EXISTS prescription_medicines (
  Prescription_ID int(9) UNSIGNED ZEROFILL,
  Medicine_Name varchar(100),
  Frequency varchar(255),
  Amount varchar(255),
  PRIMARY KEY (Prescription_ID, Medicine_Name),
  FOREIGN KEY (Prescription_ID) REFERENCES prescription(Prescription_ID)
);

-- INSERT INTO prescription_medicines (Prescription_ID, Medicine_Name, Frequency, Amount) VALUES
-- ('800000004', 'Drug A', 'whenever ur heart desires', 200),
-- ('800000004', 'Drug B', 'whenever ur heart desires', 150)
-- COMMIT;

INSERT INTO prescription_medicines (Prescription_ID, Medicine_Name, Frequency, Amount) VALUES
('800000001', 'Aspirin', 'Every 4-6 hours as needed', '2 tablets'),
('800000001', 'Flexeril', 'Once a day', '1 tablet'),
('800000001', 'Teriparatide', 'Once a day', '1 tablet'),
('800000002', ' Paracetamol', 'Every 4-6 hours as needed, no longer than 2 days', '1 tablet'),
('800000003', 'Naproxen Sodium', 'Twice a day', '2 tablets'),
('800000003', 'Capsaicin Topical Cream', '3-4 times a day', 'As needed');
COMMIT;


DROP TABLE IF EXISTS diagnostic_test;
CREATE TABLE IF NOT EXISTS diagnostic_test (
  Test_ID int UNSIGNED ZEROFILL AUTO_INCREMENT PRIMARY KEY,
  Test_DateTime datetime not null,
  Test_Type varchar(255) not null,
  Test_Results varchar(255) not null,
  Patient_ID int(9) UNSIGNED ZEROFILL,
  Appt_DateTime datetime not null,
  FOREIGN KEY (Patient_ID, Appt_DateTime) REFERENCES appointment_history(Patient_ID, Appt_DateTime)
);

INSERT INTO diagnostic_test (Test_DateTime, Test_Type, Test_Results, Patient_ID, Appt_DateTime) VALUES
('2022-12-28 10:45:00', 'X-ray', 'Left Distal Radius Fracture', '000000003', '2022-12-28 10:20:00'),
('2023-01-28 16:00:00', 'CT Scan', 'Lumbar Scoliosis', '000000002', '2023-01-28 15:40:00'),
('2023-02-20 13:18:00', 'MRI', 'Monoarticular Osteoarthritis at the knee', '000000001', '2023-02-20 13:00:00'),
('2023-03-11 16:35:00', 'X-ray', 'No signs of abnormality', '000000003', '2023-03-11 16:30:00');
COMMIT;

INSERT INTO prescription (Appt_DateTime, Patient_ID, Prescription_ID)
VALUES
('2023-04-01 09:00:00', '000000001', 800000004),
('2023-04-02 10:30:00', '000000001', 800000005),
('2023-04-03 14:15:00', '000000001', 800000006),
('2023-04-04 11:00:00', '000000001', 800000007),
('2023-04-05 15:30:00', '000000001', 800000008),
('2023-04-01 08:45:00', '000000002', 800000009),
('2023-04-02 13:00:00', '000000002', 800000010),
('2023-04-03 16:45:00', '000000002', 800000011),
('2023-04-04 09:30:00', '000000002', 800000012),
('2023-04-05 11:30:00', '000000002', 800000013),
('2023-04-01 12:30:00', '000000003', 800000014),
('2023-04-02 16:00:00', '000000003', 800000015),
('2023-04-03 13:15:00', '000000003', 800000016),
('2023-04-04 14:30:00', '000000003', 800000017),
('2023-04-05 10:45:00', '000000003', 800000018);
COMMIT;

INSERT INTO prescription_medicines (Prescription_ID, Medicine_Name, Frequency, Amount) VALUES
  -- Prescription 800000004
  (800000004, 'Ibuprofen', 'Once a day', 30),
  (800000004, 'Acetaminophen', 'Twice a day', 60),
  -- Prescription 800000005
  (800000005, 'Acetaminophen', 'Once a day', 30),
  (800000005, 'Ibuprofen', 'Once a day', 30),
  -- Prescription 800000006
  (800000006, 'Aspirin', 'Once a day', 30),
  -- Prescription 800000007
  (800000007, 'Lisinopril', 'Once a day', 30),
  -- Prescription 800000008
  (800000008, 'Amoxicillin', 'Twice a day', 20),
  -- Prescription 800000009
  (800000009, 'Ibuprofen', 'Once a day', 30),
  (800000009, 'Paracetamol', 'Once a day', 30),
  -- Prescription 800000010
  (800000010, 'Paracetamol', 'Once a day', 60),
  -- Prescription 800000011
  (800000011, 'Doxycycline', 'Once a day', 14),
  (800000011, 'Ibuprofen', 'Once a day', 30),
  -- Prescription 800000012
  (800000012, 'Metformin', 'Twice a day', 60),
  -- Prescription 800000013
  (800000013, 'Atorvastatin', 'Once a day', 30),
  -- Prescription 800000014
  (800000014, 'Ibuprofen', 'Once a day', 30),
  (800000014, 'Lorazepam', 'Once a day', 30),
  -- Prescription 800000015
  (800000015, 'Metoprolol', 'Once a day', 30),
  -- Prescription 800000016
  (800000016, 'Doxycycline', 'Once a day', 14),
  (800000016, 'Ibuprofen', 'Once a day', 30),
  -- Prescription 800000017
  (800000017, 'Simvastatin', 'Once a day', 30),
  -- Prescription 800000018
  (800000018, 'Ibuprofen', 'Once a day', 30),
  (800000018, 'Lorazepam', 'Once a day', 30);
COMMIT;

/* ok i generated everything except diagnostic test cos i dont rly know the details for it
pls add if wanted/needed thanks */