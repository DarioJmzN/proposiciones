import re
import itertools
import os
import matplotlib.pyplot as plt

# Clase Nodo, que representa un nodo en un árbol binario

class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierda = None
        self.derecha = None

# Función que toma una oración y la convierte en una fórmula lógica

def Formula(oracion):
    # Diccionario de operadores lógicos en forma de texto, se reemplazan por símbolos lógicos
    operadores = {
        " y ": "∧", 
        " o ": "∨", 
        "∧no ": "∧¬",
        "∨no ": "∨¬",
        "No ": "¬",
        " pero ": "∧", 
        " además, ": "∧", 
        " Además, ": "∧",
    }
    # Reemplazar las palabras clave por los símbolos correspondientes
  
    for conector, simbolo in operadores.items():
        oracion = oracion.replace(conector, simbolo)
        # Separar la fórmula en sus componentes
    frase = Separador(oracion)
    

    frases_vistas = {}
    contador = 1

    # Función interna para reemplazar cada sub-expresión por una variable única
    def reemplazar_por_variable(match):
        nonlocal contador
        frase = match.group(0)
        if frase in frases_vistas:
            return frases_vistas[frase]
        else:
            resultado = f"X{contador}"
            frases_vistas[frase] = resultado 
            contador += 1
            return resultado

    # Usamos expresiones regulares para identificar y reemplazar las partes de la fórmula 
    formula = re.sub(r"[^∧∨¬]+", reemplazar_por_variable, oracion)
    # Separar la fórmula y devolverla
    formula = Separador(formula)
    return formula, frase

# Función que separa la fórmula en sus componentes (operadores y literales)
def Separador(oracion):
    separacion = oracion.replace("∧", "☺∧☺")
    separacion = separacion.replace("∨", "☺∨☺")
    separacion = separacion.replace("¬", "☺¬☺")
    separacion = re.split(r"☺", separacion)
    separacion = [elemento for elemento in separacion if elemento != '']
    return separacion

# Función que reconstruye una cadena a partir de una lista de elementos
def Unir(frase):
    union = ""
    for i in range(len(frase)):
        union = union + frase[i]
    return union

# Función que genera la tabla de átomos para las proposiciones
def Tabla_Atomos(formula, frase):
    res_formula = Unir(formula)
    res_frase = Unir(frase)
    # Separamos los literales de la fórmula y la frase
    res_frase = re.split(r'[∧∨¬]', res_frase)
    res_frase = [elemento for elemento in res_frase if elemento != '']
    res_formula = re.split(r'[∧∨¬]', res_formula)
    res_formula = [elemento for elemento in res_formula if elemento != '']
    # Creamos listas de variables únicas para la fórmula y la frase
    array_var = []
    vistos = set()
    for elemento in res_formula:
        if elemento not in vistos:
            vistos.add(elemento)
            array_var.append(elemento)
    array_frase = []
    vistos2 = set()
    for elemento in res_frase:
        if elemento not in vistos2:
            vistos2.add(elemento)
            array_frase.append(elemento)
            
# Mostramos la tabla de átomos
    print("Tabla de Átomos en las proposiciones")
    print("____________________________")
    for i in range(len(array_frase)):
        print("____________________________\n")
        print(array_var[i] + ":" + array_frase[i])
        print("____________________________")
   
    return 

# Función que genera y muestra la tabla de verdad
def Tabla_Booleana(oracion):
    formula = Unir(oracion)
    print(formula)
    # Convertir la fórmula a una expresión compatible con Python
    formula_python = formula.replace("∧", " and ").replace("∨", " or ").replace("¬", " not ")
    # Extraer las variables de la fórmula
    variables = sorted(set(re.findall(r'X\d+', formula)))
    # Generar todas las combinaciones posibles de valores para las variables
    valores = [True, False]
    combinaciones = list(itertools.product(valores, repeat=len(variables)))

# Encabezado de la tabla
    encabezado = "\t".join(variables) + "\tResultado"
    print(encabezado)
    print("-" * (len(encabezado) + 1))

    # Evaluar la fórmula para cada combinación de valores
    for combinacion in combinaciones:
        contexto = dict(zip(variables, combinacion))
        try:
            resultado = eval(formula_python, {}, contexto)
        except Exception as e:
            resultado = f"Error: {e}"
        valores_str = "\t".join(str(contexto[var]) for var in variables)
        print(f"{valores_str}\t{resultado}")
    return
