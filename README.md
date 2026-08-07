# Vending Machine Database System: A Centralized Architecture for Automated Retail

**Author:** Alan Sanjit  

## Abstract
This project presents a robust, centralized SQL database system designed to optimize and manage distributed vending machine operations. By tracking inventory levels, geographical machine locations, transaction histories, and personnel workflows, the system provides a comprehensive data foundation for automated retail networks. The repository includes a complete relational database schema, a synthetic data generation pipeline utilizing Python's `Faker` library, and a suite of analytical SQL procedures and views to support real-time operational intelligence.

---

## 1. Introduction
Managing a network of vending machines requires precise coordination of physical inventory, financial transactions, and hardware maintenance. Traditional decentralized methods often lead to stockouts, delayed repairs, and disjointed financial reporting. This system addresses these inefficiencies by implementing a highly normalized relational database model that acts as a single source of truth. It tracks everything from individual machine deployment dates to technician licensing and localized consumer trends across Canadian provinces.

---

## 2. System Architecture & Entity-Relationship Model
The database is built on MySQL and employs a strict relational structure utilizing superclass/subclass hierarchies to eliminate data redundancy. 

### 2.1 Personnel Management Hierarchy
The system uses `Employee` as a superclass to manage basic personnel data (Names, Emails, Roles), branching into specialized subclasses based on operational constraints:
*   **Management:** Tracks administrative seniority levels (Junior, Senior, Director) and manages salary allocations.
*   **Maintenance:** Tracks technician-specific licensing (`lic_No`) to ensure only qualified personnel are dispatched for hardware repairs.

### 2.2 Operational Records (Polymorphic Design)
To maintain a unified chronological ledger, all operational actions are mapped to a central `Record` superclass containing timestamps (`date_Requested`, `date_Completed`). This branches into three distinct transaction types:
1.  **Payment_Record:** Logs financial transactions, supporting various gateways (Apple Pay, Google Pay, Bank Transfers, Credit/Debit).
2.  **Maintenance_Record:** Logs hardware interventions, tracking machine statuses (`functional`, `repair`, `decommissioned`).
3.  **Restock_Record:** Quantifies inventory replenishment and associated wholesale costs.

### 2.3 Inventory & Hardware
*   **Manufacturer & Model:** Maps the supply chain of the vending machines themselves (e.g., *VendTech Inc.* supplying *QuickCan 2000* models), tracking pricing and volumetric capacity.
*   **Stock:** A centralized catalog of restockable items, tracking wholesale costs, item categories, and specific warehouse bin locations.
*   **Customer:** Tracks user accounts (Standard vs. Premium) and geographic demographics for targeted regional analysis.

---

## 3. Data Pipeline & Synthetic Generation
To stress-test the database and simulate years of operational data, a custom data pipeline (`Source/database.py`) was developed. 

*   **Algorithmic Generation:** Utilizes the Python `Faker` library (configured with the `en_CA` locale) to generate highly realistic, Canadian-specific data profiles.
*   **Volume:** Automatically synthesizes 3,000 vending machines, 5,000 unique product SKUs, 5,000 operation records, and comprehensive personnel files.
*   **Relational Integrity:** The script programmatically maintains foreign key constraints during generation, randomly assigning valid `record_IDs`, `employee_IDs`, and `supplier_IDs` across tables before exporting to flat `.csv` files.

---

## 4. Analytical Capabilities
The system is equipped with pre-compiled SQL procedures and views (`Select_Statements.sql`, `ViewCreate_visualise.sql`) designed for immediate business intelligence extraction:

*   **Predictive Maintenance Tracking:** `vw_overdue_maintenance` automatically flags repair requests open for more than 7 days.
*   **Financial Aggregation:** Queries map total transaction volumes and average payment sizes segmented by completion dates and payment methods.
*   **Supply Chain Optimization:** `vw_model_supplier_prices` provides a cross-referenced view of hardware models against competing manufacturer pricing, aiding procurement decisions.
*   **Geographical Analysis:** Analyzes Premium customer densities across Canadian provinces to determine optimal locations for new machine deployments.
*   **Automated Data Cleansing:** Stored procedures seamlessly handle data lifecycle management, such as purging deprecated maintenance records and dynamically calculating personnel salaries based on seniority and role.

---

## 5. Technical Implementation & Deployment

### Prerequisites
*   Python 3.x (with `faker` installed)
*   MySQL Server

### Initialization Steps

1.  **Generate the Dataset:**
    Run the Python pipeline to synthesize the database records. This will populate the `/dump` directory with the necessary CSV files.
    ```bash
    cd Source
    python database.py
    ```
2.  **Build the Schema:**
    Execute the table creation script to initialize the relational framework.
    ```sql
    SOURCE SQL/Tables_Creation.sql;
    ```
3.  **Load the Data:**
    Import the synthesized CSV flat files into the MySQL database. *(Note: Ensure MySQL is configured to allow `LOAD DATA LOCAL INFILE`)*.
    ```sql
    SOURCE SQL/Data_Loading.sql;
    ```
4.  **Initialize Business Logic:**
    Compile the stored procedures and analytical views.
    ```sql
    SOURCE SQL/Data_updation_Procedures.sql;
    SOURCE SQL/ViewCreate_visualise.sql;
    ```
