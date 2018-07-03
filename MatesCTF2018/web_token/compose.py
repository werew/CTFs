from base64 import b64decode, b64encode
from Crypto.Cipher import AES
from hashlib import md5
from Crypto.Hash import HMAC
import base64


BLOCK_SIZE = 16
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * \
                chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]


def gen_hmac(user,secret):
    h = HMAC.new(secret.encode("utf-8"))
    h.update(user.encode("utf-8"))
    mac = h.hexdigest()
    return mac.encode("utf-8")

key="0123456789abcdef"
secret = "x"*16
user = "x"*16
mac = gen_hmac(user+":admin",secret)




padding = "0"*ord("0")
msg = padding+secret+user


a = base64.b64decode("ICJDLumdipinjur89h/c6SAiQy7pnYqYp47q/PYf3OnOM1M1tXoRYxx+0pPQNnLOwdJSDQ7sQbtJaEbXyopIZg==")
enc_padding = base64.b64decode("hh4SzvTuzCqTZ3R+Rlbeb4YeEs707swqk2d0fkZW3m+GHhLO9O7MKpNndH5GVt5vzjNTNbV6EWMcftKT0DZyzsHSUg0O7EG7SWhG18qKSGY=")[:len(padding)]

enc_secret = a[:16]
enc_user = a[16:] # "x"*16+":user"+hmac_secret+padding
token = base64.b64encode(enc_user+enc_secret+enc_padding)+mac


def encrypt(raw):
    raw = pad(raw)
    cipher = AES.new(key)
    return b64encode(cipher.encrypt(raw))

def decrypt(enc):
    enc = b64decode(enc)
    cipher = AES.new(key)
    return unpad(cipher.decrypt(enc)).decode('utf8')

def verify_hmac(secret, mac, msg):
    h = HMAC.new(secret.encode("utf-8"))
    h.update(msg.encode("utf-8"))
    if h.hexdigest() == mac:
        return True
    else:
        return False

def verify_token(token):
    if len(token) < 53:
        return 0, ""
    mac = token[-32:]
    token = token[:-32]
    try:
        data = decrypt(token)
        if len(data) >= 21:
            secret = data[-16:]
            data = data[:-16]
            i = data.rfind(":")
            if i >= 0:
                user = data[:i]
                if verify_hmac(secret, mac, user + ":user"):
                    return 1, user
                elif verify_hmac(secret, mac, user + ":admin"):
                    return 2, user
    except:
        pass
    return 0, 0


#enc_msg = b64decode(encrypt(msg))[:len(msg)]
#print verify_token(b64encode(enc_msg)+mac)
