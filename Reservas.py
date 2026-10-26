import csv
import os

import Funciones


ARCHIVO_RESERVAS = os.path.join(os.path.dirname(__file__), "reservas.txt")
ARCHIVO_TEMPORAL_RESERVAS = ARCHIVO_RESERVAS + ".tmp"
_persistencia_habilitada = True
reservas = []


def _cargar_reservas():
    global _persistencia_habilitada
    if not os.path.exists(ARCHIVO_RESERVAS):
        return

    reservas_cargadas = []
    try:
        with open(ARCHIVO_RESERVAS, "r", encoding="utf-8", newline="") as archivo:
            lector = csv.reader(archivo, delimiter=";")
            encabezado = next(lector, None)
            if encabezado != ["id_reserva", "tipo_sala", "id_usuario", "fecha", "inicio", "fin"]:
                raise ValueError("El encabezado del archivo de reservas no es valido.")
            for numero_linea, fila in enumerate(lector, start=2):
                if len(fila) != 6:
                    raise ValueError(f"Formato invalido en la linea {numero_linea}.")
                id_reserva, tipo_sala, id_usuario = (int(valor) for valor in fila[:3])
                fecha, inicio, fin = fila[3:]
                if tipo_sala not in (1, 2, 3):
                    raise ValueError(f"Tipo de sala invalido en la linea {numero_linea}.")
                reservas_cargadas.append(
                    [id_reserva, tipo_sala, id_usuario, fecha, inicio, fin]
                )
    except (OSError, UnicodeError, csv.Error, ValueError) as error:
        _persistencia_habilitada = False
        print(f"No se pudo cargar el archivo de reservas: {error}")
        return

    reservas.extend(reservas_cargadas)


def _guardar_reservas(matriz):
    if matriz is not reservas:
        return
    if not _persistencia_habilitada:
        print("No se guardaron los cambios porque el archivo de reservas no se pudo leer.")
        return

    try:
        with open(ARCHIVO_TEMPORAL_RESERVAS, "w", encoding="utf-8", newline="") as archivo:
            escritor = csv.writer(archivo, delimiter=";")
            escritor.writerow(
                ["id_reserva", "tipo_sala", "id_usuario", "fecha", "inicio", "fin"]
            )
            escritor.writerows(matriz)
        os.replace(ARCHIVO_TEMPORAL_RESERVAS, ARCHIVO_RESERVAS)
    except (OSError, csv.Error, TypeError, ValueError) as error:
        try:
            os.remove(ARCHIVO_TEMPORAL_RESERVAS)
        except FileNotFoundError:
            pass
        except OSError as error_limpieza:
            print(f"No se pudo limpiar el archivo temporal: {error_limpieza}")
        print(f"No se pudieron guardar las reservas: {error}")


def volver_al_menu(valor):
    if valor == "-1":
        print("Volviendo al menu principal...")
        return True
    return False


def convertir_entero(texto):
    try:
        return int(texto)
    except ValueError:
        return None


def reservas_por_usuario(matriz, usuario):
    filtradas = Funciones.filtrar_reservas_por_usuario(matriz, usuario)
    return [(reserva[0], reserva) for reserva in filtradas]


def imprimir_Reservas(matriz, usuario=None):
    '''
    pre: recibe una matriz de reservas, donde cada fila representa una reserva con sus datos
         [id_reserva, sala, id_usuario, fecha, inicio, fin].
    pos: devuelve por pantalla la matriz de reservas formateada.
    '''

    print("=" * 70)
    print(f"{'Reservas':42}")
    print("=" * 70)
    print(f"{'Id':<12}{'Sala':<8}{'Usuario':<12}{'Fecha':<14}{'Inicio':<12}{'Fin':<12}")
    print("-" * 70)

    reservas_ordenadas = Funciones.ordenar_reservas_por_fecha(matriz)

    if usuario is not None:
        lista = reservas_por_usuario(reservas_ordenadas, usuario)
        if not lista:
            print("No hay reservas para este usuario.")
            return
        for id_reserva, reserva in lista:
            _, sala, id_usuario, fecha, inicio, fin = reserva
            print(f"{id_reserva:<12}{sala:<8}{id_usuario:<12}{fecha:<14}{inicio:<12}{fin:<12}")
        return

    for reserva in reservas_ordenadas:
        _, sala, id_usuario, fecha, inicio, fin = reserva
        print(f"{_:<12}{sala:<8}{id_usuario:<12}{fecha:<14}{inicio:<12}{fin:<12}")


