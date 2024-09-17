import requests

from ..core.V1.sessions import get_db
from ..schemas.V1.config_scheme import settings_env
from ..models.V1.bot import Bot_report


def telegram_message(chat_id:str,text:str)-> requests.Response:
    TOKEN = settings_env.TOKEN_TELEGRAM_BOT
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    response = requests.post(url, data={'chat_id': chat_id, "text": text})
    return response

def telegram_message_error(text:str):
    db = next(get_db())
    user_report = db.query(Bot_report).all()
    for user in user_report:
        telegram_message(user.user_id,text)

