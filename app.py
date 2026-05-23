from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250))
    author = db.Column(db.String(200))
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)


@app.route('/create_book', methods=['GET', 'POST'])
def book_create():
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')

        book = Book(title=title, author=author)

        db.session.add(book)
        db.session.commit()

        return redirect('/create_book')

    return render_template('create_book.html')


@app.route('/books')
def books():
    books = Book.query.all()

    return render_template('books.html', books=books)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)
