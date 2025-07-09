from flask import Blueprint, request, jsonify
from app.utils.jwt_utils import create_token
from app.utils.decorators import token_required

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/registration', methods=['POST'])
def register():
    if request.is_json:
        data = request.get_json(force=True)
        token = create_token(data.get('phoneNumber'))
        refresh_token = create_token(data.get('phoneNumber'), refresh=True)

        return jsonify({
            "message": "User registration successful",
            "token": token,
            "refreshToken": refresh_token,
            "expiresIn": 86400
        }), 200
    return jsonify({"error": "Request must be JSON"}), 400

@auth_bp.route('/signin', methods=['POST'])
def signin():
    if request.is_json:
        data = request.get_json()
        token = create_token(data.get('phoneNumber'))
        refresh_token = create_token(data.get('phoneNumber'), refresh=True)

        return jsonify({
            "message": "Login successful",
            "token": token,
            "refreshToken": refresh_token,
            "expiresIn": 86400
        }), 200
    return jsonify({"error": "Request must be JSON"}), 400

@auth_bp.route('/refresh-token', methods=['POST'])
def refresh_token():
    from jwt import ExpiredSignatureError, InvalidTokenError, decode
    from flask import current_app

    if request.is_json:
        data = request.get_json()
        r_token = data.get('refreshToken')

        try:
            payload = decode(r_token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            new_token = create_token(payload['sub'].replace('_refresh', ''))
            return jsonify({
                "token": new_token,
                "expiresIn": 86400
            }), 200
        except ExpiredSignatureError:
            return jsonify({'error': 'Refresh token expired'}), 401
        except InvalidTokenError:
            return jsonify({'error': 'Invalid refresh token'}), 401
    return jsonify({"error": "Request must be JSON"}), 400

@auth_bp.route('/verify-otp', methods=['POST'])
def verify_otp():
    if request.is_json:
        data = request.get_json()
        if not all(k in data for k in ['phoneNumber', 'otpCode']):
            return jsonify({"error": "Missing required fields"}), 400

        token = create_token(data['phoneNumber'])
        refresh_token = create_token(data['phoneNumber'], refresh=True)

        return jsonify({
            "message": "OTP verified",
            "token": token,
            "refreshToken": refresh_token,
            "expiresIn": 86400
        }), 200
    return jsonify({"error": "Request must be JSON"}), 400

@auth_bp.route('/setup-passcode', methods=['POST'])
@token_required
def setup_passcode():
    if request.is_json:
        data = request.get_json()
        if 'passcode' not in data:
            return jsonify({"error": "Missing passcode"}), 400
        return jsonify({"message": "Passcode set", "status": "success"}), 200
    return jsonify({"error": "Request must be JSON"}), 400

@auth_bp.route('/logout', methods=['POST'])
@token_required
def logout():
    return jsonify({"message": "Logout successful"}), 200
