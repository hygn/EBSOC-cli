import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES
bs = 16
def _unpad(s):
    return s[:-ord(s[len(s)-1:])]
def _pad(s):
    return s + (bs - len(s) % bs) * b'\x00'
def dataAssembly(memberSeq,lctreLrnSqno,progress):
    return f"{memberSeq}|{lctreLrnSqno}|{progress}"
def encrypt(key,iv,data):
    data = _pad(data.encode('utf-8'))
    cipher = AES.new(key.encode("utf8"), AES.MODE_CBC, iv.encode("utf8"))
    return base64.b64encode(cipher.encrypt(data)).decode('utf-8')
def decrypt(key,iv,data):
    enc = base64.b64decode(data)
    cipher = AES.new(key.encode("utf8"), AES.MODE_CBC, iv.encode("utf8"))
    return (cipher.decrypt(enc).decode('utf-8'))
