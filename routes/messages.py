"""
routes/messages.py — Messagerie instantanée (Flask-SocketIO)
"""
import os
from datetime import timedelta
from flask import Blueprint, render_template, redirect, url_for, request, jsonify, current_app, make_response
from flask_login import login_required, current_user
from flask_socketio import emit, join_room
from werkzeug.utils import secure_filename
from models import db, User, Conversation, Message, heure_benin
from extensions import socketio

messages_bp = Blueprint("messages", __name__)


# ── Helpers ──────────────────────────────────────────────────

def formater_date_badge(dt):
    """Retourne 'Aujourd\'hui', 'Hier' ou la date 'JJ/MM/AAAA'."""
    if not dt:
        return ""
    aujourdhui = heure_benin().date()
    date_msg = dt.date()
    if date_msg == aujourdhui:
        return "Aujourd'hui"
    elif date_msg == aujourdhui - timedelta(days=1):
        return "Hier"
    else:
        return date_msg.strftime("%d/%m/%Y")


def get_or_create_conversation(user1_id: int, user2_id: int) -> Conversation:
    """Retourne la conversation existante ou en crée une nouvelle."""
    conv = Conversation.query.filter(
        ((Conversation.user1_id == user1_id) & (Conversation.user2_id == user2_id)) |
        ((Conversation.user1_id == user2_id) & (Conversation.user2_id == user1_id))
    ).first()

    if not conv:
        conv = Conversation(user1_id=user1_id, user2_id=user2_id)
        db.session.add(conv)
        db.session.commit()
    return conv


def room_id(conv_id: int) -> str:
    return f"conv_{conv_id}"


# ── Routes HTTP ───────────────────────────────────────────────

@messages_bp.route("/messages")
@login_required
def liste():
    """Liste toutes les conversations triées par le plus récent message (style WhatsApp)."""
    convs = Conversation.query.filter(
        (Conversation.user1_id == current_user.id) |
        (Conversation.user2_id == current_user.id)
    ).all()

    conversations = []
    for conv in convs:
        interlocuteur = conv.user2 if conv.user1_id == current_user.id else conv.user1
        
        # Récupération directe du VRAI dernier message par son ID le plus récent
        dernier_msg = Message.query.filter_by(conversation_id=conv.id).order_by(Message.id.desc()).first()
        
        nb_non_lus = conv.messages.filter_by(
            lu=False
        ).filter(Message.expediteur_id != current_user.id).count()

        conversations.append({
            "conv": conv,
            "interlocuteur": interlocuteur,
            "dernier_msg": dernier_msg,
            "non_lus": nb_non_lus,
        })

    # Tri strict par l'ID du dernier message (le dernier message envoyé a l'ID le plus élevé)
    conversations.sort(
        key=lambda c: c["dernier_msg"].id if c["dernier_msg"] else 0,
        reverse=True
    )

    response = make_response(render_template("messages.html", conversations=conversations))
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


@messages_bp.route('/conversation', methods=['GET', 'POST'])
@messages_bp.route('/conversation/<int:user_id>', methods=['GET', 'POST'])
@login_required
def ouvrir_conversation(user_id=None):
    """Ouvre ou crée une conversation avec un autre utilisateur."""
    if user_id is None:
        user_id = request.args.get('user_id', type=int)

    if not user_id:
        return redirect(url_for('messages.liste'))

    interlocuteur = db.get_or_404(User, user_id)
    conv = get_or_create_conversation(current_user.id, interlocuteur.id)

    Message.query.filter_by(conversation_id=conv.id, lu=False, expediteur_id=interlocuteur.id).update({"lu": True})
    db.session.commit()

    historique = conv.messages.order_by(Message.date_envoi.asc()).all()

    return render_template(
        "conversation.html",
        interlocuteur=interlocuteur,
        conv=conv,
        historique=historique,
        formater_date_badge=formater_date_badge
    )


@messages_bp.route('/upload_fichier', methods=['POST'])
@login_required
def upload_fichier():
    """Réceptionne et enregistre les fichiers joints."""
    if 'fichier' not in request.files:
        return jsonify({'error': 'Aucun fichier fourni'}), 400
    
    file = request.files['fichier']
    if file.filename == '':
        return jsonify({'error': 'Nom de fichier vide'}), 400

    filename = secure_filename(file.filename)
    upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
    os.makedirs(upload_folder, exist_ok=True)
    
    file_path = os.path.join(upload_folder, filename)
    file.save(file_path)

    file_url = url_for('static', filename='uploads/' + filename)
    return jsonify({'url': file_url})


# ── Événements SocketIO ───────────────────────────────────────

@socketio.on("connect")
def on_connect():
    """Associe automatiquement le socket connecté au canal personnel de l'utilisateur."""
    if current_user.is_authenticated:
        user_room = f"user_{current_user.id}"
        join_room(user_room)


@socketio.on("rejoindre")
def on_rejoindre(data):
    """Le client rejoint la room d'une conversation spécifique."""
    room_name = room_id(data["conv_id"])
    join_room(room_name)


@socketio.on("envoyer_message")
def on_message(data):
    """Reçoit un message du client, le persiste, et le diffuse aux participants."""
    try:
        conv_id_int = int(data["conv_id"])
        conv = db.session.get(Conversation, conv_id_int)
        
        if conv is None or current_user.id not in (conv.user1_id, conv.user2_id):
            return

        contenu = data.get("contenu", "").strip()
        fichier_url = data.get("fichier_url")

        if not contenu and not fichier_url:
            return

        maintenant = heure_benin()

        msg = Message(
            conversation_id=conv.id,
            expediteur_id=current_user.id,
            contenu=contenu,
            fichier_url=fichier_url,
            date_envoi=maintenant
        )
        db.session.add(msg)
        db.session.commit()

        # Diffusion du message dans le chat
        emit("nouveau_message", {
            "id":            msg.id,
            "contenu":       msg.contenu,
            "fichier_url":   msg.fichier_url,
            "expediteur_id": msg.expediteur_id,
            "prenom":        current_user.prenom,
            "nom":           current_user.nom,
            "date_envoi":    msg.date_envoi.strftime("%H:%M"),
        }, room=room_id(conv.id))

        # Mise à jour en temps réel des listes de conversations
        aperçu_msg = contenu if contenu else "📄 Fichier joint"
        payload_liste = {
            "conv_id":       conv.id,
            "dernier_msg":   aperçu_msg,
            "date_envoi":    msg.date_envoi.strftime("%H:%M"),
            "expediteur_id": msg.expediteur_id
        }

        emit("update_conv_list", payload_liste, room=f"user_{conv.user1_id}")
        emit("update_conv_list", payload_liste, room=f"user_{conv.user2_id}")

    except Exception as e:
        print(f"🔴 [DEBUG SOCKET] ERREUR : {str(e)}")
