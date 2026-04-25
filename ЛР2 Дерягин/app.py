import random
from functools import lru_cache
from flask import Flask, render_template, abort, request, make_response
from faker import Faker
import re

fake = Faker()

# Указываем, что шаблоны и статика лежат в папке app
app = Flask(__name__,
            template_folder='app/templates',
            static_folder='app/static')
application = app

images_ids = ['7d4e9175-95ea-4c5f-8be5-92a6b708bb3c',
              '2d2ab7df-cdbc-48a8-a936-35bba702def5',
              '6e12f3de-d5fd-4ebb-855b-8cbc485278b7',
              'afc2cfe7-5cac-4b80-9b9a-d5c65ef0c728',
              'cab5b7f2-774e-4884-a200-0c0180fa777f']


def generate_comments(replies=True):
    comments = []
    for _ in range(random.randint(1, 3)):
        comment = {'author': fake.name(), 'text': fake.text()}
        if replies:
            comment['replies'] = generate_comments(replies=False)
        comments.append(comment)
    return comments


def generate_post(i):
    return {
        'id': i,  # ДОБАВЛЕНИЕ у поста id
        'title': 'Заголовок поста',
        'text': fake.paragraph(nb_sentences=100),
        'author': fake.name(),
        'date': fake.date_time_between(start_date='-2y', end_date='now'),
        'image_id': f'{images_ids[i]}.jpg',
        'comments': generate_comments()
    }


@lru_cache
def posts_list():
    return sorted([generate_post(i) for i in range(5)], key=lambda p: p['date'], reverse=True)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/posts')
def posts():
    return render_template('posts.html', title='Посты', posts=posts_list())


@app.route('/posts/<int:index>')
def post(index):
    posts = posts_list()
    if index < 0 or index >= len(posts):
        abort(404)
    p = posts[index]
    return render_template('post.html', title=p['title'], post=p)


# Алиас для совместимости с post_id
@app.route('/posts/<int:post_id>')
def post_detail(post_id):
    posts = posts_list()
    if post_id < 0 or post_id >= len(posts):
        abort(404)
    p = posts[post_id]
    return render_template('post.html', title=p['title'], post=p)


@app.route('/about')
def about():
    return render_template('about.html', title='Об авторе')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', title='Страница не найдена'), 404

@app.route('/url-params')
def url_params():
    params = request.args.to_dict()
    return render_template('url_params.html', params=params)


@app.route('/headers')
def headers():
    headers_dict = dict(request.headers)
    return render_template('headers.html', headers=headers_dict)


@app.route('/cookies')
def cookies():
    cookie_name = 'user_preference'
    response = make_response(render_template('cookies.html'))

    if cookie_name in request.cookies:
        response.delete_cookie(cookie_name)
    else:
        response.set_cookie(cookie_name, 'test_value', max_age=3600)

    return response


@app.route('/form-params', methods=['GET', 'POST'])
def form_params():
    submitted_data = None
    if request.method == 'POST':
        submitted_data = request.form.to_dict()
    return render_template('form_params.html', submitted_data=submitted_data)


def validate_phone(phone):
    # Удаляем все разрешенные символы, оставляем только цифры
    allowed_chars = re.sub(r'[+\d\s\(\)\-\.]', '', phone)
    if allowed_chars:
        return None, 'Недопустимый ввод. В номере телефона встречаются недопустимые символы.'

    # Извлекаем только цифры
    digits = re.sub(r'\D', '', phone)

    # Проверка количества цифр
    if len(digits) == 11:
        if digits[0] not in ['7', '8']:
            return None, 'Недопустимый ввод. Неверное количество цифр.'
    elif len(digits) == 10:
        pass  # 10 цифр - допустимо
    else:
        return None, 'Недопустимый ввод. Неверное количество цифр.'

    # Форматирование номера
    if len(digits) == 11 and digits[0] == '8':
        formatted = f"8-{digits[1:4]}-{digits[4:7]}-{digits[7:9]}-{digits[9:11]}"
    elif len(digits) == 11 and digits[0] == '7':
        formatted = f"8-{digits[1:4]}-{digits[4:7]}-{digits[7:9]}-{digits[9:11]}"
    else:  # 10 цифр
        formatted = f"8-{digits[0:3]}-{digits[3:6]}-{digits[6:8]}-{digits[8:10]}"

    return formatted, None


@app.route('/phone-validation', methods=['GET', 'POST'])
def phone_validation():
    error = None
    formatted_phone = None
    phone_input = ''

    if request.method == 'POST':
        phone_input = request.form.get('phone', '')
        formatted_phone, error = validate_phone(phone_input)

    return render_template('phone_validation.html',
                           error=error,
                           formatted_phone=formatted_phone,
                           phone_input=phone_input)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)