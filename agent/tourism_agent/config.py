# coding=UTF-8
import socket

class Config:
    def __init__(self):
        # 确保所有字符串都是UTF-8编码
        self.appcode = "1e912859f0e4492c8aec9c1bfc2128d0"  # 开通服务后 买家中心-查看AppCode
        self.host = "https://scenicspot.market.alicloudapi.com"
        self.path = "/lianzhuo/scenicspot"
        self.method = "GET"
        
        # 添加超时设置和重试次数
        self.timeout = 10  # 请求超时时间(秒)
        self.max_retries = 3  # 最大重试次数
        
        # 确保中文正常显示
        self.ensure_utf8()
    
    def ensure_utf8(self):
        """确保系统环境支持UTF-8编码"""
        import sys
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8')
        elif hasattr(sys.stdout, 'encoding') and sys.stdout.encoding != 'utf-8':
            import io
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')