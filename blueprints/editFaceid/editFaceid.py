from flask import session, request, redirect, url_for, render_template, flash, Blueprint

editFaceid_bp = Blueprint('editFaceid', __name__, template_folder='template')


@editFaceid_bp.route('/editFaceid', methods=['post', 'get'])
def editFaceid():
    if 'login_default_data' in session:
        if request.method == 'POST':
            
            faceid = session.get('profile', {}).get('faceid')
            if faceid == None:
                faceidinput = 'Get a face ID'
            else:
                faceidinput = 'Update your face ID'
            
            return render_template('newFaceid.html', scanLabel=faceidinput)
        else:
            return redirect(url_for('profile.profile'))
    else:
        flash('Your session has ended. Please log in again!', 'warning')
        return redirect(url_for('pages.login_page'))