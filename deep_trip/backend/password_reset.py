# password_reset.py
import pymysql
from pymysql.cursors import DictCursor
from datetime import datetime, timedelta
import random

class PasswordReset:
    def __init__(self):
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': '123456',
            'db': 'deeptrip',
            'charset': 'utf8mb4',
            'cursorclass': DictCursor
        }

    def _conn(self):
        try:
            return pymysql.connect(**self.db_config)
        except Exception as e:
            print(f"[PasswordReset] 数据库连接失败: {e}")
            return None

    # ---------- 用户与验证码 ----------
    def user_exists(self, email: str) -> bool:
        conn = self._conn()
        if not conn:
            return False
        try:
            with conn.cursor() as c:
                c.execute("SELECT id FROM user_login WHERE email=%s", (email,))
                return c.fetchone() is not None
        finally:
            conn.close()

    def _gen_code(self) -> str:
        return ''.join(random.choice('0123456789') for _ in range(6))

    def create_code(self, email: str, minutes: int = 10) -> str:
        code = self._gen_code()
        expire = datetime.now() + timedelta(minutes=minutes)
        conn = self._conn()
        if not conn:
            return None
        try:
            with conn.cursor() as c:
                c.execute(
                    "INSERT INTO password_reset_codes (email, code, expire_at) VALUES (%s, %s, %s)",
                    (email, code, expire.strftime('%Y-%m-%d %H:%M:%S'))
                )
            conn.commit()
            return code
        except pymysql.MySQLError as e:
            conn.rollback()
            print(f"[PasswordReset] 写入验证码失败: {e}")
            return None
        finally:
            conn.close()

    def verify_code_valid(self, email: str, code: str) -> bool:
        conn = self._conn()
        if not conn:
            return False
        try:
            with conn.cursor() as c:
                c.execute(
                    """
                    SELECT id FROM password_reset_codes
                    WHERE email=%s AND code=%s AND used=0 AND expire_at > NOW()
                    ORDER BY id DESC LIMIT 1
                    """,
                    (email, code)
                )
                return c.fetchone() is not None
        finally:
            conn.close()

    def mark_code_used(self, email: str, code: str) -> None:
        conn = self._conn()
        if not conn:
            return
        try:
            with conn.cursor() as c:
                c.execute(
                    """
                    UPDATE password_reset_codes
                    SET used=1
                    WHERE email=%s AND code=%s AND used=0
                    ORDER BY id DESC LIMIT 1
                    """,
                    (email, code)
                )
            conn.commit()
        except pymysql.MySQLError as e:
            conn.rollback()
            print(f"[PasswordReset] 标记验证码已用失败: {e}")
        finally:
            conn.close()

    # ---------- 密码更新 ----------
    def update_user_password_plain(self, email: str, new_password: str) -> bool:
        """与现有明文登录逻辑保持一致：更新 user_login.password"""
        conn = self._conn()
        if not conn:
            return False
        try:
            with conn.cursor() as c:
                c.execute("UPDATE user_login SET password=%s WHERE email=%s", (new_password, email))
            conn.commit()
            return True
        except pymysql.MySQLError as e:
            conn.rollback()
            print(f"[PasswordReset] 更新密码失败: {e}")
            return False
        finally:
            conn.close()
