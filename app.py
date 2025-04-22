from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
import datetime  
import logging 

app = Flask(__name__)

# 配置数据库
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'PASSword@0'
app.config['MYSQL_DB'] = 'hotel_db'
app.secret_key = 'many random bytes'

mysql = MySQL(app)

# 配置日志
logging.basicConfig(filename='hotel.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

# 主页路由
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_term = request.form['search_term']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Rooms WHERE RoomID LIKE %s OR RoomType LIKE %s OR Status LIKE %s", 
                    ('%' + search_term + '%', '%' + search_term + '%', '%' + search_term + '%'))
        rooms = cur.fetchall()
        
        cur.execute("SELECT * FROM Customers WHERE CustomerID LIKE %s OR Name LIKE %s OR Phone LIKE %s OR Email LIKE %s", 
                    ('%' + search_term + '%', '%' + search_term + '%', '%' + search_term + '%', '%' + search_term + '%'))
        customers = cur.fetchall()
        
        cur.execute("SELECT * FROM Reservations WHERE ReservationID LIKE %s OR CustomerID LIKE %s OR RoomID LIKE %s OR Status LIKE %s", 
                    ('%' + search_term + '%', '%' + search_term + '%', '%' + search_term + '%', '%' + search_term + '%'))
        reservations = cur.fetchall()
        
        cur.execute("SELECT * FROM Services WHERE ServiceID LIKE %s OR ServiceType LIKE %s OR Price LIKE %s", 
                    ('%' + search_term + '%', '%' + search_term + '%', '%' + search_term + '%'))
        services = cur.fetchall()
        
        cur.close()
        return render_template('index.html', rooms=rooms, customers=customers, reservations=reservations, services=services, search_term=search_term, sql_result=None)
    return render_template('index.html')

@app.route('/terminal')
def terminal():
    return render_template('terminal.html', sql_result=None)

@app.route('/execute_sql', methods=['POST'])
def execute_sql():
    sql_code = request.form['sql_code']
    cur = mysql.connection.cursor()
    try:
        cur.execute(sql_code)
        mysql.connection.commit()
        flash("SQL 执行成功！")
        sql_result = cur.fetchall()
    except Exception as e:
        mysql.connection.rollback()
        flash(f"SQL 执行失败：{e}")
        sql_result = None
    
    cur.close()
    return render_template('terminal.html', sql_result=sql_result)

# 房间管理路由
@app.route('/rooms', methods=['GET', 'POST'])
def rooms():
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        if request.form.get('action') == 'add':
            roomid = request.form['roomid']
            roomtype = request.form['roomtype']
            price = request.form['price']
            status = request.form['status']
            floor = request.form['floor']
            orientation = request.form['orientation']
            cur.execute("INSERT INTO Rooms VALUES (%s, %s, %s, %s, %s, %s)", 
                       (roomid, roomtype, price, status, floor, orientation))
            mysql.connection.commit()
            flash("房间添加成功！")
        elif request.form.get('action') == 'delete':
            roomid = request.form['roomid']
            try:
                # 删除与该房间相关的预订记录
                cur.execute("DELETE FROM Reservations WHERE RoomID = %s", (roomid,))
                # 删除房间
                cur.execute("DELETE FROM Rooms WHERE RoomID = %s", (roomid,))
                mysql.connection.commit()
                flash("房间删除成功！")
                return redirect(url_for('rooms'))
            except Exception as e:
                mysql.connection.rollback()
                flash(f"删除失败：数据库错误！{e}")
    
    cur.execute("SELECT * FROM Rooms")
    rooms = cur.fetchall()
    cur.close()
    return render_template('rooms.html', rooms=rooms)

@app.route('/rooms/edit/<int:id>', methods=['GET', 'POST'])
def edit_rooms(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Rooms WHERE RoomID = %s", (id,))
    room = cur.fetchone()
    cur.close()

    if request.method == 'POST':
        roomid = request.form['roomid']
        roomtype = request.form['roomtype']
        price = request.form['price']
        status = request.form['status']
        floor = request.form['floor']
        orientation = request.form['orientation']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE Rooms SET RoomID = %s, RoomType = %s, Price = %s, Status = %s, Floor = %s, Orientation = %s WHERE RoomID = %s",
                    (roomid, roomtype, price, status, floor, orientation, id))
        mysql.connection.commit()
        flash("房间信息更新成功！")
        return redirect(url_for('rooms'))

    return render_template('edit_rooms.html', room=room)

