import csv
import random
import string
from datetime import datetime, timedelta
from faker import Faker

# Initialize Faker with Canadian locale
fake = Faker('en_CA')

# --- Data Constants ---

MANUFACTURER_BRANDS = [
    'VendTech Inc.', 'QuickSnack Co.', 'AutoBrew Ltd.', 'SnackMaster Pro',
    'MegaVend Systems', 'CoolCan Machines', 'SnackWave Innovations',
    'FastFood Automate', 'FreshBite Vends', 'BeveragePro Systems',
    'VendCore Solutions', 'SnackSync Co.', 'EcoVend Tech', 'QuickBite Machines',
    'AutoSnack Systems', 'VendGenius Pro', 'CoolDrink Vends', 'SnackMaster Plus',
    'MegaSnack Systems', 'BrewMaster Vends'
]

MODEL_TYPES = ['VM-100', 'VM-200', 'VM-300', 'BeveragePro', 'SnackMaster X', 'QuickCan 2000']

CATEGORIES = [
    'Snack', 'Beverage', 'Candy', 'Health Food', 'Chips',
    'Cookies', 'Energy Drinks', 'Water', 'Soda', 'Juice'
]

WAREHOUSES = [
    f'Aisle {random.randint(1, 5)} - Bin {random.randint(1, 10)}'
    for _ in range(1, 21)
]

PROVINCES = ['ON', 'QC', 'BC', 'AB', 'MB', 'NS', 'SK', 'NB', 'NL', 'PE', 'NT', 'NU', 'YT']

CITIES = [
    'Toronto', 'Montreal', 'Vancouver', 'Calgary', 'Ottawa', 'Edmonton',
    'Winnipeg', 'Quebec City', 'Halifax', 'Victoria', 'Saskatoon', 'Regina',
    'Charlottetown', 'Yellowknife', 'Iqaluit', "St. John's", 'Fredericton',
    'Whitehorse', 'London', 'Kitchener', 'Windsor', 'Oshawa', 'Hamilton',
    'Kingston', 'Sudbury', 'Thunder Bay', 'Kelowna', 'Nanaimo', 'Kamloops',
    'Abbotsford'
]

# --- Helper Functions ---

def random_date(start, end):
    """Generate a random date between start and end."""
    delta = end - start
    int_delta = delta.days
    random_days = random.randint(0, int_delta)
    return start + timedelta(days=random_days)

def generate_supplier_id():
    """Generate 10-character supplier ID (SUP + 7 digits)."""
    return f"SUP{random.randint(1000000, 9999999)}"

def generate_customer_id():
    return random.randint(1, 10000)

def generate_machine_id():
    return f"VM{random.randint(100, 999)}"

def generate_item_id():
    return random.randint(1, 10000)

def generate_record_id():
    return random.randint(1, 100000)

def generate_employee_id():
    return f"EMP{random.randint(100, 999)}"

def generate_license_number(role):
    """LIC-M-XXXX for Management, LIC-T-XXXX for Technicians."""
    if role == 'Management':
        return f"LIC-M-{random.randint(2000, 2999)}"
    else:
        return f"LIC-T-{random.randint(1000, 1999)}"

# --- Data Generation Functions ---

def generate_models():
    """One model per base MODEL_TYPES; PK-safe and matches FK."""
    models = []
    for base in MODEL_TYPES:
        models.append({
            'model_Type': base,
            'price': round(random.uniform(1800, 4500), 2),
            'capacity': random.randint(80, 450)
        })
    return models

def generate_manufacturers(models, count=100):
    manufacturers = []
    used_ids = set()
    used_emails = set()
    model_types = [m['model_Type'] for m in models]

    for _ in range(count):
        supplier_id = generate_supplier_id()
        while supplier_id in used_ids:
            supplier_id = generate_supplier_id()
        used_ids.add(supplier_id)

        brand = random.choice(MANUFACTURER_BRANDS)
        # domain from brand name
        domain = ''.join(c for c in brand.lower() if c.isalnum())
        email = fake.email(domain=f"{domain}.com")
        while email in used_emails:
            email = fake.email(domain=f"{domain}.com")
        used_emails.add(email)

        supply_type = random.choice(model_types)  # FK-safe

        manufacturers.append({
            'supplier_ID': supplier_id,
            'manufact_Brand': brand,
            'contactInfo': email,
            'supply_Type': supply_type,
            'Price': round(random.uniform(1500, 5000), 2)
        })
    return manufacturers

