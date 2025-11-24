USE vending_machine_database_system;

-- Removing the seniority levels from the maintenance employees
UPDATE Employee
SET seniority_level = ''
WHERE employee_ID IN (SELECT employee_ID FROM Maintenance);
DELIMITER $$

-- Helper procedure: add salary column only if it does NOT exist
DROP PROCEDURE IF EXISTS add_salary_column$$

CREATE PROCEDURE add_salary_column()
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = DATABASE()
          AND TABLE_NAME   = 'Employee'
          AND COLUMN_NAME  = 'salary'
    ) THEN
        ALTER TABLE Employee
        ADD COLUMN salary DECIMAL(10,2) NOT NULL DEFAULT 0;
    END IF;
END$$

DELIMITER ;

CALL add_salary_column();
DROP PROCEDURE add_salary_column;

DELIMITER $$

-- DML 1: Inserting salaries to the employees table in the salary column

DROP PROCEDURE IF EXISTS set_employee_salaries$$

CREATE PROCEDURE set_employee_salaries()
BEGIN
    UPDATE Employee
    SET salary = CASE
        WHEN role = 'Technician'        THEN 50000
        WHEN role = 'Supervisor_Tech'   THEN 60000
        WHEN role = 'Lead_Tech'         THEN 70000

        WHEN role = 'Management' AND seniority_level = 'Junior'   THEN 80000
        WHEN role = 'Management' AND seniority_level = 'Senior'   THEN 95000
        WHEN role = 'Management' AND seniority_level = 'Director' THEN 120000

        ELSE 45000  -- fallback, just in case
    END;
END$$
DELIMITER ;

------------------------------------------------------------------------------------------------
-- DML 2: removing the license_num from Management Employees

DELIMITER $$
DROP PROCEDURE IF EXISTS remove_management_licenses$$

CREATE PROCEDURE remove_management_licenses()
BEGIN
    UPDATE Employee
    SET lic_num = ''
    WHERE role = 'Management';
END$$

DELIMITER ;

-------------------------------------------------------------------------------------------------

-- DML 3: Delete maintenance records completed before 2022-01-01

DELIMITER $$

DROP PROCEDURE IF EXISTS delete_old_maintenance_records$$

CREATE PROCEDURE delete_old_maintenance_records()
BEGIN
    -- Delete maintenance records whose related Record
    -- was completed before 2022-01-01
    DELETE FROM Maintenance_Record MR
    WHERE MR.record_ID IN (
        SELECT r.record_ID
        FROM Record r
        WHERE r.record_ID = MR.record_ID
          AND r.date_Completed IS NOT NULL
          AND r.date_Completed < '2022-01-01'
    );
END$$

DELIMITER ;

CALL set_employee_salaries();
select * from employee;
CALL remove_management_licenses();
select * from employee;
CALL delete_old_maintenance_records();
SELECT
    mr.record_ID,
    r.date_Requested,
    r.date_completed,
    mr.Description,
    mr.Status
FROM Maintenance_Record mr
JOIN Record r
      ON mr.record_ID = r.record_ID
ORDER BY r.date_completed DESC;