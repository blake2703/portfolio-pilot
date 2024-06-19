from flask import render_template, Blueprint

bp = Blueprint("index", __name__, url_prefix="/index")

@bp.route('/test')
def index():
    user = {'username': 'Blake'}
    return render_template('index.html', title='Home', user=user)