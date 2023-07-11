from database.models import User, Password
from database import get_db

# Регистрация пользователя
def register_user_db(phone_number:int, name:str, password:str, pincode:int):
    # Проверка номера
    db = next(get_db())
    #Проверка номера
    checker = db.query(User).filter_by(phone_number=phone_number).first()
    if checker:
        return "Пользователь с таким номером уже есть в БД"
    #Если нет пользователя в БД
    new_user = User(phone_number=phone_number, name=name)
    db.add(new_user)
    db.commit()
    new_user_password = Password(user_id = new_user.user_id, password=password, pincode=pincode)
    db.add(new_user_password)
    db.commit()

    return "Пользователь успешно создан"

# Проверка пароля
def check_password_db(phone_number, password):
    db = next(get_db())
    cheker1 = db.query(User).filter_by(phone_number=phone_number).first()
    try:
        cheker2 = db.query(Password).filter_by(user_id = cheker1.user_id).first()
    except:
        cheker2 = False
    if cheker1 and cheker2.password == password:
        return cheker2.user_id
    if cheker1 != phone_number:
        return "Ошибка в номере"
    if cheker2.password != password:
        return "Неверный пароль"

# Получение информации пользователя
def get_user_cabinet_db(user_id):
    db = next(get_db())
    cheker = db.query(User).filter_by(user_id=user_id).first()
    if cheker:
        return cheker
    return "Ошибка в данных"

