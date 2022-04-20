from Crypto.PublicKey import RSA

def gen_prk(RSA_len: int = 1024) -> tuple:
    key = RSA.generate(RSA_len)
    prk_key = key.export_key()
    return (key, prk_key)

def gen_puk(prk: object) -> str:
    puk_key = prk.publickey().export_key()
    return puk_key

def write_key(key: str, file_name: str):
    file_out = open(f"{file_name}", "wb")
    file_out.write(key)
    file_out.close()
