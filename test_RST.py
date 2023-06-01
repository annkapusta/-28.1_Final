
from time import sleep
from base_data import *
from settings import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


### тест RST_01 - общий вид (с сохранением скриншота)
def test_01_vision(selenium):
    form = AuthForm(selenium)
    form.driver.save_screenshot('screenshot_01.jpg')


### тест RST_02 - проверка, что по-умолчанию выбрана форма авторизации по телефону
def test_02_by_phone(selenium):
    form = AuthForm(selenium)

    assert form.placeholder.text == 'Мобильный телефон'


### тест RST_03 - проверка смены "таб ввода"
def test_03_change_placeholder(selenium):
    form = AuthForm(selenium)

    # ввод телефона
    form.username.send_keys('+79139159171')
    form.password.send_keys('_')
    sleep(7)

    assert form.placeholder.text == 'Мобильный телефон'

    # очистка поля логина
    form.username.send_keys(Keys.CONTROL, 'a')
    form.username.send_keys(Keys.DELETE)

    # ввод почты
    form.username.send_keys('ann.kapusta@mail.ru')
    form.password.send_keys('_')
    sleep(7)

    assert form.placeholder.text == 'Электронная почта'

    # очистка поля логина
    form.username.send_keys(Keys.CONTROL, 'a')
    form.username.send_keys(Keys.DELETE)

    # ввод логина
    form.username.send_keys('MyLogin')
    form.password.send_keys('_')
    sleep(7)

    assert form.placeholder.text == 'Логин'


### тест RST_04 - проверка позитивного сценария авторизации по телефону
def test_04_positive_by_phone(selenium):
    form = AuthForm(selenium)

    # ввод телефона
    form.username.send_keys(valid_phone)
    form.password.send_keys(valid_pass)
    sleep(7)
    form.btn_click()

    assert form.get_current_url() != '/account_b2c/page'


### тест RST_05 - проверка негативного сценария авторизации по телефону
def test_05_negative_by_phone(selenium):
    form = AuthForm(selenium)

    # ввод телефона
    form.username.send_keys('+79139159173')
    form.password.send_keys('any_password')
    sleep(7)
    form.btn_click()

    err_mess = form.driver.find_element(By.ID, 'form-error-message')
    assert err_mess.text == 'Неверный логин или пароль'


### тест RST_06 - проверка позитивного сценария авторизации по почте
def test_06_positive_by_email(selenium):
    form = AuthForm(selenium)

    # ввод почты
    form.username.send_keys(valid_email)
    form.password.send_keys(valid_pass)
    sleep(7)
    form.btn_click()

    assert form.get_current_url() != '/account_b2c/page'


### тест RST_07 - проверка негативного сценария авторизации по почте
def test_07_negative_by_email(selenium):
    form = AuthForm(selenium)

    # ввод почты
    form.username.send_keys('fghj@google.ru')
    form.password.send_keys('any_password')
    sleep(7)
    form.btn_click()

    err_mess = form.driver.find_element(By.ID, 'form-error-message')
    assert err_mess.text == 'Неверный логин или пароль'


### тест RST_08 - проверка получения кода на телефон и открытия формы для ввода кода
def test_08_get_code(selenium):
    form = CodeForm(selenium)

    # ввод телефона
    form.address.send_keys(valid_phone)

    # длительная пауза предназначена для ручного ввода captcha при необходимости
    sleep(30)
    form.get_click()

    rt_code = form.driver.find_element(By.ID, 'rt-code-0')

    assert rt_code


### тест RST_09 - проверка перехода в форму восстановления пароля и её открытия
def test_09_forgot_pass(selenium):
    form = AuthForm(selenium)

    # клик по надписи "Забыл пароль"
    form.forgot.click()
    sleep(7)

    reset_pass = form.driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div/h1')

    assert reset_pass.text == 'Восстановление пароля'


### тест RST_10 - проверка перехода в форму регистрации и её открытия
def test_10_register(selenium):
    form = AuthForm(selenium)

    # клик по надписи "Зарегистрироваться"
    form.register.click()
    sleep(7)

    reset_pass = form.driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div/h1')

    assert reset_pass.text == 'Регистрация'

### тест RST_11 - проверка открытия пользовательского соглашения
def test_11_agreement(selenium):
    form = AuthForm(selenium)

    original_window = form.driver.current_window_handle
    # клик по надписи "Пользовательским соглашением" в подвале страницы
    form.agree.click()
    sleep(7)
    WebDriverWait(form.driver, 7).until(EC.number_of_windows_to_be(2))
    for window_handle in form.driver.window_handles:
        if window_handle != original_window:
            form.driver.switch_to.window(window_handle)
            break
    win_title = form.driver.execute_script("return window.document.title")

    assert win_title == 'User agreement'

### тест RST_12 - проверка перехода по ссылке авторизации пользователя через вконтакте
def test_12_auth_vk(selenium):
    form = AuthForm(selenium)
    form.vk_btn.click()
    sleep(7)

    assert form.get_base_url() == 'oauth.vk.com'


### тест RST_13 - проверка перехода по ссылке авторизации пользователя через одноклассники
def test_13_auth_ok(selenium):
    form = AuthForm(selenium)
    form.ok_btn.click()
    sleep(7)

    assert form.get_base_url() == 'connect.ok.ru'


### тест RST_14 - проверка перехода по ссылке авторизации пользователя через майлру
def test_14_auth_mailru(selenium):
    form = AuthForm(selenium)
    form.mailru_btn.click()
    sleep(7)

    assert form.get_base_url() == 'connect.mail.ru'


### тест RST_15 - проверка перехода по ссылке авторизации пользователя через яндекс
def test_15_auth_ya(selenium):
    form = AuthForm(selenium)
    form.ya_btn.click()
    sleep(7)

    assert form.get_base_url() == 'passport.yandex.ru'