def obtener_dias_del_mes(mes):
    dias_por_mes = {
        1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30,
        7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31
    }
    return dias_por_mes.get(mes, 0)


def pedir_opcion(mensaje, opciones_validos):
    while True:
        valor = input(mensaje).strip()
        if valor == "-1":
            print("Volviendo al menu principal...")
            return "-1"
        if valor in opciones_validos:
            return valor
        print("Opcion invalida. Intente nuevamente.")


def hay_conflicto_reserva_usuario(matriz, usuario, fecha, inicio, reserva_excluida=None):
    usuario_id = str(usuario)
    for reserva in matriz:
        if reserva is reserva_excluida:
            continue
        if str(reserva[2]) == usuario_id and reserva[3] == fecha and reserva[4] == inicio:
            return True
    return False


def contar_reservas_solapadas(
    matriz, tipo_sala, fecha, inicio, fin, reserva_excluida=None
):
    inicio_solicitado = int(inicio[:2])
    fin_solicitado = int(fin[:2])
    cantidad = 0
    for reserva in matriz:
        if reserva is reserva_excluida or reserva[1] != tipo_sala or reserva[3] != fecha:
            continue
        inicio_existente = int(reserva[4][:2])
        fin_existente = int(reserva[5][:2])
        if inicio_solicitado < fin_existente and inicio_existente < fin_solicitado:
            cantidad += 1
    return cantidad


def hay_capacidad_disponible(
    matriz, tipo_sala, fecha, inicio, fin, reserva_excluida=None
):
    import Salas

    capacidad = Salas.cantidad_salas_tipo(tipo_sala)
    ocupadas = contar_reservas_solapadas(
        matriz, tipo_sala, fecha, inicio, fin, reserva_excluida
    )
    return ocupadas < capacidad


