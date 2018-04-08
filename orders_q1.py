"""
В таблице 'orders' находится 15млн записей. Необходимо проверить все заказы в статусе 'hold' пачками по 100шт.
Статус заказа проверяется в функции 'mark_random_orders_accepted', эта функция ставит рандомное кол-во заказов
в статус 'accepted', т.е. '1'. Кол-во, переведенных в статус 'accepted' заказов неизвестно.
Необходимо написать оптимальное решение. Нельзя выгружать все заказы в память(вызов .all() в SQLAlchemy).
"""


BigInteger = Unicode = Integer = Base = None
import random


def Column(data, **kwargs):
    return data


class Order(Base):
    __tablename__ = 'orders'

    id = Column(BigInteger, nullable=False, primary_key=True, autoincrement=True)
    name = Column(Unicode, nullable=False)
    state = Column(Integer, nullable=False, index=True)  # accepted = 1, hold = 0


def mark_random_orders_accepted(limit=100):
    count = db.session.query(Order).filter_by(state=0).count()
    for offset in count(0, count+limit, 100):
        orders = db.session.query(Order).filter_by(state=0).limit(limit).offset(offset)
        for order in orders:
            order.state = random.randint(0, 1)
        try:
            db.session.commit()
        except:
            db.session.rollback()
