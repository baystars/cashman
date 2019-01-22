# -*- mode: python -*- -*- coding: utf-8 -*-
from flask import (Flask, jsonify, request)

from .model.expense import (Expense, ExpenseSchema)
from .model.income import (Income, IncomeSchema)
from .model.transaction_type import TransactionType

app = Flask(__name__)

transactions = [
    Income('Salary', 5000),
    Income('Dividends', 200),
    Expense('pizza', 50),
    Expense('Rock Concert', 100)
]

@app.route('/incomes')
def get_incomes():
    schema = IncomeSchema(many=True)
    incomes = schema.dump(
        filter(lambda t: t.tipe == TransactionType.INCOME, transactions)
    )
    return jsonify(incomes.data)


@app.route('/incomes', methods=['POST'])
def add_income():
    income = IncomeSchema().load(request.get_json())
    transactions.append(income.data)
    return "", 204


@app.route('/expenses')
def get_expenses():
    schema = ExpenseSchema(many=True)
    expenses = schema.dump(
        filter(lambda t: t.tipe == TransactionType.EXPENSE, transactions)
    )
    return jsonify(expenses.data)

@app.route('/expenses', methods=['POST'])
def add_expense():
    expense = ExpenseSchema().load(request.get_json())
    transactions.append(expense.data)
    return "", 204


if __name__ == "__main__":
    app.run()
