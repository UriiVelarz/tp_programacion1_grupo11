import re
import datetime 
from Reservas import reservas

salas = [
    [1, "Sala A", "Primer  Piso", 2, 1],
    [2, "Sala B", "Primer  Piso", 2, 2],
    [3, "Sala C", "Primer  Piso", 4, 3],
    [4, "Sala A", "Segundo Piso", 2, 1],
    [5, "Sala B", "Segundo Piso", 2, 2],
    [6, "Sala C", "Segundo Piso", 4, 3]
]

TIPOS_SALA = {
    1: {"nombre": "Pequeña", "cantidad": 0},
    2: {"nombre": "Mediana", "cantidad": 0},
    3: {"nombre": "Grande", "cantidad": 0},
}

dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

COLOR_VERDE = "\033[32m"
COLOR_AMARILLO = "\033[33m"
COLOR_AZUL = "\033[34m"
COLOR_ROJO = "\033[31m"
COLOR_RESET = "\033[0m"


def limpiar_ansi(texto):
    return re.sub(r"\x1b\[[0-9;]*m", "", texto)


def validar_id_sala(texto):
    return re.fullmatch(r"[1-9]\d*", texto) is not None


def validar_nombre_sala(texto):
    patron = r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ0-9]+(?:[ -]+[A-Za-zÁÉÍÓÚÜÑáéíóúüñ0-9]+)*"
    return re.fullmatch(patron, texto.strip()) is not None


def validar_ubicacion(texto):
    patron = r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ0-9]+(?:[ -]+[A-Za-zÁÉÍÓÚÜÑáéíóúüñ0-9]+)*"
    return re.fullmatch(patron, texto.strip()) is not None


def validar_capacidad(texto):
    return re.fullmatch(r"[1-9]\d*", texto) is not None


def convertir_entero(texto):
    try:
        return int(texto)
    except ValueError:
        return None


def formatear_celda(texto, ancho):
    texto_limpio = limpiar_ansi(texto)
    espacios = max(0, ancho - len(texto_limpio))
    return texto + (" " * espacios)


def tipo_sala(sala):
    if len(sala) > 4 and sala[4] in TIPOS_SALA:
        return sala[4]
    nombre = sala[1].strip().casefold()
    if nombre.endswith("a"):
        return 1
    if nombre.endswith("b"):
        return 2
    if nombre.endswith("c"):
        return 3
    return None


def cantidad_salas_tipo(tipo, matriz=None):
    matriz = salas if matriz is None else matriz
    return sum(1 for sala in matriz if tipo_sala(sala) == tipo)


def actualizar_cantidad_tipos(matriz=None):
    matriz = salas if matriz is None else matriz
    for tipo in TIPOS_SALA:
        TIPOS_SALA[tipo]["cantidad"] = cantidad_salas_tipo(tipo, matriz)


actualizar_cantidad_tipos()


matriz_disponibilidad = [
    [1, 1, 0, 1, 1, 0, 1],
    [0, 1, 1, 1, 0, 1, 1],
    [1, 0, 1, 0, 1, 1, 1],
    [0, 1, 0, 1, 1, 1, 1],
    [1, 0, 1, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0],
]


def mostrar_matriz():
    print("\nMatriz de disponibilidad por sala y dia")
    print("=" * 102)

    encabezado = f"{'Sala':<25}" + "".join(f"{d:<11}" for d in dias)
    print(encabezado)
    print("-" * len(encabezado))

    for i in range(len(salas)):
        _, nombre, piso, _ = salas[i][:4]
        etiqueta = f"{nombre}({piso})"
        disponibilidad = matriz_disponibilidad[i % len(matriz_disponibilidad)]
        fila = f"{etiqueta:<25}" + "".join(f"{disponibilidad[j]:<11}" for j in range(len(dias)))
        print(fila)
    print("\nAclaracion: 1 = disponible, 0 = ocupado")


def fecha_maxima_consulta(fecha_actual=None):
    fecha_actual = fecha_actual or datetime.date.today()
    mes = fecha_actual.month + 6
    anio = fecha_actual.year + (mes - 1) // 12
    mes = (mes - 1) % 12 + 1
    ultimo_dia = obtener_dias_mes(mes)
    dia = min(fecha_actual.day, ultimo_dia)
    return datetime.date(anio, mes, dia)


def obtener_dias_mes(mes):
    dias_por_mes = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
    return dias_por_mes.get(mes, 0)


