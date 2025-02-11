import pandas as pd
from flask import Blueprint, Response
from services.api import fetch_data

reports_bp = Blueprint("reports", __name__)

@reports_bp.route("/<platform>", methods=["GET"])
def export_platform_csv(platform):
    """Gera um relatório CSV com todos os anúncios de uma plataforma específica."""

    PLATFORM_MAPPING = {
        "facebook": "meta_ads",
        "google": "ga4",
        "tiktok": "tiktok_insights"
    }

    platform_value = PLATFORM_MAPPING.get(platform.lower())
    if not platform_value:
        return jsonify({"error": "Plataforma inválida. Use: facebook, google ou tiktok."}), 400

    accounts_data = fetch_data("accounts", {"platform": platform_value})["accounts"]

    all_insights = []
    fields = "clicks,impressions,spend"

    for account in accounts_data:
        insights = fetch_data("insights", {
            "platform": platform_value,
            "account": account["id"],
            "token": account["token"],
            "fields": fields
        })["insights"]

        for item in insights:
            item["account_name"] = account["name"]
            item["platform"] = platform
            all_insights.append(item)

    if not all_insights:
        return jsonify({"error": "Nenhum insight encontrado."}), 404

    df = pd.DataFrame(all_insights)
    csv_data = df.to_csv(index=False, encoding="utf-8")

    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment; filename={platform}.csv"}
    )
