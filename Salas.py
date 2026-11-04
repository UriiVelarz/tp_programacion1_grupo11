import csv
import json
import os
import re
import datetime 
from Reservas import reservas

ARCHIVO_SALAS = os.path.join(os.path.dirname(__file__), "salas.txt")
ARCHIVO_CONFIGURACION_SALAS = os.path.join(
    os.path.dirname(__file__), "tipo salas.json"
)
ARCHIVO_TEMPORAL_SALAS = ARCHIVO_SALAS + ".tmp"
_persistencia_salas_habilitada = True
salas = []


def _cargar_configuracion_salas():
    try:
        with open(ARCHIVO_CONFIGURACION_SALAS, "r", encoding="utf-8") as archivo:
            configuracion = json.load(archivo)
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise RuntimeError(
            f"No se pudo cargar la configuracion de salas: {error}"
        ) from error

    if not isinstance(configuracion, dict):
        raise ValueError("La configuracion de salas debe ser un objeto JSON.")

    tipos_configurados = configuracion.get("tipos_sala")
    if not isinstance(tipos_configurados, dict) or not tipos_configurados:
        raise ValueError("La configuracion debe incluir al menos un tipo de sala.")

    tipos_sala = {}
    for id_texto, datos in tipos_configurados.items():
        try:
            tipo = int(id_texto)
        except (TypeError, ValueError) as error:
            raise ValueError(f"Tipo de sala invalido en la configuracion: {id_texto}.") from error
        if tipo < 1 or str(tipo) != id_texto or not isinstance(datos, dict):
            raise ValueError(f"Tipo de sala invalido en la configuracion: {id_texto}.")

        nombre = datos.get("nombre")
        capacidad_minima = datos.get("capacidad_minima")
        capacidad_maxima = datos.get("capacidad_maxima")
        if (
            not isinstance(nombre, str)
            or not nombre.strip()
            or type(capacidad_minima) is not int
            or type(capacidad_maxima) is not int
            or capacidad_minima < 1
            or capacidad_maxima < capacidad_minima
        ):
            raise ValueError(f"Datos invalidos para el tipo de sala {tipo}.")

        tipos_sala[tipo] = {
            "nombre": nombre,
            "cantidad": 0,
            "capacidad_minima": capacidad_minima,
            "capacidad_maxima": capacidad_maxima,
        }

    return tipos_sala


TIPOS_SALA = _cargar_configuracion_salas()

COLOR_VERDE = "\033[32m"
COLOR_AMARILLO = "\033[33m"
COLOR_AZUL = "\033[34m"
COLOR_ROJO = "\033[31m"
COLOR_RESET = "\033[0m"


def limpiar_ansi(texto):
    '''
    pre: recibe un texto que puede contener codigos de color ANSI.
    pos: devuelve el texto sin los codigos de color ANSI.   
    '''
    return re.sub(r"\x1b\[[0-9;]*m", "", texto)


def validar_id_sala(texto):
    '''
    pre: recibe un texto que representa el identificador de una sala.
    pos: devuelve True si el texto contiene un numero entero positivo sin ceros iniciales y False en caso contrario.
    '''
    return re.fullmatch(r"[1-9]\d*", texto) is not None


def validar_capacidad(texto):
    '''
    pre: recibe un texto que representa la capacidad de una sala.
    pos: devuelve True si el texto contiene un numero entero positivo sin ceros iniciales y False en caso contrario.
    '''
    return re.fullmatch(r"[1-9]\d*", texto) is not None


def convertir_entero(texto):
    '''
    pre: recibe un texto que se desea convertir a un numero entero.
    pos: devuelve el valor convertido a entero o None si ocurre un error de conversion.
    '''
    try:
        return int(texto)
    except ValueError:
        return None


def formatear_celda(texto, ancho):
    '''
    pre: recibe un texto y el ancho deseado para una celda.
    pos: devuelve el texto completado con espacios hasta alcanzar el ancho indicado, sin contar los codigos ANSI.
    '''
    texto_limpio = limpiar_ansi(texto)
    espacios = max(0, ancho - len(texto_limpio))
    return texto + (" " * espacios)


