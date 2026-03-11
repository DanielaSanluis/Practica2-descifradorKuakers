from math import gcd
import os
import descifrador

# Carpeta donde se guardará todo
OUTPUT_DIR = "resultados_descifrado"
# Como 256 es una potencia de 2, los números coprimos con 256 son exactamente los números impares entre 1 y 255.
COPRIMOS = list(range(1, 256, 2))     
# Lista de archivos a procesar y sus algoritmos correspondientes (si se quiere probar solo una llave específica por algoritmo)
ARCHIVOS = ["file1.lol", "file2.lol", "file3.lol", "file4.lol"]
ALGORITMOS = ["cesar", "decimado", "afin", "base64"]


def preparar_directorio():
    """
    Prepara el directorio de salida para guardar los resultados del descifrado.
    Si el directorio no existe, lo crea.
    """
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)


def guardar_resultado(nombre_archivo, algoritmo, llave_info, datos):
    """
    Guarda el resultado del descifrado en un archivo dentro del directorio de salida.
    Args:
    nombre_archivo (str): El nombre base del archivo original sin extensión.
    algoritmo (str): El nombre del algoritmo utilizado para el descifrado.
    llave_info (str): Información sobre la llave utilizada.
    datos (bytes): Los datos descifrados que se desean guardar en el archivo.
    """
    nombre = f"{nombre_archivo}_{algoritmo}_{llave_info}.bin"
    ruta = os.path.join(OUTPUT_DIR, nombre)

    with open(ruta, "wb") as f:
        f.write(datos)

def imagen(datos):
    """
    Verifica si los datos descifrados contienen una firma de formato de archivo de imagen común (PNG, JPG, BMP).
    Args:
        datos (bytes): Los datos descifrados que se desean verificar.
    Returns:
        bool: True si se detecta una firma de formato de archivo de imagen común, False en caso contrario.
    """
    # PNG : 89 50 4E 47 0D 0A 1A 0A
    if datos.startswith(bytes.fromhex("89504E470D0A1A0A")):
        return True
    # JPG : FF D8 FF + [DB | EE | E1]
    if len(datos) >= 4 and datos[0:3] == bytes.fromhex("FFD8FF") and datos[3] in [0xDB,0xEE,0xE1]:
        return True
    # BMP : 42 4D
    if datos.startswith(bytes.fromhex("424D")):
        return True
    return False

def audio(datos):
    """
    Verifica si los datos descifrados contienen una firma de formato de archivo de audio común (MP3, WAV, OGG).
    Args:
        datos (bytes): Los datos descifrados que se desean verificar.
    Returns:
        bool: True si se detecta una firma de formato de archivo de audio común, False en otro caso.
    """
    # MP3 : FF FB, FF F3, FF F2, 49 44 33
    if datos.startswith(bytes.fromhex("FFFB")):
        return True
    if datos.startswith(bytes.fromhex("FFF3")):
        return True
    if datos.startswith(bytes.fromhex("FFF2")):
        return True
    if datos.startswith(bytes.fromhex("494433")):
        return True
    # WAV : 52 49 46 46 ?? ?? ?? ?? 57 41 56 45
    if len(datos) >= 12 and datos[0:4] == bytes.fromhex("52494646") and datos[8:12] == bytes.fromhex("57415645"):
        return True
    # OGG : 4F 67 67 53
    if datos.startswith(bytes.fromhex("4F676753")):
        return True
    return False

def video(datos):
    """
    Verifica si los datos descifrados contienen una firma de formato de archivo de video común (MP4, AVI, MKV).
    Args:
        datos (bytes): Los datos descifrados que se desean verificar.
    Returns:
        bool: True si se detecta una firma de formato de archivo de video común, False en otro caso.
    """
    # MP4 : 66 74 79 70 [ 69 73 6F 6D | 4D 53 4E 56 ]
    if len(datos) >= 12 and datos[4:8] == bytes.fromhex("66747970"):
        if datos[8:12] == bytes.fromhex("69736F6D") or datos[8:12] == bytes.fromhex("4D534E56"):
            return True
    # AVI : 52 49 46 46 ?? ?? ?? ?? 41 56 49 20
    if len(datos) >= 12 and datos[0:4] == bytes.fromhex("52494646") and datos[8:12] == bytes.fromhex("41564920"):
        return True
    # MKV : 1A 45 DF A3
    if datos.startswith(bytes.fromhex("1A45DFA3")):
        return True
    return False