def mes_consultable(anio, mes, fecha_hoy=None, fecha_maxima=None):
    fecha_hoy = fecha_hoy or datetime.date.today()
    fecha_maxima = fecha_maxima or fecha_maxima_consulta(fecha_hoy)
    if anio < 1 or not 1 <= mes <= 12:
        return False
    try:
        inicio_mes = datetime.date(anio, mes, 1)
        fin_mes = datetime.date(anio, mes, obtener_dias_mes(mes))
    except ValueError:
        return False
    return inicio_mes <= fecha_maxima and fin_mes >= fecha_hoy


def contar_reservas_por_tamanio(anio, mes, dia, tamaño):
    fecha = f"{dia:02d}/{mes:02d}/{anio}"
    cantidad = 0
    for reserva in reservas:
        if reserva[3] == fecha and reserva[1] == tamaño:
            cantidad += 1
    return cantidad, cantidad_salas_tipo(tamaño)


def estado_horario(anio, mes, dia, tamaño, hora_inicio):
    fecha = f"{dia:02d}/{mes:02d}/{anio}"
    hora_fin = hora_inicio + 2
    capacidad = cantidad_salas_tipo(tamaño)
    conflictos = 0

    for reserva in reservas:
        if reserva[1] != tamaño or reserva[3] != fecha:
            continue

        inicio = int(reserva[4][:2])
        fin = int(reserva[5][:2])
        bloque_actual = (hora_inicio, hora_fin)
        bloque_reserva = (inicio, fin)

        if not (bloque_actual[1] <= bloque_reserva[0] or bloque_actual[0] >= bloque_reserva[1]):
            conflictos += 1

    if capacidad == 0 or conflictos >= capacidad:
        color = COLOR_ROJO
        estado = f"Ocupada {conflictos}/{capacidad}"
    elif conflictos == 0:
        color = COLOR_VERDE
        estado = f"Libre {conflictos}/{capacidad}"
    else:
        color = COLOR_AMARILLO
        estado = f"Parcial {conflictos}/{capacidad}"

    return f"{color}{estado}{COLOR_RESET}"


def consultar_disponibilidad_mensual():
    fecha_hoy = datetime.date.today()
    fecha_maxima = fecha_maxima_consulta(fecha_hoy)

    while True:
        anio_input = input(
            f"Ingrese el año ({fecha_hoy.year} a {fecha_maxima.year}) o -1 para volver: "
        ).strip()
        if anio_input == "-1":
            return
        if anio_input.isdigit():
            anio = convertir_entero(anio_input)
            if anio is not None and fecha_hoy.year <= anio <= fecha_maxima.year:
                break
        print(
            f"Mes fuera de rango. El periodo disponible va desde "
            f"{fecha_hoy:%d/%m/%Y} hasta {fecha_maxima:%d/%m/%Y}. Ingrese el año nuevamente."
        )

    while True:
        mes_input = input(
            f"Ingrese el mes del año {anio} dentro del periodo disponible "
            f"({fecha_hoy:%m/%Y} a {fecha_maxima:%m/%Y}) o -1 para volver: "
        ).strip()
        if mes_input == "-1":
            return
        if mes_input.isdigit():
            mes = convertir_entero(mes_input)
            if mes is not None and mes_consultable(
                anio, mes, fecha_hoy, fecha_maxima
            ):
                break
        print(
            f"Mes fuera de rango. Para el año {anio}, elija un mes entre "
            f"{fecha_hoy:%m/%Y} y {fecha_maxima:%m/%Y}."
        )

    while True:
        dia_inicio_input = input("Ingrese el dia de inicio (o -1 para volver): ").strip()
        if dia_inicio_input == "-1":
            return
        if dia_inicio_input.isdigit():
            dia_inicio = convertir_entero(dia_inicio_input)
            try:
                fecha_inicio = datetime.date(anio, mes, dia_inicio)
            except (TypeError, ValueError):
                fecha_inicio = None
            if (
                fecha_inicio is not None
                and fecha_hoy <= fecha_inicio <= fecha_maxima
            ):
                break
        print("El dia debe ser valido y estar dentro de los proximos 6 meses.")

    while True:
        max_dias = min(30, (fecha_maxima - fecha_inicio).days + 1)
        cantidad_dias_input = input(
            f"Ingrese la cantidad de dias a imprimir (maximo {max_dias}): "
        ).strip()
        if cantidad_dias_input.isdigit():
            cantidad_dias = convertir_entero(cantidad_dias_input)
            if cantidad_dias is not None and 1 <= cantidad_dias <= max_dias:
                break
        print(f"La cantidad de dias debe estar entre 1 y {max_dias}.")

    fechas = [
        fecha_inicio + datetime.timedelta(days=desplazamiento)
        for desplazamiento in range(cantidad_dias)
    ]

    print(f"\n{'Disponibilidad mensual - ' + str(mes) + '/' + str(anio):^120}")
    actualizar_cantidad_tipos()
    plurales = {1: "pequeñas", 2: "medianas", 3: "grandes"}
    detalle_salas = ", ".join(
        f"{datos['cantidad']} {plurales[tipo]}"
        for tipo, datos in TIPOS_SALA.items()
    )
    print(f"{('Total de salas: ' + detalle_salas):^120}")
    print("=" * 120)

    for fecha in fechas:
        anio_actual, mes_actual, dia_actual = fecha.year, fecha.month, fecha.day
        print(f"\n=== Dia {dia_actual:02d}/{mes_actual:02d}/{anio_actual} ===")
        print(f"{'Horario':<15} | {'Pequeña':^10} | {'Mediana':^10} | {'Grande':^10}")
        print("-" * 62)

        for hora_inicio in range(9, 18):
            hora_fin = hora_inicio + 2
            if hora_fin > 18:
                continue

            horario = f"{hora_inicio:02d}:00-{hora_fin:02d}:00"
            peq = estado_horario(anio_actual, mes_actual, dia_actual, 1, hora_inicio)
            med = estado_horario(anio_actual, mes_actual, dia_actual, 2, hora_inicio)
            gra = estado_horario(anio_actual, mes_actual, dia_actual, 3, hora_inicio)

            print(f"{horario:^15} | {peq:^10} | {med:^10} | {gra:^10}")

        print("-" * 62)

    print(f"\n{COLOR_VERDE}Libre{COLOR_RESET}   {COLOR_AMARILLO}Parcial{COLOR_RESET}   {COLOR_ROJO}Ocupada{COLOR_RESET}")
    print("Los horarios validos para reservar son desde 09:00 hasta 16:00, con reservas de 2 horas.")


