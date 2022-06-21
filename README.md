# Fetch Rewards Backend Software Engineering Takehome
A REST API designed to receive HTTP requests and return responses based on a user's transactions, reward points balance, and reward points spend. 

## Overview
* A `user` can have reward points balances in their account from various `payers` (presumably businesses where a user transacts)
  * e.g., `{"Nike": 500, "Cheesecake Factory": 1000}`
 
* `Transactions` are submitted to add or subtract points from a user's reward points balance
  * Payer balances in a user's account cannot go below 0
 
* A user can `spend` points from their account/payer balances
  * User's total points cannot go below 0
  * Points are spent in First-In-First-Out order based on transaction timestamp, irrespective of payer

## Dependencies 
* [Python](https://www.python.org/downloads/) - The latest version of Python to run the program, or at least version 3.7+
* [FastAPI](https://fastapi.tiangolo.com/) - A modern, fast, web framework for building APIs with Python 3.6+ based on standard Python type hints
* [Pydantic](https://pydantic-docs.helpmanual.io/) - Data validation and settings management using python type annotations
* [Pytest](https://docs.pytest.org/en/7.1.x/index.html) - Python testing framework

## Installation

1) Clone git repo to your local machine 
   ```
    git clone https://github.com/alexsmaldone/fetchrewards-takehome.git
   ```
2) Cd into the project's root directory 
   ```
    cd fetchrewards-takehome/
   ```
3) Install dependencies
   ```
    pip install -r requirements.txt
   ```
4) Start the server
   ```
    uvicorn main:app --reload
   ```
   Your terminal should read: 
   ` Uvicorn running on http://127.0.0.1:8000`
   
   You can verify the server is running by visiting http://localhost:8000 in your browser, where you should see this response: 
   
   `Hi! Welcome to Alex Smaldone's Fetch Rewards Backend Engineer Takehome Test`
   
## Using the API
_This service uses no database or persistent storage, so user points / payer transactions will reset every time the server is started/restarted_

I recommend using a tool like [Postman](https://www.postman.com/downloads/) to test out API calls. 

## POST Route "/points" - Add Payer Transaction
***Request Format*** 
```
{"payer": <str>, "points": <int>, "timestamp": <datetime>}
```

***Example Request and Response*** 
```
{"payer": "Nike, "points": 500, "timestamp": "2022-06-20T11:07:01.017197"}
```
```
{"Message": "Transaction Successful", "Current Balance": 500}
```

***Example Request and Response (including previous)*** 
```
{"payer": "Adidas, "points": 500, "timestamp": "2022-06-20T11:07:02.017197"}
```
```
{"Message": "Transaction Successful", "Current Balance": 1000}
```

***Error Handling***
* Preventing payer balances from going negative
* Preventing 0 points transactions 
* Type checking for request body values 

## POST Route "/points/spend" - Spend User Points 
***Request Format*** 
```
{"points": <int>}
```

***Example Request and Response*** 
```
{"points": 250}
```
Subtracts 250 points from Nike payer balance as it is the oldest transaction. 
```
{"payer": "Nike", "points": -250}
```

***Error Handling***
* Preventing spend that is greater than total user points
* Preventing negative spend 
* Type checking for request body values 

## GET Route "/points" - Get User Points by Payer
After making the above transaction and spend requests, the payer points would look like:
```
{
"Nike": 250, "Adidas": 500
}
```

## Running Tests
You can run the tests in `test_main.py` from the main directory by running:
```
pytest
```

The tests check the following:
* Returns the proper points balance
* Cannot create negative payer balances with a transaction
* Cannot add 0 point transactions 
* Tests valid transaction sequences
* Tests valid spend sequences 
* Spend must be greater than 0 and less than total available points 
