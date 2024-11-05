def convertir_a_clausula_horn(oracion):
    # Separar la oración en fragmentos usando " y "
    fragmentos = oracion.split(" y ")
    
    # Crear una lista para los fragmentos negados excepto el último
    clausula_horn = [
        f"no {fragmento.strip()}" if not fragmento.strip().startswith("no ") else fragmento.strip()
        for fragmento in fragmentos[:-1]
    ]
    
    # Agregar el último fragmento sin negación
    ultimo_fragmento = fragmentos[-1].strip()
    clausula_horn.append(ultimo_fragmento[3:] if ultimo_fragmento.startswith("no ") else ultimo_fragmento)

    # Unir los fragmentos con " o "
    return " o ".join(clausula_horn)

def procesar_archivo():
    # Leer el archivo de entrada
    try:
        with open("Reglas.txt", 'r', encoding='utf-8') as archivo_entrada:
            oraciones = [linea.strip() for linea in archivo_entrada if linea.strip()]
    except FileNotFoundError:
        print("Error: El archivo oraciones.txt no fue encontrado.")
        return

    # Procesar y guardar en el archivo de salida
    with open("oraciones_horn.txt", 'w', encoding='utf-8') as archivo_salida:
        for idx, oracion in enumerate(oraciones, start=1):
            # Convertir a cláusula de Horn
            oracion_horn = convertir_a_clausula_horn(oracion)
            
            # Imprimir la oración original y convertida con nuevo formato
            print(f"[Oración {idx}]")
            print(f" - Original: {oracion}")
            print(f" - Convertida: {oracion_horn}\n")

            # Guardar en el archivo de salida con encabezado y separación entre oraciones
            archivo_salida.write(f"Oración {idx}:\n")
            archivo_salida.write(f"Original: {oracion}\n")
            archivo_salida.write(f"Convertida a cláusula de Horn: {oracion_horn}\n\n")

    print("Todas las conversiones se han guardado en el archivo oraciones_horn.txt.")

# Ejecutar el proceso
procesar_archivo()

