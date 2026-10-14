from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory data
books = [
    {"id": 1, "title": "Clean Code", "author": "Robert C. Martin", "available": True},
    {"id": 2, "title": "The Pragmatic Programmer", "author": "Andrew Hunt", "available": True},
    {"id": 3, "title": "Introduction to Algorithms", "author": "CLRS", "available": True}
]

members = [
    {"id": 1, "name": "Alice", "email": "alice@example.com"},
    {"id": 2, "name": "Bob", "email": "bob@example.com"}
]

issued_books = []


@app.route("/")
def home():
    return jsonify({
        "message": "Library Management Server",
        "status": "running"
    })


# Get all books
@app.route("/books", methods=["GET"])
def get_books():
    return jsonify(books)


# Get a specific book
@app.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = next((b for b in books if b["id"] == book_id), None)

    if not book:
        return jsonify({"error": "Book not found"}), 404

    return jsonify(book)


# Add a new book
@app.route("/books", methods=["POST"])
def add_book():
    data = request.get_json()

    if not data or "title" not in data or "author" not in data:
        return jsonify({
            "error": "title and author are required"
        }), 400

    new_book = {
        "id": len(books) + 1,
        "title": data["title"],
        "author": data["author"],
        "available": True
    }

    books.append(new_book)

    return jsonify(new_book), 201


# Get all members
@app.route("/members", methods=["GET"])
def get_members():
    return jsonify(members)


# Add a member
@app.route("/members", methods=["POST"])
def add_member():
    data = request.get_json()

    if not data or "name" not in data or "email" not in data:
        return jsonify({
            "error": "name and email are required"
        }), 400

    member = {
        "id": len(members) + 1,
        "name": data["name"],
        "email": data["email"]
    }

    members.append(member)

    return jsonify(member), 201


# Issue a book
@app.route("/issue", methods=["POST"])
def issue_book():
    data = request.get_json()

    book_id = data.get("book_id")
    member_id = data.get("member_id")

    book = next((b for b in books if b["id"] == book_id), None)
    member = next((m for m in members if m["id"] == member_id), None)

    if not book:
        return jsonify({"error": "Book not found"}), 404

    if not member:
        return jsonify({"error": "Member not found"}), 404

    if not book["available"]:
        return jsonify({"error": "Book is already issued"}), 400

    book["available"] = False

    record = {
        "book_id": book_id,
        "member_id": member_id
    }

    issued_books.append(record)

    return jsonify({
        "message": "Book issued successfully",
        "record": record
    })


# Return a book
@app.route("/return", methods=["POST"])
def return_book():
    data = request.get_json()
    book_id = data.get("book_id")

    record = next(
        (r for r in issued_books if r["book_id"] == book_id),
        None
    )

    if not record:
        return jsonify({
            "error": "Book is not currently issued"
        }), 404

    book = next((b for b in books if b["id"] == book_id), None)

    if book:
        book["available"] = True

    issued_books.remove(record)

    return jsonify({
        "message": "Book returned successfully"
    })


# Get currently issued books
@app.route("/issued", methods=["GET"])
def get_issued_books():
    return jsonify(issued_books)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
