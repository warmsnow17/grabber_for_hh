import time
import schedule
from selenium import webdriver
from selenium.common import NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException, \
    TimeoutException
from selenium.webdriver.common.by import By
from loguru import logger
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import os
from selenium.webdriver.chrome.options import Options

load_dotenv()
letter_text=os.getenv('LETTER_TEXT')
search_request = 'Name:(python or django or drf or backend or telegram-bot or aiogram) and DESCRIPTION:' \
                 '(django or drf or fastapi or telegram-bot or aiogram) NOT ментор NOT senior not Преподаватель ' \
                 'NOT TechLead NOT техлид NOT middlle+ NOT Middle+ NOT ml NOT ML NOT Full-Stack NOT Full-stack NOT FullStack'


def script():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    with webdriver.Chrome(options=chrome_options) as browser:
        logger.info('Старт')
        browser.get('https://hh.ru/account/login?backurl=%2F&hhtmFrom=main')
        button = browser.find_elements(By.CLASS_NAME, 'bloko-link.bloko-link_pseudo')
        button[1].click()
        time.sleep(1)
        field = browser.find_elements(By.CLASS_NAME, 'bloko-input-text')
        field[1].send_keys(os.getenv('LOGIN'))
        time.sleep(1)
        field[2].send_keys(os.getenv('PASSWORD'))
        time.sleep(1)
        button_login = browser.find_elements(By.CLASS_NAME, 'bloko-button.bloko-button_kind-primary')
        button_login[1].click()
        logger.warning('Вошел в hh')
        time.sleep(2)
        advanced_search = browser.find_element(By.CLASS_NAME, 'bloko-button.bloko-button_icon-only').click()
        time.sleep(1)
        input_request = browser.find_elements(By.CLASS_NAME, 'bloko-input-text')
        input_request[1].send_keys(search_request)
        time.sleep(1)
        remote_checkbox = browser.find_element(By.XPATH, '//input[@data-qa="advanced-search__schedule-item_remote"]')
        browser.execute_script("arguments[0].click();", remote_checkbox)
        logger.warning('Написал запрос')
        button_input_request = browser.find_element(By.CLASS_NAME, 'bloko-button.bloko-button_kind-primary.bloko-button_scale-large.bloko-button_stretched').click()
        time.sleep(1)
        vacancies = browser.find_elements(By.CSS_SELECTOR, '.serp-item__title')
        logger.warning('Получил вакансии')
        links = [vacancy.get_attribute('href') for vacancy in vacancies]
        logger.warning('нашел ссылки')
        time.sleep(1)
        count = 1
        for link in links:
            try:
                browser.get(link)

                time.sleep(2)

                respond_button = browser.find_element(By.CSS_SELECTOR, 'a[data-qa="vacancy-response-link-top"]')
                respond_button.click()
                logger.warning(f'Перешел по ссылке {count} {link}')
                time.sleep(.5)
                count += 1

                try:
                    try:
                        time.sleep(1)
                        write_letter_button = browser.find_element(By.CSS_SELECTOR,
                                                                   'button[data-qa="vacancy-response-letter-toggle"]')
                        time.sleep(1)
                        write_letter_button.click()

                        time.sleep(1)

                        letter_text_area = browser.find_element(By.CSS_SELECTOR, 'textarea[name="text"]')
                        letter_text_area.send_keys(letter_text)
                        time.sleep(1)
                        send_button = browser.find_element(By.CSS_SELECTOR,
                                                           'button[data-qa="vacancy-response-letter-submit"]')
                        send_button.click()
                        time.sleep(1)
                    except (NoSuchElementException, TimeoutException, ElementClickInterceptedException,
                            ElementNotInteractableException) as e:
                        logger.warning(f'Ошибка при попытке найти кнопку "Написать сопроводительное": {e.msg}')

                    try:
                        time.sleep(1)
                        letter_text_area = WebDriverWait(browser, 20).until(
                            EC.element_to_be_clickable(
                                (By.CSS_SELECTOR, 'textarea[data-qa="vacancy-response-popup-form-letter-input"]'))
                        )
                        letter_text_area.send_keys(letter_text)
                        time.sleep(1)
                        send_button = WebDriverWait(browser, 20).until(
                            EC.element_to_be_clickable(
                                (By.CSS_SELECTOR, 'button[data-qa="vacancy-response-submit-popup"]'))
                        )
                        send_button.click()
                        time.sleep(1)
                    except (NoSuchElementException, TimeoutException, ElementClickInterceptedException,
                            ElementNotInteractableException) as e:
                        logger.warning(
                            f'Ошибка при попытке найти текстовую область для ввода сопроводительного письма: {e.msg}')
                    logger.warning('отправил сопроводительное письмо')
                    time.sleep(1)


                except (NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException, TimeoutException) as e:
                    logger.warning(
                        f'Не удалось найти кнопку "Написать сопроводительное" на {link} или произошла ошибка при клике, пропускаем. Ошибка: {str(e)}')
            except (NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException, TimeoutException) as e:
                logger.warning(
                    f'Не удалось найти кнопку "Откликнуться" на {link} или произошла ошибка при клике, пропускаем. Ошибка: {str(e)}')
        logger.info('Скрипт остановлен')
schedule.every().day.at("06:05").do(script)
schedule.every().day.at("10:05").do(script)
logger.info('Скрипт запущен и ожидает начала начала выполнения в 06:05 и в 10:05')

while True:
    schedule.run_pending()
    time.sleep(1)
