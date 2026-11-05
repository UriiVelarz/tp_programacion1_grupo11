import csv
import datetime
import os

import Funciones


ARCHIVO_RESERVAS = os.path.join(os.path.dirname(__file__), "reservas.txt")
ARCHIVO_TEMPORAL_RESERVAS = ARCHIVO_RESERVAS + ".tmp"
_persistencia_habilitada = True
reservas = []


def _cargar_reservas():
    '''
    pre: utiliza el archivo reservas.txt, que contiene los datos de las reservas
         registradas en formato CSV, separados por punto y coma.
    pos: lee y valida los datos del archivo, comprueba que el encabezado y los
         registros tengan el formato correcto y carga las reservas en la matriz
         correspondiente. Si encuentra errores, deshabilita la persistencia
         e informa el problema.
    '''
    global _persistencia_habilitada
    if not os.path.exists(ARCHIVO_RESERVAS):
        return

    reservas_cargadas = []
    try:
        with open(ARCHIVO_RESERVAS, "r", encoding="utf-8", newline="") as archivo:
            lector = csv.reader(archivo, delimiter=";")
            encabezado = next(lector, None)
            if encabezado is not None:
                encabezado = [columna.strip() for columna in encabezado]
            if encabezado != ["id_reserva", "tipo_sala", "id_usuario", "fecha", "inicio", "fin"]:
                raise ValueError("El encabezado del archivo de reservas no es valido.")
            for numero_linea, fila in enumerate(lector, start=2):
                fila = [valor.strip() for valor in fila]
                if len(fila) != 6:
                    raise ValueError(f"Formato invalido en la linea {numero_linea}.")
                id_reserva, tipo_sala, id_usuario = (int(valor) for valor in fila[:3])
                fecha, inicio, fin = fila[3:]
                if tipo_sala not in (1, 2, 3):
                    raise ValueError(f"Tipo de sala invalido en la linea {numero_linea}.")
                datetime.datetime.strptime(f"{fecha} {fin}", "%d/%m/%Y %H:%M")
                hora_inicio = datetime.datetime.strptime(inicio, "%H:%M")
                hora_fin = datetime.datetime.strptime(fin, "%H:%M")
                if hora_fin <= hora_inicio:
                    raise ValueError(f"Horario invalido en la linea {numero_linea}.")
                reservas_cargadas.append(
                    [id_reserva, tipo_sala, id_usuario, fecha, inicio, fin]
                )
    except (OSError, UnicodeError, csv.Error, ValueError) as error:
        _persistencia_habilitada = False
        print(f"No se pudo cargar el archivo de reservas: {error}")
        return

    reservas.extend(reservas_cargadas)
    limpiar_reservas_vencidas()


def limpiar_reservas_vencidas(ahora=None, persistir=True):
    '''
    pre: recibe opcionalmente la fecha y hora actual.
    pos: elimina de la matriz y del archivo las reservas cuyo horario de fin
         ya paso.
    '''
    ahora = datetime.datetime.now() if ahora is None else ahora
    reservas_vigentes = [
        reserva
        for reserva in reservas
        if datetime.datetime.strptime(
            f"{reserva[3]} {reserva[5]}", "%d/%m/%Y %H:%M"
        ) > ahora
    ]
    if len(reservas_vigentes) != len(reservas):
        reservas[:] = reservas_vigentes
        if persistir:
            _guardar_reservas(reservas)


