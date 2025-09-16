# merchant_login.py
from db_util import get_db_connection
from pymysql.cursors import DictCursor
from datetime import datetime, timedelta
import random

class MerchantAuth:
    def _conn(self):
        return get_db_connection()

    # ---------- 校验唯一性 ----------
    def exists_by_email(self, email: str) -> bool:
        conn = self._conn()
        if not conn: return True
        try:
            with conn.cursor() as c:
                c.execute("SELECT id FROM merchant_login WHERE email=%s", (email,))
                return c.fetchone() is not None
        finally:
            conn.close()

    def exists_by_username(self, username: str) -> bool:
        conn = self._conn()
        if not conn: return True
        try:
            with conn.cursor() as c:
                c.execute("SELECT id FROM merchant_login WHERE username=%s", (username,))
                return c.fetchone() is not None
        finally:
            conn.close()

    def exists_by_phone(self, phone: str) -> bool:
        conn = self._conn()
        if not conn: return True
        try:
            with conn.cursor() as c:
                c.execute("SELECT id FROM merchant_login WHERE phone=%s", (phone,))
                return c.fetchone() is not None
        finally:
            conn.close()

    # ---------- 登录 ----------
    def check_login(self, email: str, password: str) -> bool:
        conn = self._conn()
        if not conn: return False
        try:
            with conn.cursor() as c:
                sql = "SELECT id FROM merchant_login WHERE email=%s AND password=%s"
                c.execute(sql, (email, password))
                return c.fetchone() is not None
        except pymysql.MySQLError as e:
            print(f"[MerchantAuth] login error: {e}")
            return False
        finally:
            conn.close()

    # ---------- 注册（插入商家） ----------
    def register(self, username: str, name: str, email: str, phone: str,
                 password: str, business_type: str):
        conn = self._conn()
        if not conn:
            return False, "数据库连接失败，请稍后重试"
        try:
            with conn.cursor() as c:
                # 唯一性检查
                c.execute("SELECT id FROM merchant_login WHERE email=%s OR username=%s OR phone=%s",
                          (email, username, phone))
                if c.fetchone():
                    return False, "用户名/邮箱/手机号已被注册"

                sql = """INSERT INTO merchant_login
                         (username, name, email, phone, password, business_type, status)
                         VALUES (%s, %s, %s, %s, %s, %s, 'pending')"""
                c.execute(sql, (username, name, email, phone, password, business_type))
            conn.commit()
            return True, "注册成功，待审核"
        except pymysql.MySQLError as e:
            conn.rollback()
            print(f"[MerchantAuth] register error: {e}")
            return False, "注册失败，请稍后重试"
        finally:
            conn.close()

    # ---------- 注册验证码 ----------
    def create_register_code(self, email: str, minutes=10) -> str | None:
        code = f"{random.randint(0, 999999):06d}"
        conn = self._conn()
        if not conn: return None
        try:
            with conn.cursor() as c:
                # 将旧的未使用、未过期的同邮箱验证码置为 used=1（可选）
                c.execute("""UPDATE merchant_register_codes
                             SET used=1 WHERE email=%s AND used=0 AND expires_at > NOW()""", (email,))
                # 插入新验证码
                expires = datetime.now() + timedelta(minutes=minutes)
                sql = """INSERT INTO merchant_register_codes (email, code, purpose, used, expires_at)
                         VALUES (%s, %s, 'register', 0, %s)"""
                c.execute(sql, (email, code, expires))
            conn.commit()
            return code
        except pymysql.MySQLError as e:
            conn.rollback()
            print(f"[MerchantAuth] create code error: {e}")
            return None
        finally:
            conn.close()

    def verify_register_code(self, email: str, code: str) -> bool:
        conn = self._conn()
        if not conn: return False
        try:
            with conn.cursor() as c:
                sql = """SELECT id FROM merchant_register_codes
                         WHERE email=%s AND code=%s AND used=0 AND expires_at > NOW()
                         ORDER BY id DESC LIMIT 1"""
                c.execute(sql, (email, code))
                row = c.fetchone()
                return row is not None
        finally:
            conn.close()

    def mark_register_code_used(self, email: str, code: str):
        conn = self._conn()
        if not conn: return
        try:
            with conn.cursor() as c:
                c.execute("""UPDATE merchant_register_codes
                            SET used=1 WHERE email=%s AND code=%s AND used=0""", (email, code))
            conn.commit()
        finally:
            conn.close()