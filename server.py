#!/usr/bin/env python2.7

import datetime
import random
import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)

DATABASEURI = "postgresql://efg2123:6670@35.237.206.133/proj1part2"
# This line creates a database engine that knows how to connect to the URI above.
engine = create_engine(DATABASEURI)

@app.before_request
def before_request():
  try:
    g.conn = engine.connect()
  except:
    print "uh oh, problem connecting to database"
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  try:
    g.conn.close()
  except Exception as e:
    pass

@app.route('/')
def index():

  # DEBUG: this is debugging code to see what request looks like
  print request.args
  return render_template("home.html")

  @app.route('/index') # home page
  def index2():
    print request.args
    return render_template("index.html")

@app.route('/tables') # tables page
def tables():
  print request.args
  cursor = g.conn.execute("SELECT * FROM tables")
  id = []
  seats = []
  arrivaltime = []
  numofcustomers = []
  available = []
  for t in cursor:
    id.append(t['tablenumber'])
    seats.append(t['seats'])
    arrivaltime.append(t['arrivaltime'])
    numofcustomers.append(t['numofcustomers'])
    available.append(t['available'])
  cursor.close()
  return render_template("tables.html",id = zip(id, seats, arrivaltime, numofcustomers, available))

@app.route('/manager') # tables page
def manager():
  print request.args
  cursor = g.conn.execute("SELECT * FROM manager")
  id = []
  name = []
  timein = []
  wage = []
  for t in cursor:
    id.append(t['mid'])
    name.append(t['name'])
    timein.append(t['timein'])
    wage.append(t['wage'])
  cursor.close()
  print(id)
  print(name)
  print(timein)
  print(wage)
  return render_template("manager.html",id = zip(id, name, timein, wage))

@app.route('/server') # tables page
def server():
  print request.args
  cursor = g.conn.execute("SELECT * FROM server")
  id = []
  name = []
  timein = []
  wage = []
  for t in cursor:
    id.append(t['sid'])
    name.append(t['name'])
    timein.append(t['timein'])
    wage.append(t['wage'])
  cursor.close()
  print(id)
  print(name)
  print(timein)
  print(wage)
  return render_template("server.html",id = zip(id, name, timein, wage))

@app.route('/orders') # tables page
def orders():
  print request.args
  cursor = g.conn.execute("SELECT * FROM orders")
  id = []
  type = []
  time = []

  for t in cursor:
    id.append(t['ordernumber'])
    type.append(t['type'])
    time.append(t['time'])
  cursor.close()
  return render_template("orders.html",id = zip(id, type, time))

@app.route('/driver') # tables page
def driver():
  print request.args
  cursor = g.conn.execute("SELECT * FROM driver")
  id = []
  name = []
  timein = []
  wage = []
  ondelivery = []
  shiftdeliveries = []
  for t in cursor:
    id.append(t['did'])
    name.append(t['name'])
    timein.append(t['timein'])
    wage.append(t['wage'])
    ondelivery.append(t['ondelivery'])
    shiftdeliveries.append(t["shiftdeliveries"])
  cursor.close()
  return render_template("driver.html",id = zip(id, name, timein, wage, ondelivery, shiftdeliveries))

@app.route('/food') # tables page
def food():
  print request.args
  cursor = g.conn.execute("SELECT * FROM food")
  id = []
  name = []
  price = []
  for t in cursor:
    id.append(t['menunumber'])
    name.append(t['name'])
    price.append(t['price'])
  cursor.close()
  return render_template("food.html",id = zip(id, name, price))

@app.route('/bills') # tables page
def bills():
  print request.args
  cursor = g.conn.execute("SELECT * FROM bills")
  id = []
  total = []
  paid = []
  time = []
  for t in cursor:
    id.append(t['billid'])
    total.append(t['total'])
    paid.append(t['paid'])
    time.append(t['time'])
  cursor.close()
  return render_template("bills.html",id = zip(id, total, paid, time))

