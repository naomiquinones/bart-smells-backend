from flask import Blueprint, request, jsonify, make_response
from app.models.report import Report
from app.models.rider import Rider
from app import db
from datetime import datetime
from colorama import init, Fore, Back, Style
# below init is for colorama
# use autoreset=True to reset colorama
init()

print(Back.GREEN + Fore.BLACK + 'Loading routes...' + Style.RESET_ALL)


root_bp = Blueprint('root', __name__)
reports_bp = Blueprint('reports', __name__, url_prefix='/reports')
riders_bp = Blueprint('riders', __name__, url_prefix='/riders')

@root_bp.route('/', methods=['GET'])
def index():
    return '''<h1 style="color:#B6AC3F;font-size:7vw">BART Smells app</h1>'''


@reports_bp.route('', methods=['GET', 'POST'], strict_slashes=False)
def handle_reports():
    print(Fore.BLUE + 'Loading reports...'+ Style.RESET_ALL)

    if request.method == "GET":
        reports = Report.query.all()
        report_list = [report.to_dict() for report in reports]
    
        return make_response(jsonify(report_list), 200)

    elif request.method == "POST":
        print(Fore.GREEN + 'Creating report...'+ Style.RESET_ALL)
        req_body = request.get_json()
        if not req_body or "type" not in req_body or "description" not in req_body or "train" not in req_body or "direction" not in req_body or "car_number" not in req_body or "rider_id" not in req_body:
            return make_response(jsonify({"error": "Missing data"}), 400)

        new_report = Report(date=datetime.now(), type=req_body["type"], description=req_body["description"], train=req_body["train"], direction=req_body["direction"], car_number=req_body["car_number"], rider_id=req_body["rider_id"])
        db.session.add(new_report)
        db.session.commit()

        return make_response(jsonify({"message": "Report created"},{"report":new_report.to_dict()}), 201)

@riders_bp.route('', methods=['GET', 'POST'], strict_slashes=False)
def handle_riders():
    print(Fore.BLUE + 'Loading riders...'+ Style.RESET_ALL)

    if request.method == "GET":
        riders = Rider.query.all()
        rider_list = [rider.to_dict() for rider in riders]

        return make_response(jsonify(rider_list), 200)

    elif request.method == "POST":
        print(Fore.GREEN + 'Creating rider...'+ Style.RESET_ALL)

        req_body = request.get_json()
        if not req_body or "name" not in req_body:
            return make_response(jsonify({"error": "Missing data"}), 400)

        new_rider = Rider(name=req_body["name"], email=req_body["email"] if "email" in req_body else None)
        db.session.add(new_rider)
        db.session.commit()

        return make_response(jsonify({"message": "Rider created"},{"rider":new_rider.to_dict()}), 201)