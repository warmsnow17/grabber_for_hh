# Установка базового образа Python
FROM python:3.9-slim-buster

# Установка зависимостей
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Установка рабочей директории
WORKDIR /app

# Копирование зависимостей проекта
COPY requirements.txt .

# Установка зависимостей Python
RUN pip3 install --no-cache-dir -r requirements.txt

# Копирование исходного кода проекта
COPY . .


# Запуск скрипта
CMD [ "python3", "bot.py" ]