def _guardar_reservas(matriz):
    ''' 
    pre: recibe una matriz de reservas, donde cada fila representa una reserva
         con sus datos [id_reserva, tipo_sala, id_usuario, fecha, inicio, fin].
    pos: guarda las reservas en el archivo reservas.txt en formato CSV,
         utilizando un archivo temporal para evitar la perdida de datos ante
         errores durante la escritura. Solo permite guardar la matriz original
         de reservas y verifica que la persistencia este habilitada.
    '''
    if matriz is not reservas:
        return
    limpiar_reservas_vencidas(persistir=False)
    if not _persistencia_habilitada:
        print("No se guardaron los cambios porque el archivo de reservas no se pudo leer.")
        return

    try:
        with open(ARCHIVO_TEMPORAL_RESERVAS, "w", encoding="utf-8", newline="") as archivo:
            escritor = csv.writer(archivo, delimiter=";")
            encabezado = ["id_reserva", "tipo_sala", "id_usuario", "fecha", "inicio", "fin"]
            filas = [[str(valor) for valor in reserva] for reserva in matriz]
            anchos = [
                max(len(encabezado[indice]), *(len(fila[indice]) for fila in filas))
                if filas else len(encabezado[indice])
                for indice in range(len(encabezado))
            ]
            escritor.writerow(
                [columna.ljust(anchos[indice]) for indice, columna in enumerate(encabezado)]
            )
            escritor.writerows(
                [
                    valor.ljust(anchos[indice])
                    for indice, valor in enumerate(fila)
                ]
                for fila in filas
            )
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
    '''
    pre: recibe un valor ingresado por el usuario.
    pos: verifica si el valor ingresado es "-1" para indicar que desea volver
         al menu principal. Devuelve True si desea regresar y False en caso contrario.
    '''
    if valor == "-1":
        print("Volviendo al menu principal...")
        return True
    return False


def convertir_entero(texto):
    ''' 
    pre: recibe una cadena de texto que representa un posible numero entero.
    pos: intenta convertir el texto a un numero entero y lo devuelve si la
         conversion es correcta. Si el valor no es valido, devuelve None.
    '''
    try:
        return int(texto)
    except ValueError:
        return None


def reservas_por_usuario(matriz, usuario):
    ''' 
    pre: recibe una matriz de reservas y el ID de un usuario.
    pos: filtra las reservas correspondientes al usuario indicado y devuelve
         una lista de tuplas que contiene el ID de cada reserva junto con
         sus datos completos.
    '''
    limpiar_reservas_vencidas()
    filtradas = Funciones.filtrar_reservas_por_usuario(matriz, usuario)
    return [(reserva[0], reserva) for reserva in filtradas]


def imprimir_Reservas(matriz, usuario=None):
    '''
    pre: recibe una matriz de reservas, donde cada fila representa una reserva con sus datos
         [id_reserva, sala, id_usuario, fecha, inicio, fin].
    pos: devuelve por pantalla la matriz de reservas formateada.
    '''

    limpiar_reservas_vencidas()
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
    '''
    pre: recibe el numero correspondiente a un mes del año.
    pos: devuelve la cantidad de dias que tiene el mes indicado, considerando
         febrero con 28 dias. Si el numero de mes no es valido, devuelve 0.
    '''
    dias_por_mes = {
        1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30,
        7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31
    }
    return dias_por_mes.get(mes, 0)


