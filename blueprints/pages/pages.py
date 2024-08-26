from flask import redirect, render_template, url_for, session, flash, Blueprint

pages_bp = Blueprint('pages', __name__, template_folder='template')


@pages_bp.route('/', methods=['POST', 'GET'])
def first_page():
    return render_template('firstpage/firstpage.html')


@pages_bp.route('/login-page', methods=['POST', 'GET'])
def login_page():
    return render_template('loginpage/login.html')

@pages_bp.route('/signup-page', methods=['POST','GET'])
def signup_page():
    return render_template('signuppage/signup.html')

@pages_bp.route('/home-page', methods=['post','get'])
def home_page():
    
    if 'login_default_data' in session:
        # session'dan ad verisini al
        ad = session.get('login_default_data', {}).get('ad')
        return render_template('homepage/home.html', username=ad)
    
    else: 
        flash('Your session has ended. Please log in again!', 'warning')
        return redirect(url_for('pages.login_page'))