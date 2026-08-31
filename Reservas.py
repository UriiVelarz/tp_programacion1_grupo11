def imprimir_Reservas(matriz):
    print("="*60)
    print(f"{"Reservas":42}")
    print("="*60)
    print(f"{"Id":<10}{"Sala":<12}{"Usuario":<12}{"Fecha":<8}{"Inicio":<20}{"Fin":<12}")
    print("-" *60)

    for i in range (len(matriz)):
        id_Reserva  = matriz [i][0]
        sala        = matriz [i][1]
        id_usuario  = matriz [i][2]
        fecha       = matriz [i][3]
        inicio      = matriz [i][4]
        fin         = matriz [i][5]
        print(f"{id_Reserva:<10}{sala:<12}{id_usuario:<8}{fecha:<20}{inicio:<12}{fin:<12}")

reservas = [
    [1, 1, 1234, "01/09/2026", "8:00",  "8:30"],
    [2, 2, 8254, "01/09/2026", "8:30",  "9:00"],
    [3, 3, 4567, "01/09/2026", "9:00",  "10:00"],
    [4, 1, 2130, "01/09/2026", "10:00", "11:00"],
    [5, 4, 1101, "02/09/2026", "8:00",  "10:00"],
    [6, 2, 3653, "02/09/2026", "10:00", "12:00"]
]


def agregar_Reserva(matriz):

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
#agregar_Reserva(reservas)
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
imprimir_Reservas(ordenFechaYHorario)

