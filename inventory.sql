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
('Drug A', 500, 300, 1000),
('Drug B', 1000, 800, 2000),
('Drug C', 200, 100, 500),
('Drug E', 700, 600, 1500),
('Drug F', 300, 200, 700),
('Drug G', 900, 500, 2000),
('Drug H', 500, 400, 1000),
('Drug I', 500, 400, 1000),
('Drug J', 500, 400, 1000);
COMMIT;