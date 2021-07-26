from flask import Blueprint, request, jsonify
from app.models.report import Report
from app.models.user import User

from colorama import init, Fore, Back, Style
init(autoreset=True)

print(Back.GREEN + 'Loading routes...')

root_bp = Blueprint('root', __name__)
reports_bp = Blueprint('reports', __name__, url_prefix='/reports')
users_bp = Blueprint('users', __name__, url_prefix='/users')

@root_bp.route('/', methods=['GET'])
def index():
    return '''<h1 style="color:#B6AC3F;font-size:7vw">BART Smells app</h1>'''


@reports_bp.route('', methods=['GET', 'POST'], strict_slashes=False)
def handle_reports():
    print(Fore.BLUE + 'Loading reports...')
    if request.method == "GET":
        reports = Report.query.all()
    return jsonify(reports.to_dict())


