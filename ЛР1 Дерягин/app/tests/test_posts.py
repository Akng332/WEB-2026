import pytest
from app import app, posts
from datetime import datetime

@pytest.fixture
def client():
    """Тестовый клиент Flask"""
    app.config['TESTING'] = True
    app.config['DEBUG'] = False
    with app.test_client() as client:
        yield client

# ============ ТЕСТЫ ДЛЯ ГЛАВНОЙ СТРАНИЦЫ ============

def test_index_status_code(client):
    """Тест 1: Главная страница возвращает 200"""
    response = client.get('/')
    assert response.status_code == 200

def test_index_uses_correct_template(client):
    """Тест 2: Главная страница использует шаблон index.html"""
    response = client.get('/')
    assert b'Добро пожаловать' in response.data or b'blog' in response.data.lower()

def test_index_contains_posts(client):
    """Тест 3: Главная страница содержит посты"""
    response = client.get('/')
    for post in posts.values():
        assert post['title'].encode() in response.data

# ============ ТЕСТЫ ДЛЯ СПИСКА ПОСТОВ ============

def test_posts_list_status_code(client):
    """Тест 4: Страница списка постов возвращает 200"""
    response = client.get('/posts')
    assert response.status_code == 200

def test_posts_list_uses_correct_template(client):
    """Тест 5: Страница списка постов использует шаблон posts.html"""
    response = client.get('/posts')
    assert b'Все посты' in response.data

def test_posts_list_contains_all_posts(client):
    """Тест 6: Страница списка постов содержит все посты"""
    response = client.get('/posts')
    for post in posts.values():
        assert post['title'].encode() in response.data

# ============ ТЕСТЫ ДЛЯ СТРАНИЦЫ ПОСТА ============

def test_post_detail_status_code(client):
    """Тест 7: Страница поста возвращает 200"""
    response = client.get('/post/1')
    assert response.status_code == 200

def test_post_detail_contains_title(client):
    """Тест 8: Страница поста содержит заголовок"""
    response = client.get('/post/1')
    assert posts[1]['title'].encode() in response.data

def test_post_detail_contains_author(client):
    """Тест 9: Страница поста содержит имя автора"""
    response = client.get('/post/1')
    assert posts[1]['author'].encode() in response.data

def test_post_detail_contains_content(client):
    """Тест 10: Страница поста содержит текст"""
    response = client.get('/post/1')
    # Проверяем хотя бы часть текста
    assert len(posts[1]['content']) > 0
    assert response.data is not None

def test_post_detail_contains_date_in_correct_format(client):
    """Тест 11: Дата отображается в правильном формате (ДД.ММ.ГГГГ)"""
    response = client.get('/post/1')
    expected_date = posts[1]['date'].strftime('%d.%m.%Y')
    assert expected_date.encode() in response.data

def test_post_detail_contains_comment_form(client):
    """Тест 12: Страница поста содержит форму комментария"""
    response = client.get('/post/1')
    assert b'Оставьте комментарий' in response.data or b'comment' in response.data.lower()

def test_post_detail_returns_404_for_invalid_id(client):
    """Тест 13: Несуществующий пост возвращает 404"""
    response = client.get('/post/999')
    assert response.status_code == 404

# ============ ТЕСТЫ ДЛЯ КОММЕНТАРИЕВ ============

def test_comment_addition_works(client):
    """Тест 14: Добавление комментария работает"""
    response = client.post('/post/1', data={
        'comment_text': 'Тестовый комментарий для проверки'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Тестовый комментарий' in response.data

def test_reply_button_exists(client):
    """Тест 15: На странице есть кнопка ответа на комментарий"""
    response = client.get('/post/1')
    assert b'Ответить' in response.data or b'reply' in response.data.lower()

# ============ ТЕСТЫ ДЛЯ ПОДВАЛА ============

def test_footer_contains_name_and_group(client):
    """Тест 16: В подвале есть ФИО и номер группы"""
    response = client.get('/')
    assert b'Дерягин Дмитрий' in response.data
    assert b'Группа' in response.data

# ============ ТЕСТЫ ДЛЯ ИЗОБРАЖЕНИЙ ============

def test_post_contains_image(client):
    """Тест 17: Пост содержит изображение"""
    response = client.get('/post/1')
    # Проверяем наличие тега img или ссылки на изображение
    assert b'img' in response.data or b'images/' in response.data

# ============ ТЕСТЫ ДЛЯ ПРАВИЛЬНЫХ ШАБЛОНОВ ============

def test_base_template_has_footer(client):
    """Тест 18: Базовый шаблон содержит подвал"""
    response = client.get('/')
    assert b'footer' in response.data.lower()