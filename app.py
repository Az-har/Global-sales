from __future__ import print_function
from flask import Flask, render_template, url_for, request, redirect, session
import sqlite3 as sql
import re
import ibm_db
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=3883e7e4-18f5-4afe-be8c-fa31c41761d2.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=31498;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=qpm23984;PWD=XaDaPlC4zHfFcbX7",'','')
app=Flask(__name__)
app.secret_key ='asdfghjklzxcvbnm'

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/dash')
def dash():
    return render_template('dashboard.html')    

@app.route('/brands')
def brands():
    return render_template('brands.html') 

@app.route('/stores')
def stores():
    return render_template('stores.html') 


@app.route('/additems')
def additems():
    return render_template('additems.html') 


@app.route('/index')
def index():
    return render_template('index.html')      

@app.route('/user/<id>')
def user_info(id):
    with sql.connect('inventorymanagement.db') as con:
        con.row_factory=sql.Row
        cur =con.cursor()
        cur.execute(f'SELECT * FROM register WHERE email="{id}"')
        user = cur.fetchall()
    return render_template("user_info.html", user=user[0]) 

@app.route('/signin',methods =['GET', 'POST'])
def signin():
    global userid
    msg = ''
    if request.method == 'POST' :
        un = request.form['username']
        pd = request.form['password']
        sql = "SELECT * FROM register WHERE username =? AND password=?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,un)
        ibm_db.bind_param(stmt,2,pd)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print (account)
        if account:
            session['loggedin'] = True
            session['id'] = account['USERNAME']
            userid=  account['USERNAME']
            session['username'] = account['USERNAME']
            msg = 'Logged in successfully !'
            
            return render_template('index.html', msg = msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('signin.html', msg = msg)

        
@app.route('/signup', methods=['POST','GET'])
def signup():
    msg=''
    if request.method == "POST":
        username=request.form['username']
        email=request.form['email']
        pw=request.form['password'] 
        sql='SELECT * FROM register WHERE email =?'
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,email)
        ibm_db.execute(stmt)
        acnt=ibm_db.fetch_assoc(stmt)
        print(acnt)
            
        if acnt:
            msg='Account already exits!!'
            
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg='Please enter the avalid email address'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg='name must contain only character and number'
        else:
            insert_sql='INSERT INTO register VALUES (?,?,?)'
            pstmt=ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(pstmt,1,username)
            ibm_db.bind_param(pstmt,2,email)
            ibm_db.bind_param(pstmt,3,pw)
            ibm_db.execute(pstmt)
            msg='You have successfully registered click signin!!'
            return render_template("signin.html")    

            
            
         
    elif request.method == 'POST':
        msg="fill out the form first!"
    return render_template("signup.html",msg=msg)    



if __name__ == '__main__':
    app.run(debug=True)
