# -*- mode: python -*- -*- coding: utf-8 -*-
from marshmallow import post_load

from .transaction import (Transaction, TransactionSchema)
from .transaction_type import TransactionType

class Expense(Transaction):
    def __init__(self, description, amount):
        super(Expense, self).__init__(description, -abs(amount), TransactionType.EXPENSE)

    def __repr__(self):
        return f'<Expense(name={self.description!r})>'

class ExpenseSchema(TransactionSchema):
    @post_load
    def make_expense(self, data):
        return Expense(**data)
