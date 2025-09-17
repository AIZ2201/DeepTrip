from .db_util import get_db_connection
from pymysql.cursors import DictCursor

class UserLogin:
    def check_user_login(self, email, password):
        """验证用户登录信息"""
        # 空值检查
        if not email or not password:
            return False
            
        conn = get_db_connection()
        if not conn:
            return False
            
        try:
            with conn.cursor() as cursor:
                # 查询用户信息
                sql = "SELECT id FROM user_login WHERE email = %s AND password = %s"
                cursor.execute(sql, (email, password))
                user = cursor.fetchone()
                
                # 如果找到用户则返回True
                return user is not None
        except Exception as e:
            print(f"数据库查询错误: {e}")
            return False
        finally:
            # 确保连接关闭
            if conn:
                conn.close()

    def get_user_info(self, email):
        """获取用户详细信息"""
        conn = get_db_connection()
        if not conn:
            return None
            
        try:
            with conn.cursor() as cursor:
                sql = "SELECT * FROM user_login WHERE email = %s"
                cursor.execute(sql, (email,))
                return cursor.fetchone()
        except Exception as e:
            print(f"获取用户信息错误: {e}")
            return None
        finally:
            if conn:
                conn.close()
