from flask import Blueprint, render_template

ai_bp = Blueprint('ai', __name__)

@ai_bp.route('/ai/chat')
def ai_chat():
    return render_template('ai_chat.html')
