import pymysql
from pymysql.cursors import DictCursor
import configparser
import os

def load_db_config():
    config = configparser.ConfigParser()
    ini_path = os.path.join(os.path.dirname(__file__), 'db_config.ini')
    config.read(ini_path, encoding='utf-8')
    # 必须全部字段都在 ini 文件中
    return {
        'host': config.get('mysql', 'host'),
        'user': config.get('mysql', 'user'),
        'password': config.get('mysql', 'password'),
        'db': config.get('mysql', 'db'),
        'charset': config.get('mysql', 'charset'),
        'cursorclass': DictCursor
    }

DB_CONFIG = load_db_config()

def get_db_connection():
    try:
        return pymysql.connect(**DB_CONFIG)
    except Exception as e:
        print(f"[db_util.py] 数据库连接失败: {e}")
        return None
