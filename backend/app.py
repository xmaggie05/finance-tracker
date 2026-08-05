from flask import Flask, jsonify
from config import Config
from models import db, Expense

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


with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)