def realizar_Reserva(matriz, id_usuario=0):
    '''
    pre: recibe una matriz de reservas, donde cada fila representa una reserva con sus datos
         [id_reserva, sala, id_usuario, fecha, inicio, fin].
    pos: genera automaticamente un id correlativo para la reserva del usuario actual,
         solicita el tamaño de sala, la fecha y la hora, y guarda la reserva.
    '''

    import Salas

    opciones = []
    print("Selecciona el tamaño de la sala:")
    for tipo, datos in Salas.TIPOS_SALA.items():
        cantidad = Salas.cantidad_salas_tipo(tipo)
        print(f"{tipo}. {datos['nombre']} ({cantidad} salas)")
        if cantidad:
            opciones.append(str(tipo))

    if not opciones:
        print("No hay salas disponibles para reservar.")
        return
    opcion_sala = pedir_opcion("Ingresar opcion: ", tuple(opciones))
    if opcion_sala == "-1":
        return
    id_sala = int(opcion_sala)

    while True:
        anio_input = input("Ingresar año (2026 o 2027) o -1 para volver al menu principal: ").strip()
        if volver_al_menu(anio_input):
            return
        if anio_input.isdigit():
            anio = convertir_entero(anio_input)
            if anio is not None and anio in (2026, 2027):
                break
        print("El año debe ser 2026 o 2027.")

    while True:
        mes_input = input("Ingresar mes (1 a 12) o -1 para volver al menu principal: ").strip()
        if volver_al_menu(mes_input):
            return
        if mes_input.isdigit():
            mes = convertir_entero(mes_input)
            if mes is not None and 1 <= mes <= 12:
                break
        print("El mes debe estar entre 1 y 12.")

    while True:
        dia_input = input("Ingresar dia o -1 para volver al menu principal: ").strip()
        if volver_al_menu(dia_input):
            return
        if dia_input.isdigit():
            dia = convertir_entero(dia_input)
            if dia is not None:
                max_dia = obtener_dias_del_mes(mes)
                if 1 <= dia <= max_dia:
                    break
        print(f"El dia debe estar entre 1 y {obtener_dias_del_mes(mes)} para ese mes.")

    while True:
        hora_input = input("Ingresar hora de inicio (entre 9 y 16, formato 24hs) o -1 para volver al menu principal: ").strip()
        if volver_al_menu(hora_input):
            return
        if hora_input.isdigit():
            hora = convertir_entero(hora_input)
            if hora is not None and 9 <= hora <= 16:
                break
        print("La hora debe estar entre 9 y 16 para reservar bloques de 2 horas.")

    hora_fin = hora + 2
    fecha = f"{dia:02d}/{mes:02d}/{anio}"
    inicio = f"{hora:02d}:00"
    fin = f"{hora_fin:02d}:00"

    if hay_conflicto_reserva_usuario(matriz, id_usuario, fecha, inicio):
        print("No puedes reservar en un dia y horario que ya habias reservado antes.")
        return

    if not hay_capacidad_disponible(matriz, id_sala, fecha, inicio, fin):
        print("No quedan salas de ese tipo disponibles en ese horario.")
        return

    contador = max((reserva[0] for reserva in matriz), default=0) + 1

    nuevaReserva = [contador, id_sala, id_usuario, fecha, inicio, fin]
    matriz.append(nuevaReserva)
    _guardar_reservas(matriz)
    print("Reserva agregada correctamente")
    print(f"Detalle: Sala {id_sala} - Fecha {fecha} - Inicio {inicio} - Fin {fin}")


def eliminar_Reserva(matriz, usuario=None):
    '''
        pre: recibe una matriz de reservas, donde cada fila representa una reserva con sus datos
             [id_reserva, sala, id_usuario, fecha, inicio, fin].
        pos: solicita un id de reserva por consola. si el id existe en la matriz, elimina la reserva de 
             la matriz original y muestra un mensaje de exito. si no existe, muestra un mensaje de error.
    '''

    if usuario is None:
        print("Debe indicar el usuario para cancelar la reserva.")
        return

    print("Estas son tus reservas:")
    imprimir_Reservas(matriz, usuario)

    while True:
        id_input = input("Ingresar el numero de reserva a cancelar o -1 para volver al menu principal: ")
        if volver_al_menu(id_input):
            return
        if id_input.isdigit():
            id_reserva = convertir_entero(id_input)
            if id_reserva is not None:
                break
        print("Debes ingresar un numero valido.")

    lista = reservas_por_usuario(matriz, usuario)

    for id_guardado, reserva in lista:
        if id_guardado == id_reserva:
            matriz.remove(reserva)
            _guardar_reservas(matriz)
            print("Reserva eliminada correctamente")
            return

    print("No se encontro esa reserva para este usuario")


