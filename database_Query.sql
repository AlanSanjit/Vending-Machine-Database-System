DROP DATABASE IF EXISTS VendingDB;
CREATE DATABASE VendingDB;
USE VendingDB;

DROP TABLE IF EXISTS Model;
CREATE TABLE Model (
    model_Type VARCHAR(50)   NOT NULL,
    price      DECIMAL(10,2) NOT NULL,
    capacity   INT           NOT NULL,

    CONSTRAINT pk_Model PRIMARY KEY (model_Type)
);

DROP TABLE IF EXISTS Manufacturer;
CREATE TABLE Manufacturer (
    supplier_ID     CHAR(10)      NOT NULL,
    manufac_Brand   VARCHAR(100)  NOT NULL,
    contact_Email   VARCHAR(255)  NOT NULL,
    contact_Number  VARCHAR(20)   NOT NULL,
    supply_Type     VARCHAR(50)   NOT NULL,
    Price           DECIMAL(10,2) NOT NULL,

    CONSTRAINT pk_Manufacturer PRIMARY KEY (supplier_ID),
    CONSTRAINT uq_Manufacturer_Email UNIQUE (contact_Email),
    CONSTRAINT uq_Manufacturer_Number UNIQUE (contact_Number),
    CONSTRAINT fk_Manufacturer_SupplyType
        FOREIGN KEY (supply_Type)
        REFERENCES Model(model_Type)
);

DROP TABLE IF EXISTS Employee;
CREATE TABLE Employee (
    employee_ID VARCHAR(50)  NOT NULL,
    f_Name      VARCHAR(50)  NOT NULL,
    l_Name      VARCHAR(50)  NOT NULL,
    Role        VARCHAR(50)  NOT NULL,
    work_Email  VARCHAR(255) NOT NULL,

    CONSTRAINT pk_Employee PRIMARY KEY (employee_ID),
    CONSTRAINT uq_Employee_Email UNIQUE (work_Email),
    CONSTRAINT chk_Employee_Role CHECK (Role IN ('Technician','Supervisor_Tech','Lead_Tech','Management')),
);

DROP TABLE IF EXISTS Maintenance;
CREATE TABLE Maintenance (
    employee_ID VARCHAR(50) NOT NULL,
    lic_No      VARCHAR(50) NOT NULL,

    CONSTRAINT pk_Maintenance PRIMARY KEY (employee_ID),
    CONSTRAINT spec_Employee CHECK (employee_ID IN (SELECT employee_ID FROM Employee WHERE Role = 'Technician', 'Supervisor_Tech', 'Lead_Tech')),
    CONSTRAINT fk_Maintenance_Employee
        FOREIGN KEY (employee_ID) REFERENCES Employee(employee_ID)
);

DROP TABLE IF EXISTS Management;
CREATE TABLE Management (
    employee_ID  VARCHAR(50) NOT NULL,
    seniority_Lvl VARCHAR(20) NOT NULL,

    CONSTRAINT pk_Management PRIMARY KEY (employee_ID),
    CONSTRAINT spec_Employee CHECK (employee_ID IN (SELECT employee_ID FROM Employee WHERE Role = 'Management')),
    CONSTRAINT spec_seniority_Lvl CHECK (seniority_Lvl IN ('Junior','Senior','Director')),
    CONSTRAINT fk_Management_Employee
        FOREIGN KEY (employee_ID) REFERENCES Employee(employee_ID)
);

DROP TABLE IF EXISTS Vending_Machine;
CREATE TABLE Vending_Machine (
    machine_ID     VARCHAR(50)  NOT NULL,
    Status         VARCHAR(20)  NOT NULL,
    purchase_Date  DATE         NOT NULL,

    CONSTRAINT pk_Vending_Machine PRIMARY KEY (machine_ID),
    CONSTRAINT chk_VendingMachine_Status CHECK 
        (Status IN ('functional', 'repair', 'decommissioned'))
);

DROP TABLE IF EXISTS Record;
CREATE TABLE Record (
    record_ID      INT  NOT NULL,
    date_Requested DATE NOT NULL,
    date_Completed DATE,

    CONSTRAINT pk_Record PRIMARY KEY (record_ID)
);

DROP TABLE IF EXISTS Maintenance_Record;
CREATE TABLE Maintenance_Record (
    record_ID   INT          NOT NULL,
    Description VARCHAR(255) NOT NULL,
    Status      VARCHAR(20)  NOT NULL,

    CONSTRAINT pk_Maintenance_Record PRIMARY KEY (record_ID),
    CONSTRAINT fk_MaintRec_Record
        FOREIGN KEY (record_ID) REFERENCES Record(record_ID),
    CONSTRAINT chk_MaintRec_Status CHECK
        (Status IN ('functional', 'repair', 'decommissioned'))
);

DROP TABLE IF EXISTS Payment_Record;
CREATE TABLE Payment_Record (
    record_ID    INT           NOT NULL,
    payment_Type VARCHAR(50)   NOT NULL,
    amount_Paid  DECIMAL(10,2) NOT NULL,

    CONSTRAINT pk_Payment_Record PRIMARY KEY (record_ID),
    CONSTRAINT fk_PayRec_Record
        FOREIGN KEY (record_ID) REFERENCES Record(record_ID)
);

DROP TABLE IF EXISTS Restock_Record;
CREATE TABLE Restock_Record (
    record_ID INT           NOT NULL,
    Quantity  INT           NOT NULL,
    Cost      DECIMAL(10,2) NOT NULL,

    CONSTRAINT pk_Restock_Record PRIMARY KEY (record_ID),
    CONSTRAINT fk_RestockRec_Record
        FOREIGN KEY (record_ID) REFERENCES Record(record_ID)
);

DROP TABLE IF EXISTS Stock;
CREATE TABLE Stock (
    item_ID        INT           NOT NULL,
    Name           VARCHAR(100)  NOT NULL,
    Category       VARCHAR(100)  NOT NULL,
    wholesale_Cost DECIMAL(10,2) NOT NULL,
    warehouse_Loc  VARCHAR(100)  NOT NULL,

    CONSTRAINT pk_Stock PRIMARY KEY (item_ID)
);

DROP TABLE IF EXISTS Customer;
CREATE TABLE Customer (
    customer_ID    INT           NOT NULL,
    Email          VARCHAR(255)  NOT NULL,
    account_Type   VARCHAR(50)   NOT NULL,
    f_Name         VARCHAR(50)   NOT NULL,
    l_Name         VARCHAR(50)   NOT NULL,
    Address        VARCHAR(255)  NOT NULL,
    Province       VARCHAR(50)   NOT NULL,
    City           VARCHAR(100)  NOT NULL,
    street_Address VARCHAR(255)  NOT NULL,

    CONSTRAINT pk_Customer PRIMARY KEY (customer_ID),
    CONSTRAINT uq_Customer_Email UNIQUE (Email)
    CONSTRAINT chk_Customer_AccountType CHECK 
        (account_Type IN ('Standard','Premium'))
);