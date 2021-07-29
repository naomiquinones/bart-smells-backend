from flask import Blueprint, request, jsonify, make_response
from sqlalchemy import desc
from app.models.report import Report
from app.models.rider import Rider
from app import db
from datetime import datetime
from colorama import init, Fore, Back, Style
# below init is for colorama
# use autoreset=True to reset colorama
init()

print(Back.WHITE + Fore.GREEN + 'Loading routes...' + Style.RESET_ALL)


root_bp = Blueprint('root', __name__)
reports_bp = Blueprint('reports', __name__, url_prefix='/reports')
riders_bp = Blueprint('riders', __name__, url_prefix='/riders')
login_bp = Blueprint('login', __name__, url_prefix='/login')


# #############################################################################
# Routes for login
# #############################################################################
@login_bp.route('', methods=['POST'])
def login():
    print(Back.BLUE + Fore.WHITE + 'Loading login route...' + Style.RESET_ALL)
    req_body = request.get_json()
    if not req_body or 'username' not in req_body or 'password' not in req_body:
        return make_response(jsonify({'error': 'Missing username or password'}), 400)

    user = Rider.query.filter_by(
        name=req_body['username'], password_hash=req_body['password']).first()
    if not user:
        return make_response(jsonify({'error': 'Username or password incorrect'}), 400)
    # return make_response(jsonify({'token': user.token}), 200)
    return make_response(jsonify({'user_id': user.id}), 200)


# #############################################################################
# Route for root
# #############################################################################
@root_bp.route('/', methods=['GET'])
def index():
    return '''<h1 style="color:#B6AC3F;font-size:7vw">BART Smells app</h1>'''

# #############################################################################
# Functions to handle report requests
# #############################################################################


@reports_bp.route('', methods=['GET', 'POST'], strict_slashes=False)
def handle_reports():
    print(Fore.BLUE + 'Loading reports...' + Style.RESET_ALL)

    if request.method == "GET":
        reports = Report.query.all()
        report_list = [report.to_dict() for report in reports]

        return make_response(jsonify(report_list), 200)

    elif request.method == "POST":
        print(Fore.GREEN + 'Creating report...' + Style.RESET_ALL)
        req_body = request.get_json()
        if not req_body or "type" not in req_body or "description" not in req_body or "route" not in req_body or "direction" not in req_body or "car_number" not in req_body or "rider_id" not in req_body:
            return make_response(jsonify({"error": "Missing data"}), 400)

        new_report = Report(date=datetime.now(), type=req_body["type"], description=req_body["description"], route=req_body["route"],
                            direction=req_body["direction"], car_number=req_body["car_number"], rider_id=req_body["rider_id"])
        db.session.add(new_report)
        db.session.commit()

        return make_response(jsonify({"message": "Report created"}, {"report": new_report.to_dict()}), 201)


@reports_bp.route('/<report_id>', methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def handle_report(report_id):
    report = Report.query.get(report_id)
    if report is None:
        return make_response("Report not found", 404)

    if request.method == "GET":
        return make_response(jsonify({"report": report.to_dict()}), 200)

    elif request.method == "PUT":
        form_data = request.get_json()
        # check for missing data
        if not form_data or "type" not in form_data or "description" not in form_data or "route" not in form_data or "direction" not in form_data or "car_number" not in form_data:
            return make_response(jsonify({"error": "Invalid or missing data"}), 400)
        # check for duplicate data
        if form_data["type"] == report.type and form_data["description"] == report.description and form_data["route"] == report.route and form_data["direction"] == report.direction and form_data["car_number"] == report.car_number and form_data["rider_id"] == report.rider_id:
            return make_response(jsonify({"error": "No change"}), 200)

        # update report
        report.update_from_form_data(form_data)
        db.session.commit()
        return make_response(jsonify({"message": "Report updated"}, {"report": report.to_dict()}), 200)

    elif request.method == "DELETE":
        db.session.delete(report)
        db.session.commit()
        return make_response(jsonify({"message": f"'{report.type}' report successfully deleted"}), 200)


@reports_bp.route('/<report_id>/votes', methods=['PATCH'])
def update_report_votes(report_id):
    report = Report.query.get(report_id)
    if report is None:
        return make_response("Report not found", 404)

    form_data = request.get_json()
    # check for missing data
    if not form_data or "vote" not in form_data:
        return make_response(jsonify({"error": "Invalid or missing data"}), 400)

    # update votes
    report.update_votes(form_data["vote"])
    db.session.commit()
    return make_response(jsonify({"message": "Report successfully updated"}, {"report": report.to_dict()}), 200)


# #############################################################################
# Functions to handle rider requests
# #############################################################################

@riders_bp.route('', methods=['GET', 'POST'], strict_slashes=False)
def handle_riders():
    print(Fore.BLUE + 'Loading riders...' + Style.RESET_ALL)

    if request.method == "GET":
        riders = Rider.query.all()
        rider_list = [rider.to_dict() for rider in riders]

        return make_response(jsonify(rider_list), 200)

    elif request.method == "POST":
        print(Fore.GREEN + 'Creating rider...' + Style.RESET_ALL)

        req_body = request.get_json()
        if not req_body or "name" not in req_body or "password" not in req_body:
            return make_response(jsonify({"error": "Missing data"}), 400)

        new_rider = Rider(name=req_body["name"], email=req_body["email"]
                          if "email" in req_body else None, password_hash=req_body["password"])
        db.session.add(new_rider)
        db.session.commit()

        return make_response(jsonify({"message": "Rider created"}, {"rider": new_rider.to_dict()}), 201)

# #############################################################################
# Functions to handle individual rider requests
# #############################################################################


@riders_bp.route('/<rider_id>', methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def handle_rider(rider_id):
    rider = Rider.query.get(int(rider_id))
    if rider is None:
        return make_response("Rider not found", 404)

    if request.method == "GET":
        return make_response(jsonify({"rider": rider.to_dict()}), 200)

    elif request.method == "PUT":
        form_data = request.get_json()
        # check for missing data
        if not form_data or "name" not in form_data:
            return make_response(jsonify({"error": "Invalid or missing data"}), 400)

        # check for duplicate data
        if form_data["name"] == rider.name:
            if ("email" in form_data and form_data["email"] == rider.email) or "email" not in form_data:
                return make_response(jsonify({"error": "No change"}), 200)

        # update rider
        rider.update_from_form_data(form_data)
        db.session.commit()
        return make_response(jsonify({"message": "Rider updated"}, {"rider": rider.to_dict()}), 200)

    elif request.method == "DELETE":
        db.session.delete(rider)
        db.session.commit()
        return make_response(jsonify({"message": f"'{rider.name}' rider successfully deleted"}), 200)


@riders_bp.route('/<rider_id>/password', methods=['PATCH'], strict_slashes=False)
def update_rider_password(rider_id):
    rider = Rider.query.get(int(rider_id))
    if rider is None:
        return make_response("Rider not found", 404)
    rider.password_hash = request.get_json()["password"]
    db.session.commit()
    return make_response(jsonify({"message": f'"{rider.name}"\'s password successfully updated'}), 200)
