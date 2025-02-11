import pandas as pd
from flask import Blueprint, render_template, jsonify
from services.api import fetch_data

views_general_bp = Blueprint("views_general", __name__, template_folder="stract_api/render_templates")

PLATFORM_MAPPING = {
    "facebok": "meta_ads",
    "google": "ga4",
    "tiktok": "tiktok_insights"
}
@views_general_bp.route("/geral", methods=["GET"])
def displpay_general_table():
    """Exibe todas os anuncios de todas plataformas em uma tabela"""
    
    all_insights = []
    
    for platform, platform_value in PLATFORM_MAPPING.items():
        fields_db = fetch_data("fields", {"platform": platform_value})
        if "error" in fields_db:
            return jsonify({"error": f"Erro ao acessar campos da plataforma {platform}"}, 500)
        
        fields = ",".join(field["value"] for field in fields_db.get("fields", []))
        
        accounts_db = fetch_data("accounts", {"platform": platform_value})
        if "error" in accounts_db:
            return jsonify({"error": f"Erro as contas da plataforma {platform}"}, 500)
        
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
        return jsonify({"error": "Nenhum insight encontrado."}, 404)
    
    df = pd.DataFrame(all_insights)
    
    # Unificar colunas duplicadas (adName e ad_name)
    if "adName" in df.columns and "ad_name" in df.columns:
        df["ad_name"] = df["ad_name"].fillna(df["adName"]) 
        df.drop(columns=["adName"], inplace=True)

    # Unificar as colunas cpc e cost_per_click que é a mesma coisa
    if "cpc" in df.columns and "cost_per_click" in df.columns:
        df["cost_per_click"] = df["cost_per_click"].fillna(df["cpc"])
        df.drop(columns=["cpc"], inplace=True)
    
    # Unificar as colunas cost e spend que aparecentemente é a mesma coisa
    if "spend" in df.columns and "cost" in df.columns:
        df["spend"] = df["spend"].fillna(df["cost"])
        df.drop(columns=["cost"], inplace=True)
    
    # Garantir que a coluna platform tem o nome correto
    df["platform"] = df["platform"].str.capitalize()

    # Aplicar a correção de spend
    df.loc[df["platform"] == "Tiktok", "spend"] = round((df["clicks"] * df["cost_per_click"]), 2)
    df.loc[df["platform"] == "Facebok", "spend"] = round((df["clicks"] * df["cost_per_click"]), 2)
    df.loc[df["platform"] == "Google", "cost_per_click"] = round((df["spend"] / df["clicks"]), 2)

    # pesquisei sobre o CTR e acredito que esteja sendo calculado e apresentado errado  
    # depois dessa analise percebi que dois valores fogem do padrão, pelo pouco que sei acredito que faltou um zero
    # no final de tal forma que nenhum impression ficou com menos de mil - ainda sim valores em % maiores que 20% são
    # considerados fora da curva
    # Identificar quantos valores de impressions estão abaixo de 1000 antes de corrigir
    df.loc[df["impressions"] < 1000, "impressions"] *= 10
    
    # -> CTR (é uma taxa mostrada em %) = clicks * 100 / impresisons
    if "ctr" not in df.columns or df["ctr"].isna().sum() > 0:  # Se CTR não existir ou houver NaN
        df["ctr"] = round(((df["clicks"] / df["impressions"]) * 100), 2)  # Conversão para %
    
    df.drop(columns=[col for col in ["id", "account_id", "ad_id"] if col in df.columns], errors="ignore", inplace=True)
    
    # Substituir NaN por string vazia nas colunas de texto
    for col in ["region", "status", "ad_name", "country"]:
        df[col] = df[col].fillna("")


    return render_template("platform_general.html", columns=df.columns, data=df.to_dict(orient="records"))
        
        