# 客户管理路由
@app.route('/customers', methods=['GET', 'POST'])
def customers():
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        if request.form.get('action') == 'add':
            customerid = request.form['customerid']
            name = request.form['name']
            phone = request.form['phone']
            email = request.form['email']
            address = request.form['address']
            idnumber = request.form['idnumber']

            # 检查客户ID是否已存在
            cur.execute("SELECT * FROM Customers WHERE CustomerID = %s", (customerid,))
            result = cur.fetchone()
            if result:
                flash("客户添加失败：客户ID已存在！")
            else:
                try:
                    cur.execute("INSERT INTO Customers VALUES (%s, %s, %s, %s, %s, %s)",
                                (customerid, name, phone, email, address, idnumber))
                    mysql.connection.commit()
                    flash("客户添加成功！")
                except Exception as e:
                    mysql.connection.rollback()
                    flash(f"客户添加失败：数据库错误！{e}")
        elif request.form.get('action') == 'delete':
            customerid = request.form['customerid']
            try:
                # 删除相关的会员信息
                cur.execute("DELETE FROM Members WHERE CustomerID = %s", (customerid,))
                # 删除相关的预订信息
                cur.execute("DELETE FROM Reservations WHERE CustomerID = %s", (customerid,))
                # 删除相关的交易记录
                cur.execute("DELETE FROM Transactions WHERE CustomerID = %s", (customerid,))
                # 删除客户信息
                cur.execute("DELETE FROM Customers WHERE CustomerID = %s", (customerid,))
                mysql.connection.commit()
                flash("客户删除成功！")
            except Exception as e:
                mysql.connection.rollback()
                flash(f"删除失败：数据库错误！{e}")

    cur.execute("SELECT * FROM Customers")
    customers = cur.fetchall()
    cur.close()
    return render_template('customers.html', customers=customers)

@app.route('/customers/edit/<int:id>', methods=['GET', 'POST'])
def edit_customers(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Customers WHERE CustomerID = %s", (id,))
    customer = cur.fetchone()
    cur.close()

    if request.method == 'POST':
        customerid = request.form['customerid']
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']
        idnumber = request.form['idnumber']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE Customers SET CustomerID = %s, Name = %s, Phone = %s, Email = %s, Address = %s, IDNumber = %s WHERE CustomerID = %s",
                    (customerid, name, phone, email, address, idnumber, id))
        mysql.connection.commit()
        flash("客户信息更新成功！")
        return redirect(url_for('customers'))

    return render_template('edit_customers.html', customer=customer)

