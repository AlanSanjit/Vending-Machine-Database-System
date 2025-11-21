import csv
import random
from datetime import datetime, timedelta
from faker import Faker
import string

# Initialize Faker with Canadian locale
fake = Faker('en_CA')

# --- Data Constants ---
MANUFACTURER_BRANDS = [
    'VendTech Inc.', 'QuickSnack Co.', 'AutoBrew Ltd.', 'SnackMaster Pro', 'MegaVend Systems',
    'CoolCan Machines', 'SnackWave Innovations', 'FastFood Automate', 'FreshBite Vends', 'BeveragePro Systems',
    'VendCore Solutions', 'SnackSync Co.', 'EcoVend Tech', 'QuickBite Machines', 'AutoSnack Systems',
    'VendGenius Pro', 'CoolDrink Vends', 'SnackMaster Plus', 'MegaSnack Systems', 'BrewMaster Vends'
]

MODEL_TYPES = ['VM-100', 'VM-200', 'VM-300', 'BeveragePro', 'SnackMaster X', 'QuickCan 2000']

CATEGORIES = ['Snack', 'Beverage', 'Candy', 'Health Food', 'Chips', 'Cookies', 'Energy Drinks', 'Water', 'Soda', 'Juice']
WAREHOUSES = [f'WH-{i:02d}' for i in range(1, 21)]
PROVINCES = ['ON', 'QC', 'BC', 'AB', 'MB', 'NS', 'SK', 'NB', 'NL', 'PE', 'NT', 'NU', 'YT']
CITIES = [
    'Toronto', 'Montreal', 'Vancouver', 'Calgary', 'Ottawa', 'Edmonton', 'Winnipeg', 'Quebec City',
    'Halifax', 'Victoria', 'Saskatoon', 'Regina', 'Charlottetown', 'Yellowknife', 'Iqaluit',
    'St. John\'s', 'Fredericton', 'Whitehorse', 'London', 'Kitchener', 'Windsor', 'Oshawa',
    'Hamilton', 'Kingston', 'Sudbury', 'Thunder Bay', 'Kelowna', 'Nanaimo', 'Kamloops', 'Abbotsford'
]
SUPPLY_TYPES = ['Full Service', 'Parts Only', 'Beverage Focus', 'Snacks & Drinks', 'High Capacity', 'Eco-Friendly Models', 'Economy Models']

# --- Helper Functions ---
def random_date(start, end):
    """Generate a random date between start and end."""
    delta = end - start
    int_delta = delta.days
    random_days = random.randint(0, int_delta)
    return start + timedelta(days=random_days)

def generate_supplier_id():
    """Generate 10-character supplier ID (uppercase letters only)"""
    return ''.join([random.choice(string.ascii_uppercase) for _ in range(10)])

def generate_customer_id():
    """Generate 8-character customer ID (4 digits + 4 uppercase letters)"""
    digits = ''.join([str(random.randint(0, 9)) for _ in range(4)])
    letters = ''.join([random.choice(string.ascii_uppercase) for _ in range(4)])
    # Shuffle the digits and letters to make it truly random
    chars = list(digits + letters)
    random.shuffle(chars)
    return ''.join(chars)

def generate_machine_id():
    """Generate 7-character machine ID (3 uppercase letters + 4 digits)"""
    letters = ''.join([random.choice(string.ascii_uppercase) for _ in range(3)])
    digits = ''.join([str(random.randint(0, 9)) for _ in range(4)])
    # Shuffle the letters and digits
    chars = list(letters + digits)
    random.shuffle(chars)
    return ''.join(chars)

def generate_item_id():
    """Generate 12-digit barcode-style item ID"""
    return ''.join([str(random.randint(0, 9)) for _ in range(12)])

def generate_record_id():
    """Generate 10-character record ID (5 uppercase letters + 5 digits)"""
    letters = ''.join([random.choice(string.ascii_uppercase) for _ in range(5)])
    digits = ''.join([str(random.randint(0, 9)) for _ in range(5)])
    # Shuffle the letters and digits
    chars = list(letters + digits)
    random.shuffle(chars)
    return ''.join(chars)

def generate_employee_id(role):
    """Generate employee ID in format MA#####[5 digits] for Management or TE#####[5 digits] for Technician"""
    number = f"{random.randint(10000, 99999)}"
    if role == 'Management':
        return f"MA{number}"
    else:  # Technician
        return f"TE{number}"