def imprimir_Salas(matriz):
    '''
    pre: recibe una matriz de salas, donde cada fila representa una sala con sus datos
         [id_sala, nombre_sala, ubicacion, capacidad].
    pos: devuelve por pantalla la matriz de salas fomateada.
    '''
    print("=" * 55)
    print(f"{'Salas':42}")
    print("=" * 55)
    print(f"{'Id_Sala':<10}{'Nombre':<10}{'Ubicacion':<15}{'capacidad':<14}{'Tipo':<14}")
    print("-" * 55)

    for i in range(len(matriz)):
        id_sala = matriz[i][0]
        nombre_sala = matriz[i][1]
        ubicacion = matriz[i][2]
        capacidad = matriz[i][3]
        tipo = tipo_sala(matriz[i])
        nombre_tipo = TIPOS_SALA[tipo]["nombre"] if tipo in TIPOS_SALA else "Sin tipo"
        print(f"{id_sala:<10}{nombre_sala:<10}{ubicacion:15}{capacidad:<14}{nombre_tipo:<14}")


def agregar_Sala(matriz):
    '''
    pre: recibe una matriz de salas, donde cada fila representa una sala con sus datos
         id_sala, nombre_sala, ubicacion, capacidad].
    pos: solicita los datos para registrar una nueva sala. si el id ya existe, muestra error y finaliza. si el id es unico, 
         agrega una sala a la matriz al final de la lista y muestra un mensaje de exito.
    '''
    while True:
        id_input = input("Ingresar Id de sala o -1 para volver al menu principal: ").strip()
        if id_input == "-1":
            return
        if not validar_id_sala(id_input):
            print("El Id debe ser un numero entero positivo.")
            continue
        id_sala = convertir_entero(id_input)
        if id_sala is None:
            print("El Id debe ser un numero entero positivo.")
            continue
        if any(sala[0] == id_sala for sala in matriz):
            print("Ese Id de sala ya existe.")
            continue
        break

    while True:
        nombre_sala = input("Ingresar nombre de sala o -1 para volver al menu principal: ").strip()
        if nombre_sala == "-1":
            return
        if validar_nombre_sala(nombre_sala):
            break
        print("El nombre solo puede contener letras, numeros, espacios y guiones.")

    while True:
        ubicacion = input("Ingresar ubicacion o -1 para volver al menu principal: ").strip()
        if ubicacion == "-1":
            return
        if validar_ubicacion(ubicacion):
            break
        print("La ubicacion solo puede contener letras, numeros, espacios y guiones.")

    while True:
        print("Tipo de sala:")
        for tipo, datos in TIPOS_SALA.items():
            print(f"{tipo}. {datos['nombre']}")
        tipo_input = input(
            "Ingresar tipo de sala o -1 para volver al menu principal: "
        ).strip()
        if tipo_input == "-1":
            return
        tipo = convertir_entero(tipo_input)
        if tipo in TIPOS_SALA:
            break
        print("Debe seleccionar un tipo de sala valido.")

    while True:
        capacidad_input = input("Ingresar capacidad o -1 para volver al menu principal: ").strip()
        if capacidad_input == "-1":
            return
        if validar_capacidad(capacidad_input):
            capacidad = convertir_entero(capacidad_input)
            if capacidad is None:
                print("La capacidad debe ser un numero entero positivo.")
                continue
            break
        print("La capacidad debe ser un numero entero positivo.")

    nuevaSala = [id_sala, nombre_sala, ubicacion, capacidad, tipo]
    matriz.append(nuevaSala)
    actualizar_cantidad_tipos(matriz)
    print("Sala agregada correctamente")


