import os
import string
import itertools

from freq_analysis import eng_freq_match_score

english_alphabet = list(string.ascii_lowercase)
alphabet_len = len(english_alphabet)
error_msg = "Por favor seleccione una opción válida"
NUM_MOST_FREQ_LETTERS = 4
MAX_KEY_LENGTH = 16 

def mcd(a, b):
    r = a % b if b != 0 else a
    return b if r == 0 else mcd(b, r)

def get_item_at_idx_one(x):
    return x[1]

def read_file():
    while True:
        path = input("Introduce la ruta del archivo a utilizar: ")
        if not os.path.isfile(path):
            print("No se ha encontrado el archivo en la ruta especificada")

        file = open(path, "r", encoding="utf-8")
        plain_text= file.read()
        file.close()
        return plain_text

# Cifrar texto
def cipher_message(key, plain_text):
    """
    Funcion que permite cifrar un texto
    @param key: Valor de la llave
    @plain_text: Texto que se va a cifrar
    @return: Cadena de texto cifrado
    """
    key = key.lower() # Se convierten los caracteres de llave a minusculas
    plain_text = plain_text.lower() #Igual los del texto
    text_indexes = [english_alphabet.index(x) for x in plain_text if x in english_alphabet] # Se buscan los indices de los caracteres del texto
    key_indexes = [english_alphabet.index(x) for x in key if x in english_alphabet] # Se buscan los indices de los caracteres de la llave

    # Existen 2 casos, cuando la llave es de menor tamaño y cuando es de mayor tamaño que el texto
    if len(key_indexes) < len(text_indexes): # Llave menor que el texto
        # Se acompleta el arreglo de indices de la llave, repitiendo los valores hasta llegar a la longitud deseada
        key_indexes = [key_indexes[i % len(key_indexes)] for i in range(len(text_indexes))] 
    elif len(key_indexes) > len(text_indexes): # Llave mayor que texto
        #Utilizar solo los caracteres de la longitud del texto
        key_indexes = key_indexes[0:len(text_indexes)]

    # Se suman los valores en ambos arreglos, posicion con posicion y se obtiene el modulo tamaño_alfabeto, para obtener la nueva posicion de las letras
    new_indexes = [(x+y) % alphabet_len for (x, y) in zip(text_indexes, key_indexes)] #Zip permite iterrar sobre 2 arreglos o listas al mismo tiempo

    # Buscamos en el alfabeto los caracteres en las nuevas posiciones y lo regresamos como una cadena
    # Esta cadena es el texto cifrado
    cipher_text = "".join([english_alphabet[x].upper() for x in new_indexes])
    return cipher_text

#Descifrar texto
def uncipher_message(key, c_text):
    """
    Funcion que permite descifrar un texto, dada la llave con la que fue cifrado
    @param key: Llave con la que ha sido cifrado el texto
    @param c_text: Texto cifrado
    @return: Cadena que corresponde al texto plano
    """
    key = key.lower() # Convertimos los caracteres de la llave a minusculas
    c_text = c_text.lower() #C Convertimos los caracteres del texto a minusculas
    translated = []  # Arreglo para los caracteres descifrados
    key_index = 0 # Indice actual 
    for symbol in c_text:  # Iterar sobre cada caracter en el texto cifrado
        if symbol in english_alphabet: # Buscamos el simbolo en el alfabeto (Solo letras, los demas caracteres son ignorados)
            num = english_alphabet.index(symbol) # Obtenemos el indice de la coincidencia
            if num != -1: # Si es un indice válido
                # Se resta la posicion, ya que estamos descifrando
                num -= english_alphabet.index(key[key_index])
                num %= alphabet_len # Aplicamos el modulo
                translated.append(english_alphabet[num].upper()) # Obtenemos el caracter en el indice obtenido y lo convertimos a mayuscula
                key_index += 1 # Siguiente indice
                if key_index == len(key): # Si hemos llegado al final de la longitud de la llave, regresamos al inicio
                    key_index = 0
            else: #Entra aqui si es un signo de puntuación (o no ;-;)
                translated.append(symbol)

    # Cadena con el texto descifrado
    return ''.join(translated)

