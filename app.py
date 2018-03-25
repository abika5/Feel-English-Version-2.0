from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
from flask_cors import CORS
import pymysql
import time
import datetime
import json


app = Flask(__name__)
app.secret_key = 'despacito'
CORS(app)

conn=pymysql.connect("localhost","admin","admin","abi")
@app.route('/login')
def login():
	return render_template('index.html')

@app.route('/signup',methods=["POST"])
def signup():
	return render_template('signup.html')

@app.route('/page1')
def page1():
	username = session.get("username")
	return render_template('page1.html')

@app.route('/level1_basic')
def level1_basic():
	username = session.get("username")
	return render_template('level1_basic.html')

@app.route('/basic')
def basic():
	username = session.get("username")
	return render_template('basic.html')

@app.route('/intermediate')
def intermediate():
	username = session.get("username")
	return render_template('intermediate.html')

@app.route('/advanced')
def advanced():
	username = session.get("username")
	return render_template('advanced.html')

@app.route('/getsignup',methods=["POST"])
def getsignup():
	firstname=str(request.form["firstname"])
	lastname=str(request.form["lastname"])
	email=str(request.form["email"])
	username=str(request.form["username"])
	password=str(request.form["password"])
	cursor=conn.cursor()
	cursor.execute("SELECT * from users where username='"+username+"'and password='"+password+"'")
	result=cursor.fetchone()
	if result is None:
		sql = "INSERT INTO users (`firstname`, `lastname`, `email`, `username`, `password`) VALUES (%s, %s,%s, %s,%s)"
		cursor.execute(sql,(firstname,lastname,email,username,password))
		conn.commit()
		return redirect(url_for("login"))
	else:
		return "The user already exists"

@app.route('/login_validation',methods=["POST"])
def login_validation():
    username = str(request.form["username"])
    password = str(request.form["password"])
    cursor = conn.cursor()
    cursor.execute("SELECT * from users where username='" + username + "' and password='" + password + "'")
    data=cursor.fetchone()
    if data is None:
    	return "Incorrect username and password"
    else:
    	session["username"]=username
    	return redirect(url_for("page1"))

@app.route('/logout',methods=["POST"])
def logout():
	print(session.get("username"))
	session['logged_in'] = False
	return redirect(url_for("login"))

@app.route('/home')
def home():
	cursor = conn.cursor()
	username = session.get("username")
	cursor.execute("SELECT * from logactions where username='" + username + "'")
	rv=cursor.fetchall()
	session['data']=[]
	for row in rv:
		x={}
		x['action']=row[1]
		x['event']=row[2]
		x['timestamp']=row[3]
		session['data'].append(x)
	cursor.execute("SELECT event,count(*) from logactions where username='" + username + "' group by event")
	rv=cursor.fetchall()
	session['data1']=[]
	for row in rv:
		x={}
		x['eventname']=row[0]
		x['count']=row[1]
		session['data1'].append(x)
	print(session['data1'])
	cursor.execute("select event,max(y.total) from (select event,count(*) as total from logactions where username='"+username+"' group by event)y");
	action1=cursor.fetchone()[0];
	session['action1']=action1
	cursor.execute("SELECT event,count(*) from logactions where username='" + username + "' and currenttime >= CURDATE() group by event")
	rv=cursor.fetchall()
	session['data2']=[]
	for row in rv:
		x={}
		x['eventname']=row[0]
		x['count']=row[1]
		session['data2'].append(x)
	print(session['data2'])
	session['data3']=[]
	cursor.execute("select event,max(y.total) from (select event,count(*) as total from logactions where username='"+username+"' and currenttime >= CURDATE() group by event)y");
	action2=cursor.fetchone()[0]
	session['action2']=action2
	session['tf1']="today"

	event1="tag interaction"
	cursor.execute("SELECT username,count(*) from logactions where username in (select name from users) and event='" + event1 + "' group by username")
	rv=cursor.fetchall()
	session['data3']=[]
	for row in rv:
		x={}
		x['username']=row[0]
		x['count']=row[1]
		session['data3'].append(x)
	cursor.execute("select username,count(*) from logactions where event='"+event1+"' and username in (select name from users) group by username limit 1;")
	name=cursor.fetchone()[0]
	session['maxuser']=name
	session['eventaction']=event1


	return render_template('home.html',data=session['data'],data1=session['data1'],data2=session['data2'],data3=session['data3'])

@app.route('/logactions',methods=["POST"])
def logactions():
	obj = request.get_json()
	event = obj.get('content')
	username = obj.get('username')
	action=obj.get('action')
	cursor=conn.cursor()
	ts=time.time()
	timestamp=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
	sql = "INSERT INTO logactions (`username`,`action`,`event`,`currenttime`) VALUES (%s,%s,%s,%s)"
	cursor.execute(sql,(username,event,action,timestamp))
	conn.commit()
	return "Hello"

@app.route('/handletimeframe',methods=["POST"])
def handletimeframe():
	cursor=conn.cursor()
	username=session.get("username")
	if(request.form.get("Timeframe")=="yesterday"):
		cursor.execute("SELECT event,count(*) from logactions where username='" + username + "' and currenttime >= DATE_SUB(CURDATE(), INTERVAL 1 DAY) AND currenttime < CURDATE() group by event")
		rv=cursor.fetchall()
		session['data2']=[]
		for row in rv:
			x={}
			x['eventname']=row[0]
			x['count']=row[1]
			session['data2'].append(x)
			print(session['data2'])
		cursor.execute("select event,max(y.total) from (select event,count(*) as total from logactions where username='"+username+"' and currenttime >= DATE_SUB(CURDATE(), INTERVAL 1 DAY) AND currenttime < CURDATE() group by event)y");
		action2=cursor.fetchone()[0]
		session['action2']=action2
		session['tf1']="yesterday"
	elif(request.form.get("Timeframe")=="month"):
		cursor.execute("SELECT event,count(*) from logactions where username='" + username + "' and currenttime >= DATE_SUB(CURDATE(), INTERVAL DAYOFMONTH(CURDATE())-1 DAY) group by event")
		rv=cursor.fetchall()
		session['data2']=[]
		for row in rv:
			x={}
			x['eventname']=row[0]
			x['count']=row[1]
			session['data2'].append(x)
			print(session['data2'])
		cursor.execute("select event,max(y.total) from (select event,count(*) as total from logactions where username='"+username+"' and currenttime >= DATE_SUB(CURDATE(), INTERVAL DAYOFMONTH(CURDATE())-1 DAY) group by event)y");
		action2=cursor.fetchone()[0]
		session['action2']=action2
		session['tf1']="this month"
	return render_template('home.html',data=session['data'],data1=session['data1'],data2=session['data2'],data3=session['data3'])


@app.route('/handleevent',methods=["POST"])
def handleevent():
	cursor=conn.cursor()
	username=session.get("username")
	event = request.form.get("Event")
	cursor.execute("SELECT username,count(*) from logactions where username in (select name from users) and event='" + event + "' group by username")
	rv=cursor.fetchall()
	session['data3']=[]
	for row in rv:
		x={}
		x['username']=row[0]
		x['count']=row[1]
		session['data3'].append(x)
	cursor.execute("select username,count(*) from logactions where event='"+event+"' and username in (select name from users) group by username limit 1;")
	name=cursor.fetchone()[0]
	session['maxuser']=name
	session['eventaction']=event
	return render_template('home.html',data=session['data'],data1=session['data1'],data2=session['data2'],data3=session['data3'])


	
	

if __name__ == "__main__":
    app.run(debug=True) 

 
 
