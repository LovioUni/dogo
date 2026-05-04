from persistence.db import get_connection
from werkzeug.security import generate_password_hash, check_password_hash
import pymysql
from enums.profile import Profile
from flask_login import UserMixin
from entities.permission import Permission
from enums.value_permission import ValuePermission

class User(UserMixin):
    def __init__(self, id: int, name: str, email: str, password: str, profile: Profile,
                 permissions: list, is_active: bool):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.profile = profile
        self.permissions = permissions
        self._is_active = is_active  

    @property
    def is_active(self): 
        return bool(self._is_active)

    def check_email_exists(email) -> bool:
        connection = get_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT email FROM user WHERE email = %s"
        cursor.execute(sql, (email,))
        row = cursor.fetchone()
        cursor.close()
        connection.close()
        return row is not None

    def save(name: str, email: str, password: str) -> bool:
        try:
            connection = get_connection()
            cursor = connection.cursor()
            hash_password = generate_password_hash(password)
            sql = "INSERT INTO user (name, email, password) VALUES (%s, %s, %s)"
            cursor.execute(sql, (name, email, hash_password))
            connection.commit()
            cursor.close()
            connection.close()
            return True
        except Exception as ex:
            print(f"Error saving user: {ex}")
            return False

    def check_login(email, password):
        try:
            connection = get_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            sql = "SELECT id, password, is_active FROM user WHERE email = %s"
            cursor.execute(sql, (email,))
            user = cursor.fetchone()
            cursor.close()
            connection.close()

            if not user:
                return None
            if user["is_active"] != 1:
                return "inactive"
            if check_password_hash(user["password"], password):
                return User.get_by_id(user["id"])
            return None
        except Exception as ex:
            print(f"Error login user: {ex}")
            return None

    def get_by_id(id):
        try:
            connection = get_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            sql = """
                SELECT u.id, u.name, u.email, u.password, u.profile, u.is_active,
                       p.id AS permission_id, p.value AS permission_value
                FROM user u
                LEFT JOIN permission p ON u.id = p.id_user
                WHERE u.id = %s
            """
            cursor.execute(sql, (id,))
            rows = cursor.fetchall()
            cursor.close()
            connection.close()

            if not rows:
                return None

            user_data = rows[0]
            permissions = []
            for r in rows:
                if r["permission_id"] is not None:
                    permissions.append(
                        Permission(r["permission_id"], ValuePermission(r["permission_value"]))
                    )

            return User(
                user_data["id"],
                user_data["name"],
                user_data["email"],
                user_data["password"],
                Profile(user_data["profile"]),
                permissions,
                user_data["is_active"]
            )
        except Exception as ex:
            print(f"Error getting user by id: {ex}")
            return None