def generate_employees():
    employees = []
    maintenance_list = []
    management_list = []
    used_ids = set()
    used_emails = set()

    # --- Managers (go into Employee + Management) ---
    for _ in range(200):
        employee_id = generate_employee_id()
        while employee_id in used_ids:
            employee_id = generate_employee_id()
        used_ids.add(employee_id)

        first_name = fake.first_name()
        last_name = fake.last_name()

        role = 'Management'
        # Must match CHECK (Junior, Senior, Director)
        seniority_level = random.choice(['Junior', 'Senior', 'Director'])
        license_number = generate_license_number(role)

        email = fake.email()
        while email in used_emails:
            email = fake.email()
        used_emails.add(email)

        employees.append({
            'employee_ID': employee_id,
            'f_Name': first_name,
            'l_Name': last_name,
            'role': role,
            'work_email': email,
            'lic_num': license_number,
            'seniority_level': seniority_level
        })

        management_list.append({
            'employee_ID': employee_id,
            'seniority_Lvl': seniority_level
        })

    # --- Technicians (go into Employee + Maintenance) ---
    for _ in range(300):
        employee_id = generate_employee_id()
        while employee_id in used_ids:
            employee_id = generate_employee_id()
        used_ids.add(employee_id)

        first_name = fake.first_name()
        last_name = fake.last_name()

        role = random.choice(['Technician', 'Lead_Tech', 'Supervisor_Tech'])
        if role in ['Lead_Tech', 'Supervisor_Tech']:
            seniority_level = random.choice(['Senior'])
        else:
            seniority_level = random.choice(['Junior', 'Mid'])

        license_number = generate_license_number('Technician')

        email = fake.email()
        while email in used_emails:
            email = fake.email()
        used_emails.add(email)

        employees.append({
            'employee_ID': employee_id,
            'f_Name': first_name,
            'l_Name': last_name,
            'role': role,
            'work_email': email,
            'lic_num': license_number,
            'seniority_level': seniority_level
        })

        maintenance_list.append({
            'employee_ID': employee_id,
            'lic_No': license_number
        })

    return employees, maintenance_list, management_list

def generate_customers(count=500):
    customers = []
    used_ids = set()
    used_emails = set()

    for _ in range(count):
        customer_id = generate_customer_id()
        while customer_id in used_ids:
            customer_id = generate_customer_id()
        used_ids.add(customer_id)

        first_name = fake.first_name()
        last_name = fake.last_name()

        email = fake.email()
        while email in used_emails:
            email = fake.email()
        used_emails.add(email)

        province = random.choice(PROVINCES)
        city = random.choice(CITIES)
        street_address = fake.street_address()

        customers.append({
            'customer_ID': customer_id,
            'Email': email,
            'account_Type': random.choice(['Standard', 'Premium']),
            'f_Name': first_name,
            'l_Name': last_name,
            'Address': street_address,
            'Province': province,
            'City': city,
            'street_Address': street_address
        })
    return customers

def generate_machine_id():
    """Generate machine ID (VM + 4 digits)"""
    return f"VM{random.randint(1000, 9999)}"

def generate_vending_machines(count=3000):
    machines = []
    used_ids = set()
    start_date = datetime(2020, 1, 1)
    end_date = datetime(2025, 11, 21)

    for _ in range(count):
        machine_id = generate_machine_id()
        while machine_id in used_ids:
            machine_id = generate_machine_id()
        used_ids.add(machine_id)

        machines.append({
            'machine_ID': machine_id,
            'Status': random.choice(['functional', 'repair', 'decommissioned']),
            'purchase_Date': random_date(start_date, end_date).strftime('%Y-%m-%d')
        })

    return machines

def generate_stock(count=5000):
    stocks = []
    used_ids = set()

    for _ in range(count):
        item_id = generate_item_id()
        while item_id in used_ids:
            item_id = generate_item_id()
        used_ids.add(item_id)

        category = random.choice(CATEGORIES)
        item_name = fake.catch_phrase()[:30] + " " + random.choice(['Bar', 'Can', 'Pack', 'Bottle', 'Box'])

        stocks.append({
            'item_ID': item_id,
            'Name': item_name,
            'Category': category,
            'wholesale_Cost': round(random.uniform(0.5, 5.0), 2),
            'warehouse_Loc': random.choice(WAREHOUSES)
        })
    return stocks

