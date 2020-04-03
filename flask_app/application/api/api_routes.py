from functools import wraps
from datetime import datetime

from flask import Blueprint, request, jsonify

from ..models import db, User, ApiToken



api_bp = Blueprint("api_bp", __name__)


def vaild_token_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if request.method != 'POST':
            return jsonify(status=400, msg="invaild API")
        data = request.get_json(silent=True)
        if data is None:
            return jsonify(status=400, msg="invaild API")
        token = data.get('token', '')
        opt = data.get('opt', '')
        params = data.get('params', {})
        if opt  == '':
            return jsonify(status=400, msg="invaild API")
        found_token = ApiToken.query.filter_by(token=token).first()
        if found_token is None or found_token.exipred <= datetime.utcnow():
            return jsonify(status=401, msg="token exipred, please apply for a new one.")
        return func(*args, **kwargs)

    return decorated_view


@api_bp.route('/get_api_token', methods=['POST'])
def get_api_token():
    data = request.get_json(silent=True)
    if data is None or 'username' not in data or 'password' not in data:
        return jsonify(status=400, msg="invaild user information")
    
    user = User.query.filter_by(name=data['username']).first()
    if user is None or user.role == 'user' or not user.check_password(data.get('password', '')):
        return jsonify(status=400, msg="invaild user information")

    Token = ApiToken.query.filter_by(user_id=user.id).first()
    if Token is None:
        token = ApiToken.gen_api_token()
        Token = ApiToken(user=user, token=token)
        db.session.add(Token)
    else:
        Token.update_api_token()
        token = Token.token
    db.session.commit()

    return jsonify(status=200, msg="success", token=token)


@api_bp.route('/api', methods=['POST'])
@vaild_token_required
def api():
    data = request.get_json(silent=True)
    opt = data.get('opt', '')
    params = data.get('params', {})
    return jsonify(status=200, msg='success', rslt={'opt':opt, 'params':params})
