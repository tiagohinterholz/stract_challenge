from flask import Blueprint, jsonify
from services.api import fetch_data

fields_bp = Blueprint("fields", __name__)

@fields_bp.route("/fields/<platform>", methods=["GET"])
def get_fields(platform):
    """Obtém os campos disponíveis para uma plataforma específica."""
    return jsonify(fetch_data("fields", {"platform": platform}))
