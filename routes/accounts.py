from flask import Blueprint, jsonify, request
from services.api import fetch_data

accounts_bp = Blueprint("accounts", __name__)

PLATFORM_MAPPING = {
    "facebook": "meta_ads",
    "google": "ga4",
    "tiktok": "tiktok_insights"
}

@accounts_bp.route("/accounts/<platform>", methods=["GET"])
def get_accounts(platform):
    """Obtém as contas de uma plataforma específica."""
    platform_value = PLATFORM_MAPPING.get(platform.lower())

    if not platform_value:
        return jsonify({"error": "Plataforma inválida. Use: facebook, google ou tiktok."}), 400

    page = request.args.get("page", 1)
    return jsonify(fetch_data("accounts", {"platform": platform_value, "page": page}))
