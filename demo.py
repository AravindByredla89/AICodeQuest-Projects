# from flask import Flask, request, jsonify

# app = Flask(__name__)

# # In-memory data
# books = [
#     {"id": 1, "title": "Clean Code", "author": "Robert C. Martin", "available": True},
#     {"id": 2, "title": "The Pragmatic Programmer", "author": "Andrew Hunt", "available": True},
#     {"id": 3, "title": "Introduction to Algorithms", "author": "CLRS", "available": True}
# ]

# members = [
#     {"id": 1, "name": "Alice", "email": "alice@example.com"},
#     {"id": 2, "name": "Bob", "email": "bob@example.com"}
# ]

# issued_books = []


# @app.route("/")
# def home():
#     return jsonify({
#         "message": "Library Management Server",
#         "status": "running"
#     })


# # Get all books
# @app.route("/books", methods=["GET"])
# def get_books():
#     return jsonify(books)


# # Get a specific book
# @app.route("/books/<int:book_id>", methods=["GET"])
# def get_book(book_id):
#     book = next((b for b in books if b["id"] == book_id), None)

#     if not book:
#         return jsonify({"error": "Book not found"}), 404

#     return jsonify(book)


# # Add a new book
# @app.route("/books", methods=["POST"])
# def add_book():
#     data = request.get_json()

#     if not data or "title" not in data or "author" not in data:
#         return jsonify({
#             "error": "title and author are required"
#         }), 400

#     new_book = {
#         "id": len(books) + 1,
#         "title": data["title"],
#         "author": data["author"],
#         "available": True
#     }

#     books.append(new_book)

#     return jsonify(new_book), 201


# # Get all members
# @app.route("/members", methods=["GET"])
# def get_members():
#     return jsonify(members)


# # Add a member
# @app.route("/members", methods=["POST"])
# def add_member():
#     data = request.get_json()

#     if not data or "name" not in data or "email" not in data:
#         return jsonify({
#             "error": "name and email are required"
#         }), 400

#     member = {
#         "id": len(members) + 1,
#         "name": data["name"],
#         "email": data["email"]
#     }

#     members.append(member)

#     return jsonify(member), 201


# # Issue a book
# @app.route("/issue", methods=["POST"])
# def issue_book():
#     data = request.get_json()

#     book_id = data.get("book_id")
#     member_id = data.get("member_id")

#     book = next((b for b in books if b["id"] == book_id), None)
#     member = next((m for m in members if m["id"] == member_id), None)

#     if not book:
#         return jsonify({"error": "Book not found"}), 404

#     if not member:
#         return jsonify({"error": "Member not found"}), 404

#     if not book["available"]:
#         return jsonify({"error": "Book is already issued"}), 400

#     book["available"] = False

#     record = {
#         "book_id": book_id,
#         "member_id": member_id
#     }

#     issued_books.append(record)

#     return jsonify({
#         "message": "Book issued successfully",
#         "record": record
#     })


# # Return a book
# @app.route("/return", methods=["POST"])
# def return_book():
#     data = request.get_json()
#     book_id = data.get("book_id")

#     record = next(
#         (r for r in issued_books if r["book_id"] == book_id),
#         None
#     )

#     if not record:
#         return jsonify({
#             "error": "Book is not currently issued"
#         }), 404

#     book = next((b for b in books if b["id"] == book_id), None)

#     if book:
#         book["available"] = True

#     issued_books.remove(record)

#     return jsonify({
#         "message": "Book returned successfully"
#     })


# # Get currently issued books
# @app.route("/issued", methods=["GET"])
# def get_issued_books():
#     return jsonify(issued_books)


# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000, debug=True)

from flask import Flask, request, jsonify
from datetime import datetime
from functools import wraps
import re

app = Flask(__name__)

app.config["JSON_SORT_KEYS"] = False


# --------------------------------------------------
# Application configuration
# --------------------------------------------------

APP_NAME = "Library Management API"
APP_VERSION = "2.0.0"
DEFAULT_PORT = 5000

books = [
    {
        "id": 1,
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "available": True,
        "category": "Programming"
    },
    {
        "id": 2,
        "title": "The Pragmatic Programmer",
        "author": "Andrew Hunt",
        "available": True,
        "category": "Programming"
    },
    {
        "id": 3,
        "title": "Introduction to Algorithms",
        "author": "CLRS",
        "available": True,
        "category": "Computer Science"
    }
]

