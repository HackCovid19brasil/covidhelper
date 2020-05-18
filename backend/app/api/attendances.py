from app import db
from flask import jsonify, request, abort, g, url_for
from app.api import bp
from app.models import User, Attendance
from app.api.errors import bad_request
from app.api.auth import token_auth
from sqlalchemy import or_


@bp.route('/attendances', methods=['GET'])
@token_auth.login_required
def get_attendances():
    """
    This route should return a json object containing the informations 
    of all attendances in the database that the logged responsible have access
    """

    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    search = request.args.get('search', '', type=str)
    conds = [ User.userid.like("%{}%".format(search)), User.name.like("%{}%".format(search)), Attendance.age.like("%{}%".format(search)), Attendance.weight.like("%{}%".format(search))]
    data = Attendance.to_collection_dict(
        Attendance.query.join(Attendance.pacient).filter(or_(*conds))
        , page, per_page, 'api.get_attendances')
    return jsonify(data)


@bp.route('/attendances', methods=['POST'])
def create_attendance():
    """
    This route should create a new attendance and return its informations
    """

    data = request.get_json() or {}
    #TODO: Verifications
    if 'userid' not in data:
        return bad_request('ID do usuario deve ser preenchido')
    user = User.get_by_userid(data['userid'])
    if not user:
        user = User()
        user.from_dict(data)
        db.session.add(user)
    
    attendance = user.add_attendance()
    print(data)
    attendance.from_dict(data)
    db.session.add(attendance)
    db.session.commit()

    response = jsonify(attendance.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.create_attendance')
    return response


@bp.route('/attendances/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_attendance(id):
    """
    This route should update an existing attendance and be available only for the responsible of the attendance
    """

    #TODO: Verifications
    #TODO: Not tested!
    if g.current_user.access < 1:
        abort(403)
    attendance = Attendance.query.get_or_404(id)
    data = request.get_json() or {}
    if 'userid' in data:
        return bad_request('you can not change userid')
    attendance.from_dict(data)
    db.session.commit()
    return jsonify(attendance.to_dict())


@bp.route('/attendances/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete_attendance(id):
    """
    This route should delete an existing attendance and is available only for the responsible of the attendance
    """

    #TODO: Verifications
    #TODO: Not tested!
    if g.current_user.access < 1:
        abort(403)
    attendance = Attendance.query.get_or_404(id)
    db.session.delete(attendance)
    db.session.commit()
    return '', 204


@bp.route('/attendances/<int:id>', methods=['GET'])
@token_auth.login_required
def get_attendances_by_id(id):
    """
    This route should return a json object containing the informations 
    of the attendance with id <id> in the database. Available only for the pacient or the logged responsible
    """
    attendance = Attendance.get_by_id(id)
    if not attendance or g.current_user.id != attendance.pacient.id:
        abort(403)

    return jsonify(Attendance.query.get_or_404(id).to_dict())