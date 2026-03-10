import sys

"""Calcula el inverso multiplicativo"""
def calcula_inverso(a, n = 256):
    for x in range(n):
        if (a * x) % n == 1:
            return x
            
    return None


"""Aplicar el descifrado o cifrado César"""
def procesar_cesar(datos, llave, modo = 'descifrar'):
    if modo == 'descifrar':
        return bytes([(b - llave) % 256 for b in datos])
        
    return bytes([(b + llave) % 256 for b in datos])


"""Aplicar el descifrado o cifrado Decimado. 'alfa' debe ser coprimo con 256"""
def procesar_decimado(datos, alfa, modo = 'descifrar'):
    lista_temporal = []
    # Obtenemos el inverso multiplicativo.
    inverso = calcula_inverso(alfa) 
    
    if inverso is None:
        # (gcd(alfa,256) debe ser 1)
        raise Exception("Error: alfa no tiene inverso módulo 256.")
        
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


"""Aplicar el descifrado o cifrado Afin"""
def procesar_afin(datos, alfa, beta, modo = 'descifrar'):
    # Lista vacia para guardar los bytes procesados
    lista_resultado = []
    # Obtenemos el inverso de alfa para poder descifrar
    inverso = calcula_inverso(alfa)

    # Detenemos el programa si alfa no tiene inverso modulo 256
    if inverso is None:
        # Usamos Exception genérica como pediste
        raise Exception("Error: alfa no tiene inverso módulo 256.")

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


"""Codifica o decodifica datos en Base64"""
def procesar_base64(datos, modo = 'cifrar'):
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    
    if modo == 'cifrar':
    
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
            
        # El fin...
        return resultado_texto.encode()
        
        
    else:  # descifrar

        texto =  datos.decode("ascii")
        # No estaría mal limpiar los saltos de línea y regresos en la misma antes de procesar.
        texto = texto.replace("\n", "").replace("\r", "").rstrip("=")
        cadena_binaria_total = ""

        for c in texto:
            valor = chars.index(c)
            binario_6 = bin(valor)[2:]
            while len(binario_6) < 6:
                binario_6 = "0" + binario_6

            cadena_binaria_total += binario_6

        resultado_bytes = []
        indice = 0

        while indice + 8 <= len(cadena_binaria_total):
            bloque_8 = cadena_binaria_total[indice:indice+8]
            valor = int(bloque_8, 2)
            resultado_bytes.append(valor)
            indice += 8

        return bytes(resultado_bytes)


"""Donde la magia ocurre..."""
def main():

    if len(sys.argv) < 4:
        print("Uso: python descifrador.py <modo: cifrar/descifrar> <algoritmo> <archivo> [llaves]")
        print("Algoritmos: cesar, decimado, afin, base64")
        return

    modo = sys.argv[1]
    algo = sys.argv[2]
    ruta = sys.argv[3]
    
    if modo not in ["cifrar", "descifrar"]:
        raise Exception("Modo inválido. Usa 'cifrar' o 'descifrar'.")

    try:
        with open(ruta, "rb") as f:
            contenido = f.read()

        if algo == "cesar":
            if len(sys.argv) < 5:
                raise Exception("Falta la llave para César.")
            beta = int(sys.argv[4])
            resultado = procesar_cesar(contenido, beta, modo)
            
        elif algo == "decimado":
            if len(sys.argv) < 5:
                raise Exception("Falta alpha.")
            alpha = int(sys.argv[4])
            resultado = procesar_decimado(contenido, alpha, modo)
            
        elif algo == "afin":
            if len(sys.argv) < 6:
                raise Exception("Faltan alpha y beta.")
            alpha = int(sys.argv[4])
            beta = int(sys.argv[5])
            resultado = procesar_afin(contenido, alpha, beta, modo)
            
        elif algo == "base64":
            resultado = procesar_base64(contenido, modo)
            
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
