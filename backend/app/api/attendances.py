from flask import jsonify, request, abort
from app.api import bp
from app.models import User, Attendance
from app.api.errors import bad_request
from app.api.auth import token_auth


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
    data = Attendance.to_collection_dict(Attendance.query, page, per_page, 'api.get_attendances')
    return jsonify(data)


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