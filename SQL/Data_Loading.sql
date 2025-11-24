USE vending_machine_database_system;

LOAD DATA LOCAL INFILE 'C:/Users/Anura/OneDrive/Desktop/Third Year/AISE 3309/Project/Vending-Machine-Database-System/dump/Model.csv'
INTO TABLE Model
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE 'C:/Users/Anura/OneDrive/Desktop/Third Year/AISE 3309/Project/Vending-Machine-Database-System/dump/Manufacturer.csv'
INTO TABLE Manufacturer
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE 'C:/Users/Anura/OneDrive/Desktop/Third Year/AISE 3309/Project/Vending-Machine-Database-System/dump/Employee.csv'
INTO TABLE Employee
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE 'C:/Users/Anura/OneDrive/Desktop/Third Year/AISE 3309/Project/Vending-Machine-Database-System/dump/Maintenance.csv'
INTO TABLE Maintenance
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE 'C:/Users/Anura/OneDrive/Desktop/Third Year/AISE 3309/Project/Vending-Machine-Database-System/dump/Management.csv'
INTO TABLE Management
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(employee_ID, @level)
SET seniority_Lvl = TRIM(@level);

LOAD DATA LOCAL INFILE 'C:/Users/Anura/OneDrive/Desktop/Third Year/AISE 3309/Project/Vending-Machine-Database-System/dump/Customer.csv'
INTO TABLE Customer
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE 'C:/Users/Anura/OneDrive/Desktop/Third Year/AISE 3309/Project/Vending-Machine-Database-System/dump/Vending_Machine.csv'
INTO TABLE Vending_Machine
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE 'C:/Users/Anura/OneDrive/Desktop/Third Year/AISE 3309/Project/Vending-Machine-Database-System/dump/Stock.csv'
INTO TABLE Stock
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE 'C:/Users/Anura/OneDrive/Desktop/Third Year/AISE 3309/Project/Vending-Machine-Database-System/dump/Record.csv'
INTO TABLE Record
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE 'C:/Users/Anura/OneDrive/Desktop/Third Year/AISE 3309/Project/Vending-Machine-Database-System/dump/Payment_Record.csv'
INTO TABLE Payment_Record
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE 'C:/Users/Anura/OneDrive/Desktop/Third Year/AISE 3309/Project/Vending-Machine-Database-System/dump/Maintenance_Record.csv'
INTO TABLE Maintenance_Record
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE 'C:/Users/Anura/OneDrive/Desktop/Third Year/AISE 3309/Project/Vending-Machine-Database-System/dump/Restock_Record.csv'
INTO TABLE Restock_Record
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;