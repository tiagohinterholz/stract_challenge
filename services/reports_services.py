import pandas as pd
from services.api import fetch_data

def export_platform_data(platform):
    """Gera um relatório CSV com todos os anúncios de uma plataforma específica."""

    PLATFORM_MAPPING = {
        "facebook": "meta_ads",
        "google": "ga4",
        "tiktok": "tiktok_insights"
    }

    platform_value = PLATFORM_MAPPING.get(platform.lower())
    if not platform_value:
        return ValueError("Plataforma inválida. Use: facebook, google ou tiktok.")

    accounts_data = fetch_data("accounts", {"platform": platform_value})["accounts"]

    all_insights = []
    
    fields_db = fetch_data("fields", {"platform": platform_value})
    if "error" in fields_db:
        return ValueError(f"Erro ao buscar campos para {platform}")
    
    fields = ",".join([field["value"] for field in fields_db.get("fields", [])])

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
        return ValueError("Nenhum insight encontrado.")

    df = pd.DataFrame(all_insights)
    df.rename(columns={"cost": "spend", "cpc": "cost_per_click"}, inplace=True)
    # Garantir que os valores numéricos estão no formato correto
    numeric_columns = ["clicks", "cost_per_click", "ctr", "id", "spend", "impressions"]
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").round(2)  # Converter para float
    

    return df.to_csv(index=False, encoding="utf-8")