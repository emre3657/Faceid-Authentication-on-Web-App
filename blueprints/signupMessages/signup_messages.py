from flask import render_template, session, flash, url_for, redirect, request, Blueprint

signup_messages_bp = Blueprint('signup_messages', __name__, template_folder='template')


@signup_messages_bp.route('/signup-warning-email')
def signup_warning_email():
    username = session.get('signup_data', {}).get('username')
    email = session.get('signup_data', {}).get('email')
    password = session.get('signup_data', {}).get('password')
    repassword = session.get('signup_data', {}).get('repassword')

    session.pop('signup_data', None)
    flash('This email already registered! Please use a different email', 'warning')
    return render_template('signuppage/signup.html', username=username,  email=email, password=password, repassword=repassword)
    
@signup_messages_bp.route('/signup-warning-char')
def signup_warning_char():
    username = session.get('signup_data', {}).get('username')
    email = session.get('signup_data', {}).get('email')
    password = session.get('signup_data', {}).get('password')

    session.pop('signup_data', None)
    flash('Password must be longer than 6 characters!', 'warning')
    return render_template('signuppage/signup.html', username=username,  email=email, password=password)

@signup_messages_bp.route('/signup-warning-password')
def signup_warning_password():
    username = session.get('signup_data', {}).get('username')
    email = session.get('signup_data', {}).get('email')
    password = session.get('signup_data', {}).get('password')
    repassword = session.get('signup_data', {}).get('repassword')

    session.pop('signup_data', None)
    flash('Passwords do not match!', 'warning')
    return render_template('signuppage/signup.html', username=username,  email=email, password=password, repassword=repassword)
    
@signup_messages_bp.route('/signup-success-default', methods=['get'])
def signup_success_default():
    if 'signup_data' in session:
        flash('User registered successfully!', 'success')       
        # İşlem tamamlandıktan sonra kullanıcıyı başka bir sayfaya yönlendirin
        return render_template('faceid.html')
    else:
        return redirect(url_for('pages.signup_page'))
    
@signup_messages_bp.route('/signup-control', methods=['post', 'get'])
def signup_control():
    if 'signup_data' in session:
        if request.method == 'POST':
            session.pop('signup_data', None)
            return redirect(url_for('pages.login_page'))
        else:
            return redirect(url_for('pages.signup_page'))
    else:
        return redirect(url_for('pages.login_page'))