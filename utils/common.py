

def hashed_password(plain_text):
    import hashlib
    # 用 ascii 编码转换成 bytes 对象
    p = plain_text.encode('ascii')
    s = hashlib.md5(p)
    # 返回摘要字符串
    return s.hexdigest()


def salted_password(password, salt='$!@><?>HUI&DWQa`'):
    
    def hashed_pwd(ascii_str):
        import hashlib
        return hashlib.sha256(ascii_str.encode('ascii')).hexdigest()

    hash1 = hashed_pwd(password)
    hash2 = hashed_pwd(hash1 + salt)
    return hash2



def check_password_strength(password):
    """ 检查密码强度 """
    
    if len(password) < 8:
        return False
    if not any(char.isdigit() for char in password):
        return False
    if not any(char.isupper() for char in password):
        return False
    if not any(char.islower() for char in password):
        return False
    import re
    if not re.search("[^a-zA-Z0-9]", password):
        return False
    
    return True
