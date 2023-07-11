from main import app
from database import transfer_money_db,add_user_card_to_db, get_all_cards_or_exact_transactions_db,get_user_cards_by_phone_number_db,delete_user_card_db, get_exact_user_card_db
from datetime import datetime
import random

# Временное создание проверочного кода
otp_test = {}

# Добавление карты
@app.post('/add_user_card')
async def add_user_card_api(user_id:int, card_number:int, card_holder:str, card_name:str, exp_date:int, otp:int):
    # Проверка одноразового кода
    if otp_test.get(user_id) == otp:
        result = add_user_card_to_db(user_id=user_id,
                                      cardholder=card_holder,
                                      card_name=card_name,
                                      card_number=card_number,
                                      exp_date=exp_date,
                                      balance = 0,
                                      added_date = datetime.now())
    else:
        result = "Неверный код"
    return {"status": 1, "message": result}

# Генерация проверочного кода
@app.get('/one_time_password')
async def get_one_time_password_api(transfer_id:int =0, user_id:int = 0):
    otp = random.randint(1000, 9999)
    if transfer_id!=0:
        #Сгенерируем рандом отп
        otp_test[transfer_id]=otp
    elif user_id != 0:
        otp_test[user_id] = otp
    return  {"status": 1, "message": otp}

# Перевод денежных средств
@app.post('/transfer_user_money')
async def transfer_user_money_api(card_from:int, card_to:int, amount:float, otp:int):
    result = transfer_money_db(card_from, card_to, datetime.now(), amount)
    return {"status": 1, "message": result}

#Удаление карты
@app.delete('/delete_user_card')
async def delete_user_card_api(card_id:int, user_id:int):
    result = delete_user_card_db(card_id=card_id,
                                 user_id=user_id)

    return {"status": 1, "message": result}

#Получить карту
@app.get('/get_user_cards')
async def get_exact_or_all_cards_api(user_id:int, card:int=0):
    result = get_exact_user_card_db(user_id, card)

    return {"status": 1, "cards": result}

#Мониторинг карты
@app.get('/get_card_monitoring')
async def get_exact_all_card_monitoring_api(card:int=0):
    result = get_all_cards_or_exact_transactions_db(card)

    return {"status": 1, "card_monitoring": result}