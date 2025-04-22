from faker import Faker
import mysql.connector
import random
import datetime

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'PASSword@0',
    'database': 'hotel_db'
}

fake = Faker('en_US')

def generate_rooms(num_rooms):
    rooms = []
    room_types = ['Single Room', 'Double Room', 'Deluxe Suite', 'Executive Suite']
    statuses = ['Available', 'Booked', 'Occupied']
    orientations = ['South', 'North', 'East', 'West']
    for i in range(1, num_rooms + 1):
        room_type = random.choice(room_types)
        price = round(random.uniform(100, 500), 2)
        status = random.choice(statuses)
        floor = random.randint(1, 10)
        orientation = random.choice(orientations)
        rooms.append((i, room_type, price, status, floor, orientation))
    return rooms

def generate_customers(num_customers):
    customers = []
    for i in range(1, num_customers + 1):
        name = fake.name()
        phone = "+"+str(random.randint(1,150))+"-"+str(random.randint(1000000000, 9999999999))
        email = fake.email()
        address = fake.address()
        idnumber = "".join([str(random.randint(1000, 9999)) for _ in range(5)])
        customers.append((i, name, phone, email, address, idnumber))
    return customers

def generate_services(num_services):
    services = []
    service_types = ['Dining Service', 'Laundry Service', 'SPA', 'Gym', 'Swimming Pool']
    for i in range(1, num_services + 1):
        service_type = random.choice(service_types)
        price = round(random.uniform(20, 200), 2)
        service_time = fake.date_between(start_date='-1y', end_date='today')
        services.append((i, service_type, price, service_time))
    return services

def generate_reservations(num_reservations, num_customers, num_rooms):
    reservations = []
    statuses = ['Booked', 'Occupied', 'Checked-Out', 'Cancelled']
    for i in range(1, num_reservations + 1):
        customerid = random.randint(1, num_customers)
        roomid = random.randint(1, num_rooms)
        reservationdate = fake.date_between(start_date='-6m', end_date='today')
        checkindate = fake.date_between(start_date=reservationdate, end_date='+30d')
        checkoutdate = fake.date_between(start_date=checkindate, end_date='+60d')
        status = random.choice(statuses)
        reservations.append((i, customerid, roomid, reservationdate, checkindate, checkoutdate, status))
    return reservations

def generate_members(num_members, num_customers):
    members = []
    membership_levels = ['Bronze', 'Silver', 'Gold', 'Platinum']
    used_customer_ids = set()
    for i in range(1, num_members + 1):
        while True:
            customerid = random.randint(1, num_customers)
            if customerid not in used_customer_ids:
                used_customer_ids.add(customerid)
                break
        membershiplevel = random.choice(membership_levels)
        points = random.randint(0, 1000)
        members.append((i, customerid, membershiplevel, points))
    return members

def generate_transactions(num_transactions, num_customers, num_rooms, num_services):
    transactions = []
    payment_methods = ['Credit Card', 'Debit Card', 'Cash', 'Paypal']
    for i in range(1, num_transactions + 1):
        customerid = random.randint(1, num_customers)
        roomid = random.randint(1, num_rooms) if random.random() > 0.5 else None
        serviceid = random.randint(1, num_services) if random.random() > 0.5 else None
        amount = round(random.uniform(50, 1000), 2)
        paymentmethod = random.choice(payment_methods)
        transactiondate = fake.date_time_between(start_date='-1y', end_date='now')
        deposit = round(random.uniform(0, 100), 2) if random.random() > 0.7 else 0.00
        refund = round(random.uniform(0, 50), 2) if random.random() > 0.8 else 0.00
        tax = round(amount * 0.08, 2)
        transactions.append((i, customerid, roomid, serviceid, amount, paymentmethod, transactiondate, deposit, refund, tax))
    return transactions

def insert_data(table_name, data, connection):
    cursor = connection.cursor()
    if table_name == 'Rooms':
        sql = "INSERT INTO Rooms (RoomID, RoomType, Price, Status, Floor, Orientation) VALUES (%s, %s, %s, %s, %s, %s)"
    elif table_name == 'Customers':
        sql = "INSERT INTO Customers (CustomerID, Name, Phone, Email, Address, IDNumber) VALUES (%s, %s, %s, %s, %s, %s)"
    elif table_name == 'Services':
        sql = "INSERT INTO Services (ServiceID, ServiceType, Price, ServiceTime) VALUES (%s, %s, %s, %s)"
    elif table_name == 'Reservations':
        sql = "INSERT INTO Reservations (ReservationID, CustomerID, RoomID, ReservationDate, CheckInDate, CheckOutDate, Status) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    elif table_name == 'Members':
        sql = "INSERT INTO Members (MemberID, CustomerID, MembershipLevel, Points) VALUES (%s, %s, %s, %s)"
    elif table_name == 'Transactions':
        sql = "INSERT INTO Transactions (TransactionID, CustomerID, RoomID, ServiceID, Amount, PaymentMethod, TransactionDate, Deposit, Refund, Tax) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    else:
        print(f"Unknown table name: {table_name}")
        return

    cursor.executemany(sql, data)
    connection.commit()
    print(f"Inserted {cursor.rowcount} records into {table_name}")
    cursor.close()

if __name__ == '__main__':
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE()")
            db_name = cursor.fetchone()
            print("Connected to database ", db_name)

            num_rooms = 15
            num_customers = 60
            num_services = 20
            num_reservations = 30
            num_members = 20
            num_transactions = 20

            rooms_data = generate_rooms(num_rooms)
            customers_data = generate_customers(num_customers)
            services_data = generate_services(num_services)
            reservations_data = generate_reservations(num_reservations, num_customers, num_rooms)
            members_data = generate_members(num_members, num_customers)
            transactions_data = generate_transactions(num_transactions, num_customers, num_rooms, num_services)

            insert_data('Rooms', rooms_data, connection)
            insert_data('Customers', customers_data, connection)
            insert_data('Services', services_data, connection)
            insert_data('Reservations', reservations_data, connection)
            insert_data('Members', members_data, connection)
            insert_data('Transactions', transactions_data, connection)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
