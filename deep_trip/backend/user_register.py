# user_register.py
import pymysql

class UserRegister:
    def __init__(self):
        # 根据你的 MySQL 实际情况修改
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': '123456',
            'db': 'deeptrip',
            'charset': 'utf8mb4',
            'cursorclass': pymysql.cursors.DictCursor
        }

    def get_db_connection(self):
        try:
            return pymysql.connect(**self.db_config)
        except Exception as e:
            print(f"[UserRegister] 数据库连接失败: {e}")
            return None

    def register_user(self, username, email, phone, password):
        """
        注册新用户（明文密码版本，先跑通；后续再升级成哈希）
        """
        conn = self.get_db_connection()
        if not conn:
            return False, "数据库连接失败，请稍后重试"

        try:
            with conn.cursor() as cursor:
                # 查重（用户名或邮箱）
                sql_check = "SELECT id FROM user_login WHERE username=%s OR email=%s"
                cursor.execute(sql_check, (username, email))
                if cursor.fetchone():
                    return False, "用户名或邮箱已被注册"

                # 插入
                sql_insert = """
                    INSERT INTO user_login (username, password, email, phonenumber)
                    VALUES (%s, %s, %s, %s)
                """
                cursor.execute(sql_insert, (username, password, email, phone))
                conn.commit()
                return True, "注册成功"
        except pymysql.MySQLError as e:
            conn.rollback()
            print(f"[UserRegister] 数据库操作失败: {e}")
            return False, "注册失败，请稍后重试"
        finally:
            if conn:
                conn.close()
