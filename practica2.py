import itertools

# Función para definir el alfabeto y estados
def definir_alfabeto():
    alfabeto = input("Ingrese el alfabeto separado por comas (ej: a,b,c): ").split(',')
    return alfabeto

def definir_estados():
    estados = input("Ingrese los estados separados por comas (ej: 0,1,2,3): ").split(',')
    return estados

# Operaciones básicas sobre lenguajes
def union_lenguajes(lenguaje1, lenguaje2):
    return list(set(lenguaje1).union(set(lenguaje2)))

def interseccion_lenguajes(lenguaje1, lenguaje2):
    return list(set(lenguaje1).intersection(set(lenguaje2)))

def diferencia_lenguajes(lenguaje1, lenguaje2):
    return list(set(lenguaje1).difference(set(lenguaje2)))

def complemento_lenguaje(lenguaje, alfabeto):
    complemento = set(itertools.chain.from_iterable(itertools.product(alfabeto, repeat=i) for i in range(1, len(max(lenguaje, key=len)) + 1)))
    return list(complemento.difference(set(lenguaje)))

# Función para generar la cerradura de Kleene basada en el alfabeto del usuario
def kleene_cerradura(alfabeto, n):
    kleene = ['']  # Incluir la cadena vacía
    for i in range(1, n + 1):
        combinaciones = [''.join(p) for p in itertools.product(alfabeto, repeat=i)]
        kleene.extend(combinaciones)
    return kleene

# Clausura positiva
def clausura_positiva(alfabeto, n):
    return kleene_cerradura(alfabeto, n)[1:]  # La clausura positiva es la cerradura de Kleene sin la cadena vacía

# Función para concatenar dos lenguajes
def concatenar_lenguajes(lenguaje1, lenguaje2):
    concatenacion = []
    for cadena1 in lenguaje1:
        for cadena2 in lenguaje2:
            concatenacion.append(cadena1 + cadena2)
    return concatenacion

# Función para potenciar un lenguaje
def potenciar_lenguaje(lenguaje, potencia):
    resultado = lenguaje.copy()
    for _ in range(potencia - 1):
        resultado = concatenar_lenguajes(resultado, lenguaje)
    return resultado

# Reflexión o inverso de un lenguaje
def reflexion_lenguaje(lenguaje):
    return [cadena[::-1] for cadena in lenguaje]

# Función para definir transiciones del AFD
def definir_transiciones(estados, alfabeto):
    transiciones = {}
    for estado in estados:
        transiciones[estado] = {}
        for simbolo in alfabeto:
            destino = input(f"Transición para el estado {estado} con '{simbolo}': ")
            transiciones[estado][simbolo] = destino
    return transiciones

# Función para definir estados de aceptación
def definir_estados_aceptacion():
    aceptados = input("Ingrese los estados de aceptación separados por comas (ej: 2,3): ").split(',')
    return aceptados

# Validar una cadena en el AFD
def validar_cadena(alfabeto, estados, transiciones, estado_inicial, aceptados, cadena):
    est_actual = estado_inicial
    for caracter in cadena:
        print(f"Estado actual: {est_actual}, procesando: '{caracter}'")
        if caracter not in alfabeto:
            print(f"Error: el carácter '{caracter}' no pertenece al alfabeto.")
            return False
        if est_actual not in transiciones or caracter not in transiciones[est_actual]:
            print("Error: Transición no definida.")
            return False
        est_actual = transiciones[est_actual][caracter]
    
    if est_actual in aceptados:
        print(f"La cadena '{cadena}' es aceptada en el estado {est_actual}.")
        return True
    else:
        print(f"La cadena '{cadena}' no es aceptada. Estado final: {est_actual}")
        return False

# Función principal
def main():
    # Parte 1: Definir alfabeto y estados
    alfabeto = definir_alfabeto()
    estados = definir_estados()
    estado_inicial = input("Ingrese el estado inicial: ")

    # Parte 2: Realizar operaciones sobre lenguajes
    while True:
        print("\nOperaciones sobre lenguajes:")
        print("1. Cerradura de Kleene")
        print("2. Clausura Positiva")
        print("3. Concatenación de lenguajes")
        print("4. Potenciación de un lenguaje")
        print("5. Reflexión de un lenguaje")
        print("6. Unión de lenguajes")
        print("7. Intersección de lenguajes")
        print("8. Diferencia de lenguajes")
        print("9. Complemento de un lenguaje")
        print("10. Definir transiciones y validar cadena")
        print("11. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            n = int(input("Ingrese el número máximo de combinaciones para la cerradura de Kleene: "))
            kleene = kleene_cerradura(alfabeto, n)
            print(f"Cerradura de Kleene hasta longitud {n}: {kleene}")

        elif opcion == "2":
            n = int(input("Ingrese el número máximo de combinaciones para la clausura positiva: "))
            positiva = clausura_positiva(alfabeto, n)
            print(f"Clausura Positiva hasta longitud {n}: {positiva}")

        elif opcion == "3":
            lenguaje1 = input("Ingrese las cadenas del primer lenguaje separadas por comas: ").split(',')
            lenguaje2 = input("Ingrese las cadenas del segundo lenguaje separadas por comas: ").split(',')
            resultado = concatenar_lenguajes(lenguaje1, lenguaje2)
            print(f"Resultado de la concatenación: {resultado}")

        elif opcion == "4":
            lenguaje = input("Ingrese las cadenas del lenguaje separadas por comas: ").split(',')
            potencia = int(input("Ingrese la potencia: "))
            resultado = potenciar_lenguaje(lenguaje, potencia)
            print(f"Resultado de la potenciación: {resultado}")

        elif opcion == "5":
            lenguaje = input("Ingrese las cadenas del lenguaje separadas por comas: ").split(',')
            resultado = reflexion_lenguaje(lenguaje)
            print(f"Resultado de la reflexión (inverso): {resultado}")

        elif opcion == "6":
            lenguaje1 = input("Ingrese las cadenas del primer lenguaje separadas por comas: ").split(',')
            lenguaje2 = input("Ingrese las cadenas del segundo lenguaje separadas por comas: ").split(',')
            resultado = union_lenguajes(lenguaje1, lenguaje2)
            print(f"Resultado de la unión: {resultado}")

        elif opcion == "7":
            lenguaje1 = input("Ingrese las cadenas del primer lenguaje separadas por comas: ").split(',')
            lenguaje2 = input("Ingrese las cadenas del segundo lenguaje separadas por comas: ").split(',')
            resultado = interseccion_lenguajes(lenguaje1, lenguaje2)
            print(f"Resultado de la intersección: {resultado}")

        elif opcion == "8":
            lenguaje1 = input("Ingrese las cadenas del primer lenguaje separadas por comas: ").split(',')
            lenguaje2 = input("Ingrese las cadenas del segundo lenguaje separadas por comas: ").split(',')
            resultado = diferencia_lenguajes(lenguaje1, lenguaje2)
            print(f"Resultado de la diferencia: {resultado}")

        elif opcion == "9":
            lenguaje = input("Ingrese las cadenas del lenguaje separadas por comas: ").split(',')
            resultado = complemento_lenguaje(lenguaje, alfabeto)
            print(f"Resultado del complemento: {resultado}")

        elif opcion == "10":
            transiciones = definir_transiciones(estados, alfabeto)
            aceptados = definir_estados_aceptacion()
            cadena = input("Ingrese la cadena a validar: ")
            validar_cadena(alfabeto, estados, transiciones, estado_inicial, aceptados, cadena)

        elif opcion == "11":
            break

        else:
            print("Opción no válida, intente nuevamente.")

if __name__ == "__main__":
    main()
