from flask import redirect, url_for, session, request, Blueprint, render_template
from database import connectDatabase

signup_control_bp = Blueprint('signup_control', __name__, template_folder='template')

@signup_control_bp.route('/signup', methods=['POST'])
def signup():
    if 'signup_data' in session:
       
        return render_template('faceid.html')

    else:
        mycursor, mydb = connectDatabase()

        # Kullanıcıdan alınan verileri request.form üzerinden alın
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        repassword = request.form['repassword']

        # Veritabanında aynı e-posta adresi olup olmadığını kontrol et
    
        sql = "SELECT email FROM faceid"
        mycursor.execute(sql)
        results = mycursor.fetchall()

        # Verileri geçici olarak session değişkeninde sakla
        # email verisi uniqe olduğundan faceid alındığında hangi kullanıcaya eklenmesini gerektiğini bildirecek.
        session['signup_data'] = {
            'email': email,
            'username' : username,
            'password' : password,
            'repassword' : repassword  
        }

        for result in results:
            if email == result[0]:
                return redirect(url_for('signup_messages.signup_warning_email'))

        # Şifrenin uzunluğunu ve şifrelerin eşleşip eşleşmediğini kontrol et
        if len(password) > 6:
            if password == repassword:

                # MySQL veritabanına kullanıcıyı kaydet
                sql = "INSERT INTO faceid (username, email, password) VALUES (%s, %s, %s)"
                val = (username, email, password)
                mycursor.execute(sql, val)
                mydb.commit()
                mydb.close()

                print('kullanıcı signup')
                
                return redirect(url_for('signup_messages.signup_success_default'))
            else:
                # Şifreler eşleşmiyorsa, hata mesajı gösterip signup sayfasına geri dön
                return redirect(url_for('signup_messages.signup_warning_password'))
        else:
            return redirect(url_for('signup_messages.signup_warning_char'))