def documento(datos):
    """
    Verifica si los datos descifrados contienen una firma de formato de archivo de documento común (DOCX, EPUB, PDF).
    Args:
        datos (bytes): Los datos descifrados que se desean verificar.
    Returns:
        bool: True si se detecta una firma de formato de archivo de documento común, False en otro caso.
    """
    # DOCX / EPUB
    if datos.startswith(bytes.fromhex("504B0304")):
        return True
    if datos.startswith(bytes.fromhex("504B0506")):
        return True
    if datos.startswith(bytes.fromhex("504B0708")):
        return True
    # PDF : 25 50 44 46 2D
    if datos.startswith(bytes.fromhex("255044462D")):
        return True
    return False

def verificar_firma(datos):
    """
    Verifica si los datos descifrados contienen una firma de formato de archivo común.
    Se revisan las firmas de archivos de imagen, audio, video y documentos.
    Args:
    datos (bytes): Los datos descifrados que se desean verificar.
    Returns:
    bool: True si se detecta una firma de formato de archivo común, False en caso contrario.
    """    
    return imagen(datos) or audio(datos) or video(datos) or documento(datos)


def buscar_cesar(datos, nombre_archivo, brute_force=True):
    """
    Realiza un ataque de fuerza bruta al cifrado César probando todas las posibles llaves (0-255) y guarda los resultados. 
    Args:    
        datos (bytes): Los datos a descifrar.
        nombre_archivo (str): El nombre base del archivo original sin extensión para guardar los resultados
        brute_force (bool): Si es True, se probarán todas las llaves entre 0 y 255. Si es False, se probará una llave específica.
    """

    print("Buscando llaves para César...")

    if not brute_force:
        llave = 77
        resultado = descifrador.procesar_cesar(datos, llave, "descifrar")
        guardar_resultado(nombre_archivo, "cesar", f"key{llave}", resultado)
        if verificar_firma(resultado):
            print("Firma detectada con llave:", llave)
            return True
        return False

    for llave in range(256):
        print(f"Probando llave: {llave}", end="\r")
        resultado = descifrador.procesar_cesar(datos, llave, "descifrar")
        if verificar_firma(resultado):
            guardar_resultado(nombre_archivo, "cesar", f"key{llave}", resultado)
            print("Firma detectada con llave:", llave)
            return True
    return False


def buscar_decimado(datos, nombre_archivo, brute_force=True):
    """
    Realiza un ataque de fuerza bruta al cifrado decimado probando todas las posibles llaves (números impares entre 1 y 255) y guarda los resultados.
    Args:    
        datos (bytes): Los datos a descifrar.
        nombre_archivo (str): El nombre base del archivo original sin extensión para guardar los resultados
        brute_force (bool): Si es True, se probarán todas las llaves impares entre 1 y 255. Si es False, se probará una llave específica (alfa=27).
    """

    print("Buscando llaves para Decimado...")

    if not brute_force:
        alpha = 27
        resultado = descifrador.procesar_decimado(datos, alpha, "descifrar")
        if verificar_firma(resultado):
            guardar_resultado(nombre_archivo, "decimado", f"alpha{alpha}", resultado)
            print("Firma detectada con alpha:", alpha)
            return True
        return False

    for alpha in COPRIMOS:
        try:
            print(f"Probando alpha: {alpha}", end="\r")
            resultado = descifrador.procesar_decimado(datos, alpha, "descifrar")
            if verificar_firma(resultado):
                guardar_resultado(nombre_archivo, "decimado", f"alpha{alpha}", resultado)
                print("Firma detectada con alpha:", alpha)
                return True
        except:
            pass
    return False


