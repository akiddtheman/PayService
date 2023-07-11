from database.models import Card, User, Transaction
from database import get_db

#Добавить карту в БД
def add_user_card_to_db(**kwargs):
    db = next(get_db())
    card_number = kwargs.get('card_number')
    #Проверка была ли добавлена карта
    checker = db.query(Card).filter_by(card_number=card_number).first()
    if checker:
        return "Карта уже существует"
    new_card = Card(**kwargs)
    db.add(new_card)
    db.commit()

    return "Карта успешно добавлена"


#Удалить карту из сервиса
def delete_user_card_db(card_id, user_id):
    db = next(get_db())
    card_delete = db.query(Card).filter_by(user_id=user_id, card_id=card_id).first()
    if card_delete:
        db.delete(card_delete)
        db.commit()
        return "Карта удалена"
    return "Вы ввели неверные данные"

#Получить все карты по номеру телефона
def get_user_cards_by_phone_number_db(phone_number):
    db = next(get_db())
    checker = db.query(Card).filter(User.phone_number==phone_number).all()
    return checker

#Получить определенную карту
def get_exact_user_card_db(user_id, card_id):
    db = next(get_db())
    if card_id == 0:
        card_data = db.query(Card).filter_by(user_id=user_id).all()
    else:
        card_data = db.query(Card).filter_by(user_id=user_id, card_id=card_id).first()
    return card_data

#Получить все транзакции по определенной карте или по всем картам
def get_all_cards_or_exact_transactions_db(card_id):
    db = next(get_db())
    if card_id == 0:
        card_monitor = db.query(Transaction).all()
    else:
        card_monitor = db.query(Transaction).filter_by(card_id=card_id).all()
    return card_monitor
