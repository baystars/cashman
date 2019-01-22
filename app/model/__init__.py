# -*- mode: python -*- -*- coding: utf-8 -*-
import datetime

from marshmallow import (Schema, fields)

class Transaction():
    def __init__(self, description, amount, tipe):
        self.description = description
        self.amount = amount
        self.created_at = datetime.datetime.now()
        self.tipe = tipe

    def __repr__(self):
        return '<Transaction(name={self.description!r})>'.format(self=self)

class TransactionSchema(Schema):
    description = fields.Str()
    amount = fields.Number()
    created_at = fields.Date()
    tipe = fields.Str()
