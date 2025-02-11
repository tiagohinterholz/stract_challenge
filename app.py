from flask import Flask
from routes.home import home_bp
from routes.platforms import platforms_bp
from routes.accounts import accounts_bp
from routes.fields import fields_bp
from routes.insights import insights_bp
from routes.reports import reports_bp
from views.views_platform import views_platform_bp
from views.views_summary import views_summary_bp
from views.views_general import views_general_bp
from views.views_general_summary import views_general_summary_bp


app = Flask(__name__)

# Registrar Blueprints (módulos de rotas)
app.register_blueprint(home_bp)
app.register_blueprint(platforms_bp)
app.register_blueprint(accounts_bp)
app.register_blueprint(fields_bp)
app.register_blueprint(insights_bp)
app.register_blueprint(views_platform_bp)
app.register_blueprint(views_summary_bp)
app.register_blueprint(views_general_bp)
app.register_blueprint(views_general_summary_bp)
app.register_blueprint(reports_bp)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
