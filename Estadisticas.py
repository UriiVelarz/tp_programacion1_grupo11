import datetime
from functools import reduce

import Reservas
import Salas
import Usuarios


def fecha_a_clave(fecha):
    partes = fecha.split("/")
    if len(partes) != 3:
        return fecha
    dia, mes, anio = partes
    return anio + mes + dia


def validar_fecha(texto):
    '''
    pre: recibe una fecha ingresada como cadena de texto en formato dd/mm/aaaa.
    pos: verifica que la fecha tenga un formato correcto, que corresponda a los
         años 2026 o 2027 y que el día y el mes sean validos. Devuelve la fecha
         normalizada con dos digitos para el dia y el mes, o None si es invalida.
    '''
    partes = texto.split("/")
    if len(partes) != 3:
        return None
    if not (partes[0].isdigit() and partes[1].isdigit() and partes[2].isdigit()):
        return None

    try:
        dia = int(partes[0])
        mes = int(partes[1])
        anio = int(partes[2])
    except ValueError:
        return None

    if anio != 2026 and anio != 2027:
        return None
    if mes < 1 or mes > 12:
        return None
    if dia < 1 or dia > Reservas.obtener_dias_del_mes(mes):
        return None

    return f"{dia:02d}/{mes:02d}/{anio}"


def filtrar_por_periodo(reservas, fecha_desde=None, fecha_hasta=None):
    '''
    pre: recibe una matriz de reservas, donde cada fila contiene los datos
         [id_reserva, sala, id_usuario, fecha, inicio, fin], y opcionalmente
         una fecha inicial y una fecha final.
    pos: filtra y devuelve una lista con las reservas comprendidas dentro del
         periodo indicado, incluyendo las fechas limite. Si alguno de los
         extremos no se especifica, no aplica un limite para ese extremo.
    '''
    desde = "00000000"
    hasta = "99999999"
    if fecha_desde is not None:
        desde = fecha_a_clave(fecha_desde)
    if fecha_hasta is not None:
        hasta = fecha_a_clave(fecha_hasta)

    return list(filter(
        lambda reserva: desde <= fecha_a_clave(reserva[3]) <= hasta,
        reservas
    ))


def total_reservas(reservas):
    '''
    pre: recibe una matriz de reservas, donde cada fila representa una reserva
         registrada.
    pos: cuenta y devuelve la cantidad total de reservas utilizando una funcion
         acumuladora.
    '''
    return reduce(lambda acumulado, reserva: acumulado + 1, reservas, 0)


def reservas_por_tipo_sala(reservas):
    '''
    pre: recibe una matriz de reservas, donde cada fila contiene el tipo de sala
         en la posicion 1.
    pos: cuenta recursivamente la cantidad de reservas correspondientes a cada
         tipo de sala y devuelve un diccionario donde cada clave representa
         un tipo y cada valor su cantidad de reservas.
    '''
    if not reservas:
        return {}
    else:
        tipo = reservas[0][1]
        conteo = reservas_por_tipo_sala(reservas[1:])
        conteo[tipo] = conteo.get(tipo, 0) + 1
        return conteo


def reservas_por_usuario(reservas):
    '''
    pre: recibe una matriz de reservas, donde cada fila contiene el ID del usuario
         en la posicion 2.
    pos: cuenta la cantidad de reservas realizadas por cada usuario y devuelve
         un diccionario donde cada clave representa un ID de usuario y cada
         valor la cantidad de reservas correspondientes.
    '''
    conteo = {}
    for reserva in reservas:
        id_usuario = str(reserva[2])
        conteo[id_usuario] = conteo.get(id_usuario, 0) + 1
    return conteo


