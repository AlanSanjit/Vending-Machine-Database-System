USE vending_machine_database_system;

-- Q1: Number of PREMIUM customers per province
SELECT 
    Province, COUNT(*) AS premium_customer_count
FROM
    Customer
WHERE
    account_Type = 'Premium'
GROUP BY Province
ORDER BY premium_customer_count DESC , Province;

-- Q2: Total payment amount per completion date
SELECT
    r.date_Completed AS payment_date,
    COUNT(*)         AS num_payments,
    SUM(p.amount_Paid) AS total_amount,
    AVG(p.amount_Paid) AS avg_payment
FROM Payment_Record p
JOIN Record r
      ON p.record_ID = r.record_ID
WHERE r.date_Completed IS NOT NULL
GROUP BY r.date_Completed
ORDER BY r.date_Completed DESC;
;

-- Q3: Open maintenance requests from the last 30 days
SELECT
    mr.record_ID,
    r.date_Requested,
    mr.Description,
    mr.Status,
    DATEDIFF(CURDATE(), r.date_Requested) AS days_open
FROM Maintenance_Record mr
JOIN Record r
      ON mr.record_ID = r.record_ID
WHERE r.date_Completed IS NULL
  AND r.date_Requested >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
ORDER BY r.date_Requested DESC;

-- Q4: Employees and whether they're in Maintenance and/or Management
SELECT
    e.employee_ID,
    e.f_Name,
    e.l_Name,
    e.role,
    e.work_email,
    e.seniority_level,
    CASE WHEN mt.employee_ID IS NOT NULL THEN 'Yes' ELSE 'No' END AS is_maintenance,
    CASE WHEN mg.employee_ID IS NOT NULL THEN 'Yes' ELSE 'No' END AS is_management
FROM Employee e
LEFT JOIN Maintenance mt ON e.employee_ID = mt.employee_ID
LEFT JOIN Management mg  ON e.employee_ID = mg.employee_ID
ORDER BY e.role, e.l_Name, e.f_Name;

-- Q5: Stock items that are more expensive than the average wholesale cost
SELECT
    item_ID,
    Name,
    Category,
    wholesale_Cost,
    warehouse_Loc
FROM Stock
WHERE wholesale_Cost >
      (SELECT AVG(wholesale_Cost) FROM Stock)
ORDER BY wholesale_Cost DESC;

-- Q6: Which manufacturers supply which models, with prices and capacities
SELECT
    mf.supplier_ID,
    mf.manufact_Brand,
    mf.contactInfo,
    m.model_Type,
    m.capacity,
    m.price        AS model_list_price,
    mf.Price       AS supplier_price
FROM Manufacturer mf
JOIN Model m
      ON mf.supply_Type = m.model_Type
ORDER BY m.model_Type, mf.manufact_Brand;

-- Q7: Provinces that have more customers than the average province
SELECT
    Province,
    COUNT(*) AS customer_count
FROM Customer
GROUP BY Province
HAVING COUNT(*) >
       (
         SELECT AVG(prov_count) 
         FROM (
             SELECT COUNT(*) AS prov_count
             FROM Customer
             GROUP BY Province
         ) AS t
       )
ORDER BY customer_count DESC;