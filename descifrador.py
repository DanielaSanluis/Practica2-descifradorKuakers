import sys

def calcula_inverso(a, n=256):
    """Calcula el inverso """
    for x in range(1, n):
        if (a * x) % n == 1:
            return x
    return None

def procesar_cesar(datos, llave, modo='descifrar'):
    if modo == 'descifrar':
        return bytes([(b - llave) % 256 for b in datos])
    return bytes([(b + llave) % 256 for b in datos])

def procesar_decimado(datos, alfa, modo='descifrar'):
    lista_temporal = []

    # Obtenemos el inverso multiplicativo.
    inverso = calcula_inverso(alfa)

    if inverso is None:
        raise Exception("Error: El valor de alfa no tiene inverso. Debe ser un numero impar.")

    if modo == 'descifrar':
        for byte_actual in datos:
            # Multiplicamos el byte cifrado por el inverso de la llave
            operacion = byte_actual * inverso
            byte_descifrado = operacion % 256

            lista_temporal.append(byte_descifrado)
    else:
        for byte_actual in datos:
            # Multiplicamos el byte original por la llave alfa
            operacion = byte_actual * alfa
            
            # Aplicamos el modulo 256
            byte_cifrado = operacion % 256
            lista_temporal.append(byte_cifrado)

    return bytes(lista_temporal)

def procesar_afin(datos, alfa, beta, modo='descifrar'):
    # 1. Creamos una lista vacia para guardar los bytes procesados
    lista_resultado = []

    # 2. Obtenemos el inverso de alfa para poder descifrar
    inverso = calcula_inverso(alfa)

    # 3. Validacion con 'raise': Detenemos el programa si alfa no es impar
    if inverso is None:
        # Usamos Exception genérica como pediste
        raise Exception("Error: El valor de alfa no es valido (debe ser impar).")

    if modo == 'descifrar':
        for byte_cifrado in datos:
            # Primero restamos el desplazamiento (beta)
            operacion_resta = byte_cifrado - beta
            
            #Luego multiplicamos por el inverso de alfa
            operacion_multiplicacion = operacion_resta * inverso
            
            # Aplicamos modulo 256 para obtener el byte original
            byte_recuperado = operacion_multiplicacion % 256
            lista_resultado.append(byte_recuperado)
    else:
        for byte_claro in datos:
            # Multiplicamos el byte original por alfa
            operacion_multiplicacion = byte_claro * alfa
            operacion_suma = operacion_multiplicacion + beta
            
            # Aplicamos modulo 256
            byte_cifrado = operacion_suma % 256
            lista_resultado.append(byte_cifrado)
    return bytes(lista_resultado)

def base64(datos):
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    
    cadena_binaria_total = ""
    for byte in datos:
        # Convertimos el numero a binario, quitamos el prefijo '0b' 
        # y rellenamos con ceros a la izquierda hasta tener 8 bits
        binario_8_bits = bin(byte)[2:]
        while len(binario_8_bits) < 8:
            binario_8_bits = "0" + binario_8_bits
        cadena_binaria_total = cadena_binaria_total + binario_8_bits

    # Calcular el relleno (padding) necesario 
    # Base64 trabaja en grupos de 3 bytes (24 bits)
    cantidad_bytes = len(datos)
    relleno_necesario = (3 - (cantidad_bytes % 3)) % 3
    
    # Agregar ceros adicionales al final de la cadena binaria.
    # Cada simbolo Base64 representa 6 bits 
    for i in range(relleno_necesario * 2):
        cadena_binaria_total = cadena_binaria_total + "0"
    resultado_texto = ""
    indice = 0
    while indice < len(cadena_binaria_total):
        bloque_6_bits = cadena_binaria_total[indice : indice + 6]
        while len(bloque_6_bits) < 6:
            bloque_6_bits = bloque_6_bits + "0"
        valor_decimal = int(bloque_6_bits, 2)
        # Usamos el valor decimal como indice para buscar el caracter en la cadena 'chars'
        caracter_base64 = chars[valor_decimal]
        resultado_texto = resultado_texto + caracter_base64
        
        # Saltamos al siguiente bloque de 6
        indice = indice + 6

    for i in range(relleno_necesario):
        resultado_texto = resultado_texto + "=" 
    return resultado_texto

def main():
    if len(sys.argv) < 4:
        print("Uso: python descifrador.py <modo: cifrar/descifrar> <algoritmo> <archivo> [llaves]")
        print("Algoritmos: cesar, decimado, afin, base64")
        return

    modo = sys.argv[1]
    algo = sys.argv[2]
    ruta = sys.argv[3]

    try:
        with open(ruta, "rb") as f:
            contenido = f.read()

        if algo == "cesar":
            beta = int(sys.argv[4])
            resultado = procesar_cesar(contenido, beta, modo)
        elif algo == "decimado":
            alpha = int(sys.argv[4])
            resultado = procesar_decimado(contenido, alpha, modo)
        elif algo == "afin":
            alpha, beta = int(sys.argv[4]), int(sys.argv[5])
            resultado = procesar_afin(contenido, alpha, beta, modo)
        elif algo == "base64":
            resultado = base64(contenido).encode() 
        else:
            print("Algoritmo no reconocido.")
            return

        nombre_salida = f"{modo}_{ruta}"
        with open(nombre_salida, "wb") as f:
            f.write(resultado)
        print(f"Éxito. Archivo guardado como: {nombre_salida}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()