# Función para guardar la fórmula en un archivo de texto
def Guardar(oracion):
    formula = Unir(oracion)
    # Si el archivo no existe, lo crea
    if not os.path.exists("Reglas.txt"):
        with open("Reglas.txt", 'w', encoding='utf-8') as archivo:
            print("Archivo guardado en Reglas.txt creado en la carpeta python program proyects.")

# Añadir la fórmula al archivo
    with open("Reglas.txt", 'a', encoding='utf-8') as archivo:
        archivo.write(formula + ".\n")
        print("entregada al duende que hace andar todo esto (•̀ ω •́)✧ .")
    return  

# Función para cargar las reglas desde un archivo de texto
def Cargar():
    if os.path.exists("Reglas.txt"):
        with open("Reglas.txt", 'r', encoding='utf-8') as archivo:
            contenido = archivo.read()
            return contenido
    else:
        print("no pues pa no guardar nada mejor >:v")
        return
    
# Función para asignar valores de verdad a las variables
def Asignar(oracion):
    formula, _ = Formula(oracion)
    variables = sorted(set(re.findall(r'X\d+', Unir(formula))))
    valores_asignados = {}

    # Solicitar valores de verdad para cada variable
    print("Asignación de valores digame usted que tanto es verdadero y falso ⌐■_■ノ♪:")
    for var in variables:
        while True:
            valor = input(f"Ingrese el valor de verdad para {var} (True/False): ")
            if valor.lower() in ['true', 'false']:
                valores_asignados[var] = valor.lower() == 'true'
                break
            else:
                print("no se haga pato!. Ingrese 'True' o 'False'.")
    return valores_asignados

# Función para evaluar y mostrar el resultado de la fórmula con los valores asignados
def Ver(oracion, valores_asignados):
    formula, _ = Formula(oracion)
    formula_str = Unir(formula)

# Reemplazar las variables por sus valores de verdad asignados
    formula_evaluada = formula_str
    for var, valor in valores_asignados.items():
        formula_evaluada = formula_evaluada.replace(var, str(valor))
    
    formula_python = formula_evaluada.replace("∧", " and ").replace("∨", " or ").replace("¬", " not ")

    try:
        resultado = eval(formula_python)
    except Exception as e:
        resultado = f"Error: {e}"

    # Mostrar la expresión original, los valores asignados y el resultado final
    print("Expresión:", formula_str)
    print("Con valores asignados:", formula_evaluada)
    print("Resultado final:", resultado)
    return resultado

# Función para construir un árbol binario con las variables
def construir_arbol(variables):
    if not variables:
        return None

    lista_variables = list(variables.keys())
    raiz = Nodo(lista_variables[0])
    cola = [(raiz, 1)]

    while cola:
        padre, idx = cola.pop(0)

        if idx < len(lista_variables):
            var_actual = lista_variables[idx]

            p_nodo_true = Nodo(f"{var_actual} = True")
            p_nodo_false = Nodo(f"{var_actual} = False")

            padre.derecha = p_nodo_true
            padre.izquierda = p_nodo_false

            cola.append((p_nodo_false, idx + 1))
            cola.append((p_nodo_true, idx + 1))

    return raiz

def construir_arbol_global(reglas):
    if not reglas:
        return None

    raiz = Nodo(reglas[0])
    cola = [(raiz, 1)]

# Construcción del árbol binario, donde cada nodo tiene dos hijos: True y False
    while cola:
        padre, idx = cola.pop(0)

        if idx < len(reglas):
            regla_actual = reglas[idx]

            p_nodo_true = Nodo(f"{regla_actual} = True")
            p_nodo_false = Nodo(f"{regla_actual} = False")

            padre.derecha = p_nodo_true
            padre.izquierda = p_nodo_false

            cola.append((p_nodo_false, idx + 1))
            cola.append((p_nodo_true, idx + 1))

    return raiz

