import flet as ft
import itertools

# Función para verificar que las cadenas pertenecen al alfabeto
def verificar_lenguaje(alfabeto, lenguaje):
    for cadena in lenguaje:
        for caracter in cadena:
            if caracter not in alfabeto:
                return False
    return True

# Funciones para operaciones de lenguajes
def kleene_cerradura(alfabeto, n):
    kleene = ['']  # Incluir la cadena vacía (λ)
    for i in range(1, n + 1):
        combinaciones = [''.join(p) for p in itertools.product(alfabeto, repeat=i)]
        kleene.extend(combinaciones)
    return kleene

def clausura_positiva(alfabeto, n):
    return kleene_cerradura(alfabeto, n)[1:]  # Sin la cadena vacía

def concatenar_lenguajes(lenguaje1, lenguaje2):
    concatenacion = []
    for cadena1 in lenguaje1:
        for cadena2 in lenguaje2:
            concatenacion.append(cadena1 + cadena2)
    return concatenacion

def potenciar_lenguaje(lenguaje, potencia):
    resultado = lenguaje.copy()
    for _ in range(potencia - 1):
        resultado = concatenar_lenguajes(resultado, lenguaje)
    return resultado

def reflexion_lenguaje(lenguaje):
    return [cadena[::-1] for cadena in lenguaje]

def union_lenguajes(lenguaje1, lenguaje2):
    return list(set(lenguaje1).union(set(lenguaje2)))

def interseccion_lenguajes(lenguaje1, lenguaje2):
    return list(set(lenguaje1).intersection(set(lenguaje2)))

def diferencia_lenguajes(lenguaje1, lenguaje2):
    return list(set(lenguaje1).difference(set(lenguaje2)))

# Funciones para el autómata
def definir_transiciones(estados, alfabeto):
    transiciones = {}
    for estado in estados:
        transiciones[estado] = {}
        for simbolo in alfabeto:
            transiciones[estado][simbolo] = ""
    return transiciones

def validar_cadena(alfabeto, estados, transiciones, estado_inicial, aceptados, cadena):
    est_actual = estado_inicial
    for caracter in cadena:
        if caracter not in alfabeto:
            return False, f"El carácter '{caracter}' no pertenece al alfabeto."
        if est_actual not in transiciones or caracter not in transiciones[est_actual]:
            return False, f"Error: Transición no definida para estado {est_actual} y símbolo '{caracter}'."
        est_actual = transiciones[est_actual][caracter]
    
    if est_actual in aceptados:
        return True, f"La cadena '{cadena}' es aceptada. Estado final: {est_actual}."
    else:
        return False, f"La cadena '{cadena}' no es aceptada. Estado final: {est_actual}."

# Mejorar la presentación de transiciones
def presentar_transiciones(transiciones):
    formatted_rows = []
    for estado, transiciones_estado in transiciones.items():
        row = [estado]
        row.extend([transiciones_estado[simbolo] for simbolo in transiciones_estado])
        formatted_rows.append(": ".join(row))
    return formatted_rows

