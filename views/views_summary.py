import pandas as pd
from flask import Blueprint, render_template, jsonify
from services.api import fetch_data

views_summary_bp = Blueprint("views_summary", __name__, template_folder="stract_api/templates")

PLATFORM_MAPPING = {
    "facebook": "meta_ads",
    "google": "ga4",
    "tiktok": "tiktok_insights"
}

@views_summary_bp.route("/<platform>/resumo", methods=["GET"])
def display_platform_summary(platform):
    """Exibe resumo agregado dos anúncios por account em uma tabela HTML."""

    platform_value = PLATFORM_MAPPING.get(platform.lower())
    if not platform_value:
        return {"error": "Plataforma inválida. Use: facebook, google ou tiktok."}, 400

    fields_db = fetch_data("fields", {"platform": platform_value})
    if "error" in fields_db:
        return {"error": f"Erro ao buscar campos para {platform}"}, 500

    fields = ",".join([field["value"] for field in fields_db.get("fields", [])])

    accounts_db = fetch_data("accounts", {"platform": platform_value})
    if "error" in accounts_db:
        return {"error": f"Erro ao buscar contas para {platform}"}, 500

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
        return {"error": "Nenhum insight encontrado."}, 404

    df = pd.DataFrame(all_insights)

    # Identificar colunas numéricas para soma
    numeric_columns = df.select_dtypes(include=["number"]).columns.tolist()

    # Agregar por conta (soma valores numéricos, mantém nome da conta)
    df_summary = df.groupby("account_name")[numeric_columns].sum().reset_index()

    return render_template("platform_summary.html", platform=platform.capitalize(), columns=df_summary.columns, data=df_summary.to_dict(orient="records"))
