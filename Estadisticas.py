from functools import reduce

import Salas
import Usuarios
from Reservas import reservas as reservas_sistema


def fecha_a_clave(fecha):
    '''
    pre: recibe una fecha en formato dd/mm/aaaa.
    pos: devuelve una cadena aaaammdd para poder comparar fechas.
    '''
    partes = fecha.split("/")
    if len(partes) != 3:
        return fecha
    dia, mes, anio = partes
    return anio + mes + dia


def filtrar_por_periodo(reservas, fecha_desde=None, fecha_hasta=None):
    '''
    pre: recibe la matriz de reservas y, de forma opcional, dos fechas dd/mm/aaaa.
    pos: devuelve las reservas cuyo dia esta dentro del periodo indicado.
    '''
    if fecha_desde is None and fecha_hasta is None:
        return list(reservas)

    desde = fecha_a_clave(fecha_desde) if fecha_desde else None
    hasta = fecha_a_clave(fecha_hasta) if fecha_hasta else None

    return list(filter(
        lambda reserva: (
            (desde is None or fecha_a_clave(reserva[3]) >= desde)
            and (hasta is None or fecha_a_clave(reserva[3]) <= hasta)
        ),
        reservas
    ))


def total_reservas(reservas):
    '''
    pre: recibe la matriz de reservas.
    pos: devuelve la cantidad total de reservas usando reduce.
    '''
    return reduce(lambda acumulado, _reserva: acumulado + 1, reservas, 0)


def reservas_por_sala(reservas):
    '''
    pre: recibe la matriz de reservas.
    pos: devuelve un diccionario {id_sala: cantidad} con el conteo por sala.
    '''
    return reduce(
        lambda acumulado, reserva: {
            **acumulado,
            reserva[1]: acumulado.get(reserva[1], 0) + 1
        },
        reservas,
        {}
    )


def reservas_por_usuario(reservas):
    '''
    pre: recibe la matriz de reservas.
    pos: devuelve un diccionario {id_usuario: cantidad} con el conteo por usuario.
    '''
    return reduce(
        lambda acumulado, reserva: {
            **acumulado,
            reserva[2]: acumulado.get(reserva[2], 0) + 1
        },
        reservas,
        {}
    )


def promedio_diario(reservas):
    '''
    pre: recibe la matriz de reservas.
    pos: devuelve el promedio de reservas por dia distinto. si no hay reservas, devuelve 0.
    '''
    total = total_reservas(reservas)
    fechas = set(map(lambda reserva: reserva[3], reservas))
    if len(fechas) == 0:
        return 0
    return total / len(fechas)


def promedio_por_sala(reservas, salas):
    '''
    pre: recibe la matriz de reservas y la matriz de salas.
    pos: devuelve el promedio de reservas por sala (incluye salas sin reservas).
    '''
    cantidad_salas = len(salas)
    if cantidad_salas == 0:
        return 0
    return total_reservas(reservas) / cantidad_salas


def porcentaje_por_sala(reservas, salas):
    '''
    pre: recibe la matriz de reservas y la matriz de salas.
    pos: devuelve un diccionario {id_sala: porcentaje} sobre el total de reservas.
    '''
    total = total_reservas(reservas)
    conteo = reservas_por_sala(reservas)
    porcentajes = {}

    for sala in salas:
        id_sala = sala[0]
        cantidad = conteo.get(id_sala, 0)
        if total == 0:
            porcentajes[id_sala] = 0
        else:
            porcentajes[id_sala] = (cantidad / total) * 100

    return porcentajes


def extremos_por_categoria(conteo):
    '''
    pre: recibe un diccionario {categoria: cantidad}.
    pos: devuelve una tupla (clave_max, valor_max, clave_min, valor_min).
         si el diccionario esta vacio, devuelve (None, 0, None, 0).
    '''
    if not conteo:
        return (None, 0, None, 0)

    id_max, maximo = max(conteo.items(), key=lambda par: par[1])
    id_min, minimo = min(conteo.items(), key=lambda par: par[1])
    return (id_max, maximo, id_min, minimo)


def nombre_sala(salas, id_sala):
    for sala in salas:
        if sala[0] == id_sala:
            return sala[1]
    return f"Sala {id_sala}"


def nombre_usuario(usuarios, id_usuario):
    if id_usuario in usuarios:
        return usuarios[id_usuario]["nombre"]
    return f"Usuario {id_usuario}"


