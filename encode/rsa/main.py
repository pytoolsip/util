from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
import base64
import os

RANDOM_GENERATOR=Random.new().read

if __name__ == '__main__':
    # 生成公钥、秘钥
    # rsa = RSA.generate(1024, RANDOM_GENERATOR)
    # # master的秘钥对的生成
    # PRIVATE_PEM = rsa.exportKey()
    # with open('master-private.pem', 'w') as f:
    #     f.write(PRIVATE_PEM.decode())
    # PUBLIC_PEM = rsa.publickey().exportKey()
    # with open('master-public.pem', 'w') as f:
    #     f.write(PUBLIC_PEM.decode())
    
    # 根据秘钥解码
    test = "fHPcI98h4u9bWCAxEXI+jK0y3LpqLuQ6airEV3CpPGDO3ijo95xQv/IPp2AGYXDHhaEk5Ao3SMHuHrevzsEzmKXbkW4COoHJnoRxDTtA16MiLiyh2cjWN5TfYcr/3rSaa32DP+5k/pZZUxL/rMx2+8GfMCQY9BcK05pmgBVYclM="
    with open('master-private.pem') as f:
        key = f.read()
    rsakey = RSA.importKey(key)
    cipher = Cipher_pkcs1_v1_5.new(rsakey)
    password = cipher.decrypt(base64.b64decode(test), RANDOM_GENERATOR)
    print("password:::", password)
