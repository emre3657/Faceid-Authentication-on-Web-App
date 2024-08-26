from flask import session, redirect, url_for, request, render_template, flash, Blueprint
from database import connectDatabase

logout_bp = Blueprint('logout', __name__)

@logout_bp.route('/logout', methods=['post', 'get'])
def logout():
  
    if 'login_default_data' in session:
        if request.method == 'POST':
            mycursor, mydb = connectDatabase()
            
            email = session.get('login_default_data', {}).get('email')
            face = session.get('login_default_data', {}).get('face')
            
            # Kullanıcı verilerini güncelle
            sql = "UPDATE faceid SET token = %s WHERE email = %s"
            val = (None, email)
            mycursor.execute(sql, val)

            sql = "UPDATE faceid SET token = %s WHERE face_features = %s"
            val = (None, face)
            mycursor.execute(sql, val)

            mydb.commit()
            mydb.close()
            
            # Bütün session verilerini(Çerezleri) yok et.
            session.clear()

            print("log out success")
            flash('You have been logged out successfully!', 'success')
            return render_template('loginpage/login.html')
        else:
            return redirect(url_for('pages.home_page'))
    else:
        flash('Your session has ended. Please log in again!', 'warning')
        return redirect(url_for('pages.login_page'))
    