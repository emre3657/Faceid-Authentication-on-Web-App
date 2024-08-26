from flask import session, flash, redirect, render_template, url_for, Blueprint
from database import connectDatabase

profile_bp = Blueprint('profile', __name__, template_folder='template')


@profile_bp.route('/profile', methods=['post','get'])
def profile():

    if 'login_default_data' in session:

        token = session.get('login_default_data', {}).get('token')

        mycursor, mydb = connectDatabase()
        sql = "SELECT username, email, password, about, token, face_features FROM faceid"
        mycursor.execute(sql)
        results = mycursor.fetchall()

        for result in results:
            if token == result[4]:
           
                username = result[0]
                email = result[1]
                password = result[2]
                about = result[3]
                faceid = result[5]
                # print(faceid)

                if about == None:
                    about = ""
                if faceid == None:
                    faceidinput = "You do not have a face ID"
                    btnface = "Get a Face ID"
                else:
                    faceidinput = "You have a face ID"
                    btnface = "Update your Face ID"

                session['profile'] = {
                    'email' : email,
                    'faceid' : faceid,
                    'btnface' : btnface
                }

                mydb.close()
                return render_template('profile.html', username=username, email=email, password=password, about=about, faceidinput=faceidinput, btnface=btnface)

    else:    
        flash('Your session has ended. Please log in again!', 'warning')
        return redirect(url_for('pages.login_page'))
