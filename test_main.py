import json
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


#  {"payer": "C", "points": 50, "timestamp": "2022-06-20T11:07:05.017197"}

# =============================================================================================
# GET /POINTS
# =============================================================================================
def test_get_payer_zero_points():
  response = client.get("/points")
  assert response.status_code == 200
  assert response.json() == {}

# =============================================================================================
# POST /POINTS
# =============================================================================================
def test_nagative_balance_transaction():
  response = client.post("/points",
  json={"payer": "A", "points": -50, "timestamp": "2022-06-20T11:07:05.017197"},
  )
  assert response.status_code == 422
  assert response.json() == {"detail": 'ERROR: Unable to add transaction; payer balance cannnot go negative. A has 0 points in account.'}

def test_zero_balance_transaction():
  response = client.post("/points",
  json={"payer": "A", "points": 0, "timestamp": "2022-06-20T11:07:05.017197"},
  )
  assert response.status_code == 422
  assert response.json() == {"detail": 'ERROR: Unable to add transaction; Points must be positive or negative integer.'}

def test_valid_transaction_sequence():
  client.post("/points",
  json={"payer": "A", "points": 100, "timestamp": "2022-06-20T11:07:05.017197"},
  )
  client.post("/points",
  json={"payer": "B", "points": 100, "timestamp": "2022-06-20T11:07:05.017197"},
  )
  client.post("/points",
  json={"payer": "A", "points": -100, "timestamp": "2022-06-20T11:07:05.017197"},
  )
  response = client.post("/points",
  json={"payer": "B", "points": -100, "timestamp": "2022-06-20T11:07:05.017197"},
  )
  assert response.status_code == 200
  assert response.json() == {"Message": "Transaction Successful", "Current Balance": {"A": 0, "B": 0}}

# =============================================================================================
# POST /POINTS/SPEND
# =============================================================================================
def test_invalid_negative_spend():
  response = client.post("/points/spend",
  json={"points": -50},
  )
  assert response.status_code == 422
  assert response.json() == {"detail": 'ERROR: Points spend must be greater than 0.'}

def test_invalid_too_many_points_spend():
  client.post("/points",
  json={"payer": "A", "points": 100, "timestamp": "2022-06-20T11:07:05.017197"},
  )
  client.post("/points",
  json={"payer": "A", "points": -100, "timestamp": "2022-06-20T11:07:05.017197"},
  )
  response = client.post("/points/spend",
  json={"points": 500},
  )
  assert response.status_code == 422
  assert response.json() == {"detail": 'ERROR: Not enough points. 0 points available to spend.'}

def test_valid_transaction_spend_sequence():
  client.post("/points",
  json={"payer": "A", "points": 100, "timestamp": "2022-06-20T11:07:01.017197"},
  )
  client.post("/points",
  json={"payer": "A", "points": -50, "timestamp": "2022-06-20T11:07:02.017197"},
  )
  client.post("/points",
  json={"payer": "B", "points": 150, "timestamp": "2022-06-20T11:07:03.017197"},
  )
  response = client.post("/points/spend",
  json={"points": 150},
  )
  assert response.status_code == 200
  assert response.json() == [{"payer": "A", "points": -50}, {"payer": "B", "points": -100}]

def test_get_payer_end_points():
  response = client.get("/points")
  assert response.status_code == 200
  assert response.json() == {"A": 0, "B": 50}
