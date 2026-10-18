from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DATABASE = "library.db"


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    with get_db() as db:
        db.executescript("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                isbn TEXT UNIQUE,
                quantity INTEGER NOT NULL DEFAULT 1
                    CHECK(quantity >= 0)
            );

            CREATE TABLE IF NOT EXISTS members (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL
            );

            CREATE TABLE IF NOT EXISTS issues (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER NOT NULL,
                member_id INTEGER NOT NULL,
                issue_date TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                return_date TEXT,
                FOREIGN KEY(book_id) REFERENCES books(id),
                FOREIGN KEY(member_id) REFERENCES members(id)
            );
        """)


def row_to_dict(row):
    return dict(row) if row else None


@app.get("/")
def home():
    return jsonify({
        "message": "Library Management API",
        "endpoints": [
            "GET /books",
            "POST /books",
            "POST /members",
            "POST /issue",
            "POST /return/<issue_id>",
            "GET /issues"
        ]
    })


@app.get("/books")
def get_books():
    with get_db() as db:
        books = db.execute(
            "SELECT * FROM books ORDER BY title"
        ).fetchall()
    return jsonify([dict(book) for book in books])


@app.post("/books")
def add_book():
    data = request.get_json(silent=True) or {}

    title = data.get("title")
    author = data.get("author")
    isbn = data.get("isbn")
    quantity = data.get("quantity", 1)

    if not isinstance(title, str) or not title.strip():
        return jsonify({"error": "Title is required"}), 400

    if not isinstance(author, str) or not author.strip():
        return jsonify({"error": "Author is required"}), 400

    if type(quantity) is not int or quantity < 0:
        return jsonify({"error": "Quantity must be a non-negative integer"}), 400

    try:
        with get_db() as db:
            cursor = db.execute(
                """INSERT INTO books (title, author, isbn, quantity)
                   VALUES (?, ?, ?, ?)""",
                (title.strip(), author.strip(), isbn, quantity)
            )
            book_id = cursor.lastrowid

        return jsonify({
            "message": "Book added successfully",
            "book_id": book_id
        }), 201

    except sqlite3.IntegrityError:
        return jsonify({"error": "ISBN already exists"}), 409


@app.post("/members")
def add_member():
    data = request.get_json(silent=True) or {}
    name = data.get("name")
    email = data.get("email")

    if not isinstance(name, str) or not name.strip():
        return jsonify({"error": "Name is required"}), 400

    if not isinstance(email, str) or not email.strip():
        return jsonify({"error": "Email is required"}), 400

    try:
        with get_db() as db:
            cursor = db.execute(
                "INSERT INTO members (name, email) VALUES (?, ?)",
                (name.strip(), email.strip())
            )

        return jsonify({
            "message": "Member registered successfully",
            "member_id": cursor.lastrowid
        }), 201

    except sqlite3.IntegrityError:
        return jsonify({"error": "Email already registered"}), 409


@app.post("/issue")
def issue_book():
    data = request.get_json(silent=True) or {}
    book_id = data.get("book_id")
    member_id = data.get("member_id")

    if type(book_id) is not int or type(member_id) is not int:
        return jsonify({"error": "Valid book_id and member_id are required"}), 400

    with get_db() as db:
        book = db.execute(
            "SELECT * FROM books WHERE id = ?", (book_id,)
        ).fetchone()

        member = db.execute(
            "SELECT * FROM members WHERE id = ?", (member_id,)
        ).fetchone()

        if not book:
            return jsonify({"error": "Book not found"}), 404

        if not member:
            return jsonify({"error": "Member not found"}), 404

        if book["quantity"] < 1:
            return jsonify({"error": "Book is unavailable"}), 409

        db.execute(
            "UPDATE books SET quantity = quantity - 1 WHERE id = ?",
            (book_id,)
        )

        cursor = db.execute(
            "INSERT INTO issues (book_id, member_id) VALUES (?, ?)",
            (book_id, member_id)
        )

        issue_id = cursor.lastrowid

    return jsonify({
        "message": "Book issued successfully",
        "issue_id": issue_id
    }), 201


@app.post("/return/<int:issue_id>")
def return_book(issue_id):
    with get_db() as db:
        issue = db.execute(
            "SELECT * FROM issues WHERE id = ?", (issue_id,)
        ).fetchone()

        if not issue:
            return jsonify({"error": "Issue record not found"}), 404

        if issue["return_date"] is not None:
            return jsonify({"error": "Book already returned"}), 409

        db.execute(
            """UPDATE issues
               SET return_date = CURRENT_TIMESTAMP
               WHERE id = ?""",
            (issue_id,)
        )

        db.execute(
            "UPDATE books SET quantity = quantity + 1 WHERE id = ?",
            (issue["book_id"],)
        )

    return jsonify({"message": "Book returned successfully"})


@app.get("/issues")
def get_issues():
    with get_db() as db:
        issues = db.execute("""
            SELECT
                i.id AS issue_id,
                b.title AS book_title,
                m.name AS member_name,
                i.issue_date,
                i.return_date
            FROM issues i
            JOIN books b ON b.id = i.book_id
            JOIN members m ON m.id = i.member_id
            ORDER BY i.id DESC
        """).fetchall()

    return jsonify([dict(issue) for issue in issues])


if __name__ == "__main__":
    init_db()
    app.run(host="127.0.0.1", port=5000, debug=True)
