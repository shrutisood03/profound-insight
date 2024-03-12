# main.py
# from vscode import create_app
from flask import Blueprint, render_template
from flask_login import login_required, current_user

# app = create_app()
main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('webpage.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)


# if __name__ == '__main__':
#     app.run(debug=True)