def pedir_fecha_reserva(etiqueta=""):
    '''
    pre: recibe opcionalmente una etiqueta para identificar la fecha que se
         solicita, por ejemplo, una fecha nueva durante la modificacion
         de una reserva.
    pos: solicita el año, el mes y el dia de la reserva, validando que la fecha
         exista y se encuentre dentro del periodo permitido para realizar
         reservas. Devuelve la fecha en formato dd/mm/aaaa o None si el usuario
         decide volver al menu principal.
    '''
    import Salas

    fecha_hoy = datetime.date.today()
    fecha_maxima = Salas.fecha_maxima_consulta(fecha_hoy)
    prefijo = f"{etiqueta} " if etiqueta else ""

    while True:
        anio_input = input(
            f"Ingresar {prefijo}año ({fecha_hoy.year} a {fecha_maxima.year}) "
            "o -1 para volver al menu principal: "
        ).strip()
        if volver_al_menu(anio_input):
            return None
        anio = convertir_entero(anio_input) if anio_input.isdigit() else None
        if anio is not None and fecha_hoy.year <= anio <= fecha_maxima.year:
            break
        print(f"El año debe estar entre {fecha_hoy.year} y {fecha_maxima.year}.")

    while True:
        mes_input = input(
            f"Ingresar {prefijo}mes (1 a 12) o -1 para volver al menu principal: "
        ).strip()
        if volver_al_menu(mes_input):
            return None
        mes = convertir_entero(mes_input) if mes_input.isdigit() else None
        if mes is not None and Salas.mes_consultable(
            anio, mes, fecha_hoy, fecha_maxima
        ):
            break
        print(
            f"No se puede reservar en meses o años anteriores. El mes debe estar "
            f"dentro del periodo {fecha_hoy:%d/%m/%Y} "
            f"a {fecha_maxima:%d/%m/%Y}."
        )

    while True:
        dia_input = input(
            f"Ingresar {prefijo}dia o -1 para volver al menu principal: "
        ).strip()
        if volver_al_menu(dia_input):
            return None
        dia = convertir_entero(dia_input) if dia_input.isdigit() else None
        try:
            fecha = datetime.date(anio, mes, dia)
        except (TypeError, ValueError):
            fecha = None
        if fecha is not None and fecha_hoy <= fecha <= fecha_maxima:
            return fecha.strftime("%d/%m/%Y")
        print(
            f"La fecha debe ser valida y estar entre {fecha_hoy:%d/%m/%Y} "
            f"y {fecha_maxima:%d/%m/%Y}; no se permiten fechas pasadas."
        )


def pedir_opcion(mensaje, opciones_validos):
    '''
    pre: recibe un mensaje para solicitar una opcion y una coleccion con los
         valores permitidos.
    pos: solicita una opcion al usuario y verifica que pertenezca a los valores
         permitidos. Devuelve la opcion ingresada si es valida o "-1" si desea
         volver al menu principal.
    '''
    while True:
        valor = input(mensaje).strip()
        if valor == "-1":
            print("Volviendo al menu principal...")
            return "-1"
        if valor in opciones_validos:
            return valor
        print("Opcion invalida. Intente nuevamente.")


def hay_conflicto_reserva_usuario(matriz, usuario, fecha, inicio, reserva_excluida=None):
    '''
    pre: recibe una matriz de reservas, el ID de un usuario, una fecha, una hora
         de inicio y opcionalmente una reserva que debe excluirse de la comparacion.
    pos: verifica si el usuario ya tiene una reserva registrada en la misma fecha
         y horario de inicio. Devuelve True si encuentra un conflicto y False
         en caso contrario.
    '''
    usuario_id = str(usuario)
    for reserva in matriz:
        if reserva is reserva_excluida:
            continue
        if str(reserva[2]) == usuario_id and reserva[3] == fecha and reserva[4] == inicio:
            return True
    return False


def contar_reservas_solapadas(
    matriz, tipo_sala, fecha, inicio, fin, reserva_excluida=None, f=0
):
    '''
    pre: recibe una matriz de reservas, un tipo de sala, una fecha, un horario
         de inicio y fin, una reserva opcional que debe excluirse y una posicion
         inicial para recorrer la matriz.
    pos: cuenta recursivamente las reservas del mismo tipo de sala y fecha cuyos
         horarios se superponen con el periodo solicitado. Devuelve la cantidad
         de reservas que ocupan ese horario, sin considerar la reserva excluida.
    '''
    if f == len(matriz):
        return 0

    reserva = matriz[f]
    cantidad_resto = contar_reservas_solapadas(
        matriz, tipo_sala, fecha, inicio, fin, reserva_excluida, f + 1
    )

    if reserva is reserva_excluida or reserva[1] != tipo_sala or reserva[3] != fecha:
        return cantidad_resto

    inicio_solicitado = int(inicio[:2])
    fin_solicitado = int(fin[:2])
    inicio_existente = int(reserva[4][:2])
    fin_existente = int(reserva[5][:2])
    if inicio_solicitado < fin_existente and inicio_existente < fin_solicitado:
        return 1 + cantidad_resto
    return cantidad_resto

