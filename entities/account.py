from persistence.db import get_connection
import pymysql
from entities.user import User

class Account():
    def __init__(self, id: int, number: int, account_date: str, id_user: int):
        self.id = id
        self.number = number
        self.account_date = account_date
        self.id_user = id_user
    
    def get_account_by_id(id_user):
        try:
            connection = get_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            sql = "SELECT id, number, creation_date, id_user FROM account WHERE id_user = %s"
            cursor.execute(sql, (id_user,))

            account = cursor.fetchone()

            cursor.close()
            connection.close()

            if account:
                return Account(
                    account["id"],
                    account["number"],
                    account["creation_date"],
                    account["id_user"]
                )

            return None
        except Exception as ex:
            print(f"Error account:{ex}")
            return False