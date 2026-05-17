from flask import Flask, jsonify, request
from config import Config
from extensions import db, login_manager, migrate
from schema import *
from werkzeug.security import generate_password_hash
from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.company import company_bp
from routes.student import std_bp
from flask_cors import CORS
import os
#factory method here
FRONTEND_URLS = [
    url.strip()
    for url in os.getenv("FRONTEND_URL", "http://localhost:5173").split(",")
    if url.strip()
]
def admin_credentials():
    return os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASSWORD")


def upsert_admin_user():
    email, password = admin_credentials()
    if not email or not password:
        return False, "EMAIL_USER or EMAIL_PASSWORD is missing"

    db.create_all()
    admin = User.query.filter_by(role="admin").first()
    if admin:
        admin.email = email
        admin.pass_hash = generate_password_hash(password)
        message = "Updated admin user from environment."
    else:
        admin = User(
            email=email,
            pass_hash=generate_password_hash(password),
            role="admin",
        )
        db.session.add(admin)
        message = "Created admin user from environment."

    db.session.commit()
    return True, message

def ensure_admin_user(app):
    if os.getenv("AUTO_CREATE_ADMIN", "").lower() not in {"1", "true", "yes"}:
        return

    with app.app_context():
        try:
            success, message = upsert_admin_user()
        except Exception:
            app.logger.exception("AUTO_CREATE_ADMIN failed.")
            return
        if success:
            app.logger.info(message)
        else:
            app.logger.warning("AUTO_CREATE_ADMIN is enabled, but %s.", message)

def create():
    app = Flask(__name__ ,static_folder = "exports")
    CORS(
        app,
        origins=FRONTEND_URLS,
        supports_credentials=True,
    )
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app,db)
    login_manager.init_app(app)
    ensure_admin_user(app)
    #my APIs
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(company_bp)
    app.register_blueprint(std_bp)
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    @app.route("/")
    def landing():
        return "Up and running"

    @app.route("/api/setup/admin", methods=["POST"])
    def setup_admin():
        setup_token = os.getenv("SETUP_TOKEN")
        if not setup_token:
            return jsonify({"success": False, "message": "Setup endpoint is disabled"}), 404
        if request.headers.get("X-Setup-Token") != setup_token:
            return jsonify({"success": False, "message": "Invalid setup token"}), 403

        success, message = upsert_admin_user()
        status = 200 if success else 400
        return jsonify({"success": success, "message": message}), status

    @app.cli.command("create-admin")
    def create_admin():
        success, message = upsert_admin_user()
        print(message)

    @app.cli.command("clean-drives")
    def clean_drives():
        drives = Drive.query.all()
        for d in drives:
            db.session.delete(d)
        db.session.commit()
    
    @app.cli.command("clean-companies")
    def clean_companies():
        companies = Company.query.all()
        for c in companies:
            db.session.delete(c)
        db.session.commit()

    @app.cli.command("clean-students")
    def clean_students():
        students= Student.query.all()
        for s in students:
            db.session.delete(s)
        db.session.commit()
        
    @app.cli.command("clean-applications")
    def clean_appn():
        applications = Application.query.all()
        for a in applications:
            db.session.delete(a)
        db.session.commit()
    @app.cli.command("clean-users")
    def clean_users():
        users = User.query.all()
        for u in users:
            db.session.delete(u)
        db.session.commit()

    return app


