
from flask import Blueprint, redirect, url_for, session, request
from database import connectDatabase
from config import app
import jwt
import datetime

login_control_bp = Blueprint('login_control', __name__, template_folder='template')


@login_control_bp.route('/login', methods=['POST', 'get'])
def login():

    mycursor, mydb = connectDatabase()
    
    email = request.form['email']
    password = request.form['password']

    # Veritabanından bütün e-posta  ve şifre verilerini al.
    sql = "SELECT username, email, password FROM faceid"
    mycursor.execute(sql)
    results = mycursor.fetchall()
    
    # print(results)
    # print(len(results))


    if len(results) > 0:
        for result in results:
            if email == result[1] and password == result[2]:
                ad = result[0]
                token = jwt.encode({'user' : ad.upper(), 'exp' : datetime.datetime.utcnow() + datetime.timedelta(seconds=10)}, app.config['SECRET_KEY'])
                # token = jwt.encode({'user' : ad.upper(), 'exp' : 20}, app_config)
                session['login_default_data'] = {
                    'email' : email,
                    'ad' : ad.upper(),
                    'token' : token
                    }
               
                
                # Kullanıcı verilerini güncelle
                sql = "UPDATE faceid SET token = %s WHERE email = %s"
                val = (token, email)
                mycursor.execute(sql, val)
                mydb.commit()
                mydb.close()

                return redirect(url_for('login_messages.login_success_default'))
        # render template route'ın ismini kullanır.
        # redirect(url_for) methodun ismini kullanır.
        return  redirect(url_for('login_messages.login_error'))

    else: # When len(results) == 0:
        return redirect(url_for('login_messages.login_warning'))