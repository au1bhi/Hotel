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
        return render_template('index.html', rooms=rooms, customers=customers, reservations=reservations, services=services, search_term=search_term)
    return render_template('index.html')

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
                # 删除与该预定相关的交易记录
                # 删除预订
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

if __name__ == '__main__':
    app.run(debug=True)







