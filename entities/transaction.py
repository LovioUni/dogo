from persistence.db import get_connection
import pymysql
from enums.transaction_type import TransactionType

class Transaction():
    def __init__(self, id: int, description: str, date: str, amount: float, type: TransactionType, id_account: int):
        self.id = id
        self.description = description
        self.date = date
        self.amount = amount
        self.type = type
        self.id_account = id_account

    def get_transactions_by_account(id_account):
        try:
            connection = get_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            sql = "SELECT id, description, date, amount, type, id_account FROM transaction WHERE id_account = %s ORDER BY date DESC"
            cursor.execute(sql, (id_account,))
            rows = cursor.fetchall()
            cursor.close()
            connection.close()
            return [
                Transaction(
                    r["id"], r["description"], r["date"],
                    r["amount"], TransactionType(r["type"]), r["id_account"]
                ) for r in rows
            ]
        except Exception as ex:
            print(f"Transaction error: {ex}")
            return []
        
    def get_balance_by_account(id_account):
        try:
            connection = get_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            sql = """
            SELECT SUM(CASE WHEN type = 1 THEN amount ELSE -amount END) AS balance FROM `transaction` WHERE id_account = %s"""

            cursor.execute(sql, (id_account,))
            result = cursor.fetchone()

            cursor.close()
            connection.close()

            return result["balance"] if result["balance"] is not None else 0

        except Exception as ex:
            print(f"Balance error: {ex}")
            return 0