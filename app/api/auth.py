from app import db
from app.api import api
from app.core.json_responser import JsonResponser
from app.models.user import User
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()


@basic_auth.verify_password
def verify_password(email, password):
    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        return user


@basic_auth.error_handler
def basic_auth_error(status):
    responser = JsonResponser(code=status, message="User authentication failed...")
    return responser.error()


@api.route('/tokens', methods=['POST'])
@basic_auth.login_required
def get_token():
    token = basic_auth.current_user().get_token()
    db.session.commit()
    responser = JsonResponser(data={'token': token}, message='User authenticated successfully')
    return responser.success()


@api.delete('/tokens')
@token_auth.login_required
def revoke_token():
    token_auth.current_user().revoke_token()
    db.session.commit()
    responser = JsonResponser(data={'token': ''}, message='User token revoked successfully', code=204)
    return responser.success()


@token_auth.verify_token
def verify_token(token):
    return User.check_token(token) if token else None


@token_auth.error_handler
def token_auth_error(status):
    responser = JsonResponser(code=status, message="Token is expired or not valid...")
    return responser.error()
