from flask import Blueprint, jsonify, request
from services.api import fetch_data

insights_bp = Blueprint("insights", __name__)

@insights_bp.route("/insights", methods=["GET"])
def get_insights():
    """Obtém insights de uma conta específica em uma plataforma."""
    platform = request.args.get("platform")
    account = request.args.get("account")
    token = request.args.get("token")
    fields = request.args.get("fields")

    if not platform or not account or not token or not fields:
        return jsonify({"error": "Parâmetros necessários: platform, account, token, fields"}), 400

    return jsonify(fetch_data("insights", {
        "platform": platform,
        "account": account,
        "token": token,
        "fields": fields
    }))
