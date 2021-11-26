from sqlalchemy import (
    Column,
    String,
    UnicodeText
)
from Livegram.mod.sql import SESSION, BASE


class BlackList(BASE):
    """ table to store BANned users """
    __tablename__ = "blacklist"
    chat_id = Column(String(14), primary_key=True)
    reason = Column(UnicodeText)

    def __init__(self, chat_id, reason):
        self.chat_id = str(chat_id)  # ensure string
        self.reason = reason

    def __repr__(self):
        return "<BL %s>" % self.chat_id


BlackList.__table__.create(checkfirst=True)


def add_user_to_bl(chat_id, reason):
    """ add the user to the blacklist """
    __user = BlackList(str(chat_id), reason)
    SESSION.add(__user)
    SESSION.commit()


def check_is_black_list(chat_id):
    """ get the user_id from the message_id """
    try:
        s__ = SESSION.query(BlackList).get(str(chat_id))
        return s__
    finally:
        SESSION.close()


def rem_user_from_bl(chat_id):
    s__ = SESSION.query(BlackList).get(str(chat_id))
    if s__:
        SESSION.delete(s__)
        SESSION.commit()
        return True
    SESSION.close()
    return False
