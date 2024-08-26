from flask import render_template, flash, session, Blueprint

loginFaceid_messages_bp = Blueprint('loginFaceid_messages', __name__)


@loginFaceid_messages_bp.route('/loginFaceid-warning-empty-database')
def loginFaceid_warning_empty_database(): 
    # Hata mesajı
    flash('Please register if you have not already done!', 'warning')
    return render_template('loginpage/login.html')

@loginFaceid_messages_bp.route('/loginFaceid-warning-no-face')
def loginFaceid_no_face(): 
    # Hata mesajı
    flash('No face detected. Make sure the camera sees your face!', 'warning')
    return render_template('loginpage/login.html')

@loginFaceid_messages_bp.route('/loginFaceid-error-multiple_faces')
def loginFaceid_error_multiple_faces(): 
    # Hata mesajı
    flash('Multiple faces detected!', 'error')
    return render_template('loginpage/login.html')

@loginFaceid_messages_bp.route('/loginFaceid-error-unknown-face')
def loginFaceid_error_unknown_face(): 
    # Hata mesajı
    flash('Unknown face. Make sure you have a face ID', 'error')
    return render_template('loginpage/login.html')

@loginFaceid_messages_bp.route('/loginFaceid-error-fake-face')
def loginFaceid_error_fake_face(): 
    # Hata mesajı
    flash('Fake face detected!', 'error')
    return render_template('loginpage/login.html')


@loginFaceid_messages_bp.route('/login-success-faceid')
def login_success_faceid():
   
    if 'login_default_data' in session:
        # session'dan ad verisini al
        ad = session.get('login_default_data', {}).get('ad')
        return render_template('homepage/home.html', username=ad)

    else:
        flash('Your session has ended. Please log in again!', 'warning')