from functools import reduce


def ordenar_usuarios_por_nombre(usuarios):
    '''
    pre: recibe un diccionario de usuarios, donde cada usuario tiene un nombre.
    pos: devuelve un nuevo diccionario con los usuarios ordenados alfabeticamente por nombre, sin modificar el original.
    '''
    return dict(sorted(
        usuarios.items(),
        key=lambda elemento: elemento[1]["nombre"].casefold()
    ))


def filtrar_usuarios_mayores(usuarios):
    '''
    pre: recibe un diccionario de usuarios que contiene la edad de cada uno.
    pos: devuelve un nuevo diccionario con los usuarios que tienen 18 anos o mas.
    '''
    return dict(filter(
        lambda elemento: elemento[1]["edad"] >= 18,
        usuarios.items()
    ))


def filtrar_reservas_por_usuario(reservas, id_usuario):
    '''
    pre: recibe una lista de reservas y el identificador de un usuario.
    pos: devuelve una lista con las reservas que pertenecen al usuario indicado.
    '''
    return list(filter(
        lambda reserva: str(reserva[2]) == str(id_usuario),
        reservas
    ))


def ordenar_reservas_por_fecha(reservas):
    '''
    pre: recibe una lista de reservas que contienen una fecha y una hora de inicio.
    pos: devuelve una nueva lista ordenada cronologicamente por fecha y hora de inicio, sin modificar la original.
    '''
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
    '''
    pre: recibe una lista de reservas y el identificador de un usuario.
    pos: devuelve la cantidad de reservas pertenecientes al usuario indicado, utilizando reduce y una funcion lambda.
    '''
    return reduce(
        lambda total, reserva: total + (str(reserva[2]) == str(id_usuario)),
        reservas,
        0
    )
