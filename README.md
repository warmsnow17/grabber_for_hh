# grabber_for_hh

Скрипт для авто рассылки резюме на hh.ru

Для запуска скрипта создайте файл .env с вашим логином, паролем от hh.ru и текстом сопроводительного письма.

LOGIN=...

PASSWORD=...

LETTER_TEXT=...(текст сопроводительного письма)

В файле bot.py в строке schedule.every().day.at("10:35").do(script) -> установите время начала выполнения скрипта.

Введите команду: 

docker build -t hh-grabber .

Введите команду: 

docker run -d hh-grabber

Если не нужно видеть как выполняются действия в окне браузера -> следите за сообщениями по прогрессу выполнения скрипта в терминале.

Если нужно наблюдать за работой алгоритма в окне браузера, уберите доп. настройки так, чтобы код принял следующий вид:


    ...
    def script():
        with webdriver.Chrome() as browser:
    
            logger.info('Старт')
        
            browser.get('https://hh.ru/account/login?backurl=%2F&hhtmFrom=main')
    ...

В переменную search_request внесите свой запрос по желаемой вакансии на hh.ru. По умолчанию запрос составлен на вакансию python backend developer