def generate_records(count=5000):
    records = []
    used_ids = set()
    start_date = datetime(2020, 1, 1)
    end_date = datetime(2025, 11, 21)

    for _ in range(count):
        record_id = generate_record_id()
        while record_id in used_ids:
            record_id = generate_record_id()
        used_ids.add(record_id)

        req_date = random_date(start_date, end_date)

        # 50% chance of being completed
        if random.choice([True, False]):
            comp_date = req_date + timedelta(days=random.randint(0, 7))
            comp_str = comp_date.strftime('%Y-%m-%d')
        else:
            # Write \N so MySQL LOAD DATA treats it as NULL
            comp_str = r'\N'

        records.append({
            'record_ID': record_id,
            'date_Requested': req_date.strftime('%Y-%m-%d'),
            'date_Completed': comp_str
        })
    return records

# --- CSV Writer ---

def write_csv(filename, fieldnames, data):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

# --- Generate Everything ---

print("Generating realistic data for all tables...")

models = generate_models()
manufacturers = generate_manufacturers(models)
employees, maintenance, management = generate_employees()
customers = generate_customers()
vending_machines = generate_vending_machines()
stock = generate_stock()
records = generate_records()

# Sub-records for Maintenance_Record, Payment_Record, Restock_Record
num_records = len(records)
num_maint = num_records // 3
num_pay = num_records // 3
num_restock = num_records - num_maint - num_pay

maint_records = []
pay_records = []
restock_records = []

all_record_ids = [r['record_ID'] for r in records]
random.shuffle(all_record_ids)

maint_ids = all_record_ids[:num_maint]
pay_ids = all_record_ids[num_maint:num_maint + num_pay]
restock_ids = all_record_ids[num_maint + num_pay:]

for record_id in maint_ids:
    maint_records.append({
        'record_ID': record_id,
        'Description': fake.sentence(nb_words=6) + " maintenance",
        'Status': random.choice(['functional', 'repair', 'decommissioned'])
    })

for record_id in pay_ids:
    pay_records.append({
        'record_ID': record_id,
        'payment_Type': random.choice([
            'Credit Card', 'Cash', 'Mobile Pay', 'Debit Card',
            'Apple Pay', 'Google Pay', 'Bank Transfer'
        ]),
        'amount_Paid': round(random.uniform(1.50, 12.99) * random.randint(1, 10), 2)
    })

for record_id in restock_ids:
    quantity = random.randint(10, 150)
    cost = round(random.uniform(0.5, 5.0) * quantity, 2)
    restock_records.append({
        'record_ID': record_id,
        'Quantity': quantity,
        'Cost': cost
    })

# --- Write CSV Files ---

write_csv('Model.csv', ['model_Type', 'price', 'capacity'], models)
write_csv('Manufacturer.csv', ['supplier_ID', 'manufact_Brand', 'contactInfo', 'supply_Type', 'Price'], manufacturers)
write_csv('Employee.csv', ['employee_ID', 'f_Name', 'l_Name', 'role', 'work_email', 'lic_num', 'seniority_level'], employees)
write_csv('Maintenance.csv', ['employee_ID', 'lic_No'], maintenance)
write_csv('Management.csv', ['employee_ID', 'seniority_Lvl'], management)
write_csv('Customer.csv', ['customer_ID', 'Email', 'account_Type', 'f_Name', 'l_Name', 'Address', 'Province', 'City', 'street_Address'], customers)
write_csv('Vending_Machine.csv', ['machine_ID', 'Status', 'purchase_Date'], vending_machines)
write_csv('Stock.csv', ['item_ID', 'Name', 'Category', 'wholesale_Cost', 'warehouse_Loc'], stock)
write_csv('Record.csv', ['record_ID', 'date_Requested', 'date_Completed'], records)
write_csv('Payment_Record.csv', ['record_ID', 'payment_Type', 'amount_Paid'], pay_records)
write_csv('Maintenance_Record.csv', ['record_ID', 'Description', 'Status'], maint_records)
write_csv('Restock_Record.csv', ['record_ID', 'Quantity', 'Cost'], restock_records)

print("Done! CSV files generated in current folder.")