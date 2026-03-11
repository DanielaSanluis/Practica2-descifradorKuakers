# Práctica 2: Cifrados Clásicos

Este directorio contiene los scripts desarrollados para aplicar cifrados clásicos (César, Decimado, Afín), codificación Base64, y un script de criptoanálisis por fuerza bruta basado en la detección de Magic Bytes.

## Archivos Principales
* `descifrador.py`: Herramienta manual para cifrar/descifrar a nivel de bytes.
* `buscarLlaves.py`: Script automatizado para romper cifrados por fuerza bruta.

## Instrucciones de Uso

### 1. Uso manual (descifrador.py)
Permite cifrar o descifrar archivos individualmente. 
**Sintaxis general:**
`python descifrador.py <cifrar|descifrar> <algoritmo> <archivo> [llaves]`

**Ejemplos de ejecución:**
* **César:** `python descifrador.py descifrar cesar file1.lol 77`
* **Afín:** `python descifrador.py descifrar afin file3.lol 99 99`
* **Base64:** `python descifrador.py descifrar base64 file4.lol`

### 2. Criptoanálisis por Fuerza Bruta (buscarLlaves.py)
Automatiza la búsqueda de llaves iterando todas las combinaciones matemáticas posibles y verificando las firmas de los archivos resultantes.

**Para ejecutarlo:**
1. Asegúrate de que los archivos a procesar (`file1.lol`, `file2.lol`, etc.) estén en el mismo directorio que los scripts.
2. Ejecuta en la terminal: `python buscarLlaves.py`
3. El script se detendrá automáticamente al encontrar la llave correcta y guardará el archivo recuperado en una subcarpeta llamada `resultados_descifrado/`.
