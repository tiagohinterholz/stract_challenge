from flask import Blueprint, jsonify, request
from services.api import fetch_data

fields_bp = Blueprint("fields", __name__)

PLATFORM_MAPPING = {
    "facebook": "meta_ads",
    "google": "ga4",
    "tiktok": "tiktok_insights"
}

@fields_bp.route("/fields/<platform>", methods=["GET"])
def get_fields(platform):
    """Obtém os campos disponíveis para uma plataforma específica."""
    platform_value = PLATFORM_MAPPING.get(platform.lower())
    if not platform_value:
        return jsonify({"error": "Plataforma inválida. Use: facebook, google ou tiktok."}), 400
    
    page = request.args.get("page", 1)
    return jsonify(fetch_data("fields", {"platform": platform_value, "page": page}))
