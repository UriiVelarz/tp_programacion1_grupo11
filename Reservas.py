reservas = [
    [1000, 1, 1234, "01/09/2026", "08:00", "10:00"],
    [1001, 2, 8254, "01/09/2026", "08:30", "10:30"],
    [1002, 3, 4567, "01/09/2026", "09:00", "11:00"],
    [1003, 1, 2130, "01/09/2026", "10:00", "12:00"],
    [1004, 4, 1101, "02/09/2026", "08:00", "10:00"],
    [1005, 2, 3653, "02/09/2026", "10:00", "12:00"],
    [1006, 4, 3653, "02/09/2026", "13:00", "15:00"],
]


def volver_al_menu(valor):
    if valor == "-1":
        print("Volviendo al menu principal...")
        return True
    return False


def reservas_por_usuario(matriz, usuario):
    usuario_id = str(usuario)
    filtradas = []
    for reserva in matriz:
        if str(reserva[2]) == usuario_id:
            filtradas.append(reserva)
    return [(indice, reserva) for indice, reserva in enumerate(filtradas, start=1)]


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

    if usuario is not None:
        lista = reservas_por_usuario(matriz, usuario)
        if not lista:
            print("No hay reservas para este usuario.")
            return
        for id_local, reserva in lista:
            _, sala, id_usuario, fecha, inicio, fin = reserva
            print(f"{id_local:<12}{sala:<8}{id_usuario:<12}{fecha:<14}{inicio:<12}{fin:<12}")
        return

    for reserva in matriz:
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


def realizar_Reserva(matriz, id_usuario=0):
    '''
    pre: recibe una matriz de reservas, donde cada fila representa una reserva con sus datos
         [id_reserva, sala, id_usuario, fecha, inicio, fin].
    pos: genera automaticamente un id correlativo para la reserva del usuario actual,
         solicita el tamaño de sala, la fecha y la hora, y guarda la reserva.
    '''

    print("Selecciona el tamaño de la sala:")
    print("1. Pequeña")
    print("2. Mediana")
    print("3. Grande")

    opcion_sala = pedir_opcion("Ingresar opcion: ", ("1", "2", "3"))
    if opcion_sala == "-1":
        return
    id_sala = int(opcion_sala)

    while True:
        anio_input = input("Ingresar año (2026 o 2027) o -1 para volver al menu principal: ").strip()
        if volver_al_menu(anio_input):
            return
        if anio_input.isdigit():
            anio = int(anio_input)
            if anio in (2026, 2027):
                break
        print("El año debe ser 2026 o 2027.")

    while True:
        mes_input = input("Ingresar mes (1 a 12) o -1 para volver al menu principal: ").strip()
        if volver_al_menu(mes_input):
            return
        if mes_input.isdigit():
            mes = int(mes_input)
            if 1 <= mes <= 12:
                break
        print("El mes debe estar entre 1 y 12.")

    while True:
        dia_input = input("Ingresar dia o -1 para volver al menu principal: ").strip()
        if volver_al_menu(dia_input):
            return
        if dia_input.isdigit():
            dia = int(dia_input)
            max_dia = obtener_dias_del_mes(mes)
            if 1 <= dia <= max_dia:
                break
        print(f"El dia debe estar entre 1 y {obtener_dias_del_mes(mes)} para ese mes.")

    while True:
        hora_input = input("Ingresar hora de inicio (formato 24hs) o -1 para volver al menu principal: ").strip()
        if volver_al_menu(hora_input):
            return
        if hora_input.isdigit():
            hora = int(hora_input)
            if 0 <= hora <= 23:
                break
        print("La hora debe estar entre 0 y 23.")

    hora_fin = (hora + 2) % 24
    fecha = f"{dia:02d}/{mes:02d}/{anio}"
    inicio = f"{hora:02d}:00"
    fin = f"{hora_fin:02d}:00"

    if hay_conflicto_reserva_usuario(matriz, id_usuario, fecha, inicio):
        print("No puedes reservar en un dia y horario que ya habias reservado antes.")
        return

    contador = 1
    for reserva in matriz:
        if str(reserva[2]) == str(id_usuario):
            contador += 1

    nuevaReserva = [contador, id_sala, id_usuario, fecha, inicio, fin]
    matriz.append(nuevaReserva)
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
            id_reserva = int(id_input)
            break
        print("Debes ingresar un numero valido.")

    lista = reservas_por_usuario(matriz, usuario)

    for numero, reserva in lista:
        if numero == id_reserva:
            matriz.remove(reserva)
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
            id_buscado = int(id_buscado_input)
            break
        print("Debes ingresar un numero valido.")

    reserva_encontrada = None
    for numero, reserva in lista:
        if numero == id_buscado:
            reserva_encontrada = reserva
            break

    if reserva_encontrada is None:
        print("Reserva no encontrada. Intente nuevamente.")
        return

    print("Selecciona el nuevo tamaño de la sala:")
    print("1. Pequeña")
    print("2. Mediana")
    print("3. Grande")

    nuevo_sala_input = pedir_opcion("Ingresar opcion: ", ("1", "2", "3"))
    if nuevo_sala_input == "-1":
        return
    nuevo_sala = int(nuevo_sala_input)

    while True:
        anio_input = input("Ingresar nuevo año (2026 o 2027) o -1 para volver al menu principal: ").strip()
        if volver_al_menu(anio_input):
            return
        if anio_input.isdigit():
            anio = int(anio_input)
            if anio in (2026, 2027):
                break
        print("El año debe ser 2026 o 2027.")

    while True:
        mes_input = input("Ingresar nuevo mes (1 a 12) o -1 para volver al menu principal: ").strip()
        if volver_al_menu(mes_input):
            return
        if mes_input.isdigit():
            mes = int(mes_input)
            if 1 <= mes <= 12:
                break
        print("El mes debe estar entre 1 y 12.")

    while True:
        dia_input = input("Ingresar nuevo dia o -1 para volver al menu principal: ").strip()
        if volver_al_menu(dia_input):
            return
        if dia_input.isdigit():
            dia = int(dia_input)
            max_dia = obtener_dias_del_mes(mes)
            if 1 <= dia <= max_dia:
                break
        print(f"El dia debe estar entre 1 y {obtener_dias_del_mes(mes)} para ese mes.")

    while True:
        hora_input = input("Ingresar nueva hora de inicio (formato 24hs) o -1 para volver al menu principal: ").strip()
        if volver_al_menu(hora_input):
            return
        if hora_input.isdigit():
            hora = int(hora_input)
            if 0 <= hora <= 23:
                break
        print("La hora debe estar entre 0 y 23.")

    nueva_fecha = f"{dia:02d}/{mes:02d}/{anio}"
    nuevo_inicio = f"{hora:02d}:00"
    if hay_conflicto_reserva_usuario(matriz, usuario, nueva_fecha, nuevo_inicio, reserva_encontrada):
        print("No puedes reservar en un dia y horario que ya habias reservado antes.")
        return

    hora_fin = (hora + 2) % 24
    reserva_encontrada[1] = nuevo_sala
    reserva_encontrada[3] = nueva_fecha
    reserva_encontrada[4] = nuevo_inicio
    reserva_encontrada[5] = f"{hora_fin:02d}:00"

    print("Reserva modificada correctamente")