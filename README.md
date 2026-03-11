# Práctica 2: Cifrados Clásicos

## Archivos Principales
* `descifrador.py`: Herramienta manual para cifrar/descifrar a nivel de bytes.
* `buscarLlaves.py`: Script automatizado para romper cifrados por fuerza bruta.

## Instrucciones de Uso

### 1. Uso manual - descifrador.py
Este nos permite cifrar o descifrar archivos individualmente. 

**Sintaxis general:**
`python descifrador.py <cifrar|descifrar> <algoritmo> <archivo> [llaves]`

**Ejemplos de ejecución:**
* **César:** `python descifrador.py descifrar cesar file1.lol 77`
* **Afín:** `python descifrador.py descifrar afin file3.lol 99 99`
* **Base64:** `python descifrador.py descifrar base64 file4.lol`

### 2. Fuerza Bruta - buscarLlaves.py
Automatizamos la búsqueda de llaves iterando en todas las combinaciones matemáticas posibles y verificando las firmas de los archivos resultantes.

**Pasos a seguir:**
1. Asegurarse de que los archivos a procesar estén en el mismo directorio que los scripts.
2. Ejecutar en la terminal: `python buscarLlaves.py`
3. El script se detendrá automáticamente al encontrar la llave correcta y guardará el archivo recuperado en una carpeta llamada `resultados_descifrado/`.
