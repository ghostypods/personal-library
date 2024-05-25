from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float


app = Flask(__name__)  # create the app


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)  # create the database with a base class
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"  # Creates the SQL Database(db) with a name (in this case 'new-books-collection')
db.init_app(app)  # Initializes the app along with SQL database extension


# This class labels the table and all the column headings
class Books(db.Model):  # 'Books' is the name of the table in the database
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)


with app.app_context():
    db.create_all()


# Home page
@app.route('/', methods=["GET", "POST"])
def home():
    book_list = db.session.execute(db.select(Books)).scalars()  # list of all books in 'my library'
    return render_template("index.html", books=book_list)


# Adds books to library list
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        book = Books(  # Add another book
            title=request.form["book_title"],
            author=request.form["author"],
            rating=request.form["rating"]
        )
        db.session.add(book)  # Add the book to the library
        db.session.commit()  # update database
    return render_template("add.html")


# Update the rating of a book
@app.route("/update-rating/<int:book_id>", methods=["GET", "POST"])
def update_rating(book_id):
    book = db.get_or_404(Books, book_id)  # Select the book
    if request.method == "POST":
        book.rating = request.form["new-rating"]  # Changes a book's rating
        db.session.commit()

        book_list = db.session.execute(db.select(Books)).scalars()
        return render_template("index.html", books=book_list)

    return render_template("update.html", book=book)


# Delete a book from list
@app.route("/delete/<int:book_id>", methods=["GET", "POST"])
def delete(book_id):
    book = db.get_or_404(Books, book_id)
    db.session.delete(book)  # delete book
    db.session.commit()

    book_list = db.session.execute(db.select(Books)).scalars()
    return render_template("index.html", books=book_list)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)