def mostrar_resumen(reservas, salas, usuarios, fecha_desde=None, fecha_hasta=None):
    '''
    pre: recibe reservas, salas y usuarios. puede recibir un periodo de fechas.
    pos: imprime el reporte estadistico (totales, promedios, porcentajes, maximos y minimos).
    '''
    filtradas = filtrar_por_periodo(reservas, fecha_desde, fecha_hasta)
    total = total_reservas(filtradas)
    fechas = set(map(lambda reserva: reserva[3], filtradas))
    conteo_salas = reservas_por_sala(filtradas)
    conteo_usuarios = reservas_por_usuario(filtradas)
    porcentajes = porcentaje_por_sala(filtradas, salas)
    conteo_salas_completo = {sala[0]: conteo_salas.get(sala[0], 0) for sala in salas}
    conteo_usuarios_completo = {uid: conteo_usuarios.get(uid, 0) for uid in usuarios}
    sala_max, cant_max, sala_min, cant_min = extremos_por_categoria(conteo_salas_completo)
    user_max, user_cant_max, user_min, user_cant_min = extremos_por_categoria(conteo_usuarios_completo)

    print("\n" + "=" * 70)
    print(f"{'Reportes estadisticos':^70}")
    print("=" * 70)

    if fecha_desde or fecha_hasta:
        desde_txt = fecha_desde if fecha_desde else "inicio"
        hasta_txt = fecha_hasta if fecha_hasta else "fin"
        print(f"Periodo: {desde_txt} a {hasta_txt}")
    else:
        print("Periodo: todas las reservas cargadas")

    print(f"Total de reservas: {total}")
    print(f"Dias con reservas: {len(fechas)}")
    print(f"Promedio diario de reservas: {promedio_diario(filtradas):.2f}")
    print(f"Promedio de reservas por sala: {promedio_por_sala(filtradas, salas):.2f}")

    print("-" * 70)
    print(f"{'Id':<8}{'Sala':<16}{'Reservas':<12}{'% ocupacion':<14}")
    print("-" * 70)

    for sala in salas:
        id_sala = sala[0]
        cantidad = conteo_salas.get(id_sala, 0)
        porcentaje = porcentajes.get(id_sala, 0)
        print(f"{id_sala:<8}{nombre_sala(salas, id_sala):<16}{cantidad:<12}{porcentaje:>6.2f}%")

    print("-" * 70)

    if sala_max is not None:
        print(
            f"Sala con mas reservas: {nombre_sala(salas, sala_max)} "
            f"(id {sala_max}) -> {cant_max}"
        )
        print(
            f"Sala con menos reservas: {nombre_sala(salas, sala_min)} "
            f"(id {sala_min}) -> {cant_min}"
        )

    if user_max is not None:
        print(
            f"Usuario con mas reservas: {nombre_usuario(usuarios, user_max)} "
            f"(id {user_max}) -> {user_cant_max}"
        )
        print(
            f"Usuario con menos reservas: {nombre_usuario(usuarios, user_min)} "
            f"(id {user_min}) -> {user_cant_min}"
        )

    print("=" * 70)


def pedir_periodo():
    print("Dejar vacio para no limitar ese extremo. -1 cancela el reporte.")
    fecha_desde = input("Fecha desde (dd/mm/aaaa): ").strip()
    if fecha_desde == "-1":
        print("Volviendo al menu...")
        return None
    if fecha_desde == "":
        fecha_desde = None

    fecha_hasta = input("Fecha hasta (dd/mm/aaaa): ").strip()
    if fecha_hasta == "-1":
        print("Volviendo al menu...")
        return None
    if fecha_hasta == "":
        fecha_hasta = None

    return (fecha_desde, fecha_hasta)


def menu_estadisticas(reservas=None, salas=None, usuarios=None):
    '''
    pre: recibe opcionalmente las estructuras del sistema.
    pos: muestra un submenu de reportes hasta que el usuario vuelva atras.
    '''
    if reservas is None:
        reservas = reservas_sistema
    if salas is None:
        salas = Salas.salas
    if usuarios is None:
        usuarios = Usuarios.usuarios

    while True:
        print("\n=== Reportes estadisticos ===")
        print("1. Resumen general")
        print("2. Resumen por periodo")
        print("0. Volver")
        opcion = input("Opcion: ").strip()

        if opcion == "1":
            mostrar_resumen(reservas, salas, usuarios)
        elif opcion == "2":
            periodo = pedir_periodo()
            if periodo is not None:
                fecha_desde, fecha_hasta = periodo
                mostrar_resumen(reservas, salas, usuarios, fecha_desde, fecha_hasta)
        elif opcion == "0":
            return
        else:
            print("Opcion invalida, intenta otra vez.")
