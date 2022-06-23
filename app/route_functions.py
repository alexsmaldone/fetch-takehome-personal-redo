from fastapi import HTTPException
from datetime import date
# =========================================================================================
# POST /points
# =========================================================================================

def validate_transaction(transaction, payer_points, transactions):
  if (transaction.payer not in payer_points and transaction.points < 0) or (transaction.payer in payer_points and payer_points[transaction.payer] + transaction.points < 0):
    raise HTTPException(status_code=422,
    detail=f'ERROR: Unable to add transaction; payer balance cannnot go negative. {transaction.payer} has {payer_points[transaction.payer] if transaction.payer in payer_points else 0} points in account.')
  if transaction.points == 0:
    raise HTTPException(status_code=422,
    detail=f'ERROR: Unable to add transaction; Points must be positive or negative integer.')

  transactions_copy = transactions[:]
  transactions_copy.append(transaction)
  try:
    transactions_copy.sort(key=lambda date: date.timestamp, reverse=True)
  except:
    raise HTTPException(status_code=422,
    detail=f'ERROR: Unable to add transaction; Date formatted incorrectly.')

def process_transaction(transactions, transaction, payer_points, user):
  user.total_points += transaction.points

  if transaction.payer not in payer_points:
    payer_points[transaction.payer] = 0
  payer_points[transaction.payer] += transaction.points
  transactions.append(transaction)
  transactions.sort(key=lambda date: date.timestamp, reverse=True)

  return {"Message": "Transaction Successful", "Current Balance": payer_points}


# =========================================================================================
# POST /points/spend
# =========================================================================================

def validate_spend(spend, user_points):
  if spend > user_points:
    raise HTTPException(status_code=422,
    detail=f'ERROR: Not enough points. {user_points} points available to spend.')
  if spend <= 0:
    raise HTTPException(status_code=422,
    detail=f'ERROR: Points spend must be greater than 0.')

def process_spend(spend, transactions, payer_points):
  spent = {}
  transaction_remove_counter = 0
  transIdx = len(transactions) - 1

  while spend > 0:
    transaction = transactions[transIdx]

    if transaction.points < spend:
      if transaction.payer not in spent:
        spent[transaction.payer] = 0
      spent[transaction.payer] -= transaction.points
      payer_points[transaction.payer] -= transaction.points
      spend -= transaction.points
      transaction.points = 0

    if transaction.points >= spend:
      if transaction.payer not in spent:
        spent[transaction.payer] = 0
      spent[transaction.payer] -= spend
      transaction.points -= spend
      payer_points[transaction.payer] -= spend
      spend = 0

    if transaction.points == 0:
      transaction_remove_counter += 1
      transIdx -= 1

  while transaction_remove_counter > 0:
    transactions.pop()
    transaction_remove_counter -= 1

  return [{"payer": payer, "points": spent[payer]} for payer in spent]
