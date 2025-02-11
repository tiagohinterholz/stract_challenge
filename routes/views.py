import pandas as pd
from flask import Blueprint, render_template, jsonify
from services.api import fetch_data

views_bp = Blueprint("views", __name__, template_folder="stract_api/templates")

PLATFROM_MAPPING = {
    "facebook": "meta_ads",
    "google": "ga4",
    "tiktok": "tiktok_insights"
}

@views_bp.route("/<platform>", methods=["GET"])
def display_platform_table(platform):
    """Exibe a tabela HTML com todos anúncios da plataforma especificada na rota"""
    
    platform_value = PLATFROM_MAPPING.get(platform.lower())
    if not platform_value:
        return jsonify({"error": "Plataforma inválida. Use: facebook, google ou tiktok."}), 400
    
    fields_db = fetch_data("fields", {"platform": platform_value})
    if "error" in fields_db:
        return jsonify({"error": f"Erro ao buscar campos para {platform}"}, 500)
    
    fields = ",".join([field["value"] for field in fields_db.get("fields", [])])
    
    accounts_db = fetch_data("accounts", {"platform": platform_value})
    if "error" in accounts_db:
        return jsonify({"error": f"Erro ao buscar constas para {platform}"})
    
    all_insights = []
    
    for account in accounts_db.get("accounts", []):
        insights = fetch_data("insights", {
            "platform": platform_value,
            "account": account["id"],
            "token": account["token"],
            "fields": fields
        })
        
        for item in insights.get("insights", []):
            item["account_name"] = account["name"]
            item["platform"] = platform.capitalize()
            all_insights.append(item)
            
    if not all_insights:
        return jsonify({"error": "Nenhum insight foi encontrado"})
    
    df = pd.DataFrame(all_insights)
    df.drop(columns=[col for col in ["id", "account_id", "ad_id"] if col in df.columns], errors='ignore', inplace=True)
    
    return render_template("platform_report.html", platform=platform.capitalize(), columns=df.columns, data=df.to_dict(orient="records"))
