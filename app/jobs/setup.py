import base64
import random
import secrets

import bcrypt
from sqlalchemy.exc import IntegrityError

from app.config import CONFIG, INI_FILE, reload_conf
from app.database import Session
from app.resources.user import User


def run_setup():
    session = Session

    generated_app_key = bcrypt.gensalt().decode('utf-8')
    CONFIG.set('app', 'key', generated_app_key)

    with open(INI_FILE, 'w') as config_file:
        CONFIG.write(config_file)

    reload_conf()

    username = "admin{}".format(random.randint(999, 9999))
    generated_password = secrets.token_urlsafe(8)
    token = base64.b64encode("{}:{}".format(username, generated_password).encode('utf-8')).decode('utf-8')

    existing_user = session.query(User).filter(User.username == username).first()
    if existing_user is not None:
        run_setup()

    user = User(
        username=username,
        password=bcrypt.hashpw(generated_password.encode('utf-8'), generated_app_key.encode('utf-8')),
        is_admin=True
    )

    try:
        session.add(user)
        session.commit()

        msg = """
            Created account:
                AppKey: {}
                Username: {}
                Password: {}
                Token: {}
        """.format(generated_app_key, username, generated_password, token)
        print(msg)
    except IntegrityError as ie:
        raise Exception('Database error. Can\'t create admin account.')
