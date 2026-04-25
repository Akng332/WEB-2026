import pytest
from app import validate_phone

# ========== ТЕСТЫ ДЛЯ ФУНКЦИИ ВАЛИДАЦИИ ==========
def test_validate_phone_valid_11_digits_with_plus7():
    """Корректный номер с +7"""
    result, error = validate_phone('+7 (123) 456-75-90')
    assert result == '8-123-456-75-90'
    assert error is None

def test_validate_phone_valid_11_digits_with_8():
    """Корректный номер с 8"""
    result, error = validate_phone('8(123)4567590')
    assert result == '8-123-456-75-90'
    assert error is None

def test_validate_phone_valid_10_digits():
    """Корректный 10-значный номер"""
    result, error = validate_phone('123.456.75.90')
    assert result == '8-123-456-75-90'
    assert error is None

def test_validate_phone_with_spaces():
    """Номер с пробелами"""
    result, error = validate_phone('+7 123 456 75 90')
    assert result == '8-123-456-75-90'
    assert error is None

def test_validate_phone_with_parentheses():
    """Номер со скобками"""
    result, error = validate_phone('(123)456-75-90')
    assert result == '8-123-456-75-90'
    assert error is None

def test_validate_phone_with_dots():
    """Номер с точками"""
    result, error = validate_phone('123.456.78.90')
    assert result == '8-123-456-78-90'
    assert error is None

def test_validate_phone_invalid_symbols():
    """Недопустимые символы"""
    result, error = validate_phone('123abc456')
    assert result is None
    assert 'недопустимые символы' in error.lower()

def test_validate_phone_wrong_digit_count():
    """Неверное количество цифр"""
    result, error = validate_phone('12345')
    assert result is None
    assert 'неверное количество цифр' in error.lower()

def test_validate_phone_11_digits_wrong_start():
    """11 цифр, но начинается не с 7 или 8"""
    result, error = validate_phone('91234567890')
    assert result is None
    assert 'неверное количество цифр' in error.lower()

# ========== ТЕСТЫ ДЛЯ МАРШРУТОВ ==========
def test_url_params_display(client):
    response = client.get('/url-params?param1=value1&param2=value2')
    assert b'param1' in response.data
    assert b'value1' in response.data
    assert b'param2' in response.data
    assert b'value2' in response.data

def test_url_params_empty(client):
    response = client.get('/url-params')
    # Проверяем по наличию слова "Нет" в HTML (в utf-8)
    assert 'Нет параметров URL'.encode('utf-8') in response.data

def test_headers_display(client):
    response = client.get('/headers')
    assert b'Host' in response.data
    assert b'User-Agent' in response.data

def test_headers_custom_header(client):
    response = client.get('/headers', headers={'X-Custom-Header': 'test-value'})
    assert b'X-Custom-Header' in response.data
    assert b'test-value' in response.data

def test_cookie_set_when_not_exists(client):
    response = client.get('/cookies')
    assert 'user_preference' in response.headers.get('Set-Cookie', '')

def test_cookie_delete_when_exists(client):
    """Тест: если куки есть, оно удаляется"""
    # Устанавливаем cookie через заголовки
    client.set_cookie('user_preference', 'test_value')
    response = client.get('/cookies')
    cookies = response.headers.get('Set-Cookie', '')
    assert 'user_preference' in cookies
    assert 'expires' in cookies.lower()

def test_form_params_display_submitted_data(client):
    response = client.post('/form-params', data={'name': 'Иван Петров', 'email': 'ivan@example.com'})
    assert 'Иван Петров'.encode('utf-8') in response.data
    assert b'ivan@example.com' in response.data

def test_form_params_empty_submit(client):
    response = client.post('/form-params', data={})
    assert 'Отправленные данные'.encode('utf-8') not in response.data

def test_phone_validation_valid_11_digits_with_plus7(client):
    response = client.post('/phone-validation', data={'phone': '+7 (123) 456-75-90'})
    assert b'8-123-456-75-90' in response.data
    assert b'alert-success' in response.data

def test_phone_validation_valid_11_digits_with_8(client):
    response = client.post('/phone-validation', data={'phone': '8(123)4567590'})
    assert b'8-123-456-75-90' in response.data

def test_phone_validation_valid_10_digits(client):
    response = client.post('/phone-validation', data={'phone': '123.456.75.90'})
    assert b'8-123-456-75-90' in response.data

def test_phone_validation_with_spaces(client):
    response = client.post('/phone-validation', data={'phone': '+7 123 456 75 90'})
    assert b'8-123-456-75-90' in response.data

def test_phone_validation_with_parentheses(client):
    response = client.post('/phone-validation', data={'phone': '(123)456-75-90'})
    assert b'8-123-456-75-90' in response.data

def test_phone_validation_invalid_symbols(client):
    response = client.post('/phone-validation', data={'phone': '123abc456'})
    assert 'Недопустимый ввод'.encode('utf-8') in response.data
    assert b'is-invalid' in response.data

def test_phone_validation_wrong_digit_count(client):
    response = client.post('/phone-validation', data={'phone': '12345'})
    assert 'Неверное количество цифр'.encode('utf-8') in response.data

def test_phone_validation_bootstrap_error_classes(client):
    response = client.post('/phone-validation', data={'phone': 'invalid'})
    assert b'is-invalid' in response.data
    assert b'invalid-feedback' in response.data

def test_phone_validation_success_no_error_classes(client):
    response = client.post('/phone-validation', data={'phone': '+7 (123) 456-75-90'})
    assert b'is-invalid' not in response.data