@app.route('/addserver', methods=['POST'])
def addserver():
  dict = request.form
  dict.to_dict()
  name = dict['name']
  wage = dict['wage']
  result = g.conn.execute('SELECT MAX(server.sid) FROM server')
  for row in result:
      for col in row:
          nexti = row
  result.close()
  nextid = int(nexti[0])
  nextid += 1
  query = "INSERT INTO server (sid, name, wage)"
  query += "VALUES ('" + str(nextid) + "', '" + name + "', '" + wage + "')"
  g.conn.execute(query + ";")
  result = g.conn.execute('SELECT manager.mid FROM manager')
  mid = []
  for t in result:
      mid.append(t['mid'])
  result.close()
  for m in mid:
      query = "INSERT INTO manages (mid, sid)"
      query += "VALUES ('" + m + "', '" + str(nextid) + "')"
      g.conn.execute(query + ";")

  return redirect('/server')

@app.route('/addmanager', methods=['POST'])
def addmanager():
  dict = request.form
  dict.to_dict()
  name = dict['name']
  wage = dict['wage']
  result = g.conn.execute('SELECT MAX(manager.mid) FROM manager')
  for row in result:
      for col in row:
          nexti = row
  result.close()
  nextid = int(nexti[0])
  nextid += 1
  query = "INSERT INTO manager (mid, name, wage)"
  query += "VALUES ('" + str(nextid) + "', '" + name + "', '" + wage + "')"
  g.conn.execute(query + ";")
  result = g.conn.execute('SELECT server.sid FROM server')
  sid = []
  for t in result:
      sid.append(t['sid'])
  result.close()
  for s in sid:
      query = "INSERT INTO manages (mid, sid)"
      query += "VALUES ('" + str(nextid) + "', '" + s + "')"
      g.conn.execute(query + ";")

  return redirect('/manager')

@app.route('/adddriver', methods=['POST'])
def adddriver():
  dict = request.form
  dict.to_dict()
  name = dict['name']
  wage = dict['wage']
  result = g.conn.execute('SELECT MAX(driver.did) FROM driver')
  for row in result:
      for col in row:
          nexti = row
  result.close()
  nextid = int(nexti[0])
  nextid += 1
  query = "INSERT INTO driver (did, name, wage, shiftdeliveries)"
  query += "VALUES ('" + str(nextid) + "', '" + name + "', '" + wage + "',0)"
  g.conn.execute(query + ";")
  return redirect('/driver')

@app.route('/manages', methods=['POST']) # open table page
def manages():
  dict = request.form
  dict.to_dict()
  mid = dict['mid']
  query = "SELECT s.sid, s.name FROM server s, manages m WHERE s.sid = m.sid"
  cursor = g.conn.execute(query + ";")
  name = []
  id = []
  for t in cursor:
        if t['sid'] not in id:
            name.append(t['name'])
            id.append(t['sid'])
  cursor.close()
  return render_template("manages.html",id = zip(name, id))

@app.route('/opentable', methods=['POST']) # open table page
def opentable():
    sql = """ UPDATE tables
                SET arrivaltime = %s, numofcustomers = %s, available = %s
                WHERE tablenumber = %s"""
    table_availability = g.conn.execute('SELECT (available), (tablenumber) FROM tables')
    table_avail = []
    table_number = []
    for t in table_availability:
        print(t)
        table_avail.append(t['available'])
        table_number.append(t['tablenumber'])
    #print(table_avail)
    #print(table_number)
    t = zip(table_avail, table_number)
    t_dict = {}
    for stuff in t:
        t_dict[stuff[1]] = stuff[0]
    #print(t_dict)
    print request.args
    print request.form
    dict = request.form
    dict.to_dict()
    tablenumberI = dict['tablenumber']
    tempnum = tablenumberI
    tempnum1 = int(tempnum)

    if t_dict[tempnum1] == True:
        numofcus = dict['numofcustomers']
        sqlquery = """SELECT seats FROM tables WHERE tablenumber = %s"""
        that_tables_seating_capacity = g.conn.execute(sqlquery, (tempnum1))
        for row in that_tables_seating_capacity:
            for col in row:
                tempcus = int(row[0])


        numofcus1 = int(numofcus)
        if numofcus1 > tempcus:
            return redirect('/tables')

     

        currtime = datetime.datetime.now()
        avail = False
        g.conn.execute(sql, (currtime, numofcus, avail, tablenumberI))
        serves(tablenumberI, False)
        return redirect('/tables')

    print("not possible to open table, as table is not available")
    return redirect('/tables')
    

