from flask import Blueprint, jsonify
from services.api import fetch_data

platforms_bp = Blueprint("platforms", __name__)

@platforms_bp.route("/platforms", methods=["GET"])
def get_platforms():
    """Obtém todas as plataformas disponíveis."""
    return jsonify(fetch_data("platforms"))
