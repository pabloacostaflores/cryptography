from Crypto.Cipher import DES3

def pad(data): 
    """
    Funcion que permite rellenar el arreglo con respecto a bloques de longitud 8
    Lo rellena con 0´s
    @param data: Arreglo original de valores
    @return: Arreglo con el padding
    """
    return data + b"\x00"*(8-len(data)%8)


def convert_to_rgb(data):
    """
    Funcion que permite convertir los valores de bytes a componentes RGB
    @param data: Arreglo de valores en bytes
    @return pixels: Arreglo de tuplas RGB
    """
    r, g, b = tuple(
        map(lambda d: [data[i] for i in range(0, len(data)) if i % 3 == d], [0, 1, 2]))
    pixels = tuple(zip(r, g, b))
    return pixels

def _ecb_mode(image_bytes, key_bytes, iv_bytes, mode):
    """
    Modo de operacion ECB
    @param image_bytes: Arreglo de bytes de la imagen ya con el padding
    @param key_bytes: Valor de la llave en bytes
    @param iv_bytes: Valor del vector de inicializacion en bytes
    @param mode: Cifrado o Descifrado
    """
    # Creamos un nuevo elemento de DES, con el modo de operacion indicado y pasamos la llave y VI
    cipher = DES3.new(key_bytes, DES3.MODE_ECB)#, iv_bytes)
    # Regresamos el arreglo de valores cifrados o descifrados
    return cipher.encrypt(image_bytes) if mode == 0 else cipher.decrypt(image_bytes)

def _cbc_mode(image_bytes, key_bytes, iv_bytes, mode):
    """
    Modo de operacion CBC
    @param image_bytes: Arreglo de bytes de la imagen ya con el padding
    @param key_bytes: Valor de la llave en bytes
    @param iv_bytes: Valor del vector de inicializacion en bytes
    @param mode: Cifrado o Descifrado
    """
    # Creamos un nuevo elemento de DES, con el modo de operacion indicado y pasamos la llave y VI
    cipher = DES3.new(key_bytes, DES3.MODE_CBC, iv_bytes)
    # Regresamos el arreglo de valores cifrados o descifrados
    return cipher.encrypt(image_bytes) if mode == 0 else cipher.decrypt(image_bytes)


def _cfb_mode(image_bytes, key_bytes, iv_bytes, mode):
    """
    Modo de operacion CBC
    @param image_bytes: Arreglo de bytes de la imagen ya con el padding
    @param key_bytes: Valor de la llave en bytes
    @param iv_bytes: Valor del vector de inicializacion en bytes
    @param mode: Cifrado o Descifrado
    """
    # Creamos un nuevo elemento de DES, con el modo de operacion indicado y pasamos la llave y VI
    cipher = DES3.new(key_bytes, DES3.MODE_CFB, iv_bytes)
    # Regresamos el arreglo de valores cifrados o descifrados
    return cipher.encrypt(image_bytes) if mode == 0 else cipher.decrypt(image_bytes)


def _ofb_mode(image_bytes, key_bytes, iv_bytes, mode):
    """
    Modo de operacion CBC
    @param image_bytes: Arreglo de bytes de la imagen ya con el padding
    @param key_bytes: Valor de la llave en bytes
    @param iv_bytes: Valor del vector de inicializacion en bytes
    @param mode: Cifrado o Descifrado
    """
    # Creamos un nuevo elemento de DES, con el modo de operacion indicado y pasamos la llave y VI
    cipher = DES3.new(key_bytes, DES3.MODE_OFB, iv_bytes)
    # Regresamos el arreglo de valores cifrados o descifrados
    return cipher.encrypt(image_bytes) if mode == 0 else cipher.decrypt(image_bytes)
