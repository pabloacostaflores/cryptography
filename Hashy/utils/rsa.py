import os
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import *

def generate_key_pair():
    key = rsa.generate_private_key(backend=default_backend(), public_exponent=65537, key_size=1024)

    encrypted_pem_private_key = key.private_bytes(encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.PKCS8, encryption_algorithm=serialization.NoEncryption())

    pem_public_key = key.public_key().public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)

    with open(f"{os.getcwd()}/keys/private.pem", "w") as pKey:
        pKey.write(encrypted_pem_private_key.decode("utf-8"))
    
    with open(f"{os.getcwd()}/keys/public.pem", "w") as pubKey:
        pubKey.write(pem_public_key.decode("utf-8"))
    
def validate_key():
    return os.path.isfile(f"{os.getcwd()}/keys/private.pem") and os.path.isfile(f"{os.getcwd()}/keys/public.pem")

def get_keys():
    with open(f"{os.getcwd()}/keys/private.pem", "rb") as pKey:
        private_key = serialization.load_pem_private_key(pKey.read(), password=None)
        pubKey = private_key.public_key().public_bytes(serialization.Encoding.OpenSSH, serialization.PublicFormat.OpenSSH)
        pem = private_key.private_bytes(encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.TraditionalOpenSSL, encryption_algorithm=serialization.NoEncryption())
        private_key_str = pem.decode('utf-8')
        public_key_str = pubKey.decode('utf-8')
        return private_key_str, public_key_str

def cipher(plain_value, key_path) -> bytes:
    try:
        public_key = open(key_path, "rb")
        public = serialization.load_pem_private_key(public_key.read(), backend=default_backend())
        cipher = public.encrypt(plain_value.encode(), padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA1()), algorithm=hashes.SHA1(), label=None))
        public_key.close()
        return cipher
    except UnsupportedAlgorithm:
        print("El algoritmo de la llave proporcionada es invalido para el metodo seleccionado")
        return None
    except ValueError:
        print("El valor de la llave seleccionada es invalido")
        return None

def uncipher(value, key_path) -> str:
    try:
        private_key = open(key_path, "rb")
        private = serialization.load_pem_private_key(private_key.read(), backend=default_backend(), password=None)
        plain = private.decrypt(value, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA1()), algorithm=hashes.SHA1(), label=None))
        return plain
    except InvalidKey:
        print("La llave proporcionada es invalida para el metodo seleccionado")
        return None
    except UnsupportedAlgorithm:
        print("El algoritmo de la llave proporcionada es invalido para el metodo seleccionado")
        return None
    except ValueError:
        print("El valor de la llave seleccionada es invalido")
        return None

def sign(value, key_path) -> tuple:
    try:
        private_key = open(key_path, "rb")
        private = serialization.load_pem_private_key(private_key.read(), backend=default_backend(), password=None)
        signed_hash = private.sign(value, padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256())
        return ("ok",signed_hash)
    except UnsupportedAlgorithm:
        print("La llave de firma es incorrecta para el modo de operacion")
        return ("error", "La llave de firma es incorrecta para el modo de operacion")
    except:
        print("Error al generar la firma")
        return ("error", "Error al generar la firma")

def verify_sign(plain_value, sign_value, key_path) -> tuple:
    try:
        public_key = open(key_path, "rb")
        public = serialization.load_pem_public_key(public_key.read(), backend=default_backend())
        public.verify(signature=sign_value, data=plain_value, padding= padding.PSS(mgf=padding.MGF1(hashes.SHA256()),salt_length=padding.PSS.MAX_LENGTH),algorithm=hashes.SHA256())
        return ("ok", "Los hashes coinciden")
    except InvalidSignature:
        return ("error", "La firma es inválida")
    except ValueError:
        print("La llave seleccionada no coincide con el formato para verificar (PRIVATE_KEY_SELECTED)")
        return ("error", "La llave seleccionada no coincide con el formato necesario (PRIVATE_KEY_SELECTED)")