def buscar_afin(datos, nombre_archivo, brute_force=True):
    """
    Realiza un ataque de fuerza bruta al cifrado afín probando todas las posibles combinaciones de llaves (alfa y beta) y guarda los resultados.
    Args:    
        datos (bytes): Los datos a descifrar.
        nombre_archivo (str): El nombre base del archivo original sin extensión para guardar los resultados
        brute_force (bool): Si es True, se probarán todas las combinaciones de alfa y beta. Si es False, se probará una combinación específica de alfa=99 y beta=99.
    """
    print("Buscando llaves para Afín...")
    if not brute_force:
        alpha = 99
        beta = 99
        resultado = descifrador.procesar_afin(datos, alpha, beta, "descifrar")
        if verificar_firma(resultado):
            guardar_resultado(nombre_archivo, "afin", f"alpha{alpha}_beta{beta}", resultado)
            print("Firma detectada con alpha:", alpha, "beta:", beta)
            return True
        return False
    
    inicio =  0
    for alpha in COPRIMOS:
        for beta in range(inicio, 256):
            try:
                print(f"Probando alpha: {alpha}, beta: {beta}", end="\r")
                resultado = descifrador.procesar_afin(datos, alpha, beta, "descifrar")
                if verificar_firma(resultado):
                    guardar_resultado(
                        nombre_archivo,
                        "afin",
                        f"alpha{alpha}_beta{beta}",
                        resultado
                    )
                    print("Firma detectada con alpha:", alpha, "beta:", beta)
                    return True
            except:
                pass
        inicio = 0
    return False

def buscar_base64(datos, nombre_archivo):
    """
    Intenta descifrar los datos utilizando el algoritmo Base64 y guarda el resultado.
    Args:    
        datos (bytes): Los datos a descifrar.
        nombre_archivo (str): El nombre base del archivo original sin extensión para guardar los resultados
    """

    print("Buscando llaves para Base64...")

    resultado = descifrador.procesar_base64(datos, "descifrar")

    guardar_resultado(nombre_archivo, "base64", "", resultado)
    print("Firma detectada con Base64")
    return True

def probar_algoritmos(datos, nombre_archivo, brute_force=True):
    """
    Prueba todos los algoritmos de cifrado (César, Decimado, Afín y Base64) para descifrar los datos y guarda los resultados.
    Args:    
        datos (bytes): Los datos a descifrar.
        nombre_archivo (str): El nombre base del archivo original sin extensión para guardar los resultados
        brute_force (bool): Si es True, se probarán todas las llaves posibles para cada algoritmo. Si es False, se probará una llave específica para cada algoritmo.
    """
    if buscar_cesar(datos, nombre_archivo, brute_force):
        return
    if buscar_decimado(datos, nombre_archivo, brute_force):
        return
    if buscar_afin(datos, nombre_archivo, brute_force):
        return
    if buscar_base64(datos, nombre_archivo):
        return

def main():

    preparar_directorio()

    fuerza_bruta = False  # Cambia a False para probar las llaves especificas.


    if fuerza_bruta:
        for archivo in ARCHIVOS:
            print(f"\nProcesando {archivo}...")
            with open(archivo, "rb") as f:
                datos = f.read()
                nombre_archivo = os.path.splitext(archivo)[0]
                probar_algoritmos(datos, nombre_archivo, brute_force=True)
    else:
        for archivo, algoritmo in zip(ARCHIVOS, ALGORITMOS):
            print(f"\nProcesando {archivo} con {algoritmo}...")
            with open(archivo, "rb") as f:
                datos = f.read()
                nombre_archivo = os.path.splitext(archivo)[0]
                if algoritmo == "cesar":
                    buscar_cesar(datos, nombre_archivo, brute_force=False)
                elif algoritmo == "decimado":
                    buscar_decimado(datos, nombre_archivo, brute_force=False)
                elif algoritmo == "afin":
                    buscar_afin(datos, nombre_archivo, brute_force=False)
                elif algoritmo == "base64":
                    buscar_base64(datos, nombre_archivo)



if __name__ == "__main__":
    main()

