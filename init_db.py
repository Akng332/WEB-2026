from app import create_app, db
from app.models import Role, User, Genre
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    # Создаём роли
    roles = [
        Role(name='admin', description='Полный доступ к системе'),
        Role(name='moderator', description='Может редактировать книги'),
        Role(name='user', description='Может оставлять рецензии и создавать подборки')
    ]

    for role in roles:
        if not Role.query.filter_by(name=role.name).first():
            db.session.add(role)

    db.session.commit()

    # Создаём админа
    if not User.query.filter_by(login='admin').first():
        admin = User(
            login='admin',
            last_name='Администратор',
            first_name='Системный',
            role_id=Role.query.filter_by(name='admin').first().id
        )
        admin.set_password('admin123')
        db.session.add(admin)

    # Создаём жанры
    genres = [
        'Фантастика', 'Детектив', 'Роман', 'Поэзия',
        'Научная литература', 'Приключения', 'Триллер', 'Исторический роман'
    ]

    for genre_name in genres:
        if not Genre.query.filter_by(name=genre_name).first():
            db.session.add(Genre(name=genre_name))

    db.session.commit()

    print("✅ База данных инициализирована")
    print("📝 Админ: login='admin', password='admin123'")