def tipo_sala(sala):
    '''
    pre: recibe una sala representada por una lista con sus datos.
    pos: devuelve el tipo de sala almacenado en la posicion 3 si es valido; de lo contrario, calcula el tipo segun el id de la sala.
    '''
    if len(sala) > 3 and sala[3] in TIPOS_SALA:
        return sala[3]
    return ((sala[0] - 1) // 2) % len(TIPOS_SALA) + 1


def capacidad_valida(tipo, capacidad):
    '''
    pre: recibe el tipo de sala y la capacidad que se desea validar.
    pos: devuelve True si la capacidad esta dentro del minimo y maximo permitido para ese tipo de sala y False en caso contrario.
    '''
    datos_tipo = TIPOS_SALA[tipo]
    return datos_tipo["capacidad_minima"] <= capacidad <= datos_tipo["capacidad_maxima"]


def _letra_sala(indice):
    '''
    pre: recibe un indice entero que representa la posicion de una sala.
    pos: devuelve una letra o combinacion de letras equivalente a esa posicion, comenzando desde A.
    '''
    letras = ""
    numero = indice + 1
    while numero:
        numero, resto = divmod(numero - 1, 26)
        letras = chr(ord("A") + resto) + letras
    return letras


def _actualizar_nombres_salas(matriz):
    '''
    pre: recibe una matriz de salas, donde cada fila contiene el id, nombre, capacidad y tipo.
    pos: ordena las salas por tipo e id, actualiza el tipo y asigna nombres consecutivos a cada sala segun su categoria.
    '''
    cantidades = {tipo: 0 for tipo in TIPOS_SALA}
    for sala in sorted(matriz, key=lambda elemento: (tipo_sala(elemento), elemento[0])):
        tipo = tipo_sala(sala)
        sala[3] = tipo
        sala[1] = f"Sala {TIPOS_SALA[tipo]['nombre'].lower()} {_letra_sala(cantidades[tipo])}"
        cantidades[tipo] += 1


def _cargar_salas():
    '''
    pre: utiliza el archivo de salas definido en ARCHIVO_SALAS y la estructura global salas.
    pos: lee y valida los datos del archivo, carga las salas en la matriz global y actualiza sus nombres. si ocurre un error de lectura o validacion, deshabilita la persistencia e informa el problema.
    '''
    global _persistencia_salas_habilitada
    if not os.path.exists(ARCHIVO_SALAS):
        print(f"No se encontro el archivo de salas: {ARCHIVO_SALAS}")
        return

    salas_cargadas = []
    try:
        with open(ARCHIVO_SALAS, "r", encoding="utf-8", newline="") as archivo:
            lector = csv.reader(archivo, delimiter=";")
            encabezado = next(lector, None)
            if encabezado not in (
                ["id_sala", "nombre", "capacidad"],
                ["id_sala", "nombre", "capacidad", "tipo"],
            ):
                raise ValueError("El encabezado del archivo de salas no es valido.")
            for numero_linea, fila in enumerate(lector, start=2):
                if len(fila) != len(encabezado):
                    raise ValueError(f"Formato invalido en la linea {numero_linea}.")
                id_sala, capacidad = int(fila[0]), int(fila[2])
                tipo = int(fila[3]) if len(fila) == 4 else tipo_sala([id_sala])
                if tipo not in TIPOS_SALA:
                    raise ValueError(f"Tipo de sala invalido en la linea {numero_linea}.")
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
    '''
    pre: recibe una matriz de salas con los datos de cada una.
    pos: guarda las salas en un archivo temporal y luego reemplaza el archivo original. solo permite guardar la matriz global salas y, si ocurre un error, intenta eliminar el archivo temporal e informa el problema.
    '''
    if matriz is not salas:
        return
    if not _persistencia_salas_habilitada:
        print("No se guardaron los cambios porque el archivo de salas no se pudo leer.")
        return

    try:
        with open(ARCHIVO_TEMPORAL_SALAS, "w", encoding="utf-8", newline="") as archivo:
            escritor = csv.writer(archivo, delimiter=";")
            escritor.writerow(["id_sala", "nombre", "capacidad", "tipo"])
            escritor.writerows(sala[:3] + [tipo_sala(sala)] for sala in matriz)
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
    '''
    pre: recibe un tipo de sala y opcionalmente una matriz de salas.
    pos: devuelve la cantidad de salas que pertenecen al tipo indicado. si no recibe una matriz, utiliza la matriz global salas.
    '''
    matriz = salas if matriz is None else matriz
    return sum(1 for sala in matriz if tipo_sala(sala) == tipo)


def actualizar_cantidad_tipos(matriz=None):
    '''
    pre: recibe opcionalmente una matriz de salas.
    pos: actualiza la cantidad de salas registradas para cada tipo dentro del diccionario global TIPOS_SALA. si no recibe una matriz, utiliza la matriz global salas.
    '''
    matriz = salas if matriz is None else matriz
    for tipo in TIPOS_SALA:
        TIPOS_SALA[tipo]["cantidad"] = cantidad_salas_tipo(tipo, matriz)


actualizar_cantidad_tipos()


def fecha_maxima_consulta(fecha_actual=None):
    '''
    pre: recibe opcionalmente una fecha actual.
    pos: devuelve la fecha maxima que se puede consultar, correspondiente a seis meses despues de la fecha recibida o de la fecha actual del sistema.
    '''
    fecha_actual = fecha_actual or datetime.date.today()
    mes = fecha_actual.month + 6
    anio = fecha_actual.year + (mes - 1) // 12
    mes = (mes - 1) % 12 + 1
    ultimo_dia = obtener_dias_mes(mes)
    dia = min(fecha_actual.day, ultimo_dia)
    return datetime.date(anio, mes, dia)


def obtener_dias_mes(mes):
    '''
    pre: recibe el numero de un mes del año.
    pos: devuelve la cantidad de dias correspondiente al mes indicado o 0 si el numero de mes no es valido.
    '''
    dias_por_mes = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
    return dias_por_mes.get(mes, 0)


def mes_consultable(anio, mes, fecha_hoy=None, fecha_maxima=None):
    '''
        pre: recibe un año, un mes y opcionalmente las fechas de inicio y limite de consulta.
        pos: devuelve True si el mes se encuentra dentro del periodo consultable y False si las fechas o el mes no son validos.
    '''
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
    '''
    pre: recibe un año, mes, dia y tipo de sala.
    pos: devuelve una tupla con la cantidad de reservas registradas para esa fecha y tipo de sala, y la cantidad de salas disponibles de ese tipo.
    '''
    fecha = f"{dia:02d}/{mes:02d}/{anio}"
    cantidad = 0
    for reserva in reservas:
        if reserva[3] == fecha and reserva[1] == tamaño:
            cantidad += 1
    return cantidad, cantidad_salas_tipo(tamaño)


def estado_horario(anio, mes, dia, tamaño, hora_inicio):
    '''
    pre: recibe una fecha, un tipo de sala y la hora de inicio de un bloque horario de dos horas.
    pos: cuenta las reservas que se superponen con el horario indicado y devuelve un texto coloreado que informa si esta libre, parcialmente ocupada u ocupada.
    '''
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
    '''
    pre: utiliza las reservas, los tipos de sala y las funciones de consulta de fechas y disponibilidad.
    pos: solicita un año, mes, dia de inicio y cantidad de dias dentro del periodo consultable. luego muestra por pantalla la disponibilidad de los distintos tipos de sala en bloques horarios de dos horas.
    '''
    from Reservas import limpiar_reservas_vencidas

    limpiar_reservas_vencidas()
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
    pre: recibe una matriz de salas, donde cada fila representa una sala con sus datos [id_sala, nombre_sala, capacidad, tipo].
    pos: muestra por pantalla los datos de las salas en formato de tabla, incluyendo su identificador, nombre, capacidad y tipo.
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
    pre: recibe una matriz de salas, donde cada fila representa una sala con sus datos [id_sala, nombre_sala, capacidad, tipo].
    pos: solicita el tipo de sala que se desea agregar. asigna un id consecutivo y la capacidad maxima permitida para ese tipo, actualiza los nombres y las cantidades, guarda los cambios y muestra un mensaje de exito.
    '''
    while True:
        print("Seleccione el tipo de sala:")
        for tipo, datos_tipo in TIPOS_SALA.items():
            print(f"{tipo}. {datos_tipo['nombre']}")
        tipo_input = input("Ingresar opcion o -1 para volver al menu principal: ").strip()
        if tipo_input == "-1":
            return
        tipo = convertir_entero(tipo_input)
        if tipo in TIPOS_SALA:
            break
        print("Opcion invalida. Seleccione 1, 2 o 3.")

    id_sala = max((sala[0] for sala in matriz), default=0) + 1
    capacidad = TIPOS_SALA[tipo]["capacidad_maxima"]
    nuevaSala = [id_sala, "", capacidad, tipo]
    matriz.append(nuevaSala)
    _actualizar_nombres_salas(matriz)
    actualizar_cantidad_tipos(matriz)
    _guardar_salas(matriz)
    print("Sala agregada correctamente")


def eliminar_Sala(matriz):
    '''
    pre: recibe una matriz de salas, donde cada fila representa una sala con sus datos [id_sala, nombre_sala, capacidad, tipo].
    pos: solicita el id de una sala y, si existe, la elimina de la matriz, actualiza los nombres y las cantidades, guarda los cambios y muestra un mensaje de exito. si no existe, informa el error.
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
    pre: recibe una matriz de salas, donde cada fila representa una sala con sus datos [id_sala, nombre_sala, capacidad, tipo].
    pos: solicita el id de una sala y permite modificar su capacidad dentro del rango permitido para su tipo. luego actualiza los nombres y las cantidades, guarda los cambios y muestra un mensaje de exito.
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

    nuevo_tipo = tipo_sala(fila_encontrada)
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
    fila_encontrada[2] = capacidad
    _actualizar_nombres_salas(matriz)
    actualizar_cantidad_tipos(matriz)
    _guardar_salas(matriz)
    print("Sala modificada correctamente")