Markdown
# 🎓 IFRI MentorLink

> Plateforme de mise en relation mentor-mentoré pour les étudiants de l'IFRI.

---

## 🛠️ Stack Technique

* **Côté serveur :** Python / Flask + Flask-SocketIO
* **Base de données :** MySQL (via SQLAlchemy + PyMySQL)
* **Authentification :** Flask-Login + Flask-Bcrypt
* **Temps réel :** SocketIO (messagerie instantanée)

---

## 🚀 Installation

### 1. Cloner le projet

git clone [https://github.com/VOTRE_COMPTE/PIL1_2526_XX.git](https://github.com/VOTRE_COMPTE/IFRI-MentorLink.git)

cd PIL1_2526_XX

### 2. Créer l'environnement virtuel
Bash

python -m venv venv

# Windows
venv\Scripts\activate

# Linux / Mac
source venv/bin/activate

### 3. Installer les dépendances

Bash

pip install -r requirements.txt

### 4. Configurer les variables d'environnement
Bash

cp .env.example .env

# Éditer le fichier .env avec vos identifiants de base de données

### 5. Créer la base de données
Bash
mysql -u root -p < schema.sql

### 6. Lancer le serveur
Bash

python app.py

Accéder à l'application via : http://localhost:5000

## 📁 Structure du Projet

Plaintext

ifri_mentorlink/

├── app.py              # Application Flask principale

├── models.py           # Modèles SQLAlchemy

├── matching.py         # Algorithme de matching

├── schema.sql          # Schéma MySQL

├── requirements.txt

├── .env.example        # Template des variables d'environnement

├── .gitignore

├── routes/

│   ├── auth.py         # Inscription / connexion

│   ├── profil.py       # Dashboard, profil, compétences

│   ├── matching.py     # Suggestions & offres

│   └── messages.py     # Messagerie (SocketIO)

├── templates/          # Templates Jinja2

└── static/             # CSS, JS, images

## 🧮 Algorithme de Matching

Le score de compatibilité est calculé ainsi :

### 50 % — Couverture des lacunes du mentoré par les compétences du mentor

### 30 % — Proximité des filières

### 20 % — Compatibilité des disponibilités horaires
