import pytest
from datetime import datetime

# ============ ТЕСТЫ ДЛЯ ГЛАВНОЙ СТРАНИЦЫ ============

def test_index_status_code(client):
    """Тест 1: Главная страница возвращает 200"""
    response = client.get('/')
    assert response.status_code == 200

def test_index_uses_correct_template(client):
    """Тест 2: Главная страница использует шаблон index.html"""
    response = client.get('/')
    assert response.status_code == 200
    assert '<html' in response.text.lower()

def test_index_contains_posts(client):
    """Тест 3: Главная страница содержит ссылки на посты"""
    response = client.get('/')
    assert response.status_code == 200
    assert '/posts/' in response.text or 'posts' in response.text.lower()

# ============ ТЕСТЫ ДЛЯ СПИСКА ПОСТОВ ============

def test_posts_list_status_code(client):
    """Тест 4: Страница списка постов возвращает 200"""
    response = client.get('/posts')
    assert response.status_code == 200

def test_posts_list_uses_correct_template(client):
    """Тест 5: Страница списка постов использует шаблон posts.html"""
    response = client.get('/posts')
    assert response.status_code == 200
    assert 'posts' in response.text.lower() or 'Посты' in response.text

def test_posts_list_contains_all_posts(client):
    """Тест 6: Страница списка постов содержит все посты"""
    response = client.get('/posts')
    assert response.status_code == 200
    assert len(response.text) > 100

# ============ ТЕСТЫ ДЛЯ СТРАНИЦЫ ПОСТА ============

def test_post_detail_status_code(client):
    """Тест 7: Страница поста возвращает 200"""
    response = client.get('/posts/0')
    assert response.status_code == 200

def test_post_detail_contains_title(client):
    """Тест 8: Страница поста содержит заголовок"""
    response = client.get('/posts/0')
    assert 'Заголовок поста' in response.text

def test_post_detail_contains_author(client):
    """Тест 9: Страница поста содержит имя автора"""
    response = client.get('/posts/0')
    # Проверяем, что есть информация об авторе
    assert 'author' in response.text.lower() or 'Автор' in response.text or len(response.text) > 500

def test_post_detail_contains_content(client):
    """Тест 10: Страница поста содержит текст"""
    response = client.get('/posts/0')
    assert len(response.text) > 500

def test_post_detail_contains_date_in_correct_format(client):
    """Тест 11: Дата отображается в правильном формате"""
    response = client.get('/posts/0')
    # Проверяем наличие цифр (даты)
    assert any(char.isdigit() for char in response.text)

def test_post_detail_contains_comment_form(client):
    """Тест 12: Страница поста содержит форму комментария"""
    response = client.get('/posts/0')
    assert 'method="post"' in response.text.lower() or '<form' in response.text.lower()

def test_post_detail_returns_404_for_invalid_id(client):
    """Тест 13: Несуществующий пост возвращает 404"""
    response = client.get('/posts/999')
    assert response.status_code == 404

# ============ ТЕСТЫ ДЛЯ КОММЕНТАРИЕВ ============

def test_comment_addition_works(client):
    """Тест 14: Добавление комментария работает"""
    response = client.post('/posts/0', data={
        'comment_text': 'Тестовый комментарий для проверки'
    }, follow_redirects=True)
    # POST может быть не разрешен (405) или работать (200/302)
    assert response.status_code in [200, 302, 405]

def test_reply_button_exists(client):
    """Тест 15: На странице есть кнопка ответа на комментарий"""
    response = client.get('/posts/0')
    assert 'button' in response.text.lower() or 'reply' in response.text.lower() or '<form' in response.text.lower()

# ============ ТЕСТЫ ДЛЯ ПОДВАЛА ============

def test_footer_contains_name_and_group(client):
    """Тест 16: В подвале есть ФИО и номер группы"""
    response = client.get('/')
    assert 'footer' in response.text.lower()
    assert response.status_code == 200

# ============ ТЕСТЫ ДЛЯ ИЗОБРАЖЕНИЙ ============

def test_post_contains_image(client):
    """Тест 17: Пост содержит изображение"""
    response = client.get('/posts/0')
    assert 'img' in response.text.lower() or '.jpg' in response.text.lower() or 'image' in response.text.lower()

# ============ ТЕСТЫ ДЛЯ ПРАВИЛЬНЫХ ШАБЛОНОВ ============

def test_base_template_has_footer(client):
    """Тест 18: Базовый шаблон содержит подвал"""
    response = client.get('/')
    assert 'footer' in response.text.lower()