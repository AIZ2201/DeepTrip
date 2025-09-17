from .db_util import get_db_connection
import pymysql

class AdminLogin:
    def check_admin_login(self, email, password):
        """验证管理员登录信息"""
        # 空值检查
        if not email or not password:
            print("邮箱或密码为空")
            return False
        conn = get_db_connection()
        if not conn:
            return False
        try:
            with conn.cursor() as cursor:
                # 查询用户信息
                sql = "SELECT * FROM admin_login WHERE email = %s AND password = %s" # cursor给数据库递纸条
                cursor.execute(sql, (email, password)) # 翻结果
                admin = cursor.fetchone() # 取数据
                #### 测试后端数据搜索 ####
                print(admin)
                ########################
                # 如果找到用户则返回True
                return admin is not None
        except pymysql.MySQLError as e:
            print(f"数据库查询错误: {e}")
            return False
        finally:
            # 确保连接关闭
            if conn:
                conn.close()

    def get_admin_info(self, email):
        """获取管理员详细信息"""
        conn = get_db_connection() # boolean
        if not conn:
            return None
            
        try:
            with conn.cursor() as cursor:
                sql = "SELECT * FROM admin_login WHERE email = %s"
                cursor.execute(sql, (email,))
                return cursor.fetchone()
        except pymysql.MySQLError as e:
            print(f"获取管理员信息错误: {e}")
            return None
        finally:
            if conn:
                conn.close()
                conn.close()

    def get_admin_info(self, email):
        """获取管理员详细信息"""
        conn = self.get_db_connection() # boolean
        if not conn:
            return None
            
        try:
            with conn.cursor() as cursor:
                sql = "SELECT * FROM admin_login WHERE email = %s"
                cursor.execute(sql, (email,))
                return cursor.fetchone()
        except pymysql.MySQLError as e:
            print(f"获取管理员信息错误: {e}")
            return None
        finally:
            if conn:
                conn.close()
