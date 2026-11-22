"""
storage.py — Stockage des photos sur Cloudinary (les fichiers de Render sont effacés à chaque redémarrage)
"""
import cloudinary
import cloudinary.uploader
from flask import url_for


def envoyer_image(fichier, nom):
    """Envoie l'image sur Cloudinary et renvoie son adresse https."""
    resultat = cloudinary.uploader.upload(
        fichier, public_id=nom, folder="mentorlink", overwrite=True
    )
    return resultat["secure_url"]


def photo_url(photo):
    """Adresse d'une photo : lien Cloudinary, ou ancien fichier local."""
    if not photo:
        return ""
    if photo.startswith("http"):
        return photo
    return url_for("static", filename="uploads/" + photo)
