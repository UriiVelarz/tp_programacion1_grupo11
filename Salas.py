import re

from Reservas import reservas

salas = [
    [1, "Sala A", "Primer  Piso", 2],
    [2, "Sala B", "Primer  Piso", 2],
    [3, "Sala C", "Primer  Piso", 4],
    [4, "Sala A", "Segundo Piso", 2],
    [5, "Sala B", "Segundo Piso", 2],
    [6, "Sala C", "Segundo Piso", 4]
]

TIPOS_SALA = {
    1: {"nombre": "Pequeña", "cantidad": 2},
    2: {"nombre": "Mediana", "cantidad": 2},
    3: {"nombre": "Grande", "cantidad": 2},
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


def formatear_celda(texto, ancho):
    texto_limpio = limpiar_ansi(texto)
    espacios = max(0, ancho - len(texto_limpio))
    return texto + (" " * espacios)


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
        id_sala, nombre, piso, capacidad = salas[i]
        etiqueta = f"{nombre}({piso})"
        fila = f"{etiqueta:<25}" + "".join(f"{matriz_disponibilidad[i][j]:<11}" for j in range(len(dias)))
        print(fila)
    print("\nAclaracion: 1 = disponible, 0 = ocupado")


def consultar_disponibilidad(sala, dia):
    if sala < 1 or sala > len(salas):
        return "La sala ingresada no existe."
    if dia < 1 or dia > len(dias):
        return "El dia ingresado no existe."

    disponible = matriz_disponibilidad[sala - 1][dia - 1]
    nombre_sala = salas[sala - 1][1]

    if disponible == 1:
        return f"La {nombre_sala} esta disponible el dia {dias[dia - 1]}."
    return f"La {nombre_sala} no esta disponible el dia {dias[dia - 1]}."


def obtener_dias_mes(mes):
    dias_por_mes = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
    return dias_por_mes.get(mes, 0)


def contar_reservas_por_tamanio(anio, mes, dia, tamaño):
    fecha = f"{dia:02d}/{mes:02d}/{anio}"
    cantidad = 0
    for reserva in reservas:
        if reserva[3] == fecha and reserva[1] == tamaño:
            cantidad += 1
    return cantidad, TIPOS_SALA[tamaño]["cantidad"]


def estado_horario(anio, mes, dia, tamaño, hora_inicio):
    fecha = f"{dia:02d}/{mes:02d}/{anio}"
    hora_fin = hora_inicio + 2
    capacidad = TIPOS_SALA[tamaño]["cantidad"]
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

    if conflictos == 0:
        color = COLOR_VERDE
        estado = f"Libre {conflictos}/{capacidad}"
    elif conflictos < capacidad:
        color = COLOR_AMARILLO
        estado = f"Parcial {conflictos}/{capacidad}"
    else:
        color = COLOR_ROJO
        estado = f"Ocupada {conflictos}/{capacidad}"

    return f"{color}{estado}{COLOR_RESET}"


def consultar_disponibilidad_mensual():
    while True:
        anio_input = input("Ingrese el año (2026 o 2027) o -1 para volver: ").strip()
        if anio_input == "-1":
            return
        if anio_input.isdigit():
            anio = int(anio_input)
            if anio in (2026, 2027):
                break
        print("El año debe ser 2026 o 2027.")

    while True:
        mes_input = input("Ingrese el mes (1 a 12) o -1 para volver: ").strip()
        if mes_input == "-1":
            return
        if mes_input.isdigit():
            mes = int(mes_input)
            if 1 <= mes <= 12:
                break
        print("El mes debe estar entre 1 y 12.")

    dias_del_mes = obtener_dias_mes(mes)

    while True:
        dia_inicio_input = input(f"Ingrese el dia de inicio (1 a {dias_del_mes}) o -1 para volver: ").strip()
        if dia_inicio_input == "-1":
            return
        if dia_inicio_input.isdigit():
            dia_inicio = int(dia_inicio_input)
            if 1 <= dia_inicio <= dias_del_mes:
                break
        print(f"El dia debe estar entre 1 y {dias_del_mes}.")

    while True:
        cantidad_dias_input = input("Ingrese la cantidad de dias a imprimir (maximo 30): ").strip()
        if cantidad_dias_input.isdigit():
            cantidad_dias = int(cantidad_dias_input)
            if 1 <= cantidad_dias <= 30:
                break
        print("La cantidad de dias debe estar entre 1 y 30.")

    fechas = []
    anio_actual = anio
    mes_actual = mes
    dia_actual = dia_inicio

    for _ in range(cantidad_dias):
        while dia_actual > obtener_dias_mes(mes_actual):
            dia_actual = 1
            mes_actual += 1
            if mes_actual > 12:
                mes_actual = 1
                anio_actual += 1

        fechas.append((anio_actual, mes_actual, dia_actual))
        dia_actual += 1

    print(f"\n{'Disponibilidad mensual - ' + str(mes) + '/' + str(anio):^120}")
    print(f"{'Total de salas: 2 pequeñas, 2 medianas y 2 grandes':^120}")
    print("=" * 120)

    for anio_actual, mes_actual, dia_actual in fechas:
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

    print(f"\n{COLOR_VERDE}Libre 0/2{COLOR_RESET}   {COLOR_AMARILLO}Parcial 1/2{COLOR_RESET}   {COLOR_ROJO}Ocupada 2/2{COLOR_RESET}")
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
    print(f"{'Id_Sala':<10}{'Nombre':<10}{'Ubicacion':<15}{'capacidad':<14}")
    print("-" * 55)

    for i in range(len(matriz)):
        id_sala = matriz[i][0]
        nombre_sala = matriz[i][1]
        ubicacion = matriz[i][2]
        capacidad = matriz[i][3]
        print(f"{id_sala:<10}{nombre_sala:<10}{ubicacion:15}{capacidad:<14}")


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
        id_sala = int(id_input)
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
        capacidad_input = input("Ingresar capacidad o -1 para volver al menu principal: ").strip()
        if capacidad_input == "-1":
            return
        if validar_capacidad(capacidad_input):
            capacidad = int(capacidad_input)
            break
        print("La capacidad debe ser un numero entero positivo.")

    nuevaSala = [id_sala, nombre_sala, ubicacion, capacidad]
    matriz.append(nuevaSala)
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
        id_sala = int(id_input)
        for sala in matriz:
            if sala[0] == id_sala:
                matriz.remove(sala)
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
        fila_encontrada = next(
            (fila for fila in matriz if fila[0] == int(id_buscado_input)),
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
        nuevo_id = int(nuevo_id_input)
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
