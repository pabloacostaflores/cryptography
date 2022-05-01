import os
from cipher import pad, convert_to_rgb, _ecb_mode, _cbc_mode, _cfb_mode, _ofb_mode
from PIL import Image

def process_image(filename):
    """
    Funcion que permite procesar de manera mas rapida la imagen solicitada
    @param filename: Ruta completa o relativa del archivo a procesar
    @return im: Imagen PIL
    @return data: Arreglo de bytes de los valores RGB de la imagen
    @return file_name: Nombre del archivo utilizado
    """
    im = Image.open(filename)
    image_parts = filename.split("/")
    file_name = image_parts[len(image_parts)-1]
    file_name = file_name.split(".")[0]
    data = im.convert("RGB").tobytes()
    return im, data, file_name

def begin_proc(op, op_mode, key, iv, file_path ):
    """
    Funcion general que comienza con el proceso de parametros y cifrado/descifrado
    @param op: Entero que representa el modo a trabajar (1 cifrado, 2 descifrado)
    @para op_mode: Modo de operacion (ECB, CBC, CFB, OFB)
    @para key: Llave a utilizar
    @para iv: Vector de inicializacion
    @para file_path: Ruta del archivo a trabajar
    """
    
    im, image_data, file_name = process_image(file_path) # Procesamos la imagen
    #Obtenemos la longitud original de los datos (arreglo) para poder eliminar el padding que agregamos
    original = len(image_data) 
    padded_img = pad(image_data) #Rellenamos con 0´s
    # Solicitamos en modo de operacion, pasamos los bytes con el padding, la llave y el VI en bytes
    # De ello, obtenemos los valores hasta la longitud original, para eliminar el padding
    # Al final, convertimos estos bytes a RGB para poder escribirlo en un archivo
    if op_mode == 0:
        mode_op = "ECB"
        cf_img = convert_to_rgb(_ecb_mode(
            padded_img, key.encode(), ("a"*16).encode(), op)[:original])
    elif op_mode == 1:
        mode_op = "CBC"
        cf_img = convert_to_rgb(_cbc_mode(padded_img, key.encode(), iv.encode(), op)[:original])
    elif op_mode == 2:
        mode_op = "CFB"
        cf_img = convert_to_rgb(_cfb_mode(padded_img, key.encode(), iv.encode(), op)[:original])
    elif op_mode == 3:
        mode_op = "OFB"
        cf_img = convert_to_rgb(_ofb_mode(padded_img, key.encode(), iv.encode(), op)[:original])

    # Creamos una nueva imagen, la cual va a ser de la misma dimension que la original
    converted_img = Image.new(im.mode, im.size)
    # Escribimos los valores RGB obtenidos
    converted_img.putdata(cf_img)
    # Guardamos con el nombre original + e/d + modo . bmp
    converted_img.save(f"{file_name}_{'d' if op == 1 else 'e'}{mode_op}.bmp")
    print("Finished")
    return True


if __name__ == "__main__":
    print("Operacion")
    print("1) Cifrar")
    print("2) Descifrar")
    op = int(input("Selecciona una operacion: "))

    print("Modo de operacion")
    print("1) ECB")
    print("2) CBC")
    print("3) CFB")
    print("4) OFB")
    op_mode = int(input("Selecciona un modo de operación: "))
    file_path = input("Introduce la ruta del archivo: ")
    if not os.path.isfile(file_path):
        # Si no encontramos el archivo, mostramos un mensaje de alerta y cerramos
        print("No se ha encontrado el archivo")
        exit(0)

    # Llave de 16 caracteres
    key = input("Introduce la llave (16 caracteres): ")
    # Buclamos por si no es una longitud valida
    while len(key) != 16:
        key = input("Introduce la llave (16 caracteres): ")
    # Mientras no sea ECB, pedimos el vector de inicializacion
    if op_mode != 1:
        iv = input("Introduce el vector de inicializacion (8 caracteres): ")
        while len(iv) != 8:
            key = input("Introduce la llave (8 caracteres): ")

    begin_proc(op - 1, op_mode - 1, key, iv, file_path)
    