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

INSERT INTO inventory (drug_full_name, threshold_amt, current_amt, topup_amt)
VALUES 
('Acetaminophen', 500, 300, 1000),
('Aspirin', 1000, 800, 2000),
('Atorvastatin', 200, 100, 500),
('Ciprofloxacin', 700, 600, 1500),
('Codeine', 300, 200, 700),
('Diazepam', 900, 500, 2000),
('Doxycycline', 500, 400, 1000),
('Fentanyl', 500, 400, 1000),
('Fluoxetine', 500, 300, 1000),
('Gabapentin', 1000, 800, 2000),
('Hydrochlorothiazide', 200, 100, 500),
('Ibuprofen', 700, 600, 1500),
('Levothyroxine', 300, 200, 700),
('Lisinopril', 900, 500, 2000),
('Lorazepam', 500, 400, 1000),
('Losartan', 500, 400, 1000),
('Metformin', 500, 400, 1000),
('Metoprolol', 1000, 800, 2000),
('Naproxen', 200, 100, 500),
('Omeprazole', 700, 600, 1500),
('Pantoprazole', 300, 200, 700),
('Paracetamol', 900, 500, 2000),
('Prednisone', 500, 400, 1000),
('Rosuvastatin', 500, 400, 1000),
('Sertraline', 700, 600, 1500),
('Simvastatin', 300, 200, 700),
('Tamsulosin', 900, 500, 2000),
('Tramadol', 500, 400, 1000),
('Venlafaxine', 500, 400, 1000),
('Warfarin', 500, 400, 1000),
('Zolpidem', 500, 400, 1000);
COMMIT;