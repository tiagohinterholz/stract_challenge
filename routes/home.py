from flask import Blueprint, jsonify

home_bp = Blueprint("home", __name__)

@home_bp.route("/", methods=["GET"])
def home():
    return jsonify({
        'nome': 'Tiago Francisco Hinterholz',
        'e-mail': 'fh.tiago@gmail.com',
        'linkedin_profile': 'https://www.linkedin.com/in/tiago-hinterholz/'
    })