def hay_capacidad_disponible(matriz, tipo_sala, fecha, inicio, fin, reserva_excluida=None):
    '''
    pre: recibe una matriz de reservas, un tipo de sala, una fecha, un horario
         de inicio y fin y opcionalmente una reserva que debe excluirse del calculo.
    pos: obtiene la cantidad de salas disponibles del tipo solicitado y la compara
         con las reservas que se superponen en ese horario. Devuelve True si
         todavia hay capacidad disponible y False en caso contrario.
    '''
    import Salas

    capacidad = Salas.cantidad_salas_tipo(tipo_sala)
    ocupadas = contar_reservas_solapadas(matriz, tipo_sala, fecha, inicio, fin, reserva_excluida)
    return ocupadas < capacidad


def realizar_Reserva(matriz, id_usuario=0):
    '''
    pre: recibe una matriz de reservas y opcionalmente el ID del usuario que
         desea realizar una reserva.
    pos: solicita el tipo de sala, la fecha y la hora de inicio, validando que
         los datos sean correctos, que el usuario no tenga otra reserva en el
         mismo horario y que exista capacidad disponible. Genera un ID correlativo,
         agrega la nueva reserva a la matriz y guarda los cambios realizados.
    '''

    limpiar_reservas_vencidas()
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

    fecha = pedir_fecha_reserva()
    if fecha is None:
        return

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
    pre: recibe una matriz de reservas y el ID del usuario que desea cancelar
         una reserva.
    pos: muestra las reservas del usuario, solicita el ID de la reserva que
         desea eliminar y verifica que le pertenezca. Si existe, la elimina
         de la matriz original y guarda los cambios realizados. Si no se
         encuentra, informa el problema.
    '''

    limpiar_reservas_vencidas()
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
    pre: recibe una matriz de reservas y el ID del usuario que desea modificar
         una reserva.
    pos: muestra las reservas del usuario, solicita el ID de la reserva y permite
         modificar el tipo de sala, la fecha y el horario. Verifica que no existan
         conflictos con otras reservas del usuario y que haya capacidad disponible.
         Si los nuevos datos son validos, actualiza la reserva original y guarda
         los cambios realizados.
    '''

    limpiar_reservas_vencidas()
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

    nueva_fecha = pedir_fecha_reserva("nuevo")
    if nueva_fecha is None:
        return

    while True:
        hora_input = input("Ingresar nueva hora de inicio (formato 24hs) o -1 para volver al menu principal: ").strip()
        if volver_al_menu(hora_input):
            return
        if hora_input.isdigit():
            hora = convertir_entero(hora_input)
            if hora is not None and 9 <= hora <= 16:
                break
        print("La hora debe estar entre 9 y 16 para reservar bloques de 2 horas.")

    nuevo_inicio = f"{hora:02d}:00"
    if hay_conflicto_reserva_usuario(matriz, usuario, nueva_fecha, nuevo_inicio, reserva_encontrada):
        print("No puedes reservar en un dia y horario que ya habias reservado antes.")
        return

    nuevo_fin = f"{hora + 2:02d}:00"
    if not hay_capacidad_disponible(matriz, nuevo_sala, nueva_fecha, nuevo_inicio, nuevo_fin, reserva_encontrada):
        print("No quedan salas de ese tipo disponibles en ese horario.")
        return

    reserva_encontrada[1] = nuevo_sala
    reserva_encontrada[3] = nueva_fecha
    reserva_encontrada[4] = nuevo_inicio
    reserva_encontrada[5] = nuevo_fin
    _guardar_reservas(matriz)

    print("Reserva modificada correctamente")


_cargar_reservas()