#### De aqui para abajo esta una version experimental de la implementacion del metodo kasiski
# Y una version de consola para este mismo programa

def find_repeat_sequences_spacings(c_text):
    seq_spacings = {}
    for seq_len in range(3, 6):
        for seq_start in range(len(c_text) - seq_len):            
            seq = c_text[seq_start:seq_start + seq_len]
            for i in range(seq_start + seq_len, len(c_text) - seq_len):
                if c_text[i:i + seq_len] == seq:
                    # Se ha encontrado una cadena repetida
                    if seq not in seq_spacings:
                        seq_spacings[seq] = []

                    # Agregamos el valor de la distancia entre los valores repetidos
                    seq_spacings[seq].append(i - seq_start)
    return seq_spacings

def get_factors(num):
    # Regresa la lista de factores utiles
    if num < 2:
        return []  # Numeros menores a 2 no tienen factores utiles

    factors = [] 

    # Validamos que sean mayores a la longitud de la llave
    for i in range(2, MAX_KEY_LENGTH + 1): 
        if num % i == 0:
            factors.append(i)
            factors.append(int(num / i))
    if 1 in factors:
        factors.remove(1)
    return list(set(factors))

def get_common_factors(seq_factors):
    # Obtenemos las veces que un factor se repite
    factor_counts = {}  # La llave es el factor, el valor es cuantas coincidencias tiene

    for seq in seq_factors:
        factor_list = seq_factors[seq]
        for factor in factor_list:
            if factor not in factor_counts:
                factor_counts[factor] = 0
            factor_counts[factor] += 1

    # Agregamos estos factores a una lista para poderlos ordenar y eliminar los duplicados
    factors_by_count = []
    for factor in factor_counts:
        if factor <= MAX_KEY_LENGTH: # Solo los factores que sean menores al tamaño maximo de la clave
            factors_by_count.append((factor, factor_counts[factor]))

    # Ordenamos la lista de tuplas
    factors_by_count.sort(key=get_item_at_idx_one, reverse=True)

    return factors_by_count

def kasiski_examination(c_text):
    repeated_seq_spacings = find_repeat_sequences_spacings(c_text)
    seq_factors = {}
    for seq in repeated_seq_spacings:
        seq_factors[seq] = []
        for spacing in repeated_seq_spacings[seq]:
            seq_factors[seq].extend(get_factors(spacing))

    factors_by_count = get_common_factors(seq_factors)
    key_lengths = []
    for tp in factors_by_count:
        key_lengths.append(tp[0])

    return key_lengths

def get_subkeys_letters(n, length, c_text):
    i = n - 1
    letters = []
    while i < len(c_text):
        letters.append(c_text[i])
        i += length
    return ''.join(letters)

def try_with_key_length(c_text, key_length):
    # Determinar las letras posibles en la llave
    all_freq_scores = []
    for nth in range(1, key_length + 1):
        subkeys_letters = get_subkeys_letters(nth, key_length, c_text)

        freq_scores = []
        for possible_key in english_alphabet:
            plain_text = uncipher_message(possible_key, subkeys_letters)            
            key_freq_tuple = (possible_key, eng_freq_match_score(plain_text))
            freq_scores.append(key_freq_tuple)
        
        # Ordenamos por indice de coincidencia
        freq_scores.sort(key=get_item_at_idx_one, reverse=True)

        all_freq_scores.append(freq_scores[:NUM_MOST_FREQ_LETTERS])

    # Se prueba cada posible combinacion de letras por cada posicion
    for indexes in itertools.product(range(NUM_MOST_FREQ_LETTERS), repeat=key_length):
        # Se crea una posible llave
        possible_key = ''
        for i in range(key_length):
            possible_key += all_freq_scores[i][indexes[i]][0]

        plain_text = uncipher_message(possible_key, c_text)

        return plain_text, possible_key

    # No English-looking decryption found, so return None.
    return None

