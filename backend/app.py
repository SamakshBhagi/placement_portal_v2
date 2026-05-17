from flask import Flask
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
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

def ensure_admin_user(app):
    if os.getenv("AUTO_CREATE_ADMIN", "").lower() not in {"1", "true", "yes"}:
        return
    if not EMAIL_USER or not EMAIL_PASSWORD:
        app.logger.warning("AUTO_CREATE_ADMIN is enabled, but EMAIL_USER or EMAIL_PASSWORD is missing.")
        return

    with app.app_context():
        admin = User.query.filter_by(role="admin").first()
        if not admin:
            admin = User(
                email=EMAIL_USER,
                pass_hash=generate_password_hash(EMAIL_PASSWORD),
                role="admin",
            )
            db.session.add(admin)
            db.session.commit()
            app.logger.info("Created admin user from environment.")

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
    @app.cli.command("create-admin")
    def create_admin():
        admin = User.query.filter_by(role="admin").first()
        if not admin:
            admin = User(email = EMAIL_USER, pass_hash = generate_password_hash(EMAIL_PASSWORD), role = "admin" )
            db.session.add(admin)
            db.session.commit()
            print("Created admin")

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