def dias_con_reservas(reservas):
    '''
    pre: recibe una matriz de reservas, donde cada fila contiene la fecha de
         la reserva en la posicion 3.
    pos: obtiene recursivamente las fechas en las que existen reservas, evitando
         repetir aquellas que aparecen mas de una vez. Devuelve una lista
         con los dias registrados.
    '''
    if len(reservas) == 0:
        return[]

    fecha  = reservas[0][3]
    fechas = dias_con_reservas(reservas[1:])

    if fecha not in fechas:
        fechas.append(fecha)

    return fechas


def contar_dias_recursivo(fechas):
    '''
    pre: recibe una lista de fechas sin repetir correspondientes a dias
         en los que existen reservas.
    pos: cuenta recursivamente la cantidad de elementos de la lista y devuelve
         el total de dias registrados.
    '''
    if len(fechas) == 0:
        return 0

    return 1 + contar_dias_recursivo(fechas[1:])


def promedio_diario(reservas):
    '''
    pre: recibe una matriz de reservas, donde cada fila representa una reserva
         y contiene su fecha correspondiente.
    pos: calcula el promedio de reservas por dia dividiendo la cantidad total
         de reservas por la cantidad de dias distintos con reservas. Devuelve
         0 si no existen reservas.
    '''
    fechas = dias_con_reservas(reservas)
    if len(fechas) == 0:
        return 0

    return total_reservas(reservas) / contar_dias_recursivo(fechas)


def promedio_por_sala(reservas, salas):
    '''
    pre: recibe una matriz de reservas y una estructura de salas registradas.
    pos: calcula y devuelve el promedio de reservas por sala, dividiendo la
         cantidad total de reservas por la cantidad de salas disponibles.
         Devuelve 0 si no existen salas registradas.
    '''
    cantidad_salas = len(salas)
    if cantidad_salas == 0:
        return 0
    return total_reservas(reservas) / cantidad_salas


def porcentaje_por_tipo_sala(reservas):
    '''
    pre: recibe una matriz de reservas, donde cada fila contiene el tipo de sala
         correspondiente.
    pos: calcula el porcentaje de reservas de cada tipo de sala respecto del
         total de reservas y devuelve un diccionario con cada tipo y su
         porcentaje. Si no existen reservas, asigna 0 a todos los tipos.
    '''
    total = total_reservas(reservas)
    conteo = reservas_por_tipo_sala(reservas)
    porcentajes = {}

    for tipo in Salas.TIPOS_SALA:
        if total == 0:
            porcentajes[tipo] = 0
        else:
            porcentajes[tipo] = (conteo.get(tipo, 0) / total) * 100

    return porcentajes


def extremos_por_categoria(conteo):
    '''
    pre: recibe un diccionario donde cada clave representa una categoria
         y cada valor indica su cantidad de reservas.
    pos: identifica las categorias con mayor y menor cantidad de reservas,
         contemplando los casos en que varias categorias tengan el mismo valor.
         Devuelve las listas de categorias maximas y minimas junto con sus
         respectivas cantidades. Si el diccionario esta vacio, devuelve
         listas vacias y valores iguales a 0.
    '''
    if len(conteo) == 0:
        return ([], 0, [], 0)

    maximo = None
    minimo = None
    for cantidad in conteo.values():
        if maximo is None or cantidad > maximo:
            maximo = cantidad
        if minimo is None or cantidad < minimo:
            minimo = cantidad

    claves_max = []
    claves_min = []
    for clave, cantidad in conteo.items():
        if cantidad == maximo:
            claves_max.append(clave)
        if cantidad == minimo:
            claves_min.append(clave)

    return (claves_max, maximo, claves_min, minimo)


def nombre_tipo_sala(tipo):
    '''
    pre: recibe el identificador de un tipo de sala.
    pos: busca el nombre correspondiente en el diccionario de tipos de sala
         y lo devuelve. Si el tipo no existe, devuelve un texto indicando
         su identificador.
    '''
    if tipo in Salas.TIPOS_SALA:
        return Salas.TIPOS_SALA[tipo]["nombre"]
    return f"Tipo {tipo}"