@app.route('/closetable', methods=['POST']) #closes a table
def closetable():
    print request.args
    print request.form
    dict = request.form
    dict.to_dict()
    tablenumberI = dict['tablenumber']
    #print(tablenumberI)
    query = "UPDATE tables SET arrivaltime = NULL, numofcustomers = 0, available = True "
    query += "WHERE tablenumber = " + str(tablenumberI)
    g.conn.execute(query + ";")
    closed = True
    serves(tablenumberI, closed)
    return redirect('/tables')

@app.route('/paid_bill', methods=['POST'])
def paid_bill():
    print request.args
    print request.form
    dict = request.form
    dict.to_dict()
    bill_id = dict['bid']
    sql = """UPDATE bills SET paid = True WHERE billid = %s"""
    g.conn.execute(sql, (bill_id))
    return redirect('/bills')

#Method that updates table serves relation when a table is closed
def serves(tablenumber, table_boolean):
    tablenum = int(tablenumber)
    sql = """SELECT * FROM serves"""
    sql1 = """ SELECT * FROM server """
    result = g.conn.execute(sql)
    results = g.conn.execute(sql1)
    sid = []
    tablenumbers = []
    for t in result:
        tablenumbers.append(t['tablenumber'])

    for x in results:
        sid.append(x['sid'])
    print("this is sid",  sid)
    if table_boolean == True: #closes server serving table relation
        sql2 = """DELETE FROM serves WHERE tablenumber = %s"""
        for i in tablenumbers:
            if tablenum == i:
                g.conn.execute(sql2, (tablenum))
    else: #opens server serving table relation
        sql2 = """INSERT INTO serves (sid, tablenumber) VALUES (%s, %s)"""
        slave = random.choice(sid)
        g.conn.execute(sql2, (slave, tablenum))
    return None

@app.route('/serves') # serves page
def server_relation():
  print request.args
  cursor = g.conn.execute("SELECT * FROM serves")
  id = []
  tablenum = []

  for t in cursor:
    id.append(t['sid'])
    tablenum.append(t['tablenumber'])
  cursor.close()
  return render_template("serves.html",id = zip(id, tablenum))


@app.route('/includes', methods = ['POST'])
def includes():
    print request.args
    print request.form
    dict = request.form
    dict.to_dict()
    ordernum = dict['ordernumber']
    ordernums = int(ordernum)
    sql = """SELECT * FROM includes"""
    result = g.conn.execute(sql)
    #print(result)
    id = []
    menunums = []
    q = []
    orders = []
    for t in result:
        orders.append(t['ordernumber'])
        #id.append(t['ordernumber'])
        menunums.append(t['menunumber'])
        q.append(t['quantity'])
    combine = zip(orders, menunums, q)
    #print(combine)
    menunum1 = []
    q1 = []
    for t in combine:
        if ordernums == t[0]:
            #print("hi")
            id.append(t[0])
            menunum1.append(t[1])
            q1.append(t[2])
    result.close()
    return render_template("includes.html",id = zip(id, menunum1, q1))