def modificar_Reserva(matriz, usuario=None):
    '''
        pre: recibe una matriz de reservas, donde cada fila representa una reserva con sus datos
             [id_reserva, sala, id_usuario, fecha, inicio, fin].
        pos: solicita un id de reserva por consola. si lo encuentra, pide los nuevos datos 
             (sala, fecha, inicio y fin) para sobreescribir los valores originales en la matriz.
             si el id no existe, la funcion termina sin realizar cambios.
    '''

    if usuario is None:
        print("Debe indicar el usuario para modificar la reserva.")
        return

    lista = reservas_por_usuario(matriz, usuario)
    if not lista:
        print("No tenes reservas para modificar.")
        return

    print("Estas son tus reservas:")
    imprimir_Reservas(matriz, usuario)

    while True:
        id_buscado_input = input("Ingresar el numero de reserva a modificar o -1 para volver al menu principal: ")
        if volver_al_menu(id_buscado_input):
            return
        if id_buscado_input.isdigit():
            id_buscado = convertir_entero(id_buscado_input)
            if id_buscado is not None:
                break
        print("Debes ingresar un numero valido.")

    reserva_encontrada = None
    for id_guardado, reserva in lista:
        if id_guardado == id_buscado:
            reserva_encontrada = reserva
            break

    if reserva_encontrada is None:
        print("Reserva no encontrada. Intente nuevamente.")
        return

    import Salas

    opciones = []
    print("Selecciona el nuevo tamaño de la sala:")
    for tipo, datos in Salas.TIPOS_SALA.items():
        cantidad = Salas.cantidad_salas_tipo(tipo)
        print(f"{tipo}. {datos['nombre']} ({cantidad} salas)")
        if cantidad:
            opciones.append(str(tipo))

    if not opciones:
        print("No hay salas disponibles para reservar.")
        return
    nuevo_sala_input = pedir_opcion("Ingresar opcion: ", tuple(opciones))
    if nuevo_sala_input == "-1":
        return
    nuevo_sala = int(nuevo_sala_input)

    while True:
        anio_input = input("Ingresar nuevo año (2026 o 2027) o -1 para volver al menu principal: ").strip()
        if volver_al_menu(anio_input):
            return
        if anio_input.isdigit():
            anio = convertir_entero(anio_input)
            if anio is not None and anio in (2026, 2027):
                break
        print("El año debe ser 2026 o 2027.")

    while True:
        mes_input = input("Ingresar nuevo mes (1 a 12) o -1 para volver al menu principal: ").strip()
        if volver_al_menu(mes_input):
            return
        if mes_input.isdigit():
            mes = convertir_entero(mes_input)
            if mes is not None and 1 <= mes <= 12:
                break
        print("El mes debe estar entre 1 y 12.")

    while True:
        dia_input = input("Ingresar nuevo dia o -1 para volver al menu principal: ").strip()
        if volver_al_menu(dia_input):
            return
        if dia_input.isdigit():
            dia = convertir_entero(dia_input)
            if dia is not None:
                max_dia = obtener_dias_del_mes(mes)
                if 1 <= dia <= max_dia:
                    break
        print(f"El dia debe estar entre 1 y {obtener_dias_del_mes(mes)} para ese mes.")

    while True:
        hora_input = input("Ingresar nueva hora de inicio (formato 24hs) o -1 para volver al menu principal: ").strip()
        if volver_al_menu(hora_input):
            return
        if hora_input.isdigit():
            hora = convertir_entero(hora_input)
            if hora is not None and 9 <= hora <= 16:
                break
        print("La hora debe estar entre 9 y 16 para reservar bloques de 2 horas.")

    nueva_fecha = f"{dia:02d}/{mes:02d}/{anio}"
    nuevo_inicio = f"{hora:02d}:00"
    if hay_conflicto_reserva_usuario(matriz, usuario, nueva_fecha, nuevo_inicio, reserva_encontrada):
        print("No puedes reservar en un dia y horario que ya habias reservado antes.")
        return

    nuevo_fin = f"{hora + 2:02d}:00"
    if not hay_capacidad_disponible(
        matriz, nuevo_sala, nueva_fecha, nuevo_inicio, nuevo_fin, reserva_encontrada
    ):
        print("No quedan salas de ese tipo disponibles en ese horario.")
        return

    reserva_encontrada[1] = nuevo_sala
    reserva_encontrada[3] = nueva_fecha
    reserva_encontrada[4] = nuevo_inicio
    reserva_encontrada[5] = nuevo_fin
    _guardar_reservas(matriz)

    print("Reserva modificada correctamente")


_cargar_reservas()