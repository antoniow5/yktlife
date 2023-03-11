import datetime


def responce_dicts(code, exception = " "):
    if code == 404:
        responce = {
                        "message": "Запрашиваемый ресурс не найден",
                        "datetime": datetime.datetime.now().strftime("%Y.%m.%d %H:%M:%S"),
                        "server_exception": exception
                        }
    elif code == 400:
        responce = {
                        "message": "Ошибка в пользовательском запросе",
                        "datetime": datetime.datetime.now().strftime("%Y.%m.%d %H:%M:%S"),
                        "server_errors": exception
                        }
    elif code == 401:
        responce = {
                        "message": "Вы должны быть авторизованы",
                        "datetime": datetime.datetime.now().strftime("%Y.%m.%d %H:%M:%S"),
                        
                        }
    elif code == 403:
        responce = {
                        "message": "У вас нет доступа",
                        "datetime": datetime.datetime.now().strftime("%Y.%m.%d %H:%M:%S"),
                        
                        }
    return responce