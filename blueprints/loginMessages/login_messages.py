from flask import Blueprint, render_template, redirect, url_for, session, flash

login_messages_bp = Blueprint('login_messages', __name__, template_folder='template')


@login_messages_bp.route('/login-error-wrong-data')
def login_error():
    flash('Email or password is wrong!', 'error')
    return render_template('loginpage/login.html')

@login_messages_bp.route('/login-warning-empty-database')
def login_warning():
    # Uyarı mesajı
    flash('Please register if you have not already done!', 'warning')
    return render_template('loginpage/login.html')

@login_messages_bp.route('/login-success-default')
def login_success_default():
    
    if 'login_default_data' in session:
        print('Başarıyla oturum açıldı')

        # session'dan ad verisini al
        ad = session.get('login_default_data', {}).get('ad')
        return render_template('homepage/home.html', username=ad)
    else:
        flash('Your session has ended. Please log in again!', 'warning')
        return redirect(url_for('pages.login_page'))