@app.route('/addorder', methods=['POST'])
def addorder():
  dict = request.form
  dict.to_dict()
  print(dict)

  if 'ordernumber' not in request.form: #new order
    inumber = dict['itemnumber']
    amount = dict['amount']
    ordertype = dict['ordertype']

    print(type(inumber))
    menunum = int(inumber)
    print(amount)
    quantity_food = int(amount)
    if ordertype == 'online':

        #get the next order number
        sql = """SELECT MAX(ordernumber) FROM orders"""
        result = g.conn.execute(sql)
        for row in result:
            for col in row:
                nextordernum = row
        result.close()
        nextorderid = int(nextordernum[0])
        nextorderid += 1

        #check item number == menunumber
        sql2 = """SELECT menunumber FROM food"""
        result1 = g.conn.execute(sql2)
        menu_num = []
        for row in result1:
            for col in row:
                 menu_num.append(row)
        menu_num = [int(i[0]) for i in menu_num]
        if menunum not in menu_num:
            print("menu number does not exist in our current menu")
            return redirect('/orders')

        #add to orders table
        currtime = datetime.datetime.now()
        ordertype1 = str(ordertype)
        sql3 = """INSERT INTO orders (type, ordernumber, time) VALUES (%s, %s, %s)"""
        g.conn.execute(sql3, (ordertype1, nextorderid, currtime))

        return redirect('/orders')

    if ordertype == 'offline':
        #print("hi3")
        #get the next order number
        sql = """SELECT MAX(ordernumber) FROM orders"""
        result = g.conn.execute(sql)
        for row in result:
            for col in row:
                nextordernum = row
        result.close()
        nextorderid = int(nextordernum[0])
        nextorderid += 1

        #check item number == menunumber
        sql2 = """SELECT menunumber FROM food"""
        result1 = g.conn.execute(sql2)
        menu_num = []
        for row in result1:
            for col in row:
                 menu_num.append(row)
        menu_num = [int(i[0]) for i in menu_num]
        if menunum not in menu_num:
            print("menu number does not exist in our current menu")
            return redirect('/orders')

        #add to orders table
        currtime = datetime.datetime.now()
        ordertype1 = str(ordertype)
        sql3 = """INSERT INTO orders (type, ordernumber, time) VALUES (%s, %s, %s)"""
        g.conn.execute(sql3, (ordertype1, nextorderid, currtime))

        #should add new order to includes too
        sql4 = """INSERT INTO includes(ordernumber, menunumber, quantity) VALUES (%s, %s, %s)"""
        g.conn.execute(sql4, (nextorderid, menunum, quantity_food))

        return redirect('/orders')
  else: #existing order
    onumber = dict['ordernumber']
    print(onumber)
    ordernum = int(onumber)
    inumber = dict['itemnumber']
    amount = dict['amount']
    menu_num = int(inumber)
    quantity = int(amount)

    #check whether ordernumber exists in orders and not just some random number
    sql = """SELECT ordernumber FROM orders"""
    result = g.conn.execute(sql)
    exist_ordernum = []
    for row in result:
        for col in row:
             exist_ordernum.append(row)
    exist_ordernum = (int(i[0]) for i in exist_ordernum)
    if ordernum not in exist_ordernum:
        print("that order does not exist")
        return redirect('/orders')

    #Need to insert new order into includes table
    sql2 = """INSERT INTO includes (ordernumber, menunumber, quantity) VALUES (%s, %s, %s)"""
    g.conn.execute(sql2, (ordernum, menu_num, quantity))

    return redirect('/orders')

@app.route('/deliveries', methods=['POST']) #view deliveries
def deliveries():
    print request.args
    print request.form
    dict = request.form
    dict.to_dict()
    did1 = dict['did']
    query = "SELECT * FROM delivers "
    query += "WHERE did = '" + str(did1) + "'"
    cursor = g.conn.execute(query + ";")
    did2 = []
    ordernumber = []
    address = []
    deliverytime = []
    outfordelivery =[]
    for t in cursor:
      did2.append(t['did'])
      ordernumber.append(t['ordernumber'])
      address.append(t['address'])
      deliverytime.append(t['deliverytime'])
      outfordelivery.append(t['outfordelivery'])
    cursor.close()
    return render_template("deliveries.html",id = zip(did2, ordernumber, address, deliverytime, outfordelivery))

@app.route('/newdelivery', methods=['POST']) #new delivery
def newdelivery():
    print request.args
    print request.form
    dict = request.form
    dict.to_dict()
    did1 = dict['did']
    ordernumber = dict['ordernumber']
    address = dict['address']

    #update shift deliveries
    query = "SELECT shiftdeliveries FROM driver "
    query += "WHERE did = '" + str(did1) + "'"
    cursor = g.conn.execute(query + ";")
    print(cursor)
    for row in cursor:
        for col in row:
            shiftdelivery = row
    cursor.close()
    newshiftdelivery = int(shiftdelivery[0])
    newshiftdelivery += 1

    query = "UPDATE driver SET shiftdeliveries = " + str(newshiftdelivery)
    query += "WHERE did = '" + did1 + "'"
    g.conn.execute(query + ";")

    sql = """INSERT INTO delivers (ordernumber, did, address, outfordelivery) VALUES (%s, %s, %s, %s)"""
    g.conn.execute(sql, (ordernumber, did1, address, False))
    return redirect('/driver')

# Example of adding new data to the database
@app.route('/add', methods=['POST'])
def add():
  name = request.form['name']
  g.conn.execute('INSERT INTO test VALUES (NULL, ?)', name)
  return redirect('/')

@app.route('/login')
def login():
    abort(401)
    this_is_never_executed()

if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using:

        python server.py

    Show the help text using:

        python server.py --help

    """

    HOST, PORT = host, port
    print "running on %s:%d" % (HOST, PORT)
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


  run()
