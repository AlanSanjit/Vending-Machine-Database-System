USE vending_machine_database_system;

CREATE OR REPLACE VIEW vw_overdue_maintenance AS
SELECT
    mr.record_ID,
    r.date_Requested,
    mr.Description,
    mr.Status,
    DATEDIFF(CURDATE(), r.date_Requested) AS days_open
FROM Maintenance_Record mr
JOIN Record r ON mr.record_ID = r.record_ID
WHERE r.date_Completed IS NULL
  AND DATEDIFF(CURDATE(), r.date_Requested) > 7;
  
CREATE OR REPLACE VIEW vw_recent_open_maintenance AS
SELECT
    mr.record_ID,
    r.date_Requested,
    mr.Description,
    mr.Status,
    DATEDIFF(CURDATE(), r.date_Requested) AS days_since_request
FROM Maintenance_Record mr
JOIN Record r
      ON mr.record_ID = r.record_ID
WHERE r.date_Completed IS NULL
  AND r.date_Requested >= DATE_SUB(CURDATE(), INTERVAL 14 DAY)
ORDER BY r.date_Requested DESC;

CREATE OR REPLACE VIEW vw_model_supplier_prices AS
SELECT
    m.model_Type,
    m.price        AS model_list_price,
    m.capacity,
    mf.supplier_ID,
    mf.manufact_Brand,
    mf.Price       AS supplier_price
FROM Model m
JOIN Manufacturer mf
      ON mf.supply_Type = m.model_Type
ORDER BY m.model_Type, mf.manufact_Brand;

select * from vw_model_supplier_prices;
select * from vw_recent_open_maintenance;
select * from vw_overdue_maintenance;