# --- Data Generation Functions ---
def generate_manufacturers(count=100):
    manufacturers = []
    used_ids = set()
    for i in range(count):
        supplier_id = generate_supplier_id()
        while supplier_id in used_ids:
            supplier_id = generate_supplier_id()
        used_ids.add(supplier_id)
        
        brand = random.choice(MANUFACTURER_BRANDS)
        manufacturers.append({
            'supplier_ID': supplier_id,
            'manufact_Brand': brand,
            'contactInfo': fake.email(domain=''.join([c for c in brand.lower() if c.isalnum() or c == ' ']).replace(' ', '') + '.com'),
            'supply_Type': random.choice(SUPPLY_TYPES),
            'Price': round(random.uniform(1500, 5000), 2)
        })
    return manufacturers

def generate_models(count=6):
    models = []
    for i in range(count):
        model_type = random.choice(MODEL_TYPES) + f"-{random.randint(100, 999)}"
        models.append({
            'model_Type': model_type,
            'price': round(random.uniform(1800, 4500), 2),
            'capacity': random.randint(80, 450)
        })
    return models

def generate_employees():
    employees = []
    used_ids = set()
    
    # Generate 200 Managers
    for i in range(200):
        employee_id = generate_employee_id('Manager')
        while employee_id in used_ids:
            employee_id = generate_employee_id('Manager')
        used_ids.add(employee_id)
        
        name = fake.name()
        employees.append({
            'employee_ID': employee_id,
            'Name': name,
            'Role': 'Manager',
            'Contact': fake.email(),
            'seniority_level': random.choice(['Junior', 'Senior', 'Director']),
            'license_number': None  # Managers don't have licenses
        })
    
    # Generate 300 Technicians
    # First, create 60 teams (300/5 = 60 teams)
    team_leaders = []
    supervisor = None
    
    for team_id in range(1, 61):  # Teams 1-60
        # Create 5 technicians per team
        for j in range(5):
            employee_id = generate_employee_id('Technician')
            while employee_id in used_ids:
                employee_id = generate_employee_id('Technician')
            used_ids.add(employee_id)
            
            name = fake.name()
            
            # Make the first technician in each team a lead technician
            if j == 0:
                is_lead = True
                license_number = f"LIC-{random.randint(10000, 99999)}"
                seniority_level = "Lead"  # Lead technician
            else:
                is_lead = False
                license_number = f"LIC-{random.randint(10000, 99999)}"
                seniority_level = None  # Regular technician
            
            employees.append({
                'employee_ID': employee_id,
                'Name': name,
                'Role': 'Technician',
                'team_ID': team_id,
                'Contact': fake.email(),
                'seniority_level': seniority_level,  # "Lead" for team leaders, None for others
                'license_number': license_number
            })
            
            # Store the first technician of each team as a potential lead
            if j == 0:
                team_leaders.append(employee_id)
    
    # Select one technician to be the supervisor for all technicians
    supervisor_id = random.choice(team_leaders)  # Pick one of the team leads
    # Update the supervisor in the employee list
    for emp in employees:
        if emp['employee_ID'] == supervisor_id:
            emp['seniority_level'] = 'Supervisor'
            break
    
    return employees

def generate_customers(count=500):
    customers = []
    used_ids = set()
    for i in range(count):
        customer_id = generate_customer_id()
        while customer_id in used_ids:
            customer_id = generate_customer_id()
        used_ids.add(customer_id)
        
        first_name = fake.first_name()
        last_name = fake.last_name()
        full_name = f"{first_name} {last_name}"
        province = random.choice(PROVINCES)
        city = random.choice(CITIES)
        street_address = fake.street_address()
        customers.append({
            'customer_ID': customer_id,
            'Email': fake.email(),
            'account_Type': random.choice(['Standard', 'Premium']),
            'Name': full_name,
            'f_Name': first_name,
            'L_Name': last_name,
            'Address': f"{street_address}, {city}, {province}",
            'Province': province,
            'City': city,
            'street_Address': street_address
        })
    return customers

def generate_vending_machines(count=3000):
    machines = []
    used_ids = set()
    start_date = datetime(2020, 1, 1)
    end_date = datetime(2025, 11, 21)
    for i in range(count):
        machine_id = generate_machine_id()
        while machine_id in used_ids:
            machine_id = generate_machine_id()
        used_ids.add(machine_id)
        
        machines.append({
            'machine_ID': machine_id,
            'Status': random.choice(['Active', 'Inactive', 'Under Maintenance']),
            'purchase_Date': random_date(start_date, end_date).strftime('%Y-%m-%d')
        })
    return machines

