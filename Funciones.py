from functools import reduce


def ordenar_usuarios_por_nombre(usuarios):
    """Devuelve los usuarios ordenados alfabeticamente por nombre."""
    return dict(sorted(
        usuarios.items(),
        key=lambda elemento: elemento[1]["nombre"].casefold()
    ))


def filtrar_usuarios_mayores(usuarios):
    """Devuelve los usuarios que tienen 18 anos o mas."""
    return dict(filter(
        lambda elemento: elemento[1]["edad"] >= 18,
        usuarios.items()
    ))


def filtrar_reservas_por_usuario(reservas, id_usuario):
    """Devuelve las reservas pertenecientes al usuario indicado."""
    return list(filter(
        lambda reserva: str(reserva[2]) == str(id_usuario),
        reservas
    ))


def ordenar_reservas_por_fecha(reservas):
    """Ordena las reservas por fecha y hora de inicio."""
    return sorted(
        reservas,
        key=lambda reserva: (
            reserva[3][6:10],
            reserva[3][3:5],
            reserva[3][:2],
            reserva[4]
        )
    )


def contar_reservas_por_usuario(reservas, id_usuario):
    """Cuenta las reservas del usuario usando reduce y una lambda."""
    return reduce(
        lambda total, reserva: total + (str(reserva[2]) == str(id_usuario)),
        reservas,
        0
    )