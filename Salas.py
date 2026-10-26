import csv
import os
import re
import datetime 
from Reservas import reservas

ARCHIVO_SALAS = os.path.join(os.path.dirname(__file__), "salas.txt")
ARCHIVO_TEMPORAL_SALAS = ARCHIVO_SALAS + ".tmp"
_persistencia_salas_habilitada = True
salas = []

TIPOS_SALA = {
    1: {"nombre": "Pequeña", "cantidad": 0, "capacidad_minima": 2, "capacidad_maxima": 6},
    2: {"nombre": "Mediana", "cantidad": 0, "capacidad_minima": 7, "capacidad_maxima": 12},
    3: {"nombre": "Grande", "cantidad": 0, "capacidad_minima": 12, "capacidad_maxima": 24},
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
    return ((sala[0] - 1) // 2) % len(TIPOS_SALA) + 1


def capacidad_valida(tipo, capacidad):
    datos_tipo = TIPOS_SALA[tipo]
    return datos_tipo["capacidad_minima"] <= capacidad <= datos_tipo["capacidad_maxima"]


def _letra_sala(indice):
    letras = ""
    numero = indice + 1
    while numero:
        numero, resto = divmod(numero - 1, 26)
        letras = chr(ord("A") + resto) + letras
    return letras


def _actualizar_nombres_salas(matriz):
    cantidades = {tipo: 0 for tipo in TIPOS_SALA}
    for sala in sorted(matriz, key=lambda elemento: (tipo_sala(elemento), elemento[0])):
        tipo = tipo_sala(sala)
        sala[3] = tipo
        sala[1] = f"Sala {TIPOS_SALA[tipo]['nombre'].lower()} {_letra_sala(cantidades[tipo])}"
        cantidades[tipo] += 1


def _cargar_salas():
    global _persistencia_salas_habilitada
    if not os.path.exists(ARCHIVO_SALAS):
        print(f"No se encontro el archivo de salas: {ARCHIVO_SALAS}")
        return

    salas_cargadas = []
    try:
        with open(ARCHIVO_SALAS, "r", encoding="utf-8", newline="") as archivo:
            lector = csv.reader(archivo, delimiter=";")
            encabezado = next(lector, None)
            if encabezado != ["id_sala", "nombre", "capacidad"]:
                raise ValueError("El encabezado del archivo de salas no es valido.")
            for numero_linea, fila in enumerate(lector, start=2):
                if len(fila) != 3:
                    raise ValueError(f"Formato invalido en la linea {numero_linea}.")
                id_sala, capacidad = int(fila[0]), int(fila[2])
                tipo = tipo_sala([id_sala])
                if id_sala < 1 or not capacidad_valida(tipo, capacidad):
                    raise ValueError(f"Datos invalidos en la linea {numero_linea}.")
                salas_cargadas.append(
                    [id_sala, fila[1], capacidad, tipo]
                )
    except (OSError, UnicodeError, csv.Error, ValueError) as error:
        _persistencia_salas_habilitada = False
        print(f"No se pudo cargar el archivo de salas: {error}")
        return

    _actualizar_nombres_salas(salas_cargadas)
    salas.extend(salas_cargadas)


def _guardar_salas(matriz):
    if matriz is not salas:
        return
    if not _persistencia_salas_habilitada:
        print("No se guardaron los cambios porque el archivo de salas no se pudo leer.")
        return

    try:
        with open(ARCHIVO_TEMPORAL_SALAS, "w", encoding="utf-8", newline="") as archivo:
            escritor = csv.writer(archivo, delimiter=";")
            escritor.writerow(["id_sala", "nombre", "capacidad"])
            escritor.writerows(sala[:3] for sala in matriz)
        os.replace(ARCHIVO_TEMPORAL_SALAS, ARCHIVO_SALAS)
    except (OSError, csv.Error, TypeError, ValueError) as error:
        try:
            os.remove(ARCHIVO_TEMPORAL_SALAS)
        except FileNotFoundError:
            pass
        except OSError as error_limpieza:
            print(f"No se pudo limpiar el archivo temporal de salas: {error_limpieza}")
        print(f"No se pudieron guardar las salas: {error}")

_cargar_salas()


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
        nombre = salas[i][1]
        etiqueta = nombre
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
         [id_sala, nombre_sala, capacidad, tipo].
    pos: devuelve por pantalla la matriz de salas fomateada.
    '''
    print("=" * 48)
    print(f"{'Salas':35}")
    print("=" * 48)
    print(f"{'Id_Sala':<10}{'Nombre':<22}{'Capacidad':<12}{'Tipo':<12}")
    print("-" * 48)

    for i in range(len(matriz)):
        id_sala = matriz[i][0]
        nombre_sala = matriz[i][1]
        capacidad = matriz[i][2]
        tipo = tipo_sala(matriz[i])
        nombre_tipo = TIPOS_SALA[tipo]["nombre"] if tipo in TIPOS_SALA else "Sin tipo"
        print(f"{id_sala:<10}{nombre_sala:<22}{capacidad:<12}{nombre_tipo:<12}")


def agregar_Sala(matriz):
    '''
    pre: recibe una matriz de salas, donde cada fila representa una sala con sus datos
         [id_sala, nombre_sala, capacidad, tipo].
    pos: solicita los datos para registrar una nueva sala. si el id ya existe, muestra error y finaliza. si el id es unico, 
         agrega la sala con el nombre que corresponde a su posicion y muestra un mensaje de exito.
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

    tipo = ((id_sala - 1) // 2) % len(TIPOS_SALA) + 1
    print(f"Categoria asignada por ID: {TIPOS_SALA[tipo]['nombre']}")

    while True:
        capacidad_input = input("Ingresar capacidad o -1 para volver al menu principal: ").strip()
        if capacidad_input == "-1":
            return
        if validar_capacidad(capacidad_input):
            capacidad = convertir_entero(capacidad_input)
            if capacidad is None:
                print("La capacidad debe ser un numero entero positivo.")
                continue
            if not capacidad_valida(tipo, capacidad):
                datos_tipo = TIPOS_SALA[tipo]
                print(
                    f"La capacidad para salas {datos_tipo['nombre'].lower()} "
                    f"debe estar entre {datos_tipo['capacidad_minima']} "
                    f"y {datos_tipo['capacidad_maxima']} personas."
                )
                continue
            break
        datos_tipo = TIPOS_SALA[tipo]
        print(
            f"La capacidad debe ser un numero entre {datos_tipo['capacidad_minima']} "
            f"y {datos_tipo['capacidad_maxima']}."
        )

    nuevaSala = [id_sala, "", capacidad, tipo]
    matriz.append(nuevaSala)
    _actualizar_nombres_salas(matriz)
    actualizar_cantidad_tipos(matriz)
    _guardar_salas(matriz)
    print("Sala agregada correctamente")


def eliminar_Sala(matriz):
    '''
        pre: recibe una matriz de salas, donde cada fila representa una sala con sus datos
             [id_sala, nombre_sala, capacidad, tipo].
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
                _actualizar_nombres_salas(matriz)
                actualizar_cantidad_tipos(matriz)
                _guardar_salas(matriz)
                print("Sala eliminado correctamente")
                return
        print("No se encontro el id de Sala")
        return


def modificar_Sala(matriz):
    '''
        pre: recibe una matriz de salas, donde cada fila representa una sala con sus datos
             [id_sala, nombre_sala, capacidad, tipo].
        pos: solicita un id de sala por consola. si lo encuentra, permite modificar el id y la capacidad.
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

    nuevo_tipo = tipo_sala([nuevo_id])
    datos_tipo = TIPOS_SALA[nuevo_tipo]
    while True:
        capacidad_input = input(
            f"Ingresar nueva capacidad ({datos_tipo['capacidad_minima']}-"
            f"{datos_tipo['capacidad_maxima']}) o -1 para volver al menu principal: "
        ).strip()
        if capacidad_input == "-1":
            return
        capacidad = convertir_entero(capacidad_input) if validar_capacidad(capacidad_input) else None
        if capacidad is not None and capacidad_valida(nuevo_tipo, capacidad):
            break
        print(
            f"La capacidad para salas {datos_tipo['nombre'].lower()} debe estar entre "
            f"{datos_tipo['capacidad_minima']} y {datos_tipo['capacidad_maxima']} personas."
        )
    fila_encontrada[0] = nuevo_id
    fila_encontrada[2] = capacidad
    _actualizar_nombres_salas(matriz)
    actualizar_cantidad_tipos(matriz)
    _guardar_salas(matriz)
    print("Sala modificada correctamente")