def nombre_usuario(usuarios, id_usuario):
    '''
    pre: recibe un diccionario de usuarios registrados y el ID de un usuario.
    pos: verifica si el ID corresponde a un usuario existente y devuelve su
         nombre acompañado del ID. Si no encuentra el usuario o el ID no es
         valido, devuelve el identificador recibido como texto.
    '''
    if str(id_usuario).isdigit():
        try:
            id_numerico = int(id_usuario)
        except ValueError:
            return str(id_usuario)
        if id_numerico in usuarios:
            return f"{usuarios[id_numerico]['nombre']} (id {id_usuario})"
    return str(id_usuario)


def unir_tipos(lista_tipos):
    '''
    pre: recibe una lista de identificadores correspondientes a tipos de sala.
    pos: obtiene el nombre de cada tipo mediante la funcion nombre_tipo_sala()
         y los une en una unica cadena de texto separados por comas.
    '''
    nombres = []
    for tipo in lista_tipos:
        nombres.append(nombre_tipo_sala(tipo))
    return ", ".join(nombres)


def unir_usuarios(usuarios, lista_ids):
    '''
    pre: recibe una lista de identificadores correspondientes a tipos de sala.
    pos: obtiene el nombre de cada tipo mediante la funcion nombre_tipo_sala()
         y los une en una unica cadena de texto separados por comas.
    '''
    nombres = []
    for id_usuario in lista_ids:
        nombres.append(nombre_usuario(usuarios, id_usuario))
    return ", ".join(nombres)


def mostrar_resumen(reservas, salas, usuarios, fecha_desde=None, fecha_hasta=None):
    '''
    pre: recibe una matriz de reservas, una estructura de salas, un diccionario
         de usuarios y opcionalmente una fecha inicial y una fecha final para
         limitar el periodo del reporte.
    pos: filtra las reservas segun el periodo indicado y muestra un informe
         estadistico con el total de reservas, dias registrados, promedios,
         cantidades por tipo de sala, porcentajes, rankings de usuarios y
         categorias con mayor y menor cantidad de reservas. Si no existen
         reservas en el periodo, informa que no hay datos disponibles.
    '''
    filtradas = filtrar_por_periodo(reservas, fecha_desde, fecha_hasta)
    total = total_reservas(filtradas)

    print("\n" + "=" * 70)
    print(f"{'Reportes estadisticos':^70}")
    print("=" * 70)

    if fecha_desde is None and fecha_hasta is None:
        print("Periodo: todas las reservas cargadas")
    else:
        desde_txt = "inicio"
        hasta_txt = "fin"
        if fecha_desde is not None:
            desde_txt = fecha_desde
        if fecha_hasta is not None:
            hasta_txt = fecha_hasta
        print(f"Periodo: {desde_txt} a {hasta_txt}")

    if total == 0:
        print("No hay reservas en el periodo indicado.")
        print("=" * 70)
        return

    conteo_tipos = reservas_por_tipo_sala(filtradas)
    conteo_tipos_totales = reservas_por_tipo_sala(reservas)
    conteo_usuarios = reservas_por_usuario(filtradas)

    conteo_tipos_completo = {}
    for tipo in Salas.TIPOS_SALA:
        conteo_tipos_completo[tipo] = conteo_tipos.get(tipo, 0)

    tipo_max, cant_max, tipo_min, cant_min = extremos_por_categoria(conteo_tipos_completo)
    user_max, user_cant_max, user_min, user_cant_min = extremos_por_categoria(conteo_usuarios)

    print(f"Total de reservas: {total}")
    print(f"Dias con reservas: {len(dias_con_reservas(filtradas))}")
    print(f"Promedio diario de reservas: {promedio_diario(filtradas):.2f}")
    print(f"Promedio de reservas por sala ({len(salas)} salas): {promedio_por_sala(filtradas, salas):.2f}")

    print("-" * 70)
    print(
        f"{'Tipo de sala':<18}{'Salas':<10}"
        f"{'Reservas actuales':<20}{'Reservas totales':<18}"
    )
    print("-" * 70)

    for tipo, datos in Salas.TIPOS_SALA.items():
        cantidad_actual = conteo_tipos.get(tipo, 0)
        cantidad_total = conteo_tipos_totales.get(tipo, 0)
        print(
            f"{datos['nombre']:<18}{datos['cantidad']:<10}"
            f"{cantidad_actual:<20}{cantidad_total:<18}"
        )

    print("-" * 70)
    print(f"Tipo de sala con mas reservas: {unir_tipos(tipo_max)} -> {cant_max}")
    print(f"Tipo de sala con menos reservas: {unir_tipos(tipo_min)} -> {cant_min}")

    print("-" * 70)
    print(f"{'Usuario':<40}{'Reservas':<12}")
    print("-" * 70)

    ranking = sorted(conteo_usuarios.items(), key=lambda par: par[1], reverse=True)
    for id_usuario, cantidad in ranking:
        print(f"{nombre_usuario(usuarios, id_usuario):<40}{cantidad:<12}")

    print("-" * 70)
    print(f"Usuario con mas reservas: {unir_usuarios(usuarios, user_max)} -> {user_cant_max}")
    print(f"Usuario con menos reservas: {unir_usuarios(usuarios, user_min)} -> {user_cant_min}")
    print("(Se consideran solo los usuarios que tienen al menos una reserva en el periodo.)")

    print("=" * 70)