def main(page: ft.Page):
    page.title = "Operaciones sobre Lenguajes y Autómatas"
    page.vertical_alignment = ft.MainAxisAlignment.START

    # Inputs para alfabeto y número n
    alfabeto_input = ft.TextField(label="Ingrese el alfabeto separado por comas (ej: a,b,c)", width=400)
    n_input = ft.TextField(label="Ingrese el número máximo de combinaciones", width=400)
    
    # Inputs para lenguajes
    lenguaje1_input = ft.TextField(label="Ingrese las cadenas del primer lenguaje separadas por comas", width=400)
    lenguaje2_input = ft.TextField(label="Ingrese las cadenas del segundo lenguaje separadas por comas", width=400)

    # Input para potencia de un lenguaje
    potencia_input = ft.TextField(label="Ingrese la potencia del lenguaje", width=400)

    # Input para definir autómata (estados, transiciones y aceptación)
    estados_input = ft.TextField(label="Ingrese los estados separados por comas (ej: 0,1,2)", width=400)
    estado_inicial_input = ft.TextField(label="Ingrese el estado inicial", width=400)
    cadena_input = ft.TextField(label="Ingrese la cadena a validar", width=400)

    transiciones = {}
    aceptados_input = ft.TextField(label="Ingrese los estados de aceptación separados por comas (ej: 2,3)", width=400)

    # Display de resultados
    resultado_text = ft.Text("", size=18)

    # Función para mostrar y ocultar la columna de definición del autómata
    def mostrar_ocultar_columna_autómata(visible):
        col_autómata.visible = visible
        page.update()

    # Función para definir transiciones
    def definir_transiciones_ui(e):
        alfabeto = alfabeto_input.value.split(',')
        estados = estados_input.value.split(',')
        transiciones.clear()
        for estado in estados:
            transiciones[estado] = {}
            for simbolo in alfabeto:
                transiciones[estado][simbolo] = ft.TextField(
                    label=f"{estado}: {simbolo} ->",
                    width=100
                )
        transicion_column.controls.clear()
        for estado in transiciones:
            row = ft.Row(controls=[transiciones[estado][simbolo] for simbolo in transiciones[estado]], spacing=5)
            transicion_column.controls.append(row)
        page.update()

    # Función para validar cadena
    def validar_cadena_ui(e):
        alfabeto = alfabeto_input.value.split(',')
        estados = estados_input.value.split(',')
        aceptados = aceptados_input.value.split(',')
        estado_inicial = estado_inicial_input.value
        cadena = cadena_input.value

        # Obtener transiciones definidas por el usuario
        transiciones_definidas = {}
        for estado in transiciones:
            transiciones_definidas[estado] = {}
            for simbolo, campo in transiciones[estado].items():
                transiciones_definidas[estado][simbolo] = campo.value
        
        aceptada, mensaje = validar_cadena(alfabeto, estados, transiciones_definidas, estado_inicial, aceptados, cadena)
        
        # Actualizar color del texto dependiendo del resultado
        if aceptada:
            resultado_text.color = ft.colors.GREEN
        else:
            resultado_text.color = ft.colors.RED
        
        resultado_text.value = mensaje
        page.update()

    # Botones para acciones
    button_definir_transiciones = ft.ElevatedButton(text="Definir Transiciones", on_click=definir_transiciones_ui)
    button_validar_cadena = ft.ElevatedButton(text="Validar Cadena", on_click=validar_cadena_ui)

    # Columna para las transiciones dinámicas con un scrollbar
    transicion_column = ft.Column()

    # Usar un ListView para permitir el scroll en la sección de transiciones
    transicion_scroll = ft.ListView(
        controls=[transicion_column],
        height=200,
        spacing=10,
        padding=10,
        auto_scroll=False
    )

    # Columna para definir autómata (inicialmente oculta)
    col_autómata = ft.Column(
        controls=[
            estados_input,
            estado_inicial_input,
            aceptados_input,
            button_definir_transiciones,
            transicion_scroll,  # Añadir el scroll aquí
            cadena_input,
            button_validar_cadena,
        ],
        visible=False,
        width=400
    )

    # Botón para mostrar/ocultar columna de autómata
    def realizar_autómata(e):
        mostrar_ocultar_columna_autómata(True)

    button_autómata = ft.ElevatedButton(text="Definir Autómata", on_click=realizar_autómata)

    # Funciones de operaciones de lenguajes
    def realizar_cerradura_kleene(e):
        alfabeto = alfabeto_input.value.split(',')
        try:
            n = int(n_input.value)
            resultado = kleene_cerradura(alfabeto, n)
            resultado_text.value = f"Cerradura de Kleene: {resultado}"
        except ValueError:
            resultado_text.value = "Por favor ingrese un número válido."
        page.update()

    def realizar_clausura_positiva(e):
        alfabeto = alfabeto_input.value.split(',')
        try:
            n = int(n_input.value)
            resultado = clausura_positiva(alfabeto, n)
            resultado_text.value = f"Clausura Positiva: {resultado}"
        except ValueError:
            resultado_text.value = "Por favor ingrese un número válido."
        page.update()

    def realizar_concatenacion(e):
        alfabeto = alfabeto_input.value.split(',')
        lenguaje1 = lenguaje1_input.value.split(',')
        lenguaje2 = lenguaje2_input.value.split(',')
        if not verificar_lenguaje(alfabeto, lenguaje1) or not verificar_lenguaje(alfabeto, lenguaje2):
            resultado_text.value = "Uno o más elementos no pertenecen al alfabeto."
        else:
            resultado = concatenar_lenguajes(lenguaje1, lenguaje2)
            resultado_text.value = f"Concatenación de lenguajes: {resultado}"
        page.update()

    def realizar_potenciacion(e):
        alfabeto = alfabeto_input.value.split(',')
        lenguaje = lenguaje1_input.value.split(',')
        try:
            potencia = int(potencia_input.value)
            resultado = potenciar_lenguaje(lenguaje, potencia)
            resultado_text.value = f"Potenciación del lenguaje: {resultado}"
        except ValueError:
            resultado_text.value = "Por favor ingrese una potencia válida."
        page.update()

    def realizar_reflexion(e):
        lenguaje = lenguaje1_input.value.split(',')
        resultado = reflexion_lenguaje(lenguaje)
        resultado_text.value = f"Reflexión del lenguaje: {resultado}"
        page.update()

    def realizar_union(e):
        lenguaje1 = lenguaje1_input.value.split(',')
        lenguaje2 = lenguaje2_input.value.split(',')
        resultado = union_lenguajes(lenguaje1, lenguaje2)
        resultado_text.value = f"Unión de lenguajes: {resultado}"
        page.update()

    def realizar_interseccion(e):
        lenguaje1 = lenguaje1_input.value.split(',')
        lenguaje2 = lenguaje2_input.value.split(',')
        resultado = interseccion_lenguajes(lenguaje1, lenguaje2)
        resultado_text.value = f"Intersección de lenguajes: {resultado}"
        page.update()

    def realizar_diferencia(e):
        lenguaje1 = lenguaje1_input.value.split(',')
        lenguaje2 = lenguaje2_input.value.split(',')
        resultado = diferencia_lenguajes(lenguaje1, lenguaje2)
        resultado_text.value = f"Diferencia de lenguajes: {resultado}"
        page.update()

    # Botones para operaciones de lenguajes
    button_kleene = ft.ElevatedButton(text="Cerradura de Kleene", on_click=realizar_cerradura_kleene)
    button_positiva = ft.ElevatedButton(text="Clausura Positiva", on_click=realizar_clausura_positiva)
    button_concat = ft.ElevatedButton(text="Concatenar lenguajes", on_click=realizar_concatenacion)
    button_potenciar = ft.ElevatedButton(text="Potenciar lenguaje", on_click=realizar_potenciacion)
    button_reflexion = ft.ElevatedButton(text="Reflexión del lenguaje", on_click=realizar_reflexion)
    button_union = ft.ElevatedButton(text="Unión de lenguajes", on_click=realizar_union)
    button_interseccion = ft.ElevatedButton(text="Intersección de lenguajes", on_click=realizar_interseccion)
    button_diferencia = ft.ElevatedButton(text="Diferencia de lenguajes", on_click=realizar_diferencia)

    # Dividir en columnas
    col1 = ft.Column(
        controls=[
            alfabeto_input,
            n_input,
            lenguaje1_input,
            lenguaje2_input,
            potencia_input,
        ],
        alignment=ft.MainAxisAlignment.START,
        width=400
    )

    col2 = ft.Column(
        controls=[
            button_kleene,
            button_positiva,
            button_concat,
            button_potenciar,
            button_reflexion,
            button_union,
            button_interseccion,
            button_diferencia,
            button_autómata,
        ],
        alignment=ft.MainAxisAlignment.START,
        width=200
    )

    # Añadir elementos a la página con estructura de columnas
    page.add(
        ft.Row(controls=[col1, col2, col_autómata], spacing=50),
        resultado_text,
    )

# Iniciar la aplicación Flet
ft.app(target=main)
