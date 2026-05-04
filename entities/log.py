from datetime import datetime
from enums.log_type import LogType
from persistence.db import get_connection
import pymysql

class Log:
    def __init__(self, id: int, date: datetime, id_user: int, description: str, type: LogType):
        self.id = id
        self.date = date
        self.user = id_user
        self.description = description
        self.type = type

    def save(type: LogType, description: str, user) -> bool:
        print(f"[LOG] {datetime.now()} | {type.name} | Usuario: {user.email} | {description}")
        try:
            connection = get_connection()
            cursor = connection.cursor()
            sql = """
                INSERT INTO log (id_user, type, description, date)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql, (user.id, type.value, description, datetime.now()))
            connection.commit()
            cursor.close()
            connection.close()
            return True
        except Exception as ex:
            print(f"Error saving log: {ex}")
            return False

    def get_all() -> list:  
        try:
            connection = get_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            sql = """
                SELECT l.id, l.date, l.description, l.type, u.name AS user_name, u.email
                FROM log l
                JOIN user u ON l.id_user = u.id
                ORDER BY l.date DESC
            """
            cursor.execute(sql)
            rows = cursor.fetchall()
            cursor.close()
            connection.close()
            return rows
        except Exception as ex:
            print(f"Error getting logs: {ex}")
            return []