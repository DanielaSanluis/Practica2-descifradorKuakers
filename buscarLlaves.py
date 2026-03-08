import sys
import os
import descifrador


# Carpeta donde se guardará todo
OUTPUT_DIR = "resultados_descifrado"


def preparar_directorio():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)


def guardar_resultado(nombre_archivo, algoritmo, llave_info, datos):
    nombre = f"{nombre_archivo}_{algoritmo}_{llave_info}.bin"
    ruta = os.path.join(OUTPUT_DIR, nombre)

    with open(ruta, "wb") as f:
        f.write(datos)


def verificar_firma(datos):

    # -------- Imagen --------

    # PNG : 89 50 4E 47 0D 0A 1A 0A
    if datos.startswith(bytes.fromhex("89504E470D0A1A0A")):
        return True

    # JPG : FF D8 FF + [DB | EE | E1]
    if len(datos) >= 4 and datos[0:3] == bytes.fromhex("FFD8FF") and datos[3] in [0xDB,0xEE,0xE1]:
        return True

    # BMP : 42 4D
    if datos.startswith(bytes.fromhex("424D")):
        return True


    # -------- Audio --------

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


    # -------- Video --------

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

     # -------- Documento --------

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


def buscar_cesar(datos, nombre_archivo):

    print("Buscando llaves para César...")

    for llave in range(256):

        resultado = descifrador.procesar_cesar(datos, llave, "descifrar")

        guardar_resultado(nombre_archivo, "cesar", f"key{llave}", resultado)

        if verificar_firma(resultado):
            print("Firma detectada con llave:", llave)


def buscar_decimado(datos, nombre_archivo):

    print("Buscando llaves para Decimado...")

    for alpha in range(1, 256):

        try:
            resultado = descifrador.procesar_decimado(datos, alpha, "descifrar")

            guardar_resultado(nombre_archivo, "decimado", f"alpha{alpha}", resultado)

            if verificar_firma(resultado):
                print("Firma detectada con alpha:", alpha)

        except:
            pass


def buscar_afin(datos, nombre_archivo):

    print("Buscando llaves para Afín...")
    inicio =  141
    for alpha in range(23, 256):

        for beta in range(inicio, 256):

            try:
                resultado = descifrador.procesar_afin(datos, alpha, beta, "descifrar")

                guardar_resultado(
                    nombre_archivo,
                    "afin",
                    f"alpha{alpha}_beta{beta}",
                    resultado
                )

                if verificar_firma(resultado):
                    print("Firma detectada con alpha:", alpha, "beta:", beta)

            except:
                pass
        inicio = 0


def main():

    preparar_directorio()

    #archivos = ["file1.lol", "file2.lol", "file3.lol", "file4.lol"]
    # archivos = [ "file2.lol", "file3.lol", "file4.lol"]
    archivos = [  "file3.lol"]
    #algoritmos = ["cesar", "decimado", "afin"]
    algoritmos = ["afin"]
    for archivo in archivos:

        print("\n============================")
        print("Probando archivo:", archivo)
        print("============================")

        with open(archivo, "rb") as f:
            datos = f.read()

        nombre_base = os.path.splitext(os.path.basename(archivo))[0]

        for algoritmo in algoritmos:

            print("\nProbando algoritmo:", algoritmo)
           # if algoritmo == "cesar":
            #    buscar_cesar(datos, nombre_base)

           # if algoritmo == "decimado":
               # buscar_decimado(datos, nombre_base)

            if algoritmo == "afin":
                buscar_afin(datos, nombre_base)


if __name__ == "__main__":
    main()

