# grabber_for_hh

Для запуска создайте файл .env с вашим логином и паролем от hh.ru в переменных.

LOGIN=...
PASSWORD=...
Введите сообщение для сопроводительного письма:
LETTER_TEXT=...

Введите команду: docker build -t hh-grabber .
Введите команду: docker run -d hh-grabber

Если не нужно видеть как выполняются действия в окне браузера -> следите за сообщениями по прогрессу выполнения скрипта в терминале.

Если нужно наблюдать за работой алгоритма в окне браузера, уберите доп. настройки так, чтобы код принял следующий вид:

...
def script():
    with webdriver.Chrome() as browser:
        logger.info('Старт')
        browser.get('https://hh.ru/account/login?backurl=%2F&hhtmFrom=main'
        ...

