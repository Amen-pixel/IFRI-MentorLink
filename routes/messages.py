"""
routes/messages.py — Messagerie instantanée (Flask-SocketIO)
"""
import os
from flask import Blueprint, render_template, redirect, url_for, request, jsonify, current_app
from flask_login import login_required, current_user
from flask_socketio import emit, join_room
from werkzeug.utils import secure_filename
from models import db, User, Conversation, Message
from extensions import socketio

messages_bp = Blueprint("messages", __name__)


# ── Helpers ──────────────────────────────────────────────────

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
    """Liste toutes les conversations de l'utilisateur."""
    convs = Conversation.query.filter(
        (Conversation.user1_id == current_user.id) |
        (Conversation.user2_id == current_user.id)
    ).all()

    conversations = []
    for conv in convs:
        interlocuteur = conv.user2 if conv.user1_id == current_user.id else conv.user1
        dernier_msg   = conv.messages.order_by(Message.date_envoi.desc()).first()
        nb_non_lus    = conv.messages.filter_by(
            lu=False
        ).filter(Message.expediteur_id != current_user.id).count()
        conversations.append({
            "conv": conv,
            "interlocuteur": interlocuteur,
            "dernier_msg": dernier_msg,
            "non_lus": nb_non_lus,
        })

    conversations.sort(
        key=lambda c: c["dernier_msg"].date_envoi if c["dernier_msg"] else c["conv"].date_creation,
        reverse=True
    )
    return render_template("messages.html", conversations=conversations)


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

@socketio.on("rejoindre")
def on_rejoindre(data):
    """Le client rejoint la room de sa conversation."""
    room_name = room_id(data["conv_id"])
    join_room(room_name)
    print(f"🟢 [DEBUG SOCKET] L'utilisateur a rejoint la room : {room_name}")


@socketio.on("envoyer_message")
def on_message(data):
    """
    Reçoit un message du client, le persiste, et le diffuse
    à tous les participants de la conversation.
    """
    print(f"🔵 [DEBUG SOCKET] Message reçu du frontend : {data}")
    
    try:
        conv_id_int = int(data["conv_id"])
        conv = db.session.get(Conversation, conv_id_int)
        
        if conv is None:
            print("🔴 [DEBUG SOCKET] Erreur : Conversation introuvable en BDD.")
            return

        if current_user.id not in (conv.user1_id, conv.user2_id):
            print(f"🔴 [DEBUG SOCKET] Erreur : L'utilisateur {current_user.id} n'a pas le droit d'écrire ici.")
            return

        contenu = data.get("contenu", "").strip()
        fichier_url = data.get("fichier_url")

        if not contenu and not fichier_url:
            print("🔴 [DEBUG SOCKET] Annulation : Aucun texte ni fichier.")
            return

        msg = Message(
            conversation_id=conv.id,
            expediteur_id=current_user.id,
            contenu=contenu,
            fichier_url=fichier_url
        )
        db.session.add(msg)
        db.session.commit()
        print("🟢 [DEBUG SOCKET] Message sauvegardé avec succès dans la base de données !")

        emit("nouveau_message", {
            "id":            msg.id,
            "contenu":       msg.contenu,
            "fichier_url":    msg.fichier_url,
            "expediteur_id": msg.expediteur_id,
            "prenom":        current_user.prenom,
            "nom":           current_user.nom,
            "date_envoi":    msg.date_envoi.strftime("%H:%M"),
        }, room=room_id(conv.id))
        
        print(f"🟢 [DEBUG SOCKET] Message renvoyé en temps réel dans la room {room_id(conv.id)}")

    except Exception as e:
        print(f"🔴 [DEBUG SOCKET] ERREUR FATALE : {str(e)}")