def pedir_fecha(mensaje):
    '''
    pre: recibe un mensaje que se utiliza para solicitar una fecha al usuario.
    pos: solicita una fecha, valida su formato y comprueba que no sea posterior
         a la fecha actual. Devuelve la fecha validada, una cadena vacia si no
         se ingresa ningun valor o "-1" si el usuario desea volver al menu.
    '''
    while True:
        texto = input(mensaje).strip()
        if texto == "-1":
            return "-1"
        if texto == "":
            return ""
        fecha = validar_fecha(texto)
        if fecha is not None:
            dia, mes, anio = map(int, fecha.split("/"))
            if datetime.date(anio, mes, dia) > datetime.date.today():
                print("No se permiten fechas futuras. Intente nuevamente.")
                continue
            return fecha
        print("Fecha invalida. Usa el formato dd/mm/aaaa con año 2026 o 2027 (ej. 15/09/2026).")


def pedir_periodo():
    '''
    pre: no recibe parametros.
    pos: solicita una fecha inicial y una fecha final para establecer el periodo
         de consulta de los reportes. Verifica que la fecha inicial no sea
         posterior a la fecha final y permite dejar cualquiera de los extremos
         sin limite. Devuelve una tupla con ambas fechas o None si el usuario
         decide volver al menu de reportes.
    '''
    while True:
        print("Dejar vacio para no limitar ese extremo. -1 para volver al menu de reportes.")

        fecha_desde = pedir_fecha("Fecha desde (dd/mm/aaaa): ")
        if fecha_desde == "-1":
            print("Volviendo al menu de reportes...")
            return None

        fecha_hasta = pedir_fecha("Fecha hasta (dd/mm/aaaa): ")
        if fecha_hasta == "-1":
            print("Volviendo al menu de reportes...")
            return None

        if fecha_desde != "" and fecha_hasta != "":
            if fecha_a_clave(fecha_desde) > fecha_a_clave(fecha_hasta):
                print("La fecha desde no puede ser posterior a la fecha hasta.")
                continue

        if fecha_desde == "":
            fecha_desde = None
        if fecha_hasta == "":
            fecha_hasta = None

        return (fecha_desde, fecha_hasta)


