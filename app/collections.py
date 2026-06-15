from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Collection, Book

collections_bp = Blueprint('collections', __name__)


@collections_bp.route('/my-collections')
@login_required
def my_collections():
    if current_user.role.name != 'user':
        flash('Подборки доступны только пользователям', 'warning')
        return redirect(url_for('books.index'))

    collections = Collection.query.filter_by(user_id=current_user.id).all()
    for collection in collections:
        collection.books_count = len(collection.books)

    return render_template('collections/my_collections.html', collections=collections)


@collections_bp.route('/create', methods=['POST'])
@login_required
def create_collection():
    if current_user.role.name != 'user':
        return jsonify({'error': 'Нет прав'}), 403

    data = request.get_json()
    name = data.get('name', '').strip()

    if not name:
        return jsonify({'error': 'Название не может быть пустым'}), 400

    existing = Collection.query.filter_by(user_id=current_user.id, name=name).first()
    if existing:
        return jsonify({'error': 'Подборка с таким названием уже существует'}), 400

    collection = Collection(name=name, user_id=current_user.id)
    db.session.add(collection)
    db.session.commit()

    return jsonify({'success': True, 'collection_id': collection.id})


@collections_bp.route('/<int:collection_id>')
@login_required
def view_collection(collection_id):
    collection = Collection.query.get_or_404(collection_id)

    if collection.user_id != current_user.id and current_user.role.name != 'admin':
        flash('У вас нет доступа к этой подборке', 'danger')
        return redirect(url_for('collections.my_collections'))

    return render_template('collections/detail.html', collection=collection)


@collections_bp.route('/<int:collection_id>/add-book/<int:book_id>', methods=['POST'])
@login_required
def add_book(collection_id, book_id):
    collection = Collection.query.get_or_404(collection_id)

    if collection.user_id != current_user.id:
        return jsonify({'error': 'Нет прав'}), 403

    book = Book.query.get_or_404(book_id)

    if book in collection.books:
        return jsonify({'error': 'Книга уже в подборке'}), 400

    collection.books.append(book)
    db.session.commit()
    return jsonify({'success': True})


@collections_bp.route('/<int:collection_id>/remove-book/<int:book_id>', methods=['POST'])
@login_required
def remove_book(collection_id, book_id):
    collection = Collection.query.get_or_404(collection_id)

    if collection.user_id != current_user.id:
        flash('Нет прав', 'danger')
        return redirect(url_for('collections.my_collections'))

    book = Book.query.get_or_404(book_id)

    if book in collection.books:
        collection.books.remove(book)
        db.session.commit()
        flash('Книга удалена из подборки', 'success')

    return redirect(url_for('collections.view_collection', collection_id=collection_id))


@collections_bp.route('/delete/<int:collection_id>', methods=['POST'])
@login_required
def delete_collection(collection_id):
    collection = Collection.query.get_or_404(collection_id)

    if collection.user_id != current_user.id and current_user.role.name != 'admin':
        flash('Нет прав', 'danger')
        return redirect(url_for('collections.my_collections'))

    db.session.delete(collection)
    db.session.commit()
    flash('Подборка удалена', 'success')
    return redirect(url_for('collections.my_collections'))


@collections_bp.route('/api/my-collections')
@login_required
def api_my_collections():
    collections = Collection.query.filter_by(user_id=current_user.id).all()
    return jsonify([{'id': c.id, 'name': c.name} for c in collections])