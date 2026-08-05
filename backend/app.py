from flask import Flask, jsonify, request
from config import Config
from models import db, Expense
from datetime import date

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.route("/")
def home():
    return {
        "message": "Welcome to Smart Finance Tracker API!",
        "status": "Backend is running"
    }

@app.route("/health")
def health():
    return {
        "status": "healthy"
    }

@app.route("/expenses")
#Reads Data
def get_expenses():
    expenses = Expense.query.all()
    result = []
    for expense in expenses:
        result.append({
            "id": expense.id,
            "user_id": expense.user_id,
            "amount": expense.amount,
            "description": expense.description,
            "category": expense.category,
            "date": expense.date.isoformat()
        })
    return jsonify(result)

@app.route("/expenses/<int:expense_id>")
def get_expense(expense_id):
    expense = db.session.get(Expense, expense_id)

    if expense is None:
        return {"error": "Expense not found"}, 404

    return jsonify({
        "id": expense.id,
        "user_id": expense.user_id,
        "amount": expense.amount,
        "description": expense.description,
        "category": expense.category,
        "date": expense.date.isoformat()
    })

@app.route("/expenses", methods=["POST"])
def create_expense():
    data = request.json

    new_expense = Expense(
        user_id = data["user_id"],
        amount = data["amount"],
        description = data.get("description"),
        category = data["category"],
        date = date.fromisoformat(data["date"])
    )

    db.session.add(new_expense)
    db.session.commit()

    return jsonify({
        "id": new_expense.id,
        "user_id": new_expense.user_id,
        "amount": new_expense.amount,
        "description": new_expense.description,
        "category": new_expense.category,
        "date": new_expense.date.isoformat()
    }), 201

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)