members = [
    {
        "id": 1,
        "name": "Alice",
        "email": "alice@example.com",
        "active": True
    },
    {
        "id": 2,
        "name": "Bob",
        "email": "bob@example.com",
        "active": True
    }
]

issued_books = []

activity_log = []


# --------------------------------------------------
# General helper functions
# --------------------------------------------------

def create_response(message, status=200, **extra):
    """Build a consistent JSON response."""
    payload = {
        "message": message,
        "timestamp": datetime.now().isoformat(timespec="seconds")
    }

    payload.update(extra)

    return jsonify(payload), status


def create_error(message, status=400):
    """Return an error response."""
    return jsonify({
        "success": False,
        "error": message,
        "timestamp": datetime.now().isoformat(timespec="seconds")
    }), status


def log_activity(action, details=None):
    """Store a basic activity record."""
    activity_log.append({
        "action": action,
        "details": details or {},
        "timestamp": datetime.now().isoformat(timespec="seconds")
    })


def get_json_data():
    """Read a JSON request body safely."""
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return None

    return data


def find_book(book_id):
    """Find a book by its identifier."""
    return next(
        (book for book in books if book["id"] == book_id),
        None
    )


def find_member(member_id):
    """Find a member by their identifier."""
    return next(
        (member for member in members if member["id"] == member_id),
        None
    )


def find_issued_record(book_id):
    """Find an issue record for a particular book."""
    return next(
        (
            record for record in issued_books
            if record["book_id"] == book_id
        ),
        None
    )


def next_book_id():
    """Generate a unique book identifier."""
    return max((book["id"] for book in books), default=0) + 1


def next_member_id():
    """Generate a unique member identifier."""
    return max((member["id"] for member in members), default=0) + 1


def validate_text(value):
    """Check that a value is a non-empty string."""
    return isinstance(value, str) and bool(value.strip())


def normalize_text(value):
    """Remove surrounding whitespace."""
    return value.strip() if isinstance(value, str) else value


def validate_email(email):
    """Perform basic email format validation."""
    if not isinstance(email, str):
        return False

    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return bool(re.match(pattern, email))


def book_summary(book):
    """Return a compact representation of a book."""
    return {
        "id": book["id"],
        "title": book["title"],
        "author": book["author"],
        "available": book["available"],
        "category": book.get("category", "General")
    }


# --------------------------------------------------
# Request hooks
# --------------------------------------------------

@app.before_request
def before_request():
    """Record incoming API requests."""
    app.logger.info(
        "Request received: %s %s",
        request.method,
        request.path
    )


@app.after_request
def after_request(response):
    """Add a basic API response header."""
    response.headers["X-API-Version"] = APP_VERSION
    return response


# --------------------------------------------------
# Home and status endpoints
# --------------------------------------------------

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "application": APP_NAME,
        "version": APP_VERSION,
        "status": "running",
        "available_endpoints": [
            "/",
            "/health",
            "/books",
            "/members",
            "/issued",
            "/statistics"
        ]
    })


@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "healthy",
        "application": APP_NAME
    })


@app.route("/about", methods=["GET"])
def about():
    return jsonify({
        "name": APP_NAME,
        "version": APP_VERSION,
        "description": "A simple library management service",
        "framework": "Flask"
    })


# --------------------------------------------------
# Book retrieval endpoints
# --------------------------------------------------

@app.route("/books", methods=["GET"])
def get_books():
    return jsonify(books)


@app.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = find_book(book_id)

    if book is None:
        return create_error("Book not found", 404)

    return jsonify(book)


@app.route("/books/available", methods=["GET"])
def get_available_books():
    available = [
        book for book in books
        if book["available"]
    ]

    return jsonify({
        "count": len(available),
        "books": available
    })


@app.route("/books/search", methods=["GET"])
def search_books():
    keyword = request.args.get("q", "").strip().lower()

    if not keyword:
        return create_error("Provide a search term using ?q=", 400)

    results = [
        book for book in books
        if keyword in book["title"].lower()
        or keyword in book["author"].lower()
        or keyword in book.get("category", "").lower()
    ]

    return jsonify({
        "query": keyword,
        "count": len(results),
        "results": results
    })


@app.route("/books/category/<string:category>", methods=["GET"])
def get_books_by_category(category):
    normalized_category = category.strip().lower()

    results = [
        book for book in books
        if book.get("category", "General").lower()
        == normalized_category
    ]

    return jsonify({
        "category": category,
        "count": len(results),
        "books": results
    })


# --------------------------------------------------
# Book creation and modification
# --------------------------------------------------

