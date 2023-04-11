import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from config import email_final, pass_final
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(autouse=True)
def testing():
   pytest.driver = webdriver.Chrome()
   # Переходим на страницу авторизации
   pytest.driver.get('https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth?client_id=account_b2c&redirect_uri=https://b2c.passport.rt.ru/account_b2c/login&response_type=code&scope=openid&state=724774ac-a190-4e20-b9ce-905773bf55ba&theme&auth_type')
   WebDriverWait(pytest.driver, 10).until(
       EC.presence_of_element_located((By.ID, 't-btn-tab-phone')))
   # pytest.driver.implicitly_wait(5)
   yield
   pytest.driver.quit()

class TestAuthorization:
    def test_number(self):
        assert pytest.driver.find_element(By.ID, 't-btn-tab-phone').text == 'Номер'

    def test_mail(self):
        assert pytest.driver.find_element(By.ID, 't-btn-tab-mail').text == 'Почта'

    def test_login(self):
        assert pytest.driver.find_element(By.ID, 't-btn-tab-login').text == 'Логин'

    def test_ls(self):
        assert pytest.driver.find_element(By.ID, 't-btn-tab-ls').text == 'Лицевой счёт'

    def test_enter(self):
        pytest.driver.find_element(By.ID, 'username').send_keys(email_final)
        pytest.driver.find_element(By.ID, 'password').send_keys(pass_final)
        pytest.driver.find_element(By.ID, 'kc-login').click()
        WebDriverWait(pytest.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'rt-btn')))
        assert pytest.driver.find_element(By.ID, 'rt-btn').text == 'Сайт Ростелекома'

    def test_enter_error(self):
        pytest.driver.find_element(By.ID, 'username').send_keys(1231231231)
        pytest.driver.find_element(By.ID, 'password').send_keys(123)
        pytest.driver.find_element(By.ID, 'kc-login').click()
        WebDriverWait(pytest.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'form-error-message')))
        assert pytest.driver.find_element(By.ID, 'form-error-message').text == 'Неверный логин или пароль'

class TestRecovery:
    def test_number(self):
        pytest.driver.find_element(By.ID, 'forgot_password').click()
        assert pytest.driver.find_element(By.ID, 't-btn-tab-phone').text == 'Номер'

    def test_mail(self):
        pytest.driver.find_element(By.ID, 'forgot_password').click()
        assert pytest.driver.find_element(By.ID, 't-btn-tab-mail').text == 'Почта'

    def test_login(self):
        pytest.driver.find_element(By.ID, 'forgot_password').click()
        assert pytest.driver.find_element(By.ID, 't-btn-tab-login').text == 'Логин'

    def test_ls(self):
        pytest.driver.find_element(By.ID, 'forgot_password').click()
        assert pytest.driver.find_element(By.ID, 't-btn-tab-ls').text == 'Лицевой счёт'

    def test_enter_error(self):
        pytest.driver.find_element(By.ID, 'forgot_password').click()
        pytest.driver.find_element(By.ID, 'reset-back').click()
        assert pytest.driver.find_element(By.ID, 'kc-login').text == 'Войти'

