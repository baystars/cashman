# Cashman - Flask Restful Application

## General

* [Python と Flask で RESTful API を開発する](https://auth0.com/blog/jp-developing-restful-apis-with-python-and-flask/)
* [Auth0 Python API SDK Quickstarts: Authorization](https://auth0.com/docs/quickstart/backend/python)

## Hello Application

run

    $ make hello

## First simple Restful API

run

    $ make run-simple

get and post

    $ curl http://localhost:5000/incomes
    [
      {
        "amount": 5000, 
        "description": "salary"
      }
    ]
    $ curl -X POST -H "Content-Type: application/json" -d '{"description": "lottery", "amount": 1000.0 }' http://localhost:5000/incomes
    $ curl http://localhost:5000/incomes
    [
      {
        "amount": 5000, 
        "description": "salary"
      }, 
      {
        "amount": 1000.0, 
        "description": "lottery"
      }
    ]

## Final API

run

    $ make run

get expenses

    $ curl http://localhost:5000/expenses
    [
      {
        "amount": -50.0, 
        "created_at": "2019-01-22T11:48:59.424475", 
        "description": "pizza", 
        "tipe": "TransactionType.EXPENSE"
      }, 
      {
        "amount": -100.0, 
        "created_at": "2019-01-22T11:48:59.424486", 
        "description": "Rock Concert", 
        "tipe": "TransactionType.EXPENSE"
      }
    ]
    
add a new expense

    $ curl -X POST -H "Content-Type: application/json" -d '{ "amount": 20, "description": "lottery ticket"}' http://localhost:5000/expenses

get incomes

    $ curl http://localhost:5000/incomes
    [
      {
        "amount": 5000.0, 
        "created_at": "2019-01-22T11:48:59.424433", 
        "description": "Salary", 
        "tipe": "TransactionType.INCOME"
      }, 
      {
        "amount": 200.0, 
        "created_at": "2019-01-22T11:48:59.424460", 
        "description": "Dividends", 
        "tipe": "TransactionType.INCOME"
      }
    ]
    
add a new income

    $ curl -X POST -H "Content-Type: application/json" -d '{"amount": 300.0, "description": "loan payment"}' http://localhost:5000/incomes


## Auth0 sample

get access token

    $ curl --request POST \
      --url https://example.com \
      --header 'content-type: application/json' \
      --data '{"client_id":"xxx,"client_secret":"xxx","audience":"https://example.com","grant_type":"client_credentials"}'
    {"access_token":"xxx","expires_in":86400,"token_type":"Bearer"}
