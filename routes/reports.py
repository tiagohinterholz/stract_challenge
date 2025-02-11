import pandas as pd
from flask import Blueprint, jsonify, Response
from services.reports_services import export_platform_data

reports_bp = Blueprint("reports", __name__)

@reports_bp.route("/export/<platform>", methods=["GET"])
def export_platform_csv(platform):
    """Call no serviço de de exportação e retorna o CSV."""
    try:
        csv_data = export_platform_data(platform)
        return Response(
            csv_data,
            mimetype="text/csv",
            headers={"Content-Disposition": f"attachment; filename={platform}.csv"}
        )
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
