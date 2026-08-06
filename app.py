from flask import Flask, jsonify, request

app = Flask(__name__)

books = []

@app.route("/")
def home():
    return jsonify({
        "name": "Library API",
        "version": "1.0",
        "status": "running"
    })

@app.route("/books")
def get_books():
    return jsonify({
        "books": books
    })

@app.route("/books", methods=["POST"])
def create_book():
    data = request.get_json()

    books.append(data)

    return jsonify({
        "message": "Book created",
        "book": data
    })

if __name__ == "__main__":
    app.run(debug=True)