from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float

app = Flask(__name__)

# Create Database
class Base(DeclarativeBase):
    pass

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///books.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Avoids warnings
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# Book Model
class Book(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)

# Create Table in Database
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    all_books = db.session.execute(db.select(Book).order_by(Book.title)).scalars().all()
    return render_template("index.html", books=all_books)

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        new_book = Book(
            title=request.form["title"],
            author=request.form["author"],
            rating=float(request.form["rating"])  # Convert rating to float
        )
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("add.html")

@app.route("/edit", methods=["GET", "POST"])
def edit():
    book_id = request.args.get('id', type=int)  # Ensure book_id is an integer
    book_selected = db.session.get(Book, book_id)

    if not book_selected:
        return "Book Not Found", 404

    if request.method == "POST":
        new_rating = request.form.get("rating")
        if new_rating:
            book_selected.rating = float(new_rating)
            db.session.commit()
        return redirect(url_for('home'))

    return render_template("edit_rating.html", book=book_selected)

@app.route("/delete")
def delete():
    book_id = request.args.get('id', type=int)  # Ensure book_id is an integer
    book_to_delete = db.session.get(Book, book_id)

    if book_to_delete:
        db.session.delete(book_to_delete)
        db.session.commit()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
