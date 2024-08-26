from config import app

# pages Blueprint
from blueprints.pages.pages import pages_bp

# login Blueprint
from blueprints.loginMessages.login_messages import login_messages_bp
from blueprints.loginControl.login import login_control_bp

# loginFaceid Blueprint
from blueprints.loginFaceidMessages.loginFaceid_messages import loginFaceid_messages_bp
from blueprints.loginFaceidControl.loginFaceid_control import loginFaceid_control_bp

# signup Blueprint
from blueprints.signupMessages.signup_messages import signup_messages_bp
from blueprints.signupControl.signup import signup_control_bp

# signupFaceid Blueprint
from blueprints.signupFaceidControl.signupFaceid_control import signupFaceid_control_bp

# profile Blueprint
from blueprints.profile.profile import profile_bp

# save Blueprint
from blueprints.save.save import save_bp

# editFaceid Blueprint
from blueprints.editFaceid.editFaceid import editFaceid_bp

# newFaceid Blueprint
from blueprints.newFaceid.newFaceid import newFaceid_bp

# logout Blueprint
from blueprints.logout.logout import logout_bp



# ------------- Blueprint'leri uygulamaya kaydet ----------------

# pages
app.register_blueprint(pages_bp)

# login
app.register_blueprint(login_messages_bp)
app.register_blueprint(login_control_bp)

# loginFaceid
app.register_blueprint(loginFaceid_messages_bp)
app.register_blueprint(loginFaceid_control_bp)

# signup
app.register_blueprint(signup_messages_bp)
app.register_blueprint(signup_control_bp)

# signupFaceid
app.register_blueprint(signupFaceid_control_bp)

# profile
app.register_blueprint(profile_bp)

# save
app.register_blueprint(save_bp)

# editFaceid
app.register_blueprint(editFaceid_bp)
   
# newFaceid
app.register_blueprint(newFaceid_bp)

# logout
app.register_blueprint(logout_bp)

    



if __name__ == '__main__':
    app.run()


