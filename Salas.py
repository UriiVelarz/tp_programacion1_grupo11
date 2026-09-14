# Sistema de disponibilidad de salas usando matriz
# Fila = sala
# Columna = día

salas = [
    [1, "Sala A", "Primer  Piso",  2],
    [2, "Sala B", "Primer  Piso",  2],
    [3, "Sala C", "Primer  Piso",  4],
    [4, "Sala A", "Segundo Piso",  2],
    [5, "Sala B", "Segundo Piso",  2],
    [6, "Sala C", "Segundo Piso",  4]
]

dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

# 1 = disponible, 0 = ocupado
matriz_disponibilidad = [
    [1, 1, 0, 1, 1, 0, 1],  # Sala 1
    [0, 1, 1, 1, 0, 1, 1],  # Sala 2
    [1, 0, 1, 0, 1, 1, 1],  # Sala 3
    [0, 1, 0, 1, 1, 1, 1],  # Sala 4
    [1, 0, 1, 0, 1, 1, 1],  # Sala 5
    [1, 0, 0, 0, 0, 0, 0],  # Sala 6
]

def mostrar_matriz():
    print("\nMatriz de disponibilidad por sala y dia")
    print("="*102)

    encabezado = f"{'Sala':<25}" + "". join (f"{d:<11}" for d in dias)
    print(encabezado)
    print("-"* len(encabezado))

    for i in range(len(salas)):
        id_sala, nombre, piso, capacidad = salas[i]
        etiqueta = f"{nombre}({piso})"
        fila = f"{etiqueta:<25}" + "". join(f"{matriz_disponibilidad[i][j]:<11}" for j in range(len(dias)) )

        print(fila)
    print("\nAclaracion: 1 = disponible, 0 = ocupado")

def consultar_disponibilidad(sala, dia):
    if sala < 1 or sala > len(salas):
        return "La sala ingresada no existe."

    if dia < 1 or dia > len(dias):
        return "El dia ingresado no existe."

    disponible  = matriz_disponibilidad[sala - 1][dia - 1]
    nombre_sala = salas[sala - 1][1]

    if disponible == 1:
        return f"La {nombre_sala} esta disponible el dia {dias[dia - 1]}."
    else:
        return f"La {nombre_sala} no esta disponible el dia {dias[dia - 1]}."

# Menú principal
#while True:
#    print("\n=== RESERVA DE SALAS ===")
#    print("1. Ver matriz de disponibilidad")
#    print("2. Consultar día disponible por coordenadas")
#    print("3. Salir")
#
#    opcion = input("Seleccione una opción: ")
#
#    if opcion == "1":
#        mostrar_matriz()
#
#    elif opcion == "2":
#        try:
#            sala = int(input("Ingrese la sala (1 a 3): "))
#            dia = int(input("Ingrese el día (1 a 7): "))
#            print(consultar_disponibilidad(sala, dia))
#        except ValueError:
#            print("Debe ingresar valores numéricos.")
#
#    elif opcion == "3":
#        print("Gracias que tenga un buen día.")
#        break
#
#    else:
#        print("Opción inválida.")


def imprimir_Salas(matriz):
    '''
    pre: recibe una matriz de salas, donde cada fila representa una sala con sus datos
         [id_sala, nombre_sala, ubicacion, capacidad].
    pos: devuelve por pantalla la matriz de salas fomateada.
    '''
     
    print("="*55)
    print(f"{"Salas":42}")
    print("="*55)
    print(f"{"Id_Sala":<10}{"Nombre":<10}{"Ubicacion":<15}{"capacidad":<14}")
    print("-" *55)

    for i in range (len(matriz)):
        id_sala     = matriz [i][0]
        nombre_sala = matriz [i][1]
        ubicacion   = matriz [i][2]
        capacidad   = matriz [i][3]
        print(f"{id_sala:<10}{nombre_sala:<10}{ubicacion:15}{capacidad:<14}")

def agregar_Sala(matriz):
    '''
    pre: recibe una matriz de salas, donde cada fila representa una sala con sus datos
         id_sala, nombre_sala, ubicacion, capacidad].
    pos: solicita los datos para registrar una nueva sala. si el id ya existe, muestra error y finaliza. si el id es unico, 
         agrega una sala a la matriz al final de la lista y muestra un mensaje de exito.
    '''

    id_sala     = int(input("Ingresar Id de sala o -1 para volver al menu principal: "))
    nombre_sala = input("Ingresar nombre de sala o -1 para volver al menu principal: ")
    ubicacion   = input ("Ingresar ubicacion o -1 para volver al menu principal: ")
    capacidad   = input("Ingresar capacidad o -1 para volver al menu principal: ")

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

    id = int(input("Ingresar Id o -1 para volver al menu principal: "))
    i = 0
    while i < len(matriz):
        if matriz [i][0] == id:
            matriz.remove(matriz[i])
            print("Sala eliminado correctamente")
            return
        i = i+1
    print("No se encontro el id de Sala")

def modificar_Sala(matriz):
    '''
        pre: recibe una matriz de salas, donde cada fila representa una sala con sus datos
             id_sala, nombre_sala, ubicacion, capacidad].
        pos: solicita un id de sala por consola. si lo encuentra, pide los nuevos datos 
             (sala, usuario, fecha, inicio y fin) para sobreescribir los valores originales en la matriz.
             si el id no existe, la funcion termina sin realizar cambios.
    '''
    sala_encontrada = False

    while not sala_encontrada:
        id_buscado = int(input("Ingresar id de la sala a modificar o -1 para volver al menu principal: "))

        for fila in matriz:
                    if fila[0] == id_buscado:
                        sala_encontrada = True
                        fila[0] = int(input("Ingresar nuevo id de sala o -1 para volver al menu principal: "))
                        fila[1] = input("Ingresar nuevo nombre de sala o -1 para volver al menu principal: ")
                        fila[2] = input("Ingresar nueva ubicacion de la sala o -1 para volver al menu principal:  ")
                        print("Sala modificada correctamente")

        if not sala_encontrada:
                    print("Sala no encontrada. Intente nuevamente.")
