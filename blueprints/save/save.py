from flask import session, request, redirect, url_for, render_template, flash, Blueprint
from database import connectDatabase

save_bp = Blueprint('save', __name__, template_folder='template')


@save_bp .route('/save', methods=['post', 'get'])
def save():

    if 'login_default_data' in session:
        if request.method == 'POST':

            mycursor, mydb = connectDatabase()

            email = session.get('profile', {}).get('email')
            faceid = session.get('profile', {}).get('faceid')
            btnface = session.get('profile', {}).get('btnface')

            if faceid == None:
                faceidinput = "You do not have a face"
            else:
                faceidinput = "You have a face ID"
        
            # Kullanıcıdan alınan verileri request.form üzerinden alın
            newUsername = request.form['newUsername']
            newEmail = request.form['newEmail']
            newPassword = request.form['newPassword']
            newRepassword = request.form['newRepassword']
            newAbout = request.form['newAbout']
            
        
            if email == newEmail:
                if len(newPassword) > 6:
                    if newPassword == newRepassword:
            
                        # MySQL veritabanına kullanıcıyı kaydet
                        sql = "UPDATE faceid SET username = %s, password = %s, about = %s WHERE email = %s"
                        val = (newUsername, newPassword, newAbout, email)
                        mycursor.execute(sql, val)
                        mydb.commit()
                        mydb.close()

                        print('kullanıcı bilgileri güncellendi')
                        print('email==newEmail')
                        flash('Informations of the user has been updated!', 'success')

                        return render_template('profile.html', username=newUsername, email=newEmail, password=newPassword, repassword=newRepassword, about=newAbout, faceidinput=faceidinput, btnface=btnface)
                    
                    else:
                        print('şifreler eşleşmiyor!')
                        flash('The passwords do not matching!', 'error')
                        return render_template('profile.html', username=newUsername, email=newEmail, password=newPassword, repassword=newRepassword, about=newAbout, faceidinput=faceidinput, btnface=btnface)
            
                else:
                    flash('Password should be longer than 6 characters!', 'error')
                    return render_template('profile.html', username=newUsername, email=newEmail, password=newPassword, repassword=newRepassword, about=newAbout, faceidinput=faceidinput, btnface=btnface)
            
            # if email != newEmail:
            else:
                # Veritabanında aynı e-posta adresi olup olmadığını kontrol et
                sql = "SELECT email FROM faceid"
                mycursor.execute(sql)
                results = mycursor.fetchall()

                for result in results:
                    if result[0] == newEmail:
                        flash('This email already registered. Please use a different email', 'error')
                        
                        return render_template('profile.html', username=newUsername, email=newEmail, password=newPassword, repassword=newRepassword, about=newAbout, faceidinput=faceidinput, btnface=btnface)
                
                if len(newPassword) > 6:
                    if newPassword == newRepassword:
                        # MySQL veritabanına kullanıcıyı kaydet
                        sql = "UPDATE faceid SET username = %s, email = %s, password = %s, about = %s WHERE email = %s"
                        val = (newUsername, newEmail, newPassword, newAbout, email)
                        mycursor.execute(sql, val)
                        mydb.commit()
                        mydb.close()

                        # !!!session bilgisi güncelleme
                        session['profile']['email'] = newEmail

                        print('kullanıcı bilgileri güncellendi')
                        print('email!=newEmail')
                        flash('Informations of the user has been updated!', 'success')

                        return render_template('profile.html', username=newUsername, email=newEmail, password=newPassword, repassword=newRepassword, about=newAbout, faceidinput=faceidinput, btnface=btnface)
                    else:
                        print('şifreler eşleşmiyor!')
                        flash('The passwords do not matching!', 'error')
                        return render_template('profile.html', username=newUsername, email=newEmail, password=newPassword, repassword=newRepassword, about=newAbout, faceidinput=faceidinput, btnface=btnface)

                else:
                    flash('Password should be longer than 6 characters!', 'error')
                    return render_template('profile.html', username=newUsername, email=newEmail, password=newPassword, repassword=newRepassword, about=newAbout, faceidinput=faceidinput, btnface=btnface)
        else:
            return redirect(url_for('profile.profile'))
    else:
        flash('Your session has ended. Please log in again!', 'warning')
        return redirect(url_for('pages.login_page'))