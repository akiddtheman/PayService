from database.models import Card, Service, Transaction
from database import get_db

# Сделать перевод с карты на карту
def transfer_money_db(card_from, card_to, date, amount):
    db = next(get_db())
    checker_card_from = get_exact_card_balance_db(card_from)
    checker_card_to = get_exact_card_balance_db(card_to)
    if (checker_card_to and checker_card_from) and (checker_card_from.balance >=amount):
        transaction = Transaction(card_to=card_to, card_id=checker_card_from.card_id, amount=amount)
        checker_card_from.balance -= amount
        checker_card_to.balance += amount
        db.add(transaction)
        db.commit()
        return "Перевод успешно выполнен"
    elif not checker_card_to or not checker_card_from:
        return "Ошибка в данных"
    return "Недостаточно средств"
def pay_for_service_db(business_id:int, from_card:int, amount:float):
    db = next(get_db())
    checker = get_exact_card_balance_db(from_card)
    if checker and checker.balance>=amount:
        transaction = Transaction(card_to=business_id, card_id=from_card, amount=amount)
        checker.balance -= amount
        db.add(transaction)
        db.commit()
        return "Услуга успешно оплачена"
    elif not checker:
        return "Ошибка в данных"
    return "Недостаточно средств"

def get_exact_card_balance_db(card_number):
    db = next(get_db())
    exact_card = db.query(Card).filter_by(card_number=card_number).first()
    return exact_card