def dibujar_arbol(nodo, x=0, y=0, dx=1.5, dy=1, ax=None, nivel=0, max_nivel=5):
    if nodo is None or nivel > max_nivel:
        return

    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.axis('off')

    ax.text(x, y, nodo.valor, ha='center', va='center', bbox=dict(boxstyle="round,pad=0.3", fc="lightblue", ec="black", lw=1))

    if nodo.izquierda:
        ax.plot([x, x - dx], [y, y - dy], 'k-')
        dibujar_arbol(nodo.izquierda, x - dx, y - dy, dx * 0.6, dy, ax, nivel + 1, max_nivel)

    if nodo.derecha:
        ax.plot([x, x + dx], [y, y - dy], 'k-')
        dibujar_arbol(nodo.derecha, x + dx, y - dy, dx * 0.6, dy, ax, nivel + 1, max_nivel)

    if nivel == 0:
        plt.show()

# Función para dibujar un árbol binario
def Arbol_binario(oracion):
    formula, _ = Formula(oracion)
    variables = sorted(set(re.findall(r'X\d+', Unir(formula))))
    variables_asignadas = {var: False for var in variables}
    
    print(f"Dibujando, produciendo, modelando, estructurando y diseñando árbol binario para la fórmula que se vea bien prrona: {Unir(formula)}")
    raiz = construir_arbol(variables_asignadas)
    dibujar_arbol(raiz)

def Arbol_binario_global():
    reglas_texto = Cargar()
    if reglas_texto:
        reglas = [linea.strip()[:-1] for linea in reglas_texto.splitlines() if linea.strip()]  # Quitar el punto final
        print("Construyendo el árbol binario mas cool del mundo global con las reglas:")
        for regla in reglas:
            print(f"Regla: {regla}")

        raiz_global = construir_arbol_global(reglas)
        dibujar_arbol(raiz_global)
    else:
        print("te falto la regla papito.")



# Mostrar el menú de opciones para el usuario
def Menu():
    print("\n" + "=" * 60)
    print("        MENÚ PRINCIPAL")
    print("=" * 60)
    print("🔹 " + "1.- Introducir una frase para obtener la fórmula .")
    print("🔹 " + "2.- Mostrar tabla de átomos.")
    print("🔹 " + "3.- Mostrar tabla de verdad.")
    print("🔹 " + "4.- Guardar regla.")
    print("🔹 " + "5.- Cargar regla.")
    print("🔹 " + "6.- Asignar valores de verdad.")
    print("🔹 " + "7.- Ver resultados.")
    print("🔹 " + "8.- Dibujar árbol binario.")
    print("🔹 " + "9.- Dibujar árbol binario global.")
    #print("🔹 " + "10.- Convertir las reglas a cláusulas de Horn")
    print("🔹 " + "11.- Salir.")
    print("═" * 60)

# Solicitar al usuario que elija una opción
    opcion = input("Elija una opción: ")
    return opcion

print("\n" + "=" * 60)
print("    Mi proyecto altamente reprobable de sistemas expertos ")
print("=" * 60)
cont=0
while True:
    # Mostrar el menú y capturar la opción elegida por el usuario
    opcion = Menu()
    
    if opcion == "1":
        oracion = input("Ingresa la frase \n")
        formula, frase = Formula(oracion)
        formula = Unir(formula)
        cont += 1
        print('El resultado es: ', formula + '\n')
    elif opcion == "2":
        if cont > 0:
            Tabla_Atomos(formula, frase)
        else:
            print('Crea una fórmula antes')
    elif opcion == "3":
        if cont > 0:
            Tabla_Booleana(formula)
        else:
            print('Crea una fórmula antes')
    elif opcion == "4":
        if cont > 0:
            Guardar(formula)
        else:
            print('Crea una fórmula antes')
    elif opcion == "5":
        BD = Cargar()
        print('El resultado es: \n', BD)
    elif opcion == "6":
        if cont>0:
            valores_asignados= Asignar(formula)
        else:
            print('Crea una fórmula antes')
    elif opcion == "7":
        if valores_asignados:
            Ver(oracion, valores_asignados)
        else:
                print('rankea valores primero.')
    elif opcion == "8":
        if cont > 0:
            Arbol_binario(oracion)
                
        else:print('se te paso un diamente al minuto 3 ntc..... Crea una fórmula antes')
        
    elif opcion == "9":
        Arbol_binario_global()

    elif opcion == "11":
        print("ta wueno pueeeee pero me necesitaras!!!!!")
        break
    else:
        print("pongase serio mijo elija algo del 1 al 11 >:v")