def uncipher_text(c_text):
    has_key = True
    bulk_to_file = False
    key_resp = input("Introduzca la clave: (blanco si desea recuperar la clave): ").lower()
    has_key = len(key_resp) != 0
    b_to_file_resp = input("¿Desea guardar la salida en un archivo? s/n: ").lower()
    bulk_to_file = b_to_file_resp == "s"

    plain_msg, key = None, None

    posible_texts = []

    if not has_key:
        probably_key_lengths = kasiski_examination(c_text)
        probably_key_lengths.sort()
        print(f"Posibles longitudes de llaves: {probably_key_lengths}")
        for key_length in probably_key_lengths:
            plain_msg, key = try_with_key_length(c_text, key_length)
            if plain_msg != None:
                posible_texts.append((key, plain_msg))

        if len(posible_texts) == 0:
            print("No hubo ninuna coincidencia por examinacion de kasiski, probando ataque de fuerza bruta...")
            #No encontró ninguna posible clave, realizando atque de fuerza bruta
            for key_len in range(1, MAX_KEY_LENGTH + 1):
                if key_len not in probably_key_lengths:
                    plain_msg, key = try_with_key_length(c_text, key_len)
                    if plain_msg != None:
                        posible_texts.append((key, plain_msg))

        print("Posibles valores:")
        for poss in posible_texts:
            print(f"Clave: {poss[0]}")
            print(f"Texto: {poss[1]}")
            if bulk_to_file:
                with open(f"temp_p_{poss[0]}.txt", "w") as f:
                    f.write(poss[1])

    else:
        plain_msg = uncipher_message(key_resp, c_text)
        print(f"Mensaje: {plain_msg}")
        if bulk_to_file:
            with open(f"temp_p.txt", "w") as f:
                f.write(plain_msg)

def cipher_text(plain_text):
    bulk_to_file = False
    key = input("Introduce la clave de cifrado: ")
    b_to_file_resp = input(
        "¿Desea guardar la salida en un archivo? s/n: ").lower()
    bulk_to_file = b_to_file_resp == "s"

    cipher_text = cipher_message(key, plain_text)

    print(f"Texto cifrado: {cipher_text}")

    if bulk_to_file:
        print("Guardando en un archivo...")

        with open("temp_c.txt", "w") as f:
            f.write(cipher_text)

def cipher_menu():
    c_opc = 0
    while c_opc != 3:
        print("=== Menu de cifrado ===")
        print("1. Cifrar texto simple")
        print("2. Leer texto de un archivo")
        print("3. Regresar")
        c_opc = int(input("Selecciona una opcion: "))
        if c_opc == 1:
            plain_text = input("Introduce el texto: ")
            cipher_text(plain_text.lower())
        elif c_opc == 2:
            plain_text = read_file()
            cipher_text(plain_text.lower())
        elif c_opc == 3:
            break
        else:
            print(error_msg)

def uncipher_menu():
    uc_opc = 0
    while uc_opc != 3:
        print("=== Menu de descifrado ===")
        print("1. Descifrar texto simple")
        print("2. Descifrar un archivo de texto")
        print("3. Regresar")
        uc_opc = int(input("Selecciona una opcion: "))
        if uc_opc == 1:
            c_text = input("Introduce el texto: ")
            uncipher_text(c_text.lower())
        elif uc_opc == 2:
            c_text = read_file()
            uncipher_text(c_text.lower())
        elif uc_opc == 3:
            break
        else:
            print(error_msg)

def menu():
    opc = 0
    while opc != 3:
        print("=== Menu principal ===")
        print("1. Cifrar texto")
        print("2. Descifrar texto")
        print("3. Salir")
        opc = int(input("Selecciona una opción: "))
        if opc == 1:
            cipher_menu()
        elif opc == 2:
            uncipher_menu()
        elif opc == 3:
            break;
        else:
            print(error_msg)


if __name__ == "__main__":
    menu()