# 预订管理路由
@app.route('/reservations', methods=['GET', 'POST'])
def reservations():
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        if request.form.get('action') == 'add':
            customerid = request.form['customerid']
            roomid = request.form['roomid']
            reservationdate_str = request.form['reservationdate']
            checkindate_str = request.form['checkindate']
            checkoutdate_str = request.form['checkoutdate']
            status = request.form['status']
            
            # 转换日期格式
            try:
                reservationdate = datetime.datetime.strptime(reservationdate_str, '%Y-%m-%d').date()
                checkindate = datetime.datetime.strptime(checkindate_str, '%Y-%m-%d').date()
                checkoutdate = datetime.datetime.strptime(checkoutdate_str, '%Y-%m-%d').date()
            except ValueError as e:
                flash(f"Invalid date format: {e}")
                mysql.connection.rollback()
                cur.close()
                return render_template('reservations.html', reservations=reservations)
            
            try:
                log_message = f"CustomerID: {customerid}, RoomID: {roomid}, ReservationDate: {reservationdate.strftime('%Y-%m-%d')}, CheckInDate: {checkindate.strftime('%Y-%m-%d')}, CheckOutDate: {checkoutdate.strftime('%Y-%m-%d')}, Status: {status}"
                logging.error(log_message)
                reservationid = request.form['reservationid']
                cur.execute("INSERT INTO Reservations (ReservationID, CustomerID, RoomID, ReservationDate, CheckInDate, CheckOutDate, Status) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                            (reservationid, customerid, roomid, reservationdate, checkindate, checkoutdate, status))
                mysql.connection.commit()
                flash("Reservation added successfully!")
            
            except Exception as e:
                mysql.connection.rollback()
                flash(f"Failed to add reservation: An unexpected error occurred. {e}")
                logging.error(f"Unexpected error details: {e}")
        elif request.form.get('action') == 'delete':
            reservationid = request.form['reservationid']
            try:
                cur.execute("DELETE FROM Reservations WHERE ReservationID = %s", (reservationid,))
                mysql.connection.commit()
                flash("预订删除成功！")
            except Exception as e:
                mysql.connection.rollback()
                flash(f"删除失败：数据库错误！{e}")
    
    cur.execute("SELECT * FROM Reservations")
    reservations = cur.fetchall()
    cur.close()
    return render_template('reservations.html', reservations=reservations)

@app.route('/reservations/edit/<int:id>', methods=['GET', 'POST'])
def edit_reservations(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Reservations WHERE ReservationID = %s", (id,))
    reservation = cur.fetchone()
    cur.close()

    if request.method == 'POST':
        reservationid = request.form['reservationid']
        customerid = request.form['customerid']
        roomid = request.form['roomid']
        reservationdate_str = request.form['reservationdate']
        checkindate_str = request.form['checkindate']
        checkoutdate_str = request.form['checkoutdate']
        status = request.form['status']
        
        # 转换日期格式
        try:
            reservationdate = datetime.datetime.strptime(reservationdate_str, '%Y-%m-%d').date()
            checkindate = datetime.datetime.strptime(checkindate_str, '%Y-%m-%d').date()
            checkoutdate = datetime.datetime.strptime(checkoutdate_str, '%Y-%m-%d').date()
        except ValueError as e:
            flash(f"Invalid date format: {e}")
            mysql.connection.rollback()
            cur.close()
            return render_template('edit_reservations.html', reservation=reservation)
        
        cur = mysql.connection.cursor()
        cur.execute("UPDATE Reservations SET ReservationID = %s, CustomerID = %s, RoomID = %s, ReservationDate = %s, CheckInDate = %s, CheckOutDate = %s, Status = %s WHERE ReservationID = %s",
                    (reservationid, customerid, roomid, reservationdate, checkindate, checkoutdate, status, id))
        mysql.connection.commit()
        flash("预订信息更新成功！")
        return redirect(url_for('reservations'))

    return render_template('edit_reservations.html', reservation=reservation)

# 服务管理路由
@app.route('/services', methods=['GET', 'POST'])
def services():
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        if request.form.get('action') == 'add':
            serviceid = request.form['serviceid']
            servicetype = request.form['servicetype']
            price = request.form['price']
            servicetime = request.form['servicetime']
            cur.execute("INSERT INTO Services VALUES (%s, %s, %s, %s)",
                        (serviceid, servicetype, price, servicetime))
            mysql.connection.commit()
            flash("服务添加成功！")
        elif request.form.get('action') == 'delete':
            serviceid = request.form['serviceid']
            try:
                # 删除与该服务相关的交易记录
                cur.execute("DELETE FROM Transactions WHERE ServiceID = %s", (serviceid,))
                # 删除服务
                cur.execute("DELETE FROM Services WHERE ServiceID = %s", (serviceid,))
                mysql.connection.commit()
                flash("服务删除成功！")
            except Exception as e:
                mysql.connection.rollback()
                flash(f"删除失败：数据库错误！{e}")

    cur.execute("SELECT * FROM Services")
    services = cur.fetchall()
    cur.close()
    return render_template('services.html', services=services)

@app.route('/services/edit/<int:id>', methods=['GET', 'POST'])
def edit_services(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Services WHERE ServiceID = %s", (id,))
    service = cur.fetchone()
    cur.close()

    if request.method == 'POST':
        serviceid = request.form['serviceid']
        servicetype = request.form['servicetype']
        price = request.form['price']
        servicetime = request.form['servicetime']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE Services SET ServiceID = %s, ServiceType = %s, Price = %s, ServiceTime = %s WHERE ServiceID = %s",
                    (serviceid, servicetype, price, servicetime, id))
        mysql.connection.commit()
        flash("服务信息更新成功！")
        return redirect(url_for('services'))

    return render_template('edit_services.html', service=service)

# 会员管理路由
@app.route('/members', methods=['GET', 'POST'])
def members():
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        if request.form.get('action') == 'add':
            memberid = request.form['memberid']
            customerid = request.form['customerid']
            membershipslevel = request.form['membershipslevel']
            points = request.form['points']
            cur.execute("INSERT INTO Members VALUES (%s, %s, %s, %s)",
                        (memberid, customerid, membershipslevel, points))
            mysql.connection.commit()
            flash("会员添加成功！")
        elif request.form.get('action') == 'delete':
            memberid = request.form['memberid']
            try:
                cur.execute("DELETE FROM Members WHERE MemberID = %s", (memberid,))
                mysql.connection.commit()
                flash("会员删除成功！")
            except Exception as e:
                mysql.connection.rollback()
                flash(f"删除失败：数据库错误！{e}")

    cur.execute("SELECT * FROM Members")
    members = cur.fetchall()
    cur.close()
    return render_template('members.html', members=members)

@app.route('/members/edit/<int:id>', methods=['GET', 'POST'])
def edit_members(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Members WHERE MemberID = %s", (id,))
    member = cur.fetchone()
    cur.close()

    if request.method == 'POST':
        memberid = request.form['memberid']
        customerid = request.form['customerid']
        membershipslevel = request.form['membershipslevel']
        points = request.form['points']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE Members SET MemberID = %s, CustomerID = %s, MembershipLevel = %s, Points = %s WHERE MemberID = %s",
                    (memberid, customerid, membershipslevel, points, id))
        mysql.connection.commit()
        flash("会员信息更新成功！")
        return redirect(url_for('members'))

    return render_template('edit_members.html', member=member)

# 交易管理路由
@app.route('/transactions', methods=['GET', 'POST'])
def transactions():
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        if request.form.get('action') == 'add':
            transactionid = request.form['transactionid']
            customerid = request.form['customerid']
            roomid = request.form['roomid']
            serviceid = request.form['serviceid']
            amount = request.form['amount']
            paymentmethod = request.form['paymentmethod']
            transactiondate = request.form['transactiondate']
            deposit = request.form['deposit']
            refund = request.form['refund']
            tax = request.form['tax']
            cur.execute("INSERT INTO Transactions VALUES (%s, %s, %s,  %s, %s, %s, %s, %s, %s, %s)",
                        (transactionid, customerid, roomid, serviceid, amount, paymentmethod, transactiondate, deposit, refund, tax))
            mysql.connection.commit()
            flash("交易添加成功！")
        elif request.form.get('action') == 'delete':
            transactionid = request.form['transactionid']
            try:
                cur.execute("DELETE FROM Transactions WHERE TransactionID = %s", (transactionid,))
                mysql.connection.commit()
                flash("交易删除成功！")
            except Exception as e:
                mysql.connection.rollback()
                flash(f"删除失败：数据库错误！{e}")

    cur.execute("SELECT * FROM Transactions")
    transactions = cur.fetchall()
    cur.close()
    return render_template('transactions.html', transactions=transactions)

@app.route('/transactions/edit/<int:id>', methods=['GET', 'POST'])
def edit_transactions(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Transactions WHERE TransactionID = %s", (id,))
    transaction = cur.fetchone()
    cur.close()

    if request.method == 'POST':
        transactionid = request.form['transactionid']
        customerid = request.form['customerid']
        roomid = request.form['roomid']
        serviceid = request.form['serviceid']
        amount = request.form['amount']
        paymentmethod = request.form['paymentmethod']
        transactiondate = request.form['transactiondate']
        deposit = request.form['deposit']
        refund = request.form['refund']
        tax = request.form['tax']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE Transactions SET TransactionID = %s, CustomerID = %s, RoomID = %s, ServiceID = %s, Amount = %s, PaymentMethod = %s, TransactionDate = %s, Deposit = %s, Refund = %s, Tax = %s WHERE TransactionID = %s",
                    (transactionid, customerid, roomid, serviceid, amount, paymentmethod, transactiondate, deposit, refund, tax, id))
        mysql.connection.commit()
        flash("交易信息更新成功！")
        return redirect(url_for('transactions'))

    return render_template('edit_transactions.html', transaction=transaction)

if __name__ == '__main__':
    app.run(debug=True)







