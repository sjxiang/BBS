

def hashed_password(plain_text):
    import hashlib
    # 用 ascii 编码转换成 bytes 对象
    p = plain_text.encode('ascii')
    s = hashlib.md5(p)
    # 返回摘要字符串
    return s.hexdigest()
