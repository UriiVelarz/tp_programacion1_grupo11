def imprimir_Reservas(matriz):
    print("="*70)
    print(f"{"Reservas":42}")
    print("="*70)
    print(f"{"Id_Reserva":<12}{"Sala":<8}{"Id_Usuario":<12}{"Fecha":<14}{"Inicio":<12}{"Fin":<12}")
    print("-" *70)

    for i in range (len(matriz)):
        id_Reserva  = matriz [i][0]
        sala        = matriz [i][1]
        id_usuario  = matriz [i][2]
        fecha       = matriz [i][3]
        inicio      = matriz [i][4]
        fin         = matriz [i][5]
        print(f"{id_Reserva:<12}{sala:<8}{id_usuario:<12}{fecha:<14}{inicio:<12}{fin:<12}")

reservas = [
    [1001, 1, 1234, "01/09/2026", "08:00", "08:30"],
    [1002, 2, 8254, "01/09/2026", "08:30", "09:00"],
    [1003, 3, 4567, "01/09/2026", "09:00", "10:00"],
    [1004, 1, 2130, "01/09/2026", "10:00", "11:00"],
    [1005, 4, 1101, "02/09/2026", "08:00", "10:00"],
    [1006, 2, 3653, "02/09/2026", "10:00", "12:00"],
    [1007, 4, 3653, "02/09/2026", "13:00", "13:30"],
]

def realizar_Reserva(matriz):

    id_reserva = len(matriz) + 1

    id_sala     = int(input("Ingresar Id de sala: "))
    id_usuario  = int(input("Ingresar Id de usuario: "))
    fecha       = input("Ingresar Fecha: ")
    inicio      = input("Ingresar Horario de inicio: ")
    fin         = input("Ingresar Horario de fin: ")
   

    nuevaReserva = [id_reserva, id_sala, id_usuario, fecha, inicio, fin]
    matriz.append(nuevaReserva)
    print("Reserva agregada correctamente")

#print(imprimir_Reservas(reservas))
#realizar_Reserva(reservas)
#print(imprimir_Reservas(reservas))

def eliminar_Reserva(matriz):
    id = int(input("Ingresar Id: "))
    i = 0
    while i < len(matriz):
        if matriz [i][0] == id:
            matriz.remove(matriz[i])
            print("Reserva eliminado correctamente")
            return
        i = i+1
    print("No se encontro el id de usuario")

#print(imprimir_Reservas(reservas))
#eliminar_Reserva(reservas)
#print(imprimir_Reservas(reservas))

ordenFechaYHorario = sorted(reservas, key=lambda fila: (fila[3],fila[4]))
#imprimir_Reservas(ordenFechaYHorario)


id_usuario_buscado = 3653
filtrarPorId = list(filter(lambda reserva: reserva[2] == id_usuario_buscado, reservas))

#imprimir_Reservas(filtrarPorId)


def modificar_Reserva(matriz):
    id_buscado = int(input("Ingresar id de la reserva a modificar: "))
    for fila in matriz:
        if fila[0] == id_buscado:
            fila[1] = input("Ingresar nuevo id de sala: ")
            fila[2] = int(input("Ingresar nuevo id de usuario: "))
            fila[3] = input("Ingresar nueva fecha de reserva: ")
            fila[4] = input("Ingresar nuevo horario de inicio: ")
            fila[5] = input("Ingresar nuevo horaio de fin: ")

#imprimir_Reservas(reservas)
#modificar_Reserva(reservas)
#imprimir_Reservas(reservas)