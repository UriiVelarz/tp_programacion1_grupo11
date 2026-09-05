reservas = [
    [1000, 1, 1234, "01/09/2026", "08:00", "08:30"],
    [1001, 2, 8254, "01/09/2026", "08:30", "09:00"],
    [1002, 3, 4567, "01/09/2026", "09:00", "10:00"],
    [1003, 1, 2130, "01/09/2026", "10:00", "11:00"],
    [1004, 4, 1101, "02/09/2026", "08:00", "10:00"],
    [1005, 2, 3653, "02/09/2026", "10:00", "12:00"],
    [1006, 4, 3653, "02/09/2026", "13:00", "13:30"],
]

def imprimir_Reservas(matriz):
    '''
    pre: recibe una matriz de reservas, donde cada fila representa una reserva con sus datos
         [id_reserva, sala, id_usuario, fecha, inicio, fin].
    pos: devuelve por pantalla la matriz de reservas fomateada.
    '''
     
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

def realizar_Reserva(matriz):
    '''
    pre: recibe una matriz de reservas, donde cada fila representa una reserva con sus datos
         [id_reserva, sala, id_usuario, fecha, inicio, fin].
    pos: genera automaticamente un id correlativo para la reserva basado en el tamaño de la lista,
         empezando desde el id 1000. solicita los datos pro consola, añade la nueva reserva al final
         de la matriz original y muestra un mensaje de exito.
    '''

    id_reserva = len(matriz) + 1000

    id_sala     = int(input("Ingresar Id de sala: "))
    id_usuario  = int(input("Ingresar Id de usuario: "))
    fecha       = input ("Ingresar Fecha: ")
    inicio      = input("Ingresar Horario de inicio: ")
    fin         = input("Ingresar Horario de fin: ")

    nuevaReserva = [id_reserva, id_sala, id_usuario, fecha, inicio, fin]
    matriz.append(nuevaReserva)
    print("Reserva agregada correctamente")


def eliminar_Reserva(matriz):
    '''
        pre: recibe una matriz de reservas, donde cada fila representa una reserva con sus datos
             [id_reserva, sala, id_usuario, fecha, inicio, fin].
        pos: solicita un id de reserva por consola. si el id existe en la matriz, elimina la reserva de 
             la matriz original y muestra un mensaje de exito. si no existe, muestra un mensaje de error.
    '''

    id = int(input("Ingresar Id: "))
    i = 0
    while i < len(matriz):
        if matriz [i][0] == id:
            matriz.remove(matriz[i])
            print("Reserva eliminado correctamente")
            return
        i = i+1
    print("No se encontro el id de usuario")

def modificar_Reserva(matriz):
    '''
        pre: recibe una matriz de reservas, donde cada fila representa una reserva con sus datos
             [id_reserva, sala, id_usuario, fecha, inicio, fin].
        pos: solicita un id de reserva por consola. si lo encuentra, pide los nuevos datos 
             (sala, usuario, fecha, inicio y fin) para sobreescribir los valores originales en la matriz.
             si el id no existe, la funcion termina sin realizar cambios.
    '''
    reserva_encontrada = False

    while not reserva_encontrada:
        id_buscado = int(input("Ingresar id de la reserva a modificar: "))

        for fila in matriz:
                    if fila[0] == id_buscado:
                        reserva_encontrada = True
                        fila[1] = input("Ingresar nuevo id de sala:: ")
                        fila[2] = int(input("Ingresar nuevo id de usuario: "))
                        fila[3] = input("Ingresar nueva fecha de reserva:  ")
                        fila[4] = (input("Ingresar nuevo horario de inicio: "))
                        fila[5] = input("Ingresar nuevo horaio de fin: ")
                        print("Reserva modificada correctamente")

        if not reserva_encontrada:
                    print("Reserva no encontrada. Intente nuevamente.")

realizar_Reserva(reservas)
imprimir_Reservas(reservas)