def menu_estadisticas(reservas=None, salas=None, usuarios=None):
    '''
    pre: recibe opcionalmente una matriz de reservas, una estructura de salas
         y un diccionario de usuarios. Si no se proporcionan, utiliza las
         estructuras globales correspondientes.
    pos: muestra un menu interactivo que permite consultar distintos reportes
         estadisticos, como el total de reservas, reservas por tipo de sala,
         porcentajes, reservas por usuario, dias registrados, promedios y
         categorias con mayor y menor cantidad de reservas. Permite generar
         resumenes generales o por periodo y regresar al menu anterior.
    '''
    if reservas is None:
        reservas = Reservas.reservas
    if salas is None:
        salas = Salas.salas
    if usuarios is None:
        usuarios = Usuarios.usuarios

    while True:
        Reservas.limpiar_reservas_vencidas()
        print(f"\n=== Reportes estadisticos ===")
        print("1. Resumen general")
        print("2. Resumen por periodo")
        print("3. Total de reservas")
        print("4. Reservas por tipo de sala")
        print("5. Porcentaje por tipo de sala")
        print("6. Reservas por usuario")
        print("7. Dias con reservas")
        print("8. Promedio diario de reservas")
        print("9. Promedio de reservas por sala")
        print("10. Categorias con mas y menos reservas")
        print("0. Volver")
        opcion = input("Seleccione una opcion: ").strip()

        if opcion == "1":
            mostrar_resumen(reservas, salas, usuarios)

        elif opcion == "2":
            periodo = pedir_periodo()
            if periodo is not None:
                desde, hasta = periodo
                mostrar_resumen(reservas, salas, usuarios, desde, hasta)

        elif opcion == "3":
            print("Total de reservas:", total_reservas(reservas))

        elif opcion == "4":
            conteo = reservas_por_tipo_sala(reservas)

            print(f"\nReservas por tipo de sala:")
            for tipo, datos in Salas.TIPOS_SALA.items():
                print(f"{datos['nombre']}: " f"{conteo.get(tipo, 0)} reservas")

        elif opcion == "5":
            porcentajes = porcentaje_por_tipo_sala(reservas)

            print(f"\nPorcentaje de reservas por tipo de sala:")
            for tipo, datos in Salas.TIPOS_SALA.items():
                print(f"{datos['nombre']}: " f"{porcentajes[tipo]:.2f}%")

        elif opcion == "6":
            conteo = reservas_por_usuario(reservas)

            if not conteo:
                print("No hay reservas registradas.")
            else:
                ranking = sorted(conteo.items(), key=lambda par: par[1], reverse=True)

                print(f"\nReservas por usuario:")
                for id_usuario, cantidad in ranking:
                    nombre = nombre_usuario(usuarios, id_usuario)
                    print(f"{nombre}: {cantidad} reservas")

        elif opcion == "7":
            fechas = dias_con_reservas(reservas)

            print("\nDias con reservas:")
            if fechas:
                for fecha in fechas:
                    print(fecha)
                print(f"Total de dias: {len(fechas)}")
            else:
                print("No hay dias con reservas.")

        elif opcion == "8":
            print("Promedio diario de reservas: " f"{promedio_diario(reservas):.2f}")

        elif opcion == "9":
            print("Promedio de reservas por sala: " f"{promedio_por_sala(reservas, salas):.2f}")

        elif opcion == "10":
            conteo_tipos = reservas_por_tipo_sala(reservas)

            conteo_completo = {
                tipo: conteo_tipos.get(tipo, 0)
                for tipo in Salas.TIPOS_SALA
            }

            if total_reservas(reservas) == 0:
                print("No hay reservas para analizar.")
            else:
                (tipos_max, maximo, tipos_min, minimo) = extremos_por_categoria(conteo_completo)

                print("Tipo(s) con mas reservas: " f"{unir_tipos(tipos_max)} -> {maximo}")
                print("Tipo(s) con menos reservas: " f"{unir_tipos(tipos_min)} -> {minimo}")

        elif opcion == "0":
            return

        else:
            print("Opcion invalida, intenta otra vez.")


if __name__ == "__main__":
    menu_estadisticas()