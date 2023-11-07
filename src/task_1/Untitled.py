import psutil
import requests
import time

# Порог потребления памяти в процентах
threshold = 90

# URL для отправки HTTP-запроса в случае превышения порога
api_url = "https://jsonplaceholder.typicode.com/posts"

# Путь к файлу для записи результатов
result_file = "alarm_results.txt"

def send_memory_alarm():
    # Получаем информацию о потреблении памяти
    memory_usage = psutil.virtual_memory().percent

    # Проверяем, превышен ли порог
    if memory_usage > threshold:
        # Генерируем данные аларма
        alarm_data = {
            "message": "Потребление памяти превысило порог!",
            "memory_usage": memory_usage
        }

        # Отправляем POST-запрос с данными аларма
        response = requests.post(api_url, json=alarm_data)

        if response.status_code == 200:
            result = "Запрос успешно отправлен."
        else:
            result = f"Ошибка при отправке запроса. Код ответа: {response.status_code}"
    else:
        result = "Потребление памяти в норме."

    # Записываем результат в файл
    with open(result_file, "a") as file:
        file.write(result + "\n")

while True:
    send_memory_alarm()

    # Пауза, чтобы не нагружать систему слишком частыми проверками
    time.sleep(60)  # Проверка каждую минуту