@app.route("/books", methods=["POST"])
def add_book():
    data = get_json_data()

    if data is None:
        return create_error("A valid JSON object is required")

    title = normalize_text(data.get("title"))
    author = normalize_text(data.get("author"))
    category = normalize_text(data.get("category", "General"))

    if not validate_text(title):
        return create_error("A valid title is required")

    if not validate_text(author):
        return create_error("A valid author is required")

    if not validate_text(category):
        return create_error("A valid category is required")

    new_book = {
        "id": next_book_id(),
        "title": title,
        "author": author,
        "available": True,
        "category": category
    }

    books.append(new_book)

    log_activity("book_added", {
        "book_id": new_book["id"]
    })

    return jsonify(new_book), 201


@app.route("/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    book = find_book(book_id)

    if book is None:
        return create_error("Book not found", 404)

    data = get_json_data()

    if data is None:
        return create_error("A valid JSON object is required")

    if "title" in data:
        title = normalize_text(data["title"])

        if not validate_text(title):
            return create_error("Title cannot be empty")

        book["title"] = title

    if "author" in data:
        author = normalize_text(data["author"])

        if not validate_text(author):
            return create_error("Author cannot be empty")

        book["author"] = author

    if "category" in data:
        category = normalize_text(data["category"])

        if not validate_text(category):
            return create_error("Category cannot be empty")

        book["category"] = category

    log_activity("book_updated", {"book_id": book_id})

    return jsonify({
        "message": "Book updated successfully",
        "book": book
    })


@app.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    book = find_book(book_id)

    if book is None:
        return create_error("Book not found", 404)

    if find_issued_record(book_id):
        return create_error(
            "Return the book before deleting it",
            409
        )

    books.remove(book)

    log_activity("book_deleted", {"book_id": book_id})

    return jsonify({
        "message": "Book deleted successfully",
        "deleted_book_id": book_id
    })


# --------------------------------------------------
# Member retrieval endpoints
# --------------------------------------------------

@app.route("/members", methods=["GET"])
def get_members():
    return jsonify(members)


@app.route("/members/<int:member_id>", methods=["GET"])
def get_member(member_id):
    member = find_member(member_id)

    if member is None:
        return create_error("Member not found", 404)

    return jsonify(member)


@app.route("/members/<int:member_id>/issued", methods=["GET"])
def get_member_issued_books(member_id):
    member = find_member(member_id)

    if member is None:
        return create_error("Member not found", 404)

    records = [
        record for record in issued_books
        if record["member_id"] == member_id
    ]

    details = []

    for record in records:
        book = find_book(record["book_id"])

        if book is not None:
            details.append({
                "issue_record": record,
                "book": book
            })

    return jsonify({
        "member": member,
        "count": len(details),
        "issued_books": details
    })


# --------------------------------------------------
# Member creation and modification
# --------------------------------------------------

@app.route("/members", methods=["POST"])
def add_member():
    data = get_json_data()

    if data is None:
        return create_error("A valid JSON object is required")

    name = normalize_text(data.get("name"))
    email = normalize_text(data.get("email"))

    if not validate_text(name):
        return create_error("A valid name is required")

    if not validate_email(email):
        return create_error("A valid email address is required")

    if any(
        member["email"].lower() == email.lower()
        for member in members
    ):
        return create_error("Email is already registered", 409)

    member = {
        "id": next_member_id(),
        "name": name,
        "email": email,
        "active": True
    }

    members.append(member)

    log_activity("member_added", {
        "member_id": member["id"]
    })

    return jsonify(member), 201


@app.route("/members/<int:member_id>", methods=["PUT"])
def update_member(member_id):
    member = find_member(member_id)

    if member is None:
        return create_error("Member not found", 404)

    data = get_json_data()

    if data is None:
        return create_error("A valid JSON object is required")

    if "name" in data:
        name = normalize_text(data["name"])

        if not validate_text(name):
            return create_error("Name cannot be empty")

        member["name"] = name

    if "email" in data:
        email = normalize_text(data["email"])

        if not validate_email(email):
            return create_error("A valid email address is required")

        duplicate = any(
            other["id"] != member_id
            and other["email"].lower() == email.lower()
            for other in members
        )

        if duplicate:
            return create_error("Email is already registered", 409)

        member["email"] = email

    log_activity("member_updated", {
        "member_id": member_id
    })

    return jsonify({
        "message": "Member updated successfully",
        "member": member
    })


@app.route("/members/<int:member_id>", methods=["DELETE"])
def delete_member(member_id):
    member = find_member(member_id)

    if member is None:
        return create_error("Member not found", 404)

    active_records = [
        record for record in issued_books
        if record["member_id"] == member_id
    ]

    if active_records:
        return create_error(
            "Member has books that must be returned first",
            409
        )

    members.remove(member)

    log_activity("member_deleted", {
        "member_id": member_id
    })

    return jsonify({
        "message": "Member deleted successfully"
    })


# --------------------------------------------------
# Book issue workflow
# --------------------------------------------------

@app.route("/issue", methods=["POST"])
def issue_book():
    data = get_json_data()

    if data is None:
        return create_error("A valid JSON object is required")

    book_id = data.get("book_id")
    member_id = data.get("member_id")

    if not isinstance(book_id, int) or isinstance(book_id, bool):
        return create_error("book_id must be an integer")

    if not isinstance(member_id, int) or isinstance(member_id, bool):
        return create_error("member_id must be an integer")

    book = find_book(book_id)
    member = find_member(member_id)

    if book is None:
        return create_error("Book not found", 404)

    if member is None:
        return create_error("Member not found", 404)

    if not member.get("active", True):
        return create_error("Member account is inactive", 403)

    if not book["available"]:
        return create_error("Book is already issued", 409)

    record = {
        "book_id": book_id,
        "member_id": member_id,
        "issued_at": datetime.now().isoformat(timespec="seconds")
    }

    book["available"] = False
    issued_books.append(record)

    log_activity("book_issued", record)

    return jsonify({
        "message": "Book issued successfully",
        "record": record
    }), 201


# --------------------------------------------------
# Book return workflow
# --------------------------------------------------

@app.route("/return", methods=["POST"])
def return_book():
    data = get_json_data()

    if data is None:
        return create_error("A valid JSON object is required")

    book_id = data.get("book_id")

    if not isinstance(book_id, int) or isinstance(book_id, bool):
        return create_error("book_id must be an integer")

    record = find_issued_record(book_id)

    if record is None:
        return create_error("Book is not currently issued", 404)

    book = find_book(book_id)

    if book is None:
        return create_error(
            "The issued book no longer exists in the catalogue",
            409
        )

    book["available"] = True
    issued_books.remove(record)

    log_activity("book_returned", {
        "book_id": book_id,
        "member_id": record["member_id"]
    })

    return jsonify({
        "message": "Book returned successfully",
        "book_id": book_id
    })


# --------------------------------------------------
# Issue record retrieval
# --------------------------------------------------

@app.route("/issued", methods=["GET"])
def get_issued_books():
    return jsonify(issued_books)


@app.route("/issued/<int:book_id>", methods=["GET"])
def get_issue_by_book(book_id):
    record = find_issued_record(book_id)

    if record is None:
        return create_error("No active issue record found", 404)

    return jsonify(record)


# --------------------------------------------------
# Library statistics
# --------------------------------------------------

@app.route("/statistics", methods=["GET"])
def get_statistics():
    total_books = len(books)
    available_count = sum(
        1 for book in books if book["available"]
    )
    issued_count = len(issued_books)

    total_members = len(members)
    active_members = sum(
        1 for member in members if member.get("active", True)
    )

    categories = {}

    for book in books:
        category = book.get("category", "General")
        categories[category] = categories.get(category, 0) + 1

    return jsonify({
        "books": {
            "total": total_books,
            "available": available_count,
            "issued": issued_count,
            "categories": categories
        },
        "members": {
            "total": total_members,
            "active": active_members
        }
    })


@app.route("/activity", methods=["GET"])
def get_activity():
    limit = request.args.get("limit", default=20, type=int)

    if limit is None or limit < 1:
        return create_error("Limit must be a positive integer")

    return jsonify({
        "count": min(limit, len(activity_log)),
        "activities": activity_log[-limit:][::-1]
    })


# --------------------------------------------------
# Error handlers
# --------------------------------------------------

@app.errorhandler(404)
def handle_not_found(error):
    return create_error("Requested endpoint was not found", 404)


@app.errorhandler(405)
def handle_method_not_allowed(error):
    return create_error("HTTP method is not allowed for this endpoint", 405)


@app.errorhandler(500)
def handle_internal_error(error):
    app.logger.exception("Unexpected internal server error")
    return create_error("An internal server error occurred", 500)


# --------------------------------------------------
# Application entry point
# --------------------------------------------------

if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=DEFAULT_PORT,
        debug=True
    )