class TestRegistration:
    def test_firstname_bound(self):
        pytest.driver.find_element(By.ID, 'kc-register').click()
        pytest.driver.find_element(By.XPATH, '//input[@name = "lastName"]').send_keys('Петров')
        pytest.driver.find_element(By.ID, 'address').send_keys('test@mail.ru')
        pytest.driver.find_element(By.ID, 'password').send_keys('TestPassword123')
        pytest.driver.find_element(By.ID, 'password-confirm').send_keys('TestPassword123')
        pytest.driver.find_element(By.XPATH, '//button[@name = "register"]').click()
        assert pytest.driver.find_element(By.XPATH, "//*[contains(@class, 'rt-input-container__meta') and (contains(@class, 'rt-input-container__meta--error'))]").text == 'Необходимо заполнить поле кириллицей. От 2 до 30 символов.'

    def test_lastname_bound(self):
        pytest.driver.find_element(By.ID, 'kc-register').click()
        pytest.driver.find_element(By.XPATH, '//input[@name = "firstName"]').send_keys('Петр')
        pytest.driver.find_element(By.ID, 'address').send_keys('test@mail.ru')
        pytest.driver.find_element(By.ID, 'password').send_keys('TestPassword123')
        pytest.driver.find_element(By.ID, 'password-confirm').send_keys('TestPassword123')
        pytest.driver.find_element(By.XPATH, '//button[@name = "register"]').click()
        assert pytest.driver.find_element(By.XPATH, "//*[contains(@class, 'rt-input-container__meta') and (contains(@class, 'rt-input-container__meta--error'))]").text == 'Необходимо заполнить поле кириллицей. От 2 до 30 символов.'

    def test_mail_bound(self):
        pytest.driver.find_element(By.ID, 'kc-register').click()
        pytest.driver.find_element(By.XPATH, '//input[@name = "firstName"]').send_keys('Петр')
        pytest.driver.find_element(By.XPATH, '//input[@name = "lastName"]').send_keys('Петров')
        pytest.driver.find_element(By.ID, 'password').send_keys('TestPassword123')
        pytest.driver.find_element(By.ID, 'password-confirm').send_keys('TestPassword123')
        pytest.driver.find_element(By.XPATH, '//button[@name = "register"]').click()
        pytest.driver.implicitly_wait(10)
        assert pytest.driver.find_element(By.XPATH, "//*[contains(@class, 'rt-input-container__meta') and (contains(@class, 'rt-input-container__meta--error'))]").text == 'Введите телефон в формате +7ХХХХХХХХХХ или +375XXXXXXXXX, или email в формате example@email.ru'

    def test_password_bound(self):
        pytest.driver.find_element(By.ID, 'kc-register').click()
        pytest.driver.find_element(By.XPATH, '//input[@name = "firstName"]').send_keys('Петр')
        pytest.driver.find_element(By.XPATH, '//input[@name = "lastName"]').send_keys('Петров')
        pytest.driver.find_element(By.ID, 'address').send_keys('test@mail.ru')
        pytest.driver.find_element(By.ID, 'password-confirm').send_keys('TestPassword123')
        pytest.driver.find_element(By.XPATH, '//button[@name = "register"]').click()
        pytest.driver.implicitly_wait(10)
        assert pytest.driver.find_element(By.XPATH, "//*[contains(@class, 'rt-input-container__meta') and (contains(@class, 'rt-input-container__meta--error'))]").text == 'Длина пароля должна быть не менее 8 символов'

    def test_password_bound(self):
        pytest.driver.find_element(By.ID, 'kc-register').click()
        pytest.driver.find_element(By.XPATH, '//input[@name = "firstName"]').send_keys('Петр')
        pytest.driver.find_element(By.XPATH, '//input[@name = "lastName"]').send_keys('Петров')
        pytest.driver.find_element(By.ID, 'address').send_keys('test@mail.ru')
        pytest.driver.find_element(By.ID, 'password').send_keys('TestPassword123')
        pytest.driver.find_element(By.XPATH, '//button[@name = "register"]').click()
        pytest.driver.implicitly_wait(10)
        assert pytest.driver.find_element(By.XPATH, "//*[contains(@class, 'rt-input-container__meta') and (contains(@class, 'rt-input-container__meta--error'))]").text == 'Длина пароля должна быть не менее 8 символов'

    def test_agreement_bound(self):
        pytest.driver.find_element(By.ID, 'kc-register').click()
        assert pytest.driver.find_element(By.XPATH, '//div[@class="auth-policy"]//span').text == 'Нажимая кнопку «Зарегистрироваться», вы принимаете условия'

    def test_firstname_min(self):
        pytest.driver.find_element(By.ID, 'kc-register').click()
        pytest.driver.find_element(By.XPATH, '//input[@name = "firstName"]').send_keys('П')
        pytest.driver.find_element(By.XPATH, '//input[@name = "lastName"]').send_keys('Петров')
        pytest.driver.find_element(By.ID, 'address').send_keys('test@mail.ru')
        pytest.driver.find_element(By.ID, 'password').send_keys('TestPassword123')
        pytest.driver.find_element(By.ID, 'password-confirm').send_keys('TestPassword123')
        pytest.driver.find_element(By.XPATH, '//button[@name = "register"]').click()
        assert pytest.driver.find_element(By.XPATH, "//*[contains(@class, 'rt-input-container__meta') and (contains(@class, 'rt-input-container__meta--error'))]").text == 'Необходимо заполнить поле кириллицей. От 2 до 30 символов.'

    def test_lastname_min(self):
        pytest.driver.find_element(By.ID, 'kc-register').click()
        pytest.driver.find_element(By.XPATH, '//input[@name = "firstName"]').send_keys('Петр')
        pytest.driver.find_element(By.XPATH, '//input[@name = "lastName"]').send_keys('-')
        pytest.driver.find_element(By.ID, 'address').send_keys('test@mail.ru')
        pytest.driver.find_element(By.ID, 'password').send_keys('TestPassword123')
        pytest.driver.find_element(By.ID, 'password-confirm').send_keys('TestPassword123')
        pytest.driver.find_element(By.XPATH, '//button[@name = "register"]').click()
        assert pytest.driver.find_element(By.XPATH, "//*[contains(@class, 'rt-input-container__meta') and (contains(@class, 'rt-input-container__meta--error'))]").text == 'Необходимо заполнить поле кириллицей. От 2 до 30 символов.'

    def test_password_min(self):
        pytest.driver.find_element(By.ID, 'kc-register').click()
        pytest.driver.find_element(By.XPATH, '//input[@name = "firstName"]').send_keys('Петр')
        pytest.driver.find_element(By.XPATH, '//input[@name = "lastName"]').send_keys('Петров')
        pytest.driver.find_element(By.ID, 'address').send_keys('test@mail.ru')
        pytest.driver.find_element(By.ID, 'password').send_keys('TestPas')
        pytest.driver.find_element(By.ID, 'password-confirm').send_keys('TestPas')
        pytest.driver.find_element(By.XPATH, '//button[@name = "register"]').click()
        assert pytest.driver.find_element(By.XPATH, "//*[contains(@class, 'rt-input-container__meta') and (contains(@class, 'rt-input-container__meta--error'))]").text == 'Длина пароля должна быть не менее 8 символов'