def eliminar_Sala(matriz):
    '''
        pre: recibe una matriz de salas, donde cada fila representa una sala con sus datos
             id_sala, nombre_sala, ubicacion, capacidad].
        pos: solicita un id de sala por consola. si el id existe en la matriz, elimina la sala de 
             la matriz original y muestra un mensaje de exito. si no existe, muestra un mensaje de error.
    '''
    while True:
        id_input = input("Ingresar Id o -1 para volver al menu principal: ").strip()
        if id_input == "-1":
            return
        if not validar_id_sala(id_input):
            print("El Id debe ser un numero entero positivo.")
            continue
        id_sala = convertir_entero(id_input)
        if id_sala is None:
            print("El Id debe ser un numero entero positivo.")
            continue
        for sala in matriz:
            if sala[0] == id_sala:
                matriz.remove(sala)
                actualizar_cantidad_tipos(matriz)
                print("Sala eliminado correctamente")
                return
        print("No se encontro el id de Sala")
        return


def modificar_Sala(matriz):
    '''
        pre: recibe una matriz de salas, donde cada fila representa una sala con sus datos
             id_sala, nombre_sala, ubicacion, capacidad].
        pos: solicita un id de sala por consola. si lo encuentra, pide los nuevos datos 
             (sala, usuario, fecha, inicio y fin) para sobreescribir los valores originales en la matriz.
             si el id no existe, la funcion termina sin realizar cambios.
    '''
    while True:
        id_buscado_input = input("Ingresar id de la sala a modificar o -1 para volver al menu principal: ").strip()
        if id_buscado_input == "-1":
            return
        if not validar_id_sala(id_buscado_input):
            print("El Id debe ser un numero entero positivo.")
            continue
        id_buscado = convertir_entero(id_buscado_input)
        if id_buscado is None:
            print("El Id debe ser un numero entero positivo.")
            continue
        fila_encontrada = next(
            (fila for fila in matriz if fila[0] == id_buscado),
            None
        )
        if fila_encontrada is not None:
            break
        print("Sala no encontrada. Intente nuevamente.")

    while True:
        nuevo_id_input = input("Ingresar nuevo id de sala o -1 para volver al menu principal: ").strip()
        if nuevo_id_input == "-1":
            return
        if not validar_id_sala(nuevo_id_input):
            print("El Id debe ser un numero entero positivo.")
            continue
        nuevo_id = convertir_entero(nuevo_id_input)
        if nuevo_id is None:
            print("El Id debe ser un numero entero positivo.")
            continue
        if any(fila is not fila_encontrada and fila[0] == nuevo_id for fila in matriz):
            print("Ese Id de sala ya existe.")
            continue
        break

    while True:
        nuevo_nombre = input("Ingresar nuevo nombre de sala o -1 para volver al menu principal: ").strip()
        if nuevo_nombre == "-1":
            return
        if validar_nombre_sala(nuevo_nombre):
            break
        print("El nombre solo puede contener letras, numeros, espacios y guiones.")

    while True:
        nueva_ubicacion = input("Ingresar nueva ubicacion de la sala o -1 para volver al menu principal: ").strip()
        if nueva_ubicacion == "-1":
            return
        if validar_ubicacion(nueva_ubicacion):
            break
        print("La ubicacion solo puede contener letras, numeros, espacios y guiones.")

    fila_encontrada[0] = nuevo_id
    fila_encontrada[1] = nuevo_nombre
    fila_encontrada[2] = nueva_ubicacion
    print("Sala modificada correctamente")