def generate_stock(count=5000):
    stocks = []
    used_ids = set()
    for i in range(count):
        item_id = generate_item_id()
        while item_id in used_ids:
            item_id = generate_item_id()
        used_ids.add(item_id)
        
        category = random.choice(CATEGORIES)
        item_name = fake.catch_phrase()[:30] + " " + random.choice(['Bar', 'Can', 'Pack', 'Bottle', 'Box'])
        stocks.append({
            'Item_ID': item_id,
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
    for i in range(count):
        record_id = generate_record_id()
        while record_id in used_ids:
            record_id = generate_record_id()
        used_ids.add(record_id)
        
        req_date = random_date(start_date, end_date)
        comp_date = req_date + timedelta(days=random.randint(0, 7))
        records.append({
            'record_ID': record_id,
            'date_Requested': req_date.strftime('%Y-%m-%d'),
            'date_Completed': comp_date.strftime('%Y-%m-%d')
        })
    return records

# --- Generate Data ---
print("Generating realistic data with new employee structure and team organization...")
manufacturers = generate_manufacturers()
models = generate_models()
employees = generate_employees()
customers = generate_customers()
vending_machines = generate_vending_machines()
stock = generate_stock()
records = generate_records()

# --- Create Sub-Records ---
# Payment Records (1500)
payment_records = []
for record in random.sample(records, 1500):
    payment_records.append({
        'record_ID': record['record_ID'],
        'payment_Type': random.choice(['Credit Card', 'Cash', 'Mobile Pay', 'Debit Card', 'Apple Pay', 'Google Pay']),
        'Amount': round(random.uniform(1.50, 12.99), 2)
    })

# Maintenance Records (1500)
maintenance_records = []
for record in random.sample(records, 1500):
    maintenance_records.append({
        'record_ID': record['record_ID'],
        'Description': fake.sentence(nb_words=6) + " maintenance",
        'Status': random.choice(['Completed', 'Pending', 'In Progress', 'Cancelled'])
    })

# Restock Records (2000)
restock_records = []
for record in random.sample(records, 2000):
    quantity = random.randint(10, 150)
    cost = round(random.uniform(0.5, 5.0) * quantity, 2)
    restock_records.append({
        'record_ID': record['record_ID'],
        'Quantity': quantity,
        'Cost': cost
    })

# --- Write CSV Files ---
def write_csv(filename, fieldnames, data):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

# Write all files with updated fieldnames
write_csv('Manufacturer.csv', ['supplier_ID', 'manufact_Brand', 'contactInfo', 'supply_Type', 'Price'], manufacturers)
write_csv('Model.csv', ['model_Type', 'price', 'capacity'], models)
write_csv('Employee.csv', ['employee_ID', 'Name', 'Role', 'team_ID', 'Contact', 'seniority_level', 'license_number'], employees)
write_csv('Customer.csv', ['customer_ID', 'Email', 'account_Type', 'Name', 'f_Name', 'L_Name', 'Address', 'Province', 'City', 'street_Address'], customers)
write_csv('Vending_Machine.csv', ['machine_ID', 'Status', 'purchase_Date'], vending_machines)
write_csv('Stock.csv', ['Item_ID', 'Name', 'Category', 'wholesale_Cost', 'warehouse_Loc'], stock)
write_csv('Record.csv', ['record_ID', 'date_Requested', 'date_Completed'], records)
write_csv('Payment_Record.csv', ['record_ID', 'payment_Type', 'Amount'], payment_records)
write_csv('Maintenance_Record.csv', ['record_ID', 'team_ID', 'Description', 'Status'], maintenance_records)
write_csv('Restock_Record.csv', ['record_ID', 'Quantity', 'Cost'], restock_records)

print("✅ CSV files generated successfully with new employee structure!")
print(f"📁 Files created: Manufacturer.csv, Model.csv, Employee.csv, Customer.csv, Vending_Machine.csv, Stock.csv, Record.csv, Payment_Record.csv, Maintenance_Record.csv, Restock_Record.csv")
print("\nNew Employee Structure:")
print("- 200 Managers: MA##### (ID format), have seniority levels (Junior/Mid/Senior/Lead), no teams")
print("- 300 Technicians: TE##### (ID format), organized into 60 teams of 5")
print("- Each team has 1 Lead Technician (seniority_level = 'Lead')")
print("- 1 overall Supervisor (selected from team leads, seniority_level = 'Supervisor')")
print("- Managers: team_ID = NULL, Technicians: team_ID = 1-60")
print("- Technicians: have license numbers, Managers: no license numbers")