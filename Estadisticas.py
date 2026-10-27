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
    return reduce(lambda acumulado, reserva: acumulado + 1, reservas, 0)


def reservas_por_tipo_sala(reservas):
    if not reservas:
        return {}
    else:
        tipo = reservas[0][1]
        conteo = reservas_por_tipo_sala(reservas[1:])
        conteo[tipo] = conteo.get(tipo, 0) + 1
        return conteo


def reservas_por_usuario(reservas):
    conteo = {}
    for reserva in reservas:
        id_usuario = str(reserva[2])
        conteo[id_usuario] = conteo.get(id_usuario, 0) + 1
    return conteo


def dias_con_reservas(reservas):
    if len(reservas) == 0:
        return[]

    fecha  = reservas[0][3]
    fechas = dias_con_reservas(reservas[1:])

    if fecha not in fechas:
        fechas.append(fecha)

    return fechas


def contar_dias_recursivo(fechas):
    if len(fechas) == 0:
        return 0

    return 1 + contar_dias_recursivo(fechas[1:])


def promedio_diario(reservas):
    fechas = dias_con_reservas(reservas)
    if len(fechas) == 0:
        return 0

    return total_reservas(reservas) / contar_dias_recursivo(fechas)


def promedio_por_sala(reservas, salas):
    cantidad_salas = len(salas)
    if cantidad_salas == 0:
        return 0
    return total_reservas(reservas) / cantidad_salas


def porcentaje_por_tipo_sala(reservas):
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
    if tipo in Salas.TIPOS_SALA:
        return Salas.TIPOS_SALA[tipo]["nombre"]
    return f"Tipo {tipo}"


def nombre_usuario(usuarios, id_usuario):
    if str(id_usuario).isdigit():
        try:
            id_numerico = int(id_usuario)
        except ValueError:
            return str(id_usuario)
        if id_numerico in usuarios:
            return f"{usuarios[id_numerico]['nombre']} (id {id_usuario})"
    return str(id_usuario)


def unir_tipos(lista_tipos):
    nombres = []
    for tipo in lista_tipos:
        nombres.append(nombre_tipo_sala(tipo))
    return ", ".join(nombres)


def unir_usuarios(usuarios, lista_ids):
    nombres = []
    for id_usuario in lista_ids:
        nombres.append(nombre_usuario(usuarios, id_usuario))
    return ", ".join(nombres)


def mostrar_resumen(reservas, salas, usuarios, fecha_desde=None, fecha_hasta=None):
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
    conteo_usuarios = reservas_por_usuario(filtradas)
    porcentajes = porcentaje_por_tipo_sala(filtradas)

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
    print(f"{'Tipo de sala':<18}{'Salas':<10}{'Reservas':<12}{'% del total':<14}")
    print("-" * 70)

    for tipo, datos in Salas.TIPOS_SALA.items():
        cantidad = conteo_tipos.get(tipo, 0)
        porcentaje = porcentajes[tipo]
        print(f"{datos['nombre']:<18}{datos['cantidad']:<10}{cantidad:<12}{porcentaje:>6.2f}%")

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
    while True:
        texto = input(mensaje).strip()
        if texto == "-1":
            return "-1"
        if texto == "":
            return ""
        fecha = validar_fecha(texto)
        if fecha is not None:
            return fecha
        print("Fecha invalida. Usa el formato dd/mm/aaaa con año 2026 o 2027 (ej. 15/09/2026).")


def pedir_periodo():
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
    if reservas is None:
        reservas = Reservas.reservas
    if salas is None:
        salas = Salas.salas
    if usuarios is None:
        usuarios = Usuarios.usuarios

    while True:
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