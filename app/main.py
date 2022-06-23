from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from .route_functions import validate_transaction, process_transaction, validate_spend, process_spend

app = FastAPI()

class PayerTransaction(BaseModel):
  payer: str
  points: int
  timestamp: datetime = datetime.now()

class SpendPoints(BaseModel):
  points: int

class User():
  def __init__(self, total_points=0):
    self.total_points = total_points
    self.payer_points = {}
    self.transactions = []

user = User()

@app.get("/")
def home():
  return "Hi! Welcome to Alex Smaldone's Fetch Rewards Backend Engineer Takehome Test"


@app.get("/points", status_code=200)
def get_payer_points():

    return user.payer_points

@app.post("/points", status_code=200)
def add_transaction(transaction: PayerTransaction):

  validate_transaction(transaction, user.payer_points, user.transactions)
  return process_transaction(user.transactions, transaction, user.payer_points, user)

@app.post("/points/spend", status_code=200)
def spend_payer_points(spend: SpendPoints):

  validate_spend(spend.points, user.total_points)
  user.total_points -= spend.points
  return process_spend(spend.points, user.transactions, user.payer_points)
