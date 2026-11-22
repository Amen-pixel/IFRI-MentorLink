"""
IFRI_MentorLink — Application principale Flask
"""
import os
import pymysql
pymysql.install_as_MySQLdb()

from dotenv import load_dotenv
from flask import Flask
from extensions import socketio, bcrypt

load_dotenv()


def ajouter_colonnes_manquantes(db):
    """Ajoute dans la base les colonnes présentes dans models.py mais absentes de la table
    (create_all() ne modifie jamais une table qui existe déjà)."""
    from sqlalchemy import inspect, text
    try:
        insp = inspect(db.engine)
        for table in db.metadata.sorted_tables:
            if not insp.has_table(table.name):
                continue
            existantes = {c["name"] for c in insp.get_columns(table.name)}
            for col in table.columns:
                if col.name in existantes:
                    continue
                sql = f"ALTER TABLE {table.name} ADD COLUMN {col.name} " \
                      f"{col.type.compile(dialect=db.engine.dialect)} NULL"
                if col.default is not None and getattr(col.default, "is_scalar", False):
                    val = col.default.arg
                    sql += f" DEFAULT {int(val) if isinstance(val, bool) else repr(val)}"
                db.session.execute(text(sql))
                print(f"[migration] colonne ajoutée : {table.name}.{col.name}")
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print("[migration] ignorée :", e)


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"]                     = os.getenv("SECRET_KEY", "dev-secret")
    app.config["SQLALCHEMY_DATABASE_URI"]        = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    from models import db, login_manager
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")

    from storage import photo_url
    app.jinja_env.globals["photo_url"] = photo_url

    login_manager.login_view    = "auth.login"
    login_message = "Veuillez vous connecter."

    from routes.auth     import auth_bp
    from routes.profil   import profil_bp
    from routes.matching import matching_bp
    from routes.messages import messages_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(profil_bp)
    app.register_blueprint(matching_bp)
    app.register_blueprint(messages_bp)

    with app.app_context():
        db.create_all()
        ajouter_colonnes_manquantes(db)

        # Remplit la liste des compétences si la table est vide
        from models import Competence
        if Competence.query.count() == 0:
            competences = [
                ("Python", "Programmation"), ("Java", "Programmation"),
                ("C/C++", "Programmation"), ("JavaScript", "Programmation"),
                ("PHP", "Programmation"), ("HTML/CSS", "Web"),
                ("React", "Web"), ("Flask/Django", "Web"), ("Node.js", "Web"),
                ("SQL/MySQL", "Bases de données"), ("PostgreSQL", "Bases de données"),
                ("MongoDB", "Bases de données"), ("Algèbre linéaire", "Mathématiques"),
                ("Probabilités", "Mathématiques"), ("Équations différentielles", "Mathématiques"),
                ("Linux/Unix", "Systèmes"), ("Réseaux", "Systèmes"),
                ("Arduino/IoT", "Systèmes"), ("Machine Learning", "Intelligence Artificielle"),
                ("Deep Learning", "Intelligence Artificielle"),
                ("Traitement d'images", "Intelligence Artificielle"),
            ]
            for nom, cat in competences:
                db.session.add(Competence(nom=nom, categorie=cat))
            db.session.commit()

    return app


if __name__ == "__main__":
    app = create_app()
    socketio.run(app, debug=True